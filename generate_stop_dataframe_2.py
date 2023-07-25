import numpy as np
import random
import pandas as pd
from tracetype import *


def define_stop_2(stop_2_signal_probability, actionchannels, n_trials, pop_names, stop_2_signal_channel, stop_2_signal_amplitude, stop_2_signal_onset, stop_2_signal_duration, stop_2_signal_present, stop_2_signal_population ):

    stop_2_df = pd.DataFrame() 
    stop_2_df["stop_2_signal_present"] = [stop_2_signal_present]
    stop_2_df["stop_2_signal_probability"] = [stop_2_signal_probability]
    stop_2_df["stop_2_signal_channel"] = [stop_2_signal_channel]
    stop_2_df["stop_2_signal_population"] = [stop_2_signal_population]

    
    trial_index = np.arange(n_trials)
    
    stop_2_amplitude_df = pd.DataFrame()
    stop_2_onset_df = pd.DataFrame()
    stop_2_duration_df = pd.DataFrame()
    
    stop_2_amplitude_df = pd.DataFrame(columns=list(actionchannels.action.values)+["trial_num"])
    stop_2_amplitude_df["trial_num"] = trial_index
    for act in list(actionchannels.action.values):
        stop_2_amplitude_df[act] = stop_2_signal_amplitude
    
    
    stop_2_onset_df = pd.DataFrame(columns=list(actionchannels.action.values)+["trial_num"])
    stop_2_onset_df["trial_num"] = trial_index
    for act in list(actionchannels.action.values):
        stop_2_onset_df[act] = stop_2_signal_onset
        
    stop_2_duration_df = pd.DataFrame(columns=list(actionchannels.action.values)+["trial_num"])
    stop_2_duration_df["trial_num"] = trial_index
    for act in list(actionchannels.action.values):
        stop_2_duration_df[act] = stop_2_signal_duration

    
    stop_2_channels_df = pd.DataFrame(columns=list(actionchannels.action.values)+["trial_num"])
    stop_2_channels_df["trial_num"] = trial_index
    for act in list(actionchannels.action.values):
        stop_2_channels_df[act] = False


    #str_pops = ["D1STR", "D2STR"]
    pops = [ untrace(x) for x in pop_names]
#     print(pops)
    stop_2_populations_df = pd.DataFrame(columns=pops+["trial_num"])
    stop_2_populations_df["trial_num"] = trial_index
    for pop in pops:
        #if optostim_signal_present:
        stop_2_populations_df[pop] = False

        
        
    trial_indices = np.zeros(n_trials)

    #print(type(opt_signal_probability))
    if isinstance(stop_2_signal_probability,float) == True:
        trials_with_stop_2_signal = np.random.choice(trial_index,int(n_trials*stop_2_signal_probability), replace=False)
    elif type(stop_2_signal_probability) == list:
        trials_with_stop_2_signal = stop_2_signal_probability
    
    stop_2_list_trials = trials_with_stop_2_signal
    
    print(trials_with_stop_2_signal)        
    
    for n in np.arange(n_trials):
        
        if stop_2_signal_channel == "any":
            channels_stop2_ = np.random.choice(list(actionchannels.action.values),1, replace=False)
        elif stop_2_signal_channel == "all":
            if stop_2_signal_population not in ['FSI','LIPI']:
                channels_stop_2 = list(actionchannels.action.values)
            else:
                channels_stop_2 = np.nan
        
        if n in trials_with_stop_2_signal:
            for col in channels_stop_2:
                stop_2_channels_df.loc[n,col] = True
    
            for pop in stop_2_signal_population:
                #print("pop stop_2",pop)
                stop_2_populations_df.loc[n,pop] = True
                #print(stop_2_populations_df.loc[n,pop])
    
    return stop_2_df, stop_2_channels_df, stop_2_amplitude_df, stop_2_onset_df, stop_2_duration_df, stop_2_populations_df, stop_2_list_trials 


def GenStopSchedule_2(stop_2_signal_probability, actionchannels, n_trials, popdata, stop_2_signal_channel, stop_2_signal_amplitude, stop_2_signal_onset, stop_2_signal_duration, stop_2_signal_present, stop_2_signal_population):

    stop_2_df, stop_2_channels_df, stop_2_amplitude_df, stop_2_onset_df, stop_2_duration_df, stop_2_populations_df, stop_2_list_trials = define_stop_2(stop_2_signal_probability, actionchannels, n_trials, popdata, stop_2_signal_channel, stop_2_signal_amplitude, stop_2_signal_onset, stop_2_signal_duration, stop_2_signal_present, stop_2_signal_population)
    

    return stop_2_df, stop_2_channels_df, stop_2_amplitude_df, stop_2_onset_df, stop_2_duration_df, stop_2_populations_df, stop_2_list_trials
