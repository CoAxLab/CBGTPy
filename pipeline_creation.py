# 1. IMPORTING SCRIPTS

import cbgt as cbgt
from frontendhelpers import * 
from tracetype import *
import qvalues as qval
import generateepochs as gen
import generate_opt_dataframe as gen_opt
from agentmatrixinit import *
import pdb

experiment_choice = None
par = "Taco"#None
popconstruct = None
interface = None
gen_stop = None
gen_stop_2 = None



def choose_pipeline(choice):
    print("in choose pipeline")
    global experiment_choice
    global par
    global popconstruct
    global interface
    global gen_stop
    global gen_stop_2
    global number_of_choices
    experiment_choice = choice
    
    if choice == 'n-choice':
        import init_params_nchoice as par
        import popconstruct_nchoice as popconstruct
        import interface_nchoice as interface
        

    if choice == 'stop-signal':
        import init_params_stopsignal as par
        import popconstruct_stopsignal as popconstruct
        import interface_stopsignal as interface
        import generate_stop_dataframe as gen_stop
        import generate_stop_dataframe_2 as gen_stop_2
        
#     return [par,popconstruct,ml]
#     print("par in choose_pipeline",par)
# 2. NETWORK PIPELINE

# 2.1. Defining necessary codeblocks:

#MODIFIERS:

#init_params.py: to modify the neuronal default values

def codeblock_experimentchoice(self):
#     print("codeblock_experimentchoice, thread_id",self.thread_id)
    choose_pipeline(self.experimentchoice)

def codeblock_modifycelldefaults(self):
#     print("par in modifycelldefaults, thread_id",self.thread_id,par)
    self.celldefaults = self.par.helper_cellparams(self.params)

def codeblock_modifypopspecific(self):
    self.popspecific = self.par.helper_popspecific(self.pops)

def codeblock_modifyreceptordefaults(self):
    self.receptordefaults = self.par.helper_receptor(self.receps)

def codeblock_modifybasestim(self):
    self.basestim = self.par.helper_basestim(self.base)

def codeblock_modifydpmndefaults(self):
    self.dpmndefaults = self.par.helper_dpmn(self.dpmns)

def codeblock_modifyd1defaults(self):
    self.d1defaults = self.par.helper_d1(self.d1)

def codeblock_modifyd2defaults(self):
    self.d2defaults = self.par.helper_d2(self.d2)

def codeblock_modifyactionchannels(self):
#     print("par in modifyactionchannels, thread_id",self.thread_id,par)
    self.actionchannels = self.par.helper_actionchannels(self.channels)
    
def codeblock_modifyexperimentdefaults(self):
    if self.inter_trial_interval == None:
        self.inter_trial_interval = 600
    if self.thalamic_threshold == None:
        self.thalamic_threshold = 30.
    if self.movement_time == None:
        self.trial_wise_movement_times = np.round(np.random.normal(250.,1.5,self.n_trials),0)
    elif isinstance(self.movement_time,list):
#         self.movement_time_type = self.movement_time[0]
        if self.movement_time[0] == "mean":
            self.trial_wise_movement_times = np.round(np.random.normal(self.movement_time[1],1.5,self.n_trials),0)
        elif self.movement_time[0] == "constant":
            self.trial_wise_movement_times = np.hstack([self.movement_time[1]]*self.n_trials)
    
    if self.choice_timeout == None:
        self.choice_timeout = 1000.

#popconstruct.py: to modify population parameters

def codeblock_popconstruct(self):
    self.popdata = self.popconstruct.helper_popconstruct(self.actionchannels, self.popspecific, self.celldefaults, self.receptordefaults, self.basestim, self.dpmndefaults, self.d1defaults, self.d2defaults)

def codeblock_poppathways(self):
    self.pathways = self.popconstruct.helper_poppathways(self.popdata,self.number_of_choices,self.newpathways)

#init_params.py: Q-values initialization and update

