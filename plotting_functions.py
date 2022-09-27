# import cbgt as cbgt
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
import plotting_helper_functions as plt_help

figure_dir = "./Figures/"
data_dir = "./Data/"

# def rename_columns(results,smooth=False):
    
#     results['popdata']['newname'] = results['popdata']['name']+'_'+results['popdata']['action']
#     new_names = dict()
#     for i in results['popdata'].index[:-2]:
#         temp = untrace(results['popdata']['newname'].iloc[i])
#         #print(type(temp))
#         if 'LIP' in temp:
#             temp1 = "Cx_"+temp.split('_')[1]
#             temp = temp1
#         new_names[i] = temp
#     new_names[i+1]='FSI_common'
#     new_names[i+2]='CxI_common'
#     results['popfreqs'] = results['popfreqs'].rename(columns=new_names)
    
#     return results


def smoothen_fr(results,win_len=50):
    
    win = np.ones(win_len)/float(win_len)
        
    for k in list(results.keys()):
        if "Time" in k:
            continue
        results[k] = np.convolve(results[k],win,mode='same')
                
    return results
        
def plot_fr(results,seed,fig_dir=figure_dir):
    
    # Plot Population firing rates
    col_order = ["D1STR", "GPeP", "GPi","D2STR", "STNE", "Th", "Cx","CxI","FSI"] # To ease comparison with reference Figure 
                 
    for i in np.arange(len(results)):
        g1 = sns.relplot(x="Time (ms)", y ="firing_rate", hue="channel",col="nuclei",data=results[i],col_wrap=3,kind="line",facet_kws={'sharey': False, 'sharex': True},col_order=col_order)
        g1.fig.savefig(fig_dir+'ActualFR_'+str(seed)+"_"+str(i)+".png", dpi=400)
        

def plot_fr_stop(results, amplitude, onset):
    
    # Plot Population firing rates
    col_order = ["Cx","CxI","FSI", "GPeP", "D1STR", "D2STR", "STNE", "GPi", "Th"] 
    for i in np.arange(len(results)):
        g1 = sns.relplot(x="Time (ms)", y ="firing_rate", hue="channel",col="nuclei",data=results[i],col_wrap=3,kind="line",facet_kws={'sharey': False, 'sharex': True},col_order=col_order)
        g1.fig.savefig(figure_dir_stop+'ActualFRs_stop_'+str(amplitude)+"_"+str(onset)+"_"+str(i)+".png", dpi=400)
        
def plot_fr_specific(results, amplitude, onset):
    
    # Plot Population firing rates
    col_order = ["GPeP", "GPi", "STNE", "Th"] 
                 
    for i in np.arange(len(results)):
        g1 = sns.relplot(x="Time (ms)", y ="firing_rate", hue="channel",col="nuclei",data=results[i],col_wrap=4,kind="line",facet_kws={'sharey': False, 'sharex': True},col_order=col_order)
        g1.fig.savefig(figure_dir_stop+'ActualFRs_stop_specific_'+str(amplitude)+"_"+str(onset)+"_"+str(i)+".png", dpi=400)
    
        
def plot_reward_Q_df(final_data,fig_dir=figure_dir):

    colors = list(sns.color_palette())
    
    for i in np.arange(len(final_data)):
        var = np.unique(final_data[i]["variable"])
        
        col_dict = dict()
        for j,v in enumerate(var):
            col_dict[v] = colors[j]
        
        print(col_dict)
        g1 = sns.catplot(x="Trials",y="value",hue="variable",col="data_type",data=final_data[i],kind='point',col_wrap=2,sharey=False,palette=col_dict)
        block = final_data[i].loc[final_data[i]["data_type"]=="block"]
        ind_change_points = np.where(block["variable"]!=block["variable"].shift(1))[0]
        for x in g1.axes:
            x.set_xticklabels(x.get_xticklabels(),fontsize=10,fontweight='bold')
            if np.max(final_data[i]["Trials"]) > 10:
                x.set_xticklabels([])
            
            for icp in ind_change_points:
                if icp == 0 or icp == len(block)-1:
                    continue
                #ylim = x.get_ylim()
                #x.vlines(x=icp,ymin=ylim[0],ymax=ylim[1],color='k',ls='dashed',lw=1.0)
                #x.set_ylim(ylim[0],ylim[1])
            
        xlim = g1.axes[0].get_xlim()
        g1.fig.savefig(fig_dir+"Reward_and_Q_df_"+final_data[i]["seed"].values[0]+".png")
    
def performance_all(performance=[],rt_dist=[],total_performance=[],fig_dir=figure_dir,src_dir=data_dir):
    if len(performance) == 0 and len(rt_dist) == 0 and len(total_performance) ==0:
        print("Pooling data")
        plt_help.pool_data(src_dir)
        performance = pd.read_csv(src_dir+"performance_all.csv")
        rt_dist = pd.read_csv(src_dir+"rt_distribution_all.csv")
        total_performance = pd.read_csv(src_dir+"total_performance_all.csv")
        
        post_fix = "all"
    else:
        post_fix = str(performance["seed"][0]).split('_')[0]
    
    
    performance = performance.loc[performance["condition"]=="Control"]
    rt_dist = rt_dist.loc[rt_dist["condition"] == "Control"]
    total_performance = total_performance.loc[total_performance["condition"]=="Control"]
    
    total_performance["conflict"] = total_performance["conflict"].replace(1.0,"No")
    total_performance["conflict"] = total_performance["conflict"].replace(0.75,"High")
    total_performance["conflict"] = total_performance["conflict"].replace(0.9,"Low")
    
    
    g1 = sns.catplot(x="block",y="%_rewarded_actions",hue="actions",data=performance,col="conflict",kind="bar")
    g1.fig.savefig(fig_dir+"Performance_rewarded_actions_all.png")
    g4 = sns.catplot(x="block",y="%_action",hue="actions",data=performance,col="conflict",kind="bar")
    g4.fig.savefig(fig_dir+"Performance_actions_"+post_fix+".png")
    g5 = sns.catplot(x="conflict",y="%_correct_actions",data=total_performance,kind="bar",order=["No","Low","High"])
    #g5 = sns.catplot(x="Q_val->dopamine_scale",y="%_correct_actions",data=total_performance,col="conflict",kind="bar")
    g5.fig.savefig(fig_dir+"Total_performance_actions_"+post_fix+".png")
    
    
    
    rt_dist = rt_dist.reset_index()
    rt_dist["conflict"] = rt_dist["conflict"].replace(1.0,"No")
    rt_dist["conflict"] = rt_dist["conflict"].replace(0.75,"High")
    rt_dist["conflict"] = rt_dist["conflict"].replace(0.9,"Low")
    
    for grp in rt_dist.groupby("Q_val->dopamine_scale"):
        fig,ax = pl.subplots(1,1,figsize=(16,16))
        hist = sns.histplot(x="decisiondurationplusdelay",data=grp[1],hue="conflict",kde=True,palette="deep",stat="density",ax=ax,lw=2.5,element="step",fill=False)
        hist.figure.suptitle("Q_val->dopamine_scale ="+str(grp[0]),fontsize=20,fontweight='bold')
        hist.figure.savefig(fig_dir+"RT_distribution_"+post_fix+"_"+str(grp[0])+".png")


    
    
