import time
import ray
import pickle
import pandas as pd

if not ray.is_initialized():
    ray.init(address='auto', _redis_password='cbgt2', include_dashboard=False)


@ray.remote
def worker(module, environment):
    return module(environment)


class Pipeline:
    # take position and return module

    def __init__(self):
        self.modulelist = []

    def add(self, module):
        # print(type(module))
        # print(isinstance(module, Pipeline))
        if isinstance(module, ModuleParent): # TODO: work with reloading
            self.modulelist.append(module)
        elif isinstance(module, Pipeline): # TODO: work with reloading
            self.modulelist.append(PipelineModule(module))
        else:
            assert callable(module), "added module must be callable, try restarting kernel"
            self.modulelist.append(CodeTaskFunctionModule(module))
        return self

    def getModuleByIndex(self, index):
        try:
            return self.modulelist[index]
        except BaseException:
            return None

    def __getattr__(self, name):
        return VariablePlaceholder(name)

    def __getitem__(self, key):
        assert callable(key), "must specify a callable object"
        return PipelineFunctionHelper(self, key)

    def __setattr__(self, key, value):
        if key == 'modulelist':
            super().__setattr__(key, value)
        elif isinstance(value, PipelineFunctionHelper):
            value.writeto(key)
        elif isinstance(value, VariablePlaceholder):
            self.modulelist.append(BasicCopyModule(key, value.varname))
        else:
            self.modulelist.append(BasicAssignmentModule(key, value))


class VariablePlaceholder:
    def __init__(self, varname):
        self.varname = varname


class ModuleParent:
    pass


class CodeTaskFunctionModule(ModuleParent):
    # return code taskfunction
    def __init__(self, bodyfunc):
        self.bodyfunc = bodyfunc

    def getTaskFunction(self):
        def Payload(variables):
            env = EnvironmentHelper(variables)
            self.bodyfunc(env)
            return env.__dictionary__
        return Payload


class EnvironmentHelper:
    def __init__(self, dictionary):
        self.__dictionary__ = dictionary

    def __getattr__(self, key):
        return self.__dictionary__[key]

    def __setattr__(self, key, value):
        if key == '__dictionary__':
            super().__setattr__(key, value)
        else:
            self.__dictionary__[key] = value

    def copy(self):
        return EnvironmentHelper(self.__dictionary__.copy())


class BasicAssignmentModule(CodeTaskFunctionModule):
    def __init__(self, varname, value):
        self.varname = varname
        self.value = value

    def getTaskFunction(self):
        def Payload(variables):
            variables = variables.copy()
            variables[self.varname] = self.value
            return variables
        return Payload


class BasicCopyModule(CodeTaskFunctionModule):
    def __init__(self, destvar, srcvar):
        self.destvar = destvar
        self.srcvar = srcvar

    def getTaskFunction(self):
        def Payload(variables):
            variables = variables.copy()
            variables[self.destvar] = variables[self.srcvar]
            return variables
        return Payload


class FunctionModule(CodeTaskFunctionModule):
    def __init__(self, bodyfunc):
        self.bodyfunc = bodyfunc
        self.arrayargs = []
        self.dictargs = {}
        self.outputvarmap = {}

    def setArrayArgs(self, array):
        self.arrayargs = array

    def setDictArgs(self, dictionary):
        self.dictargs = dictionary

    def addOutputVar(self, varname, idxpath):
        self.outputvarmap[varname] = idxpath

    def getTaskFunction(self):
        def Payload(variables):
            array = [variables[arg.varname] if isinstance(
                arg, VariablePlaceholder) else arg for arg in self.arrayargs]
            dictionary = {key: (variables[val.varname] if isinstance(
                val, VariablePlaceholder) else val) for key, val in self.dictargs.items()}

            result = self.bodyfunc(*array, **dictionary)
            variables = variables.copy()

            for varname, idxpath in self.outputvarmap.items():
                value = result
                for idx in idxpath:
                    value = value[idx]
                variables[varname] = value

            return variables

        return Payload


def expandtupleshape(tup):
    if isinstance(tup, int):
        if tup == 1:
            return 0
        return [0] * tup
    if len(tup) == 1:
        return expandtupleshape(tup[0])
    return [expandtupleshape(x) for x in tup]


