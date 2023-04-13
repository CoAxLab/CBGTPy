from tracetype import *
import cbgt as cbgt
import seaborn as sns
import matplotlib.pyplot as plt
import pylab as pl
import plotting_helper_functions as plt_help

# figure_dir = "./Figures/"
# data_dir = "./Data/"



def smoothen_fr(results,win_len=50):
    
    win = np.ones(win_len)/float(win_len)
        
    for k in list(results.keys()):
        if "Time" in k:
            continue
        results[k] = np.convolve(results[k],win,mode='same')
                
    return results
        
def plot_fr(results, datatables):
    
    # Plot Population firing rates
    col_order = ["Cx", "CxI", "FSI","GPeP", "D1STR", "D2STR", "STNE","GPi","Th"] # To ease comparison with reference Figure
    colors = list(sns.color_palette(['darkorange', 'steelblue', 'green']))
    col_list = dict()
    col_list['left'] = colors[0]
    col_list['right'] = colors[1]
    col_list['common'] = colors[2]
                 
    fig_handles = []
    
    for i in np.arange(len(results)):
        g1 = sns.relplot(x="Time (ms)", y ="firing_rate", hue="channel",col="nuclei",data=results[i],col_wrap=3,palette=col_list, kind="line",facet_kws={'sharey': False, 'sharex': True},col_order=col_order)
        #g1.fig.savefig(fig_dir+'ActualFR_'+str(seed)+"_"+str(i)+".png", dpi=400)
       
        for j in np.arange(len(datatables[i])):
            for ax in g1.axes.flat:
                ax.axvline(datatables[i].stimulusstarttime[j], color='silver')
                ax.axvline(datatables[i].rewardtime[j], color='silver')
                for k in np.arange(datatables[i].stimulusstarttime[j], datatables[i].rewardtime[j]):
                    ax.axvline(k,color='whitesmoke', alpha=0.02)
        
        fig_handles.append(g1)
       
    return fig_handles
        

def plot_fr_stop(results, datatables):
    
    # Plot Population firing rates
    col_order = ["Cx", "CxI", "FSI","GPeP", "GPeA", "D2STR", "D1STR", "STNE","GPi","Th"] # To ease comparison with reference Figure 
    colors = list(sns.color_palette(['darkorange', 'steelblue', 'green']))
    col_list = dict()
    col_list['left'] = colors[0]
    col_list['right'] = colors[1]
    col_list['common'] = colors[2]

                 
    fig_handles = []
    
    for i in np.arange(len(results)):
        g1 = sns.relplot(x="Time (ms)", y ="firing_rate", hue="channel",col="nuclei",data=results[i],col_wrap=3,palette=col_list,kind="line",facet_kws={'sharey': False, 'sharex': True},col_order=col_order)
        
        #g1.fig.savefig(fig_dir+'ActualFR_'+str(seed)+"_"+str(i)+".png", dpi=400)
        for j in np.arange(len(datatables[i])):
            for ax in g1.axes.flat:
                ax.axvline(datatables[i].stimulusstarttime[j], color='silver')
                ax.axvline(datatables[i].rewardtime[j], color='silver')
                for k in np.arange(datatables[i].stimulusstarttime[j], datatables[i].rewardtime[j]):
                    ax.axvline(k,color='whitesmoke', alpha=0.02)
        
        fig_handles.append(g1)
        #g1.fig.savefig('ActualFR_'+str(i)+".png", dpi=400)
    return fig_handles



def plot_fr_flex(firing_rates, channel, nuclei, interval):
    
    #nuclei = []
    fr = pd.DataFrame()
    fig_handles = []
    
    if len(channel) != 0:

        if channel[0] != 'all':

            fr = firing_rates[firing_rates['channel'] == channel[0]]
            fr_single = pd.concat([fr, firing_rates[firing_rates['channel'] == 'common']])
            
            if 'GPeA' not in firing_rates['nuclei'].unique():
                col_order = ["Cx", "CxI", "FSI","GPeP", "D2STR", "D1STR", "STNE","GPi","Th"]  
            else: 
                col_order = ["Cx", "CxI", "FSI","GPeP", "GPeA", "D2STR", "D1STR", "STNE","GPi","Th"]
            #for i in np.arange(len(results)):
            # set the hue palette as a dict for custom mapping
            palette = {'left': "darkorange", 'right':"steelblue", 'common':'forestgreen'}
            
            if len(nuclei) == 0:
                g1 = sns.relplot(x="Time (ms)", y ="firing_rate", col="nuclei",data=fr_single,col_wrap=3,kind="line",facet_kws={'sharey': False, 'sharex': True},col_order=col_order, hue='channel', palette=palette)
            else:
                g1 = sns.relplot(x="Time (ms)", y ="firing_rate", col="nuclei",data=fr_single.loc[fr_single['nuclei'].isin(nuclei)],col_wrap=3,kind="line",facet_kws={'sharey': False, 'sharex': True}, hue='channel', palette=palette)
            
            if len(interval) != 0: 
                g1.set(xlim=interval)
                
            fig_handles.append(g1)

        else:  #'all'
            fr_1 = firing_rates[firing_rates['channel'] == 'left']
            fr_left = pd.concat([fr_1, firing_rates[firing_rates['channel'] == 'common']])
            fr_2 = firing_rates[firing_rates['channel'] == 'right']
            fr_right = pd.concat([fr_2, firing_rates[firing_rates['channel'] == 'common']])
            #fr = firing_rates
            
            if 'GPeA' not in firing_rates['nuclei'].unique():
                col_order = ["Cx", "CxI", "FSI","GPeP", "D2STR", "D1STR", "STNE","GPi","Th"]  
            else: 
                col_order = ["Cx", "CxI", "FSI","GPeP", "GPeA", "D2STR", "D1STR", "STNE","GPi","Th"]         
            palette = {'left': "darkorange", 'right':"steelblue", 'common':'forestgreen'}
            
            #for i in np.arange(len(results)):
            if len(nuclei) == 0:
                g1 = sns.relplot(x="Time (ms)", y ="firing_rate", col="nuclei", data=fr_right,col_wrap=3,kind="line",facet_kws={'sharey': False, 'sharex': True},col_order=col_order, hue='channel', palette=palette)
                g2 = sns.relplot(x="Time (ms)", y ="firing_rate", col="nuclei",data=fr_left,col_wrap=3,kind="line",facet_kws={'sharey': False, 'sharex': True},col_order=col_order, hue='channel', palette=palette)
            else: 
                g1 = sns.relplot(x="Time (ms)", y ="firing_rate", col="nuclei", data=fr_right.loc[fr_right['nuclei'].isin(nuclei)],col_wrap=3,kind="line",facet_kws={'sharey': False, 'sharex': True}, hue='channel', palette=palette)
                g2 = sns.relplot(x="Time (ms)", y ="firing_rate", col="nuclei",data=fr_left.loc[fr_left['nuclei'].isin(nuclei)],col_wrap=3,kind="line",facet_kws={'sharey': False, 'sharex': True}, hue='channel', palette=palette)
                
            if len(interval) != 0: 
                g1.set(xlim=interval)
                g2.set(xlim=interval)
                
            fig_handles.append(g1)
            fig_handles.append(g2)

    else: 
        print('Specify if <left>, <right> or <all> channel option.')
                
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



