from common.frontendhelpers import *
from stopsignal.init_params_stopsignal import *
import pandas as pd


# ----------------------  helper_popconstruct FUNCTION  ------------------
# helper_popconstruct sets for each population the corrisponding specific
# parameters with either the defaults or the values passed as arguments
# (through the functions implemented in init_params.py)

# inputs:   channels = action channels related parameters - through helper_actionchannels (init_params.py)
#           popspecific = population specific parameters dictionary - through helper_popspecific (init_params.py)
#           celldefaults = neuron parameters, which are either default values or values set by the user - through helper_cellparams (init_params.py)
#           receptordefaults = receptor specific parameters dictionary - through helper_receptor (init_paras.py)
#           basestim = base stimulus parameter dictionary - through helper_basestim (init_params.py)
#           dpmn_defaults = dopamine related parameters dictionary - through helper_dpmn (init_params.py)
#           d1defaults = dopamine related parameters for D1-MSN - through helper_d1 (init_params.py)
# d2defaults = dopamine related parameters for D2-MSN - through helper_d2
# (init_params.py)

# outputs:  popdata = populations dataframe, each one containing the
# corresponding specific parameters

def helper_popconstruct(
        channels,
        popspecific,
        celldefaults,
        receptordefaults,
        basestim,
        dpmndefaults,
        d1defaults,
        d2defaults):

    popdata = pd.DataFrame()

    popdata['name'] = [
        'GPi',
        'STN',
        'GPeP',
        'GPeA',
        'dSPN',
        'iSPN',
        'Cx',
        'Th',
        'FSI',
        'CxI',
    ]
    popdata = trace(popdata, 'init')

    popdata = ModifyViaSelector(popdata, channels, SelName(
        ['GPi', 'STN', 'GPeP','GPeA', 'dSPN', 'iSPN', 'Cx', 'Th']))

    popdata = ModifyViaSelector(popdata, celldefaults)

    for key, data in popspecific.items():
        params = ParamSet('popspecific', data)
        popdata = ModifyViaSelector(popdata, params, SelName(key))

    popdata = ModifyViaSelector(popdata, receptordefaults)

    for key, data in basestim.items():
        params = ParamSet('basestim', data)
        popdata = ModifyViaSelector(popdata, params, SelName(key))

    popdata = ModifyViaSelector(
        popdata, dpmndefaults, SelName(['dSPN', 'iSPN']))
    popdata = ModifyViaSelector(popdata, d1defaults, SelName('dSPN'))
    popdata = ModifyViaSelector(popdata, d2defaults, SelName('iSPN'))
    #print('popdata', popdata)

    return popdata


def update_poppathways(oldpathway,newpathway):
    #columns=['src', 'dest', 'receptor', 'type', 'con', 'eff', 'plastic']
    cols = list(oldpathway.columns)
    newpathway = pd.DataFrame(newpathway,columns=cols)
    print(newpathway)

    copy_old = untrace(oldpathway.copy())
    # Go through all the pathways sent by the user
    for i in np.arange(len(newpathway)):
        # The first 4 fields are unique for all pathways, check if the user want to change an existing connection or make a new one
        dat_slice = newpathway.iloc[i].copy()
        temp = copy_old.loc[(copy_old[cols[0]] == dat_slice[cols[0]]) & (copy_old[cols[1]] == dat_slice[cols[1]]) & (copy_old[cols[2]] == dat_slice[cols[2]]) & (copy_old[cols[3]] == dat_slice[cols[3]])].copy()

        if len(temp) > 0:
            # edit an existing connection
            print("changing a connection")
            ind = temp.index.tolist()[0]
            #print(oldpathway.iloc[ind]["eff"], dat_slice["eff"])
            if oldpathway.iloc[ind]["con"] != dat_slice["con"]:
                oldpathway.at[ind,"con"] = dat_slice["con"]
            if oldpathway.iloc[ind]["eff"] != dat_slice["eff"]:
                #print('changing eff')
                oldpathway.at[ind,"eff"] = dat_slice["eff"]
            if oldpathway.iloc[ind]["plastic"] != dat_slice["plastic"]:
                oldpathway.at[ind,"plastic"] = dat_slice["plastic"]
        else:
            # add a new connection
            print("add a new connection")
            oldpathway = pd.concat([oldpathway,pd.DataFrame(dat_slice).transpose()],ignore_index=True)
    
    
    oldpathway = oldpathway.reset_index()
    return oldpathway