class PipelineFunctionHelper:
    def __init__(
            self,
            pipeline,
            appliedfunction,
            arrayargs=None,
            dictargs=None,
            module=None,
            shapearray=[],
            idxpath=[]):
        self.pipeline = pipeline
        self.appliedfunction = appliedfunction
        self.arrayargs = arrayargs
        self.dictargs = dictargs
        self.module = module
        self.shapearray = shapearray
        self.idxpath = idxpath

    def __call__(self, *array, **dictionary):
        assert self.arrayargs is None and self.dictargs is None, "function arguments specified more than once"
        # print(array)
        # print(dictionary)
        self.arrayargs = array
        self.dictargs = dictionary

        self.module = FunctionModule(self.appliedfunction)
        self.module.setArrayArgs(self.arrayargs)
        self.module.setDictArgs(self.dictargs)

        self.pipeline.add(self.module)

        return self

    def __getitem__(self, key):
        assert self.arrayargs is not None and self.dictargs is not None, "function arguments not specified"

        valid = True
        try:
            self.shapearray[key]
        except BaseException:
            valid = False
        if not valid:
            raise IndexError('incorrect shape for function result')

        newshapearray = self.shapearray[key]
        newidxpath = self.idxpath.copy()
        newidxpath.append(key)

        return PipelineFunctionHelper(
            self.pipeline,
            self.appliedfunction,
            self.arrayargs,
            self.dictargs,
            self.module,
            newshapearray,
            newidxpath,
        )

    def shape(self, *args):
        # print(args)
        self.shapearray = expandtupleshape(args)
        # print(self.shapearray)
        return self

    def writeto(self, varname):
        self.module.addOutputVar(varname, self.idxpath)


class PipelineModule(ModuleParent):

    def __init__(self, pipeline):
        self.pipeline = pipeline

    def getPipeline(self):
        return self.pipeline

# class ParallelModule(ModuleParent):
#
#    def __init__(self):
#        pass
#
#    def getControlPipeline(self):
#        return ...


class ThreadManager:
    # ID number
    # location
    # variable mapping
    # other state

    def __init__(self, ID, variables={}):
        self.ID = ID
        self.location = 0
        self.variables = variables

    def run(self, pipeline, taskfunctionresult=None, childresults=None):

        if taskfunctionresult is not None:
            self.variables = taskfunctionresult
            self.location += 1

        if childresults is not None:
            module = pipeline.getModuleByIndex(self.location)
            if isinstance(module, PipelineModule):
                self.variables = childresults[0]
                self.location += 1

        module = pipeline.getModuleByIndex(self.location)

        if module is None:
            return {
                'status': 'finished',
            }

        if isinstance(module, CodeTaskFunctionModule):
            return {
                'status': 'waitingfortaskfunction',
                'taskfunction': module.getTaskFunction(),
                'environment': self.variables,
            }

        if isinstance(module, PipelineModule):
            return {
                'status': 'waitingforchildren',
                'pipelines': [module.getPipeline()],
                'environments': [self.variables],
            }


