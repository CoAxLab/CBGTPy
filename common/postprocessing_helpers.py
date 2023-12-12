import common.cbgt as cbgt
from common.tracetype import *
import seaborn as sns
import matplotlib.pyplot as plt
import pylab as pl
import os
import gc
import pickle
import glob

def extract_recording_variables(results,list_variables,seed):
    
    recorded_variables = dict()
    actions = results[0]['channels']['action'].values
    print(actions)
    for var_name in list_variables:
        if var_name == "weight":
            weights_df = pd.DataFrame(columns=["weights","trials","nuclei"])
            for i in np.arange(len(results)):
                datatables = cbgt.collateVariable(results,'datatables')
                weights = np.array(results[i]['agent'].hist_w)
                reshaped_wts = weights.reshape(len(weights),len(actions)*2)
                
                nuc_list = np.hstack([ ["dSPN-"+ac, "iSPN-"+ac] for ac in actions])  #['D1-left','D2-left','D1-right','D2-right' ]
                ind_list = np.hstack([ [(i1,0),(i1,1)]   for i1 in np.arange(len(actions))])  #[(0,0),(0,1),(1,0),(1,1)]
                print("nuc_list",nuc_list)
                print("ind_list",ind_list)
                for j in np.arange(len(actions)*2):
                    temp = pd.DataFrame()

                    temp["weights"] = [ np.mean(reshaped_wts[:,j][datatables[i]['stimulusstarttime'][i1]:datatables[i]['stimulusstarttime'][i1+1]])   for i1 in np.arange(len(datatables[i])-1) ]
                    #temp["weights"] = [ weights[:,ind_list[j][0],ind_list[j][1],:,:][datatables[0]['stimulusstarttime'][i]:datatables[0]['stimulusstarttime'][i+1]])   for i in np.arange(len(datatables[0])-1) ]
                    temp["trials"] = np.arange(0,len(datatables[i])-1)
                    temp["nuclei"] = nuc_list[j]
                    temp["seed"] = str(seed) +"_"+str(i)
                    weights_df = pd.concat([weights_df,temp])#weights_df.append(temp)
            
            recorded_variables[var_name] = weights_df
    
        elif var_name == "optogenetic_input":
            opt_inp_df = pd.DataFrame()
            for i in np.arange(len(results)):
                for j,op in enumerate(results[i]['opt_signal_population']):
                    opt_inp = np.array(results[i]['agent'].opt_inp[j])
                    opt_pop = op
#                     print("opt_inp",np.shape(opt_inp)[1])
                    temp = pd.DataFrame()
                    if np.shape(opt_inp)[1] > 1:
                        
                        for i1,ac in enumerate(actions):
                            temp_ac = pd.DataFrame()
                            temp_ac["value"] = opt_inp[:,i1]
                            temp_ac["nuclei"] = [opt_pop+"-"+ac]*len(opt_inp)
                            temp_ac["Time(ms)"] = np.arange(len(opt_inp))
                            temp = pd.concat([temp,temp_ac])#temp.append(temp_ac)
                            del temp_ac
                        #temp[opt_pop+"_right"] = opt_inp[:,1]
                    else:
                        temp["value"] = opt_inp[:,0]
                        temp["nuclei"] = [op]*len(opt_inp)
                        temp["Time(ms)"] = np.arange(len(opt_inp))

                    temp["seed"] = str(seed)+"_"+str(i)#]*len(opt_inp)
                    opt_inp_df = pd.concat([opt_inp_df,temp])#opt_inp_df.append(temp)
                    
                    del temp
                    
            opt_inp_df = opt_inp_df.reset_index()
            recorded_variables[var_name] = opt_inp_df
            
        elif var_name == "stop_input":
            stop_inp_df = pd.DataFrame()
            for i in np.arange(len(results)):
                for j,sp in enumerate(results[i]['stop_signal_population']):
                    stop_inp = np.array(results[i]['agent'].stop_inp[j])
                    stop_pop = sp
                    temp = pd.DataFrame()
                    if np.shape(stop_inp)[1] > 1:

                        for i1,ac in enumerate(actions):
                            temp_ac = pd.DataFrame()
                            temp_ac["value"] = stop_inp[:,i1]
                            temp_ac["nuclei"] = [stop_pop+"-"+ac]*len(stop_inp)
                            temp_ac["Time(ms)"] = np.arange(len(stop_inp))
                            temp = pd.concat([temp,temp_ac]) #temp.append(temp_ac)
                            del temp_ac
                        #temp[opt_pop+"_right"] = opt_inp[:,1]
                    else:
                        temp["value"] = stop_inp[:,0]
                        temp["nuclei"] = [sp]*len(stop_inp)
                        temp["Time(ms)"] = np.arange(len(stop_inp))
                        
                        
                    temp["seed"] = str(seed)+"_"+str(i)
                    
                    stop_inp_df = pd.concat([stop_inp_df,temp])#stop_inp_1_df.append(temp)
                    del temp
                    

            stop_inp_df = stop_inp_df.reset_index()
            
            recorded_variables[var_name] = stop_inp_df
            
#         elif var_name == "stop_input_2":
#             stop_inp_2_df = pd.DataFrame()
#             for i in np.arange(len(results)):
#                 stop_inp_2 = np.array(results[i]['agent'].stop_2_inp)
#                 stop_pop_2 = results[i]['stop_2_signal_population'][0]
#                 temp = pd.DataFrame()
#                 if np.shape(stop_inp_2)[1] > 1:
#                     for i1,ac in enumerate(actions):
#                         temp[stop_pop_2+"_"+ac] = stop_inp_2[:,i1]
#                     #temp[stop_pop_2+"_right"] = stop_inp_2[:,1]
#                 else:
#                     temp[stop_pop_2] = stop_inp_2[:,0]
#                 temp["seed"] = str(seed)+"_"+str(i)
#                 temp["Time(ms)"] = np.arange(len(stop_inp_2))
#                 stop_inp_2_df = pd.concat([stop_inp_2_df,temp]) #stop_inp_2_df.append(temp)
            
#             stop_inp_2_df = stop_inp_2_df.reset_index()
#             recorded_variables[var_name] = stop_inp_2_df
                   
    
    return recorded_variables
            
    