# ----------------------  helper_poppathways FUNCTION  -------------------
# helper_poppathays sets for each connection between populations the
# corrisponding specific parameters with either the defaults or the values
# passed

# inputs:  popdata = populations dataframe, each one containing the corresponding specific parameters
# newpathways = connectivity parameters sent as argument. This is a
# dataframe and allows setting only a subset of parameters.

# outputs:  pathways = dataframe that defines the source and the
# destination of each connection, which is the type of receptor involved,
# the probability of connection and efficiency


def helper_poppathways(popdata,number_of_choices, newpathways=None):

    if newpathways is None:
        newpathways = pd.DataFrame()

    dpmn_ratio = 0.5
    dpmn_implied = 0.7
    
    #number_of_choices = 2
    if number_of_choices >1:
        scaling_conn = 2./float(number_of_choices)
        scaling_wts = 1
    else:
        scaling_conn = 1
        scaling_wts = 2./float(number_of_choices)
        
        
    print("scaling_conn",scaling_conn)
    print("scaling_wts",scaling_wts)
    #Stop signal task 
    simplepathways = pd.DataFrame(
        [
            ['Cx', 'dSPN', 'AMPA', 'syn', 1, 0.022, True], 
            ['Cx', 'dSPN', 'NMDA', 'syn', 1, 0.03, False], 
            ['Cx', 'iSPN', 'AMPA', 'syn', 1, 0.022, True], 
            ['Cx', 'iSPN', 'NMDA', 'syn', 1, 0.028, False], 
            ['Cx', 'FSI', 'AMPA', 'all', 1*scaling_conn, 0.085*scaling_wts, False],
            ['Cx', 'Th', 'AMPA', 'syn', 1, 0.025, False], 
            ['Cx', 'Th', 'NMDA', 'syn', 1, 0.029, False],

            ['dSPN', 'dSPN', 'GABA', 'syn', 0.45, 0.28, False],
            ['dSPN', 'iSPN', 'GABA', 'syn', 0.45, 0.28, False], 
            ['dSPN', 'GPi', 'GABA', 'syn', 1, 1.8, False], 
            ['dSPN', 'GPeA', 'GABA', 'syn', 0.4, 0.054, False],

            ['iSPN', 'iSPN', 'GABA', 'syn', 0.45, 0.28, False],
            ['iSPN', 'dSPN', 'GABA', 'syn', 0.5, 0.28, False], 
            ['iSPN', 'GPeP', 'GABA', 'syn', 1, 4.07, False], 
#             ['iSPN', 'GPeP', 'GABA', 'syn', 1, 5.0, False], 
            ['iSPN', 'GPeA', 'GABA', 'syn', 0.4, 0.61, False],

            ['FSI', 'FSI', 'GABA', 'all', 1, 2.7, False], 
            ['FSI', 'dSPN', 'GABA', 'all', 1, 1.25, False], 
            ['FSI', 'iSPN', 'GABA', 'all', 1, 1.15, False],

            ['GPeP', 'GPeP', 'GABA', 'all', 0.4*scaling_conn, 0.45*scaling_wts, False], 
            
            ['GPeP', 'STN', 'GABA', 'syn', 0.1, 0.37, False], 
            ['GPeP', 'GPi', 'GABA', 'syn', 1, 0.058, False], 
            ['GPeP', 'FSI', 'GABA', 'all', 0.4*scaling_conn, 0.1*scaling_wts, False], 
            ['GPeP', 'GPeA', 'GABA', 'syn', 0.5, 0.30, False], #0.35
            
            #['GPeA', 'GPeP', 'GABA', 'syn', 0.8, 0, False], # 0.05 / prob=0.667
            ['GPeA', 'FSI', 'GABA', 'all', 0.4*scaling_conn, 0.01*scaling_wts, False], 
            ['GPeA', 'iSPN', 'GABA', 'syn', 0.4, 0.12, False],
            ['GPeA', 'dSPN', 'GABA', 'syn', 0.4, 0.32, False], #0.018
            ['GPeA', 'GPeA', 'GABA', 'all', 0.4*scaling_conn, 0.15*scaling_wts, False], #0.05 


            ['STN', 'GPeP', 'AMPA', 'syn', 0.161666, 0.10, False], 
            ['STN', 'GPeP', 'NMDA', 'syn', 0.161666, 1.51, False], 
            ['STN', 'GPeA', 'AMPA', 'syn', 0.161666, 0.026, False], 
            ['STN', 'GPeA', 'NMDA', 'syn', 0.161666, 0.075, False], #0.1
            ['STN', 'GPi', 'NMDA', 'all', 1*scaling_conn, 0.0325*scaling_wts, False], 
#             ['STN', 'GPi', 'NMDA', 'all', 1, 0.0325, False], 

            ['GPi', 'Th', 'GABA', 'syn', 1, 0.3315, False], 

            ['Th', 'dSPN', 'AMPA', 'syn', 1, 0.3285, False],
            ['Th', 'iSPN', 'AMPA', 'syn', 1, 0.3285, False],
            ['Th', 'FSI', 'AMPA', 'all', 0.8334*scaling_conn, 0.1*scaling_wts, False],
            ['Th', 'Cx', 'NMDA', 'all', 0.8334*scaling_conn, 0.03*scaling_wts, False],
#             ['Th', 'Cx', 'NMDA', 'all', 0.8334, 0.03, False],

            # ramping ctx

            ['Cx', 'Cx', 'AMPA', 'syn', 0.13, 0.0127, False],
            ['Cx', 'Cx', 'NMDA', 'syn', 0.13, 0.1, False], 
            ['Cx', 'CxI', 'AMPA', 'all', 0.0725*scaling_conn, 0.113*scaling_wts, False],
            ['Cx', 'CxI', 'NMDA', 'all', 0.0725*scaling_conn, 0.525*scaling_wts, False],

            ['CxI', 'Cx', 'GABA', 'all', 0.5, 1.05, False],
            ['CxI', 'CxI', 'GABA', 'all', 1, 1.075, False],

            ['Th', 'CxI', 'NMDA', 'all', 0.8334*scaling_conn, 0.015*scaling_wts, False],

        ],
        columns=['src', 'dest', 'receptor', 'type', 'con', 'eff', 'plastic']
    )


    simplepathways = trace(simplepathways, 'init')

    if len(newpathways) != 0:

        simplepathways = update_poppathways(simplepathways, newpathways)

    pathways = simplepathways.copy()
    pathways['biselector'] = None
    for idx, row in pathways.iterrows():
        if row['type'] == 'syn':
            pathways.loc[idx, 'biselector'] = NamePathwaySelector(
                row['src'], row['dest'], 'action')
        elif row['type'] == 'all':
            pathways.loc[idx, 'biselector'] = NamePathwaySelector(
                row['src'], row['dest'])
    pathways = trace(pathways, 'auto')

    return pathways