class ExecutionManager:
    # mapping from ThreadManager ID to pipeline

    def __init__(self, cores=1):
        self.idtothreadmanager = {}
        self.HIDcounter = 0
        self.idtopipeline = {}
        self.idtostatus = {}
        self.idtowaiting = {}

        self.QIDcounter = 0
        self.qidqueue = []
        self.funcqueue = []
        self.envqueue = []

        self.taskfunctionresults = {}

        assert cores > 0 and isinstance(cores, int), 'cores must be > 0'
        self.maxchildren = cores
        self.workerrefs = {}

    def spawnThreadManager(self, pipeline, environment):
        newid = self.HIDcounter
        self.HIDcounter += 1
        threadmanager = ThreadManager(newid, environment)
        self.idtothreadmanager[newid] = threadmanager
        self.idtopipeline[newid] = pipeline
        self.idtostatus[newid] = 'new'
        return newid

    def spawnThreadManagers(self, pipelines, environments):
        newids = []
        for p, e in zip(pipelines, environments):
            newids.append(self.spawnThreadManager(p, e))
        return newids

    def cyclethrough(self):
        items = list(self.idtothreadmanager.keys())
        for HID in items:

            if HID not in self.idtothreadmanager.keys():
                continue

            if self.idtostatus[HID] == 'new':
                request = self.idtothreadmanager[HID].run(
                    self.idtopipeline[HID])
                self.processThreadManagerRequest(HID, request)

            if self.idtostatus[HID] == 'waitingfortaskfunction':
                if self.idtowaiting[HID] in self.taskfunctionresults.keys():
                    taskfunctionresult = self.taskfunctionresults[self.idtowaiting[HID]]
                    request = self.idtothreadmanager[HID].run(
                        self.idtopipeline[HID], taskfunctionresult=taskfunctionresult)
                    self.taskfunctionresults.pop(self.idtowaiting[HID], None)
                    self.idtowaiting.pop(HID, None)
                    self.processThreadManagerRequest(HID, request)

            if self.idtostatus[HID] == 'waitingforchildren':
                childresults = []
                for childid in self.idtowaiting[HID]:
                    if self.idtostatus[childid] != 'finished':
                        break
                    childresults.append(
                        self.idtothreadmanager[childid].variables)
                else:  # LOL
                    request = self.idtothreadmanager[HID].run(
                        self.idtopipeline[HID], childresults=childresults)
                    for childid in self.idtowaiting[HID]:
                        self.idtothreadmanager.pop(childid, None)
                        self.idtopipeline.pop(childid, None)
                        self.idtostatus.pop(childid, None)
                        self.idtowaiting.pop(childid, None)
                    self.idtowaiting.pop(HID, None)
                    self.processThreadManagerRequest(HID, request)

    def processThreadManagerRequest(self, HID, request):
        self.idtostatus[HID] = request['status']
        if request['status'] == 'finished':
            pass
        if request['status'] == 'waitingfortaskfunction':
            qid = self.addToQueue(
                request['taskfunction'],
                request['environment'])
            self.idtowaiting[HID] = qid
        if request['status'] == 'waitingforchildren':
            hids = self.spawnThreadManagers(
                request['pipelines'], request['environments'])
            self.idtowaiting[HID] = hids

    def addToQueue(self, taskfunction, variables):
        newid = self.QIDcounter
        self.QIDcounter += 1
        self.qidqueue.append(newid)
        self.funcqueue.append(taskfunction)
        self.envqueue.append(variables)
        return newid

    def consumeQueue(self):
        if len(self.qidqueue) == 0:
            return

        for i in range(len(self.workerrefs), min(
                self.maxchildren, len(self.qidqueue))):
            wid = worker.remote(self.funcqueue[i], self.envqueue[i])
            self.workerrefs[wid] = self.qidqueue[i]

        ready_ids, _remaining_ids = ray.wait(
            list(self.workerrefs.keys()), num_returns=1)

        taskfunctionresult = ray.get(ready_ids[0])
        qid = self.workerrefs.pop(ready_ids[0])
        self.taskfunctionresults[qid] = taskfunctionresult
        index = self.qidqueue.index(qid)
        self.qidqueue.pop(index)
        self.funcqueue.pop(index)
        self.envqueue.pop(index)

        while len(self.qidqueue) >= self.maxchildren:
            for i in range(len(self.workerrefs), min(
                    self.maxchildren, len(self.qidqueue))):
                wid = worker.remote(self.funcqueue[i], self.envqueue[i])
                self.workerrefs[wid] = self.qidqueue[i]

            ready_ids, _remaining_ids = ray.wait(
                list(self.workerrefs.keys()), num_returns=1)

            taskfunctionresult = ray.get(ready_ids[0])
            qid = self.workerrefs.pop(ready_ids[0])
            self.taskfunctionresults[qid] = taskfunctionresult
            index = self.qidqueue.index(qid)
            self.qidqueue.pop(index)
            self.funcqueue.pop(index)
            self.envqueue.pop(index)

    def run(self, pipelines, environments={}):

        listform = True
        if not isinstance(pipelines, list) and not isinstance(environments, list):
            listform = False
        if not isinstance(pipelines, list):
            pipelines = [pipelines]
        if not isinstance(environments, list):
            environments = [environments]

        if len(pipelines) == 1:
            pipelines = pipelines * len(environments)
        if len(environments) == 1:
            environments = environments * len(pipelines)

        rootids = []
        for i in range(len(pipelines)):
            rootids.append(self.spawnThreadManager(pipelines[i], environments[i]))

        self.cyclethrough()
        while not self.allfinished(rootids):
            self.consumeQueue()
            self.cyclethrough()

        results = [self.idtothreadmanager[rootid].variables for rootid in rootids]
        if listform:
            return results
        else:
            return results[0]


    def allfinished(self, rootids):
        for rootid in rootids:
            if self.idtostatus[rootid] != 'finished':
                return False
        return True

def saveResults(results,prefix,varnames):

    saveddatas = []

    for result in results:
        saveddata = {}
        for varname in varnames:
            saveddata[varname] = result[varname]
        saveddatas.append(saveddata)

    pickle.dump(saveddatas, open(prefix, "wb"))

def loadResults(prefix):
    return pickle.load(open(prefix, "rb"))

def comparisonTable(results,varnames):

    if not isinstance(results,list):
        results = [results]

    table = pd.DataFrame([],columns=varnames)

    for result in results:
        row = pd.DataFrame([[result[varname] for varname in varnames]],columns=varnames)
        table = pd.concat([table,row],ignore_index=True)
    return table

def collateVariable(results,varname):
    if not isinstance(results,list):
        results = [results]
    return [result[varname] for result in results]
