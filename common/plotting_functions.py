from common.tracetype import *
import common.cbgt as cbgt
import seaborn as sns
import matplotlib.pyplot as plt
import pylab as pl
import common.plotting_helper_functions as plt_help

# figure_dir = "./Figures/"
# data_dir = "./Data/"




def smoothen_fr(results,win_len=50):
    
    win = np.ones(win_len)/float(win_len)
        
    for k in list(results.keys()):
        if "Time" in k:
            continue
        results[k] = np.convolve(results[k],win,mode='same')
                
    return results
       
    
def plot_fr(firing_rates, datatables, results, experiment_choice,display_stim=False):

    sns.set(style="white", font_scale=2.5)
    # Plot Population firing rates
    if experiment_choice == "n-choice":
        col_order = ["Cx", "CxI", "FSI","GPe", "dSPN", "iSPN", "STN","GPi","Th"] # To ease comparison with reference Figure
        aspect = 1.2
    elif experiment_choice == "stop-signal":
        col_order = ["Cx", "CxI", "FSI","GPeP", "GPeA", "iSPN", "dSPN", "STN","GPi","Th"]
        aspect = 1.4
    
    colors = list(sns.color_palette())
    col_list = dict()
    actions = firing_rates[0].channel.unique()
    for i,ac in enumerate(actions):
        col_list[ac] = colors[i]
    
                 
    fig_handles = []
    
    for i in np.arange(len(firing_rates)):
        
        g1 = sns.relplot(x="Time (ms)", y ="firing_rate", hue="channel",col="nuclei",data=firing_rates[i],col_wrap=3,palette=col_list, kind="line",facet_kws={'sharey': False, 'sharex': True},col_order=col_order,aspect=aspect,height=7,lw=3.0)
        #g1.fig.savefig(fig_dir+'ActualFR_'+str(seed)+"_"+str(i)+".png", dpi=400)
    
        for ax in g1.axes.flat:
            tit = ax.get_title().split(' = ')[1]
            ax.set_title(tit,fontweight='bold')
            if len(ax.get_ylabel()) > 0:
                ax.set_ylabel("Firing rates (spikes/s)")
        

        for j in np.arange(len(datatables[i])):
            for ax in g1.axes.flat:
                ax.axvline(datatables[i].stimulusstarttime[j], color='mistyrose')
                ax.axvline(datatables[i].decisiontime[j], color='mistyrose')
                ax.axvline(datatables[i].rewardtime[j], color='silver')
                for k in np.arange(datatables[i].stimulusstarttime[j], datatables[i].decisiontime[j]):
                    ax.axvline(k,color='mistyrose', alpha=0.02)
                for k in np.arange(datatables[i].decisiontime[j], datatables[i].rewardtime[j]):
                    ax.axvline(k,color='grey', alpha=0.01)
                
        if experiment_choice == 'stop-signal' and display_stim == True:
            for ni,nuc in enumerate(results[i]['stop_signal_population']):
                
                if results[i]['stop_signal_present'][ni] == True:
                    
                    ind = np.where(np.array(col_order)==nuc)[0][0]
                    axes = g1.axes.flatten()
                    ylim = g1.axes[ind].get_ylim()
                    
                    for tr in results[i]['stop_list_trials_list'][ni]:
                        if isinstance(results[i]['stop_duration_dfs'][ni].iloc[0][0],str):
                            which_phase_df = results[i]['stop_duration_dfs'][ni].iloc[tr]
                            ac = results[i]['channels'].action.unique()[0]
                            
                            which_phase = int(which_phase_df[ac].split(' ')[1]) # Doesn't matter which channel, display is the 
                            
                            if which_phase == 0:
                                start = datatables[i].stimulusstarttime[tr]
                                end = datatables[i].decisiontime[tr]
                            elif which_phase == 1:
                                start = datatables[i].decisiontime[tr]
                                end = datatables[i].rewardtime[tr]
                            elif which_phase == 2:
                                start = datatables[i].rewardtime[tr]
                                end = datatables[i].rewardtime[tr]+results[i]['inter_trial_interval']
                            
                            for ax in axes:
                                g1.axes[ind].hlines(y=ylim[1],xmin=start, 
                                                    xmax=end,color='red', linewidth=15)
                            
                        elif isinstance(results[i]['stop_duration_dfs'][ni].iloc[0][0],(float,int)):
                            start = datatables[i].stimulusstarttime[tr]+results[i]['stop_signal_onset'][ni]
                            end = datatables[i].stimulusstarttime[tr]+results[i]['stop_signal_onset'][ni]+results[i]['stop_signal_duration'][ni]
                            for ax in axes:
                                g1.axes[ind].hlines(y=ylim[1],xmin= start,xmax=end, 
                                                    color='red', linewidth=15)
                    
              
                 
        if display_stim == True:
            for ni,nuc in enumerate(results[i]['opt_signal_population']):
                if results[i]['opt_signal_present'][ni] == True:
                    if results[i]['opt_signal_amplitude'][ni]>0:
                        col_opt='skyblue'
                    elif results[i]['opt_signal_amplitude'][ni]<0:
                        col_opt='gold'

                    ind = np.where(np.array(col_order)==nuc)[0][0]
                    axes = g1.axes.flatten()
                    ylim = g1.axes[ind].get_ylim()
                    

                    for tr in results[i]['opt_list_trials_list'][ni]:
                        if isinstance(results[i]['opt_duration_dfs'][ni].iloc[0][0],str):
                            which_phase_df = results[i]['opt_duration_dfs'][ni].iloc[tr]
                            ac = results[i]['channels'].action.unique()[0]
                            
                            which_phase = int(which_phase_df[ac].split(' ')[1]) # Doesn't matter which channel, display is the 
                            
                            if which_phase == 0:
                                start = datatables[i].stimulusstarttime[tr]
                                end = datatables[i].decisiontime[tr]
                            elif which_phase == 1:
                                start = datatables[i].decisiontime[tr]
                                end = datatables[i].rewardtime[tr]
                            elif which_phase == 2:
                                start = datatables[i].rewardtime[tr]
                                end = datatables[i].rewardtime[tr]+results[i]['inter_trial_interval']
                            
                            for ax in axes:
                                g1.axes[ind].hlines(y=ylim[1],xmin=start, xmax=end,
                                                    color=col_opt, linewidth=15)
                            
                        elif isinstance(results[i]['opt_duration_dfs'][ni].iloc[0][0],(float,int)):
                            start = datatables[i].stimulusstarttime[tr]+results[i]['opt_signal_onset'][ni]
                            end = datatables[i].stimulusstarttime[tr]+results[i]['opt_signal_onset'][ni]+results[i]['opt_signal_duration'][ni]
                            for ax in axes:
                                g1.axes[ind].hlines(y=ylim[1],xmin= start,xmax=end, color=col_opt, linewidth=15)
        leg = g1._legend
        #print(leg.legendHandles)
        for line in leg.get_lines():
            line.set_linewidth(4.0)        