def codeblock_init_Q_support_params(self):
    self.Q_support_params = qval.helper_init_Q_support_params(self.Q_support_params)

def codeblock_update_Q_support_params(self,reward_val, chosen_action):
    self.Q_support_params = qval.helper_update_Q_support_params(self.Q_support_params,self.reward_val,pl.chosen_action)

def codeblock_init_Q_df(self):
    self.Q_df = qval.helper_init_Q_df(self.channels,self.Q_df_set)

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
        
    print("in reward pipeline")
    return rsg


def create_stop_pipeline(pl): #STN
    stop = cbgt.Pipeline() 

    
    (stop.stop_df, stop.stop_channels_dfs, stop.stop_amplitude_dfs, stop.stop_onset_dfs, stop.stop_duration_dfs, stop.stop_populations_dfs, stop.stop_list_trials_list) = stop[gen_stop.GenStopSchedule](
        stop.stop_signal_probability,
        pl.actionchannels,
        stop.n_trials,
        stop.popdata,
        stop.stop_signal_channel,
        stop.stop_signal_amplitude,
        stop.stop_signal_onset,
        stop.stop_signal_duration,
        stop.stop_signal_present,
        stop.stop_signal_population
     ).shape(7)
   
    #print(stop)
    return stop


# def create_stop_pipeline_2(pl): #D2STR
#     stop_2 = cbgt.Pipeline() 

    
#     (stop_2.stop_2_df, stop_2.stop_2_channels_df, stop_2.stop_2_amplitude_df, stop_2.stop_2_onset_df, stop_2.stop_2_duration_df, stop_2.stop_2_populations_df, stop_2.stop_2_list_trials) = stop_2[gen_stop_2.GenStopSchedule_2](
#         stop_2.stop_2_signal_probability,
#         pl.actionchannels,
#         stop_2.n_trials,
#         stop_2.popdata,
#         stop_2.stop_2_signal_channel,
#         stop_2.stop_2_signal_amplitude,
#         stop_2.stop_2_signal_onset,
#         stop_2.stop_2_signal_duration,
#         stop_2.stop_2_signal_present, 
#         stop_2.stop_2_signal_population,
#      ).shape(7)
    
#     #print(stop)
#     return stop_2


def create_opt_pipeline(pl):
    opt = cbgt.Pipeline() #rsg is short for 'reward schedule generator'
    
    (opt.opt_df, opt.opt_channels_df, opt.opt_amplitude_df, opt.opt_onset_df, opt.opt_duration_df, opt.opt_populations_df,opt.opt_list_trials) = opt[gen_opt.GenOptSchedule](
        opt.opt_signal_probability,
        pl.actionchannels,
        opt.n_trials,
        opt.popdata,
        opt.opt_signal_channel,
        opt.opt_signal_amplitude,
        opt.opt_signal_onset,
        opt.opt_signal_duration,
        opt.opt_signal_present,
        opt.opt_signal_population
     ).shape(7)
    
    #print(stop)
    return opt


# 2.3 Create q-values pipeline 

def create_q_val_pipeline(pl): 
    
    q_val_pipe = cbgt.Pipeline()

    #Defining necessary function modules: 
    #qvalues.py
    q_val_pipe.Q_support_params = q_val_pipe[qval.helper_init_Q_support_params](pl.Q_support_params)
    q_val_pipe.Q_df = q_val_pipe[qval.helper_init_Q_df](pl.actionchannels,pl.Q_df_set)

    #rsg.reward_val = q_val_pipe[qval.get_reward_value](rsg.t1_epochs,rsg.t2_epochs,pl.chosen_action,pl.trial_num) 
    #q_val_pipe.Q_support_params = q_val_pipe[qval.helper_update_Q_support_params](q_val_pipe.Q_support_params,rsg.reward_val,pl.chosen_action)
    #(q_val_pipe.Q_df, q_val_pipe.Q_support_params, pl.dpmndefaults) = q_val_pipe[qval.helper_update_Q_df](q_val_pipe.Q_df,q_val_pipe.Q_support_params,pl.dpmndefaults,pl.trial_num).shape(3)
    return q_val_pipe
    
    
    
