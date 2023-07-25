import numpy as np
import random
import pandas as pd
from tracetype import *



def define_opt(opt_signal_probability, actionchannels, n_trials, pop_names, opt_signal_channel,opt_signal_amplitude,opt_signal_onset,opt_signal_duration,opt_signal_present,opt_signal_population ):
    #print(actionchannels)

    opt_df = pd.DataFrame() 
#     stop_df["stop_signal_amplitude"] = [stop_signal_amplitude]
#     stop_df["stop_signal_onset"] = [stop_signal_onset]
    opt_df["opt_signal_present"] = [opt_signal_present]
    opt_df["opt_signal_probability"] = [opt_signal_probability]
    opt_df["opt_signal_channel"] = [opt_signal_channel]
    opt_df["opt_signal_population"] = [opt_signal_population]
    
    
    trial_index = np.arange(n_trials)
    
    opt_amplitude_df = pd.DataFrame()
    opt_onset_df = pd.DataFrame()
    
    opt_amplitude_df = pd.DataFrame(columns=list(actionchannels.action.values)+["trial_num"])
    opt_amplitude_df["trial_num"] = trial_index
    for act in list(actionchannels.action.values):
        opt_amplitude_df[act] = opt_signal_amplitude
    
    
    opt_onset_df = pd.DataFrame(columns=list(actionchannels.action.values)+["trial_num"])
    opt_onset_df["trial_num"] = trial_index
    for act in list(actionchannels.action.values):
        opt_onset_df[act] = opt_signal_onset

    opt_duration_df = pd.DataFrame(columns=list(actionchannels.action.values)+["trial_num"])
    opt_duration_df["trial_num"] = trial_index
    for act in list(actionchannels.action.values):
        opt_duration_df[act] = opt_signal_duration    
    
    opt_channels_df = pd.DataFrame(columns=list(actionchannels.action.values)+["trial_num"])
    opt_channels_df["trial_num"] = trial_index
    for act in list(actionchannels.action.values):
        opt_channels_df[act] = False


    #str_pops = ["D1STR", "D2STR"]
    pops = [ untrace(x) for x in pop_names]
#     print(pops)
    opt_populations_df = pd.DataFrame(columns=pops+["trial_num"])
    opt_populations_df["trial_num"] = trial_index
    for pop in pops:
        #if optostim_signal_present:
        opt_populations_df[pop] = False

        
        
    trial_indices = np.zeros(n_trials)

    print(type(opt_signal_probability))
    if isinstance(opt_signal_probability,float) == True:
        trials_with_opt_signal = np.random.choice(trial_index,int(n_trials*opt_signal_probability), replace=False)
    elif type(opt_signal_probability) == list or type(opt_signal_probability) == np.ndarray:
        trials_with_opt_signal = opt_signal_probability
    
    opt_list_trials = trials_with_opt_signal
    
    print(trials_with_opt_signal)        
    
    for n in np.arange(n_trials):
        
        if opt_signal_channel == "any":
            channels_opt = np.random.choice(list(actionchannels.action.values),1, replace=False)
        elif opt_signal_channel == "all":
            if opt_signal_population not in ['FSI','LIPI']:
                channels_opt = list(actionchannels.action.values)
            else:
                channels_opt = np.nan
        
        if n in trials_with_opt_signal:
            for col in channels_opt:
                opt_channels_df.loc[n,col] = True
    
            for pop in opt_signal_population:
                print("pop",pop)
                opt_populations_df.loc[n,pop] = True
                print(opt_populations_df.loc[n,pop])
    
    return opt_df, opt_channels_df, opt_amplitude_df, opt_onset_df,opt_duration_df,opt_populations_df, opt_list_trials #reward_t1, reward_t2


def GenOptSchedule(opt_signal_probability, actionchannels, n_trials,popdata, opt_signal_channel, opt_signal_amplitude, opt_signal_onset,opt_signal_duration, opt_signal_present,opt_signal_population):
    
    print("begin GenOptSchedule")
    #reward_t1, reward_t2
    opt_df, opt_channels_df, opt_amplitude_df, opt_onset_df,opt_duration_df,opt_populations_df,opt_list_trials = define_opt(
        opt_signal_probability, actionchannels, n_trials,popdata, opt_signal_channel,opt_signal_amplitude, opt_signal_onset,opt_signal_duration,opt_signal_present,opt_signal_population)
    
    print("opt_df")
    print(opt_df)
    
    print("opt_channels_df")
    print(opt_channels_df)
    return opt_df, opt_channels_df, opt_amplitude_df, opt_onset_df,opt_duration_df, opt_populations_df, opt_list_trials
