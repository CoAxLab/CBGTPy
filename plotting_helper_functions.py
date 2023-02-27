import cbgt as cbgt
# from frontendhelpers import *
from tracetype import *
# import init_params as par
# import popconstruct as popconstruct
# import qvalues as qval
# import generateepochs as gen
# from agentmatrixinit import *
# from agent_timestep import timestep_mutator, multitimestep_mutator
# import pipeline_creation as pl_creat
import seaborn as sns
import matplotlib.pyplot as plt
import pylab as pl
import os
import pickle
import glob

# figure_dir = "./Figures/"
# data_dir = "./Data/"


def rename_columns(results,smooth=False):
    
    results['popdata']['newname'] = results['popdata']['name']+'_'+results['popdata']['action']
    new_names = dict()
    for i in results['popdata'].index[:-2]:
        temp = untrace(results['popdata']['newname'].iloc[i])
        #print(type(temp))
        if 'LIP' in temp:
            temp1 = "Cx_"+temp.split('_')[1]
            temp = temp1
        new_names[i] = temp
    new_names[i+1]='FSI_common'
    new_names[i+2]='CxI_common'
    results['popfreqs'] = results['popfreqs'].rename(columns=new_names)
    
    return results


    

def extract_relevant_frames(results,seed):

    t_epochs = cbgt.collateVariable(results,'t_epochs')
    Q_df = cbgt.collateVariable(results,'Q_df')
    datatables = cbgt.collateVariable(results,'datatables')
    dpmn_cpp_scale = results[0]['Q_support_params']['dpmn_CPP_scale'].values[0]
    
    firing_rates = []
    q_df = []
    performance = pd.DataFrame()
    total_performance = pd.DataFrame()
    rt_distribution = pd.DataFrame()
        
    for i in np.arange(len(results)):
        if results[i]["opt_signal_present"]:
            condition = results[i]["opt_signal_population"][0].split('STR')[0]+"-Stimulation"
        else:
            condition = "Control"
            
        exp_params = cbgt.comparisonTable(results[i], ['n_trials','volatility','conflict'])
        results[i] = rename_columns(results[i]) # Overwrites the column names in popfreqs
        results_local = results[i]['popfreqs'].copy()
    
        results_local_melt = results_local.melt("Time (ms)")
    
    
        results_local_melt["nuclei"] = [ x.split('_')[0]  for x in results_local_melt["variable"]]
        results_local_melt["channel"] = [ x.split('_')[1]  for x in results_local_melt["variable"]]
        
        #print(results_local_melt)
        results_local_melt = results_local_melt.rename(columns={"value":"firing_rate"})
        results_local_melt["seed"] = [ str(seed)+"_"+str(i) for j in np.arange(len(results_local_melt)) ]
        results_local_melt["n_trials"] = [ float(exp_params["n_trials"]) for j in np.arange(len(results_local_melt))]
        results_local_melt["volatility"] = [float(exp_params["volatility"]) for j in np.arange(len(results_local_melt))]
        results_local_melt["conflict"] = [float(exp_params["conflict"]) for j in np.arange(len(results_local_melt))]
                
        firing_rates.append(results_local_melt)
        
        rew_df = t_epochs[i].copy()
        rew_df["Trials"] = t_epochs[i].index
        rew_df = rew_df.melt("Trials")
        rew_df["data_type"] = "reward_df"
        rew_df = rew_df.reset_index()
        #print(rew_df)
    
        chosen_action = pd.DataFrame(datatables[i]["decision"].copy())
        chosen_action["Trials"] = chosen_action.index
        chosen_action = chosen_action.rename(columns={"decision":"variable"})
        chosen_action["value"] = chosen_action.groupby("variable").ngroup()
        chosen_action["data_type"] = "chosen action"
        chosen_action = chosen_action.reset_index()
    
        block = pd.DataFrame(datatables[i]["correctdecision"].copy())
        block["Trials"] = block.index
        #print(block)
        block = block.rename(columns={"correctdecision":"variable"})
        block["value"] = block.groupby("variable").ngroup()
        block["data_type"] = "block"
        block = block.reset_index()
        #print(block)
    
        Q_df_local = Q_df[i].copy()
        #print(Q_df_local)

        Q_df_local = Q_df_local.reset_index()
        #Q_df_local.index-=1
        Q_df_local["Trials"] = Q_df_local.index
        Q_df_local = Q_df_local.melt("Trials")
        Q_df_local = Q_df_local.loc[Q_df_local["variable"]!= "index"]
        Q_df_local = Q_df_local.reset_index()
        Q_df_local["data_type"] = "Q_df"
        
        final_data = Q_df_local.append(rew_df)
        final_data = final_data.append(chosen_action)
        final_data = final_data.append(block)
        
        final_data["seed"] = [str(seed)+"_"+str(i)  for j in np.arange(len(final_data))]
        final_data["n_trials"] = [float(exp_params["n_trials"]) for j in np.arange(len(final_data))] 
        final_data["volatility"] = [float(exp_params["volatility"]) for j in np.arange(len(final_data))] 
        #final_data["volatility/num_trials"] = [(float(exp_params["volatility"])/float(exp_params["n_trials"]))*100 for j in np.arange(len(final_data))] 
        final_data["conflict"] = [float(exp_params["conflict"]) for j in np.arange(len(final_data))] 
        final_data["condition"] = [condition for j in np.arange(len(final_data))] 
        
        final_data = final_data.reset_index()
        
        #final_data = final_data.replace(to_replace='None', value=np.nan).dropna() # drop 
        final_data = final_data.mask(final_data.eq('None')).dropna()

        q_df.append(final_data)
        
        perf = pd.DataFrame(columns=["%_rewarded_actions", "%_action","actions","block"])

        prob_act = datatables[i].groupby("decision")["decision"].count()/len(datatables[i])
        for grp in datatables[i].groupby(["correctdecision","decision"]):
            #print(grp)
            df1 = grp[1].loc[grp[1]["decision"]==grp[1]["correctdecision"]]
            df2 = grp[1].loc[grp[1]["reward"]==1.0]
            num = (len(grp[1])/len(datatables[i]))*100
            rr = (len(df2)/len(grp[1]))*100
            perf = perf.append({'%_rewarded_actions':rr,"block":grp[0][0], "actions":grp[0][1],"%_action":num},ignore_index=True)
        perf["seed"] = [str(seed)+"_"+str(i) for j in np.arange(len(perf))]
        perf["n_trials"] = [ float(exp_params["n_trials"]) for j in np.arange(len(perf))]
        perf["volatility"] = [ float(exp_params["volatility"]) for j in np.arange(len(perf))]
        #perf["volatility/num_trials"] = [ (float(exp_params["volatility"])/float(exp_params["n_trials"]))*100 for j in np.arange(len(perf))]
        perf["conflict"] = [float(exp_params["conflict"]) for j in np.arange(len(perf))]
