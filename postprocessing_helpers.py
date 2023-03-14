import cbgt as cbgt
from tracetype import *
import seaborn as sns
import matplotlib.pyplot as plt
import pylab as pl
import os
import pickle
import glob

def extract_recording_variables(results,list_variables,seed):
    
    recorded_variables = dict()
    
    for var_name in list_variables:
        if var_name == "weight":
            weights_df = pd.DataFrame(columns=["weights","trials","nuclei"])
            for i in np.arange(len(results)):
                datatables = cbgt.collateVariable(results,'datatables')
                weights = np.array(results[i]['agent'].hist_w)
                reshaped_wts = weights.reshape(len(weights),4)
                nuc_list = ['D1-left','D2-left','D1-right','D2-right' ]
                ind_list = [(0,0),(0,1),(1,0),(1,1)]

                for j in np.arange(4):
                    temp = pd.DataFrame()

                    temp["weights"] = [ np.mean(reshaped_wts[:,j][datatables[i]['stimulusstarttime'][i1]:datatables[i]['stimulusstarttime'][i1+1]])   for i1 in np.arange(len(datatables[i])-1) ]
                    #temp["weights"] = [ weights[:,ind_list[j][0],ind_list[j][1],:,:][datatables[0]['stimulusstarttime'][i]:datatables[0]['stimulusstarttime'][i+1]])   for i in np.arange(len(datatables[0])-1) ]
                    temp["trials"] = np.arange(0,len(datatables[i])-1)
                    temp["nuclei"] = nuc_list[j]
                    temp["seed"] = str(seed) +"_"+str(i)
                    weights_df = weights_df.append(temp)
            
            recorded_variables[var_name] = weights_df
    
        elif var_name == "optogenetic_input":
            opt_inp_df = pd.DataFrame()
            for i in np.arange(len(results)):
                opt_inp = np.array(results[i]['agent'].opt_inp)
                opt_pop = results[i]['opt_signal_population'][0]
                temp = pd.DataFrame()
                if np.shape(opt_inp)[1] > 1:
                    temp[opt_pop+"_left"] = opt_inp[:,0]
                    temp[opt_pop+"_right"] = opt_inp[:,1]
                else:
                    temp[opt_pop] = opt_inp[:,0]
                temp["seed"] = str(seed)+"_"+str(i)
                temp["Time(ms)"] = np.arange(len(opt_inp))
                opt_inp_df = opt_inp_df.append(temp)
            
            opt_inp_df = opt_inp_df.reset_index()
            recorded_variables[var_name] = opt_inp_df
                

    
    
    return recorded_variables
            
    