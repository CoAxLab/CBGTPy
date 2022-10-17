# 1. IMPORTING SCRIPTS

import cbgt as cbgt
from frontendhelpers import * 
from tracetype import *
#import init_params as par 
#import popconstruct as popconstruct
import qvalues as qval
import generateepochs as gen
#import mega_loop as ml
from agentmatrixinit import *

experiment_choice = None
par = None
popconstruct = None
ml = None
gen_stop = None
gen_stop_2 = None
# timestep_mutator = None
# multitimestep_mutator = None

def choose_pipeline(choice):
    global experiment_choice
    global par
    global popconstruct
    global ml
    global gen_stop
    global gen_stop_2
#     global timestep_mutator
#     global multitimestep_mutator
    experiment_choice = choice
    if choice == 'plastic':
        import init_params_direct_indirect as par
        import popconstruct_direct_indirect as popconstruct
        import megaloop_plasticity as ml
#         from agent_timestep_plasticity import timestep_mutator, multitimestep_mutator
    if choice == 'stopsignal':
        import init_params_hyperdirect as par
        import popconstruct_hyperdirect as popconstruct
        import megaloop_stop_signal as ml
#         from agent_timestep_stop_signal import timestep_mutator, multitimestep_mutator
        import generate_stop_dataframe as gen_stop
        import generate_stop_dataframe_2 as gen_stop_2

# 2. NETWORK PIPELINE

# 2.1. Defining necessary codeblocks:

#MODIFIERS:

#init_params.py: to modify the neuronal default values

def codeblock_experimentchoice(self):
    choose_pipeline(self.experimentchoice)

def codeblock_modifycelldefaults(self):
    self.celldefaults = par.helper_cellparams(self.params)

def codeblock_modifypopspecific(self):
    self.popspecific = par.helper_popspecific(self.pops)

def codeblock_modifyreceptordefaults(self):
    self.receptordefaults = par.helper_receptor(self.receps)

def codeblock_modifybasestim(self):
    self.basestim = par.helper_basestim(self.base)

def codeblock_modifydpmndefaults(self):
    self.dpmndefaults = par.helper_dpmn(self.dpmns)

def codeblock_modifyd1defaults(self):
    self.d1defaults = par.helper_d1(self.d1)

def codeblock_modifyd2defaults(self):
    self.d2defaults = par.helper_d2(self.d2)

def codeblock_modifyactionchannels(self):
    self.actionchannels = par.helper_actionchannels(self.channels)

#popconstruct.py: to modify population parameters

def codeblock_popconstruct(self):
    self.popdata = popconstruct.helper_popconstruct(self.actionchannels, self.popspecific, self.celldefaults, self.receptordefaults, self.basestim, self.dpmndefaults, self.d1defaults, self.d2defaults)

def codeblock_poppathways(self):
    self.pathways = popconstruct.helper_poppathways(self.popdata, self.newpathways)

#init_params.py: Q-values initialization and update

def codeblock_init_Q_support_params(self):
    self.Q_support_params = qval.helper_init_Q_support_params(self.q_support)

def codeblock_update_Q_support_params(self,reward_val, chosen_action):
    self.Q_support_params = qval.helper_update_Q_support_params(self.Q_support_params,self.reward_val,pl.chosen_action)

def codeblock_init_Q_df(self):
    self.Q_df = qval.helper_init_Q_df(self.channels)

def codeblock_update_Q_df(self):
    self.Q_df, self.Q_support_params, self.dpmndefaults = qval.helper_update_Q_df(self.Q_df, self.Q_support_params, self.dpmndefaults,pl.trial_num)

# 2.2 Create reward pipeline 
    
def create_reward_pipeline(pl):
    rsg = cbgt.Pipeline() #rsg is short for 'reward schedule generator'

    # = 
    (rsg.volatile_pattern, rsg.cp_idx,  rsg.cp_indicator, rsg.noisy_pattern, rsg.t_epochs, rsg.block) = rsg[gen.GenRewardSchedule](
        rsg.n_trials,
        rsg.volatility,
        rsg.conflict,
        rsg.reward_mu,
        rsg.reward_std, pl.actionchannels
    ).shape(6)
    
    return rsg


def create_stop_pipeline(pl): #STN
    stop = cbgt.Pipeline() 

    
    (stop.stop_df, stop.stop_channels_df, stop.stop_amplitude_df, stop.stop_onset_df, stop.stop_duration_df) = stop[gen_stop.GenStopSchedule](
        stop.stop_signal_probability,
        pl.actionchannels,
        stop.n_trials,
        stop.stop_signal_channel,
        stop.stop_signal_amplitude,
        stop.stop_signal_onset,
        stop.stop_signal_present, stop.stop_signal_duration
     ).shape(5)
    
    #print(stop)
    return stop


def create_stop_pipeline_2(pl): #D2STR
    stop_2 = cbgt.Pipeline() 

    
    (stop_2.stop_df_2, stop_2.stop_channels_df_2, stop_2.stop_amplitude_df_2, stop_2.stop_onset_df_2, stop_2.stop_duration_df_2) = stop_2[gen_stop_2.GenStopSchedule_2](
        stop_2.stop_signal_probability_2,
        pl.actionchannels,
        stop_2.n_trials,
        stop_2.stop_signal_channel_2,
        stop_2.stop_signal_amplitude_2,
        stop_2.stop_signal_onset_2,
        stop_2.stop_signal_present_2, stop_2.stop_signal_duration_2
     ).shape(5)
    
    #print(stop)
    return stop_2


# 2.3 Create q-values pipeline 

def create_q_val_pipeline(pl): 
    
    q_val_pipe = cbgt.Pipeline()

    #Defining necessary function modules: 
    #qvalues.py
    q_val_pipe.Q_support_params = q_val_pipe[qval.helper_init_Q_support_params]()
    q_val_pipe.Q_df = q_val_pipe[qval.helper_init_Q_df](pl.actionchannels)

    #rsg.reward_val = q_val_pipe[qval.get_reward_value](rsg.t1_epochs,rsg.t2_epochs,pl.chosen_action,pl.trial_num) 
    #q_val_pipe.Q_support_params = q_val_pipe[qval.helper_update_Q_support_params](q_val_pipe.Q_support_params,rsg.reward_val,pl.chosen_action)
    #(q_val_pipe.Q_df, q_val_pipe.Q_support_params, pl.dpmndefaults) = q_val_pipe[qval.helper_update_Q_df](q_val_pipe.Q_df,q_val_pipe.Q_support_params,pl.dpmndefaults,pl.trial_num).shape(3)
    return q_val_pipe
    
# 3. CREATE CBGT PIPELINE - MAIN

def create_main_pipeline(runloop):
    
    pl = cbgt.Pipeline()
    
    pl.add(codeblock_experimentchoice)
    
    pl.add(codeblock_modifyactionchannels)
    
    rsg = create_reward_pipeline(pl)
    #Adding rsg pipeline to the network pipeline: 
    pl.add(rsg)
    
    if experiment_choice == 'stopsignal':
        stop = create_stop_pipeline(pl)
        stop_2 = create_stop_pipeline_2(pl)
        pl.add(stop)
        pl.add(stop_2)
    
    #to update the Q-values 
    pl.trial_num = 0 #first row of Q-values df - initialization data 
    pl.chosen_action = None # 2 #chosen action for the current trial
    
    #Defining necessary function modules: 

    #init_params.py: default neuronal values 
    pl.celldefaults = par.helper_cellparams()
    pl.popspecific = par.helper_popspecific()
    pl.receptordefaults = par.helper_receptor()
    pl.basestim = par.helper_basestim()
    pl.dpmndefaults = par.helper_dpmn()
    pl.d1defaults = par.helper_d1()
    pl.d2defaults = par.helper_d2()
    #pl.actionchannels = pl[par.helper_actionchannels]()


    #popconstruct.py: default population parameters 
    pl.popdata = pl[popconstruct.helper_popconstruct](pl.actionchannels, pl.popspecific, pl.celldefaults, pl.receptordefaults, pl.basestim, pl.dpmndefaults, pl.d1defaults, pl.d2defaults)
    pl.pathways = pl[popconstruct.helper_poppathways](pl.popdata)
    pl.add(codeblock_poppathways)
    
    #popconstruct.py: to create connectivity grids
    pl.connectivity_AMPA, pl.meaneff_AMPA, pl.plastic_AMPA = pl[popconstruct.helper_connectivity]('AMPA', pl.popdata, pl.pathways).shape(3)
    pl.connectivity_GABA, pl.meaneff_GABA, pl.plastic_GABA = pl[popconstruct.helper_connectivity]('GABA', pl.popdata, pl.pathways).shape(3)
    pl.connectivity_NMDA, pl.meaneff_NMDA, pl.plastic_NMDA = pl[popconstruct.helper_connectivity]('NMDA', pl.popdata, pl.pathways).shape(3)
    
    #Adding codeblocks to the newtork pipeline: 
    pl.add(codeblock_modifycelldefaults)
    pl.add(codeblock_modifypopspecific)
    pl.add(codeblock_modifyreceptordefaults)
    pl.add(codeblock_modifybasestim)
    pl.add(codeblock_modifydpmndefaults)
    pl.add(codeblock_modifyd1defaults)
    pl.add(codeblock_modifyd2defaults)
    pl.add(codeblock_popconstruct)
    
    
    q_val_pipe = create_q_val_pipeline(pl)
    
    #Adding the q_val_pipe to the main network pipeline pl:
    pl.add(q_val_pipe)
    
    # Agent mega loop - updated trial wise qvalues and chosen action
    if runloop:
        mega_loop = ml.mega_loop
        pl.add(mega_loop)
    
    return pl