#         perf["Q_val->dopamine_scale"] = [ dpmn_cpp_scale for j in np.arange(len(perf))]
        perf["condition"] = [ condition for j in np.arange(len(perf))]
        
        performance = performance.append(perf)
        
        total_perf = pd.DataFrame(columns=["%_correct_actions", "seed","n_trials","volatility","conflict"])
        overall_perf = (len(datatables[i].loc[datatables[i]["correctdecision"]==datatables[i]["decision"]])/len(datatables[i]))*100
        total_perf["%_correct_actions"] = [overall_perf]
        total_perf["seed"] = [str(seed)]
        total_perf["volatility"] = [float(exp_params["volatility"])]
        #total_perf["volatility/num_trials"] = [(float(exp_params["volatility"])/float(exp_params["n_trials"]))*100]
        total_perf["conflict"] = [float(exp_params["conflict"])]
        #total_perf["Q_val->dopamine_scale"] = [ dpmn_cpp_scale ]
        total_perf["condition"] = [ condition ]
        
        total_performance = total_performance.append(total_perf)
        
        
        rt = pd.DataFrame()
        rt["decisiondurationplusdelay"] = datatables[i]["decisiondurationplusdelay"].copy()
        rt["n_trials"] = [ float(exp_params["n_trials"]) for j in np.arange(len(rt))]
        rt["volatility"] = [float(exp_params["volatility"]) for j in np.arange(len(rt))]
        rt["conflict"] = [ float(exp_params["conflict"]) for j in np.arange(len(rt))]
        #rt["volatility/num_trials"] = [(float(exp_params["volatility"])/exp_params["n_trials"])*100 for j in np.arange(len(rt))]
        rt["seed"] = [str(seed)+"_"+str(i) for j in np.arange(len(rt))]
        #rt["Q_val->dopamine_scale"] = [dpmn_cpp_scale for j in np.arange(len(rt))]
        rt["condition"] = [condition for j in np.arange(len(rt))]

        rt_distribution = rt_distribution.append(rt)
  
    return firing_rates, q_df, performance, rt_distribution, total_performance


def extract_relevant_frames_stop(results,seed):

    t_epochs = cbgt.collateVariable(results,'t_epochs')
    datatables = cbgt.collateVariable(results,'datatables')
    
    firing_rates = []
    rt_distribution = pd.DataFrame()
        
    #print(q_df)   
    #print(performance)
    #save_dataframes(firing_rates,q_df, performance, rt_distribution,total_performance, seed,src_dir)
    for i in np.arange(len(results)):
       
        results[i] = rename_columns(results[i]) # Overwrites the column names in popfreqs
        results_local = results[i]['popfreqs'].copy()
    
        results_local_melt = results_local.melt("Time (ms)")
    
    
        results_local_melt["nuclei"] = [ x.split('_')[0]  for x in results_local_melt["variable"]]
        results_local_melt["channel"] = [ x.split('_')[1]  for x in results_local_melt["variable"]]
        
       
        results_local_melt = results_local_melt.rename(columns={"value":"firing_rate"})
        results_local_melt["seed"] = [ str(seed)+"_"+str(i) for j in np.arange(len(results_local_melt)) ]
        
                
        firing_rates.append(results_local_melt)
        
        rt = pd.DataFrame()
        rt["decisiondurationplusdelay"] = datatables[i]["decisiondurationplusdelay"].copy()
        rt["seed"] = [str(seed)+"_"+str(i) for j in np.arange(len(rt))]
        
        rt_distribution = rt_distribution.append(rt)

    return firing_rates, rt_distribution

    
    
    