# ----------------------  helper_connectivity FUNCTION  ------------------
# helper_connectivity sets three connectivity grids defining,
# correspondingly, the probability of connection, the mean synaptic
# efficacy and the plasticity of connections between each population,
# referring only to AMPA receptors. With plasticity of connection it is
# meant whether or not the weights of that connection could ever change -
# particularly, referring to the Ctx-STR connections modulated by AMPA
# receptors.

# inputs:  receptor = which type of receptor involved (AMPA, GABA, NMDA)
#          popdata = populations dataframe, each one containing the corresponding specific parameters
# pathways = dataframe defining the source and the destination of each
# connection, which is the type of receptor involved, the probability of
# connection and efficiency

# outputs:  connectivity = connectivity matrix defining the probability of connection between each population
#           meanEff = connectivity matrix defining the mean synaptic efficacy of each connection between populations
# plasticity = connectivity matrix defining the plasticity of connections
# between each population (true or false, 0 if not applicable)


def helper_connectivity(receptor, popdata, pathways):

    connectiongrid = constructSquareDf(untrace(popdata['name'].tolist()))
    connectiongrid = trace(connectiongrid, 'init')
    #print('conngrid', connectiongrid)

    connectivity = connectiongrid.copy()
    meanEff = connectiongrid.copy()
    plasticity = connectiongrid.copy()

    for idx, row in pathways.iterrows():
        if row['receptor'] == receptor:
            biselector = row['biselector']
            receptor = row['receptor']
            con = row['con']
            eff = row['eff']
            plastic = row['plastic']

            connectivity = FillGridSelection(
                connectivity, popdata, biselector, con)
            meanEff = FillGridSelection(
                meanEff, popdata, biselector, eff)
            plasticity = FillGridSelection(
                plasticity, popdata, biselector, plastic)

    return connectivity, meanEff, plasticity
