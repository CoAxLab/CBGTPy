from tracetype import *
import seaborn as sns
import matplotlib.pyplot as plt
import pylab as pl
import plotting_helper_functions as plt_help


def smoothen_fr(results,win_len=50):
    
    win = np.ones(win_len)/float(win_len)
        
    for k in list(results.keys()):
        if "Time" in k:
            continue
        results[k] = np.convolve(results[k],win,mode='same')
                
    return results
        
def plot_fr(results):
    
    # Plot Population firing rates
    col_order = ["Cx", "CxI", "FSI","GPeP", "D1STR", "D2STR", "STNE","GPi","Th"] # To ease comparison with reference Figure 
                 
    fig_handles = []
    for i in np.arange(len(results)):
        g1 = sns.relplot(x="Time (ms)", y ="firing_rate", hue="channel",col="nuclei",data=results[i],col_wrap=3,kind="line",facet_kws={'sharey': False, 'sharex': True},col_order=col_order)
        #g1.fig.savefig(fig_dir+'ActualFR_'+str(seed)+"_"+str(i)+".png", dpi=400)
        fig_handles.append(g1)
    
    return fig_handles


def plot_fr_stop(results):
    
    # Plot Population firing rates
    col_order = ["Cx", "CxI", "FSI","GPeP", "GPeA", "D2STR", "D1STR", "STNE","GPi","Th"] # To ease comparison with reference Figure 
                 
    fig_handles = []
    for i in np.arange(len(results)):
        g1 = sns.relplot(x="Time (ms)", y ="firing_rate", hue="channel",col="nuclei",data=results[i],col_wrap=3,kind="line",facet_kws={'sharey': False, 'sharex': True},col_order=col_order)
        #g1.fig.savefig(fig_dir+'ActualFR_'+str(seed)+"_"+str(i)+".png", dpi=400)
        fig_handles.append(g1)
    
    return fig_handles
        
        
def plot_reward_Q_df(final_data):

    fig_handles = []
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
        #g1.fig.savefig(fig_dir+"Reward_and_Q_df_"+final_data[i]["seed"].values[0]+".png")
        fig_handles.append(g1)
    
    return fig_handles