#         for legobj in leg.legendHandles:
#             legobj.set_linewidth(2.0)
                
#         plt.tight_layout()    
        fig_handles.append(g1)
       
    return fig_handles
        

def plot_fr_flex(firing_rates, datatables, results, channel, nuclei, interval, experiment_choice):
    
    #nuclei = []
    fr = pd.DataFrame()
    fig_handles = []
    
    if len(channel) != 0:

        if channel[0] != 'all':

            fr = firing_rates[firing_rates['channel'] == channel[0]]
            fr_single = pd.concat([fr, firing_rates[firing_rates['channel'] == 'common']])
            
            if experiment_choice == "n-choice":
                col_order = ["Cx", "CxI", "FSI","GPe", "dSPN", "iSPN", "STN","GPi","Th"]
                
            elif experiment_choice == "stop-signal":
                col_order = ["Cx", "CxI", "FSI","GPeP", "GPeA", "iSPN", "dSPN", "STN","GPi","Th"]
            
            colors = list(sns.color_palette())
            col_list = dict()
            actions = firing_rates.channel.unique()
            
            for i,ac in enumerate(actions):
                col_list[ac] = colors[i]
        
            if len(nuclei) == 0:
                g1 = sns.relplot(x="Time (ms)", y ="firing_rate",
                                 col="nuclei",data=fr_single,col_wrap=3,kind="line",
                                 facet_kws={'sharey':False, 'sharex': True},col_order=col_order,
                                 hue='channel', palette=col_list)
                
            else:
                g1 = sns.relplot(x="Time (ms)", y ="firing_rate", col="nuclei",
                                 data=fr_single.loc[fr_single['nuclei'].isin(nuclei)],
                                 col_wrap=3,kind="line", 
                                 facet_kws={'sharey':False, 'sharex': True},
                                 col_order=col_order, hue='channel', palette=col_list)
                
            if len(interval) != 0: 
                g1.set(xlim=interval)
            
            for j in np.arange(len(datatables)):
                for ax in g1.axes.flat:
                    ax.axvline(datatables.stimulusstarttime[j], color='silver')
                    ax.axvline(datatables.decisiontime[j], color='mistyrose')
                    ax.axvline(datatables.rewardtime[j], color='silver')                                 
                    for k in np.arange(datatables.stimulusstarttime[j], datatables.decisiontime[j]):
                        ax.axvline(k,color='mistyrose', alpha=0.02)
                    for k in np.arange(datatables.decisiontime[j], datatables.rewardtime[j]):
                        ax.axvline(k,color='whitesmoke', alpha=0.02)
                        
            leg = g1._legend
            #print(leg.legendHandles)
            for line in leg.get_lines():
                line.set_linewidth(4.0)    
            
            fig_handles.append(g1)
            
            if experiment_choice == 'stop-signal':
                if results['stop_signal_present'] == True:
                    for n in results['stop_signal_population']:
                        ind = np.where(np.array(col_order)==n)[0]
                        #print('inside')
                        axes = g1.axes.flatten()
                        ylim = g1.axes[ind].get_ylim()
                        #print(axes)
                        for j in np.arange(len(datatables)):
                            for ax in axes:
                                g1.axes[ind].hlines(y=ylim[1],
xmin=datatables.stimulusstarttime[j]+results['stop_signal_onset'],
                                           xmax=datatables.stimulusstarttime[j]+
                                           results['stop_signal_onset']+results['stop_signal_duration'],
                                           color='', linewidth=4.5)
                        
            
            if results['opt_signal_present'] == True:
                if results['opt_signal_amplitude']>0:
                    col_opt='firebrick'
                elif results['opt_signal_amplitude']<0:
                    col_opt='gold'
                for n in results['opt_signal_population']:
                    ind = np.where(np.array(col_order)==n)[0]
                    #print('inside')
                    axes = g1.axes.flatten()
                    ylim = g1.axes[ind].get_ylim()
                    #print(axes)
                    for j in np.arange(len(datatables)):
                        for ax in axes:
                            g1.axes[ind].hlines(y=ylim[1],
xmin=datatables.stimulusstarttime[j]+results['opt_signal_onset'],
                                       xmax=datatables.stimulusstarttime[j]+
                                       results['opt_signal_onset']+results['opt_signal_duration'],
                                       color=col_opt, linewidth=4.5)
            
        else:  #'all'
            
            
            actions = firing_rates.channel.unique()
            fr=pd.DataFrame(columns=np.arange(len(actions)))

            colors = list(sns.color_palette())
            col_list = dict()
            #print('actions', actions)
            for i,ac in enumerate(actions):
                col_list[ac] = colors[i]
            
            if experiment_choice == "n-choice":
                col_order = ["Cx", "CxI", "FSI","GPe", "dSPN", "iSPN", "STN","GPi","Th"]
                
            elif experiment_choice == "stop-signal":
                col_order = ["Cx", "CxI", "FSI","GPeP", "GPeA", "iSPN", "dSPN", "STN","GPi","Th"]
            
            for i,ac in enumerate(actions[:-1]):
                
                fr_chann = firing_rates[firing_rates['channel'] == ac]
                fr = pd.concat([fr_chann, firing_rates[firing_rates['channel'] == 'common']])
                #print('fr', fr)
                
                if len(nuclei) == 0:

                    g1 = sns.relplot(x="Time (ms)", y ="firing_rate", col="nuclei", data=fr,col_wrap=3,kind="line",facet_kws={'sharey': False, 'sharex': True},col_order=col_order, hue='channel', palette=col_list)
                
                else: 

                    g1 = sns.relplot(x="Time (ms)", y ="firing_rate", col="nuclei", data=fr.loc[fr['nuclei'].isin(nuclei)],col_wrap=3,kind="line",facet_kws={'sharey': False, 'sharex': True}, hue='channel', palette=col_list)
            

                if len(interval) != 0: 
                    g1.set(xlim=interval)
                    #g2.set(xlim=interval)


                for j in np.arange(len(datatables)):
                    for ax in g1.axes.flat:
                        ax.axvline(datatables.stimulusstarttime[j], color='silver')
                        ax.axvline(datatables.decisiontime[j], color='mistyrose')
                        ax.axvline(datatables.rewardtime[j], color='silver')
                        for k in np.arange(datatables.stimulusstarttime[j], datatables.decisiontime[j]):
                            ax.axvline(k,color='mistyrose', alpha=0.02)
                        for k in np.arange(datatables.decisiontime[j], datatables.rewardtime[j]):
                            ax.axvline(k,color='whitesmoke', alpha=0.02)
            
            #for j in np.arange(len(datatables)):
                #for ax in g2.axes.flat:
                    #ax.axvline(datatables.stimulusstarttime[j], color='silver')
                    #ax.axvline(datatables.decisiontime[j], color='mistyrose')
                    #ax.axvline(datatables.rewardtime[j], color='silver')
                    #for k in np.arange(datatables.stimulusstarttime[j], datatables.decisiontime[j]):
                        #ax.axvline(k,color='mistyrose', alpha=0.02)
                    #for k in np.arange(datatables.decisiontime[j], datatables.rewardtime[j]):
                        #ax.axvline(k,color='whitesmoke', alpha=0.02)
                        
                fig_handles.append(g1)
                
                if experiment_choice == 'stop-signal':
                    if results['stop_signal_present'] == True:
                        for n in results['stop_signal_population']:
                            ind = np.where(np.array(col_order)==n)[0]
                            #print('inside')
                            axes = g1.axes.flatten()
                            ylim = g1.axes[ind].get_ylim()
                            #print(axes)
                            for j in np.arange(len(datatables)):
                                for ax in axes:
                                    g1.axes[ind].hlines(y=ylim[1],
    xmin=datatables.stimulusstarttime[j]+results['stop_signal_onset'],
                                               xmax=datatables.stimulusstarttime[j]+
                                               results['stop_signal_onset']+results['stop_signal_duration'],
                                               color='', linewidth=4.5)
                        
            
                if results['opt_signal_present'] == True:
                    if results['opt_signal_amplitude']>0:
                        col_opt='firebrick'
                    elif results['opt_signal_amplitude']<0:
                        col_opt='gold'
                    for n in results['opt_signal_population']:
                        ind = np.where(np.array(col_order)==n)[0]
                        #print('inside')
                        axes = g1.axes.flatten()
                        ylim = g1.axes[ind].get_ylim()
                        #print(axes)
                        for j in np.arange(len(datatables)):
                            for ax in axes:
                                g1.axes[ind].hlines(y=ylim[1],
    xmin=datatables.stimulusstarttime[j]+results['opt_signal_onset'],
                                           xmax=datatables.stimulusstarttime[j]+
                                           results['opt_signal_onset']+results['opt_signal_duration'],
                                           color=col_opt, linewidth=4.5)

    else: 
        
        print('Specify if <channel_n_name> or <all> channel option.')
                
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