def create_test_pipeline(runloop):
    
    pl = cbgt.Pipeline()
    
    pl.add(codeblock_experimentchoice)
    pl.par = par
    pl.popconstruct = popconstruct
    pl.interface = interface
    
    pl.add(codeblock_modifyactionchannels)
    pl.add(codeblock_modifycelldefaults)
    
    return pl
    
    
    
# 3. CREATE CBGT PIPELINE - MAIN

def create_main_pipeline(runloop):#,num_choices):
    
    pl = cbgt.Pipeline()
    
    
    pl.add(codeblock_experimentchoice)
    pl.par = par
    pl.popconstruct = popconstruct
    pl.interface = interface
    if experiment_choice == "stop-signal":
        pl.gen_stop = gen_stop
        pl.gen_stop_2 = gen_stop_2
        
        
    pl.add(codeblock_modifyactionchannels)
    
    pl.add(codeblock_modifyexperimentdefaults)
    
    rsg = create_reward_pipeline(pl)
    #Adding rsg pipeline to the network pipeline: 
    pl.add(rsg)
    
#    if experiment_choice == 'stopsignal':
#        stop = create_stop_pipeline(pl)
#        stop_2 = create_stop_pipeline_2(pl)
#        pl.add(stop)
#        pl.add(stop_2)
    
    #to update the Q-values 
    pl.trial_num = 0 #first row of Q-values df - initialization data 
    pl.chosen_action = None # 2 #chosen action for the current trial
    #pl.number_of_choices = num_choices
    #print("number of choices",pl.number_of_choices)
    
    
    # Default experimental parameters
#     if pl.inter_trial_interval == None:
#         pl.inter_trial_interval = 600
        
    
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
    pl.pathways = pl[popconstruct.helper_poppathways](pl.popdata,pl.number_of_choices)
  
    #popconstruct.py: to create connectivity grids
    opt = create_opt_pipeline(pl)
    pl.add(opt)
    
    if experiment_choice == 'stop-signal':
       stop = create_stop_pipeline(pl)
       #stop_2 = create_stop_pipeline_2(pl)
       pl.add(stop)
       #pl.add(stop_2)
   
    #Adding codeblocks to the newtork pipeline: 
    pl.add(codeblock_modifycelldefaults)
    pl.add(codeblock_modifypopspecific)
    pl.add(codeblock_modifyreceptordefaults)
    pl.add(codeblock_modifybasestim)
    pl.add(codeblock_modifydpmndefaults)
    pl.add(codeblock_modifyd1defaults)
    pl.add(codeblock_modifyd2defaults)
    pl.add(codeblock_popconstruct)
    pl.add(codeblock_poppathways)
    
    
    
    pl.connectivity_AMPA, pl.meaneff_AMPA, pl.plastic_AMPA = pl[popconstruct.helper_connectivity]('AMPA', pl.popdata, pl.pathways).shape(3)
    pl.connectivity_GABA, pl.meaneff_GABA, pl.plastic_GABA = pl[popconstruct.helper_connectivity]('GABA', pl.popdata, pl.pathways).shape(3)
    pl.connectivity_NMDA, pl.meaneff_NMDA, pl.plastic_NMDA = pl[popconstruct.helper_connectivity]('NMDA', pl.popdata, pl.pathways).shape(3)
    
    q_val_pipe = create_q_val_pipeline(pl)
    
    #Adding the q_val_pipe to the main network pipeline pl:
    pl.add(q_val_pipe)
    
    
    # Agent mega loop - updated trial wise qvalues and chosen action
    if runloop:
        mega_loop = interface.mega_loop
        pl.add(mega_loop)
    
    return pl
