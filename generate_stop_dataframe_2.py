import numpy as np
import random
import pandas as pd




def define_stop_2(stop_signal_probability_2, actionchannels, n_trials, stop_signal_channel_2, stop_signal_amplitude_2, stop_signal_onset_2, stop_signal_present_2, stop_signal_duration_2):
    #print(actionchannels)

    stop_df_2 = pd.DataFrame() 
    #stop_df["stop_signal_amplitude"] = [stop_signal_amplitude]
    #stop_df["stop_signal_onset"] = [stop_signal_onset]
    stop_df_2["stop_signal_present_2"] = [stop_signal_present_2]
    stop_df_2["stop_signal_probability_2"] = [stop_signal_probability_2]
    stop_df_2["stop_signal_channel_2"] = [stop_signal_channel_2]
    
    
    
    
    trial_index = np.arange(n_trials)
    
    stop_amplitude_df_2 = pd.DataFrame()
    stop_onset_df_2 = pd.DataFrame()
    
    stop_amplitude_df_2 = pd.DataFrame(columns=list(actionchannels.action.values)+["trial_num"])
    stop_amplitude_df_2["trial_num"] = trial_index
    for act in list(actionchannels.action.values):
        stop_amplitude_df_2[act] = stop_signal_amplitude_2
    
    
    stop_onset_df_2 = pd.DataFrame(columns=list(actionchannels.action.values)+["trial_num"])
    stop_onset_df_2["trial_num"] = trial_index
    for act in list(actionchannels.action.values):
        stop_onset_df_2[act] = stop_signal_onset_2
        
    stop_duration_df_2 = pd.DataFrame(columns=list(actionchannels.action.values)+["trial_num"])
    stop_duration_df_2["trial_num"] = trial_index
    for act in list(actionchannels.action.values):
        stop_duration_df_2[act] = stop_signal_duration_2

    
    
    stop_channels_df_2 = pd.DataFrame(columns=list(actionchannels.action.values)+["trial_num"])
    stop_channels_df_2["trial_num"] = trial_index
    for act in list(actionchannels.action.values):
        stop_channels_df_2[act] = False
         
    trial_indices = np.zeros(n_trials)

    print(type(stop_signal_probability_2))
    if isinstance(stop_signal_probability_2,float) == True:
        trials_with_stop_signal = np.random.choice(trial_index,int(n_trials*stop_signal_probability_2), replace=False)
    elif type(stop_signal_probability_2) == list:
        trials_with_stop_signal = stop_signal_probability_2
    
    print(trials_with_stop_signal)        
    for n in np.arange(n_trials):
        
        if stop_signal_channel_2 == "any":
            channels_stop = np.random.choice(list(actionchannels.action.values),1, replace=False)
        elif stop_signal_channel_2 == "all":
            channels_stop = list(actionchannels.action.values)
        
        if n in trials_with_stop_signal:
            for col in channels_stop:
                stop_channels_df_2.loc[n,col] = True
    
    return stop_df_2, stop_channels_df_2, stop_amplitude_df_2, stop_onset_df_2, stop_duration_df_2 #reward_t1, reward_t2


def GenStopSchedule_2(stop_signal_probability_2, actionchannels, n_trials, stop_signal_channel_2, stop_signal_amplitude_2, stop_signal_onset_2, stop_signal_present_2, stop_signal_duration_2):
    
    #print("begin GenStopSchedule")
    #reward_t1, reward_t2
    stop_df_2, stop_channels_df_2, stop_amplitude_df_2, stop_onset_df_2, stop_duration_df_2 = define_stop_2(
        stop_signal_probability_2, actionchannels, n_trials, stop_signal_channel_2, stop_signal_amplitude_2, stop_signal_onset_2, stop_signal_present_2, stop_signal_duration_2)
    
    #print("stop_df")
    #print(stop_df)
    
    #print("stop_channels_df")
    #print(stop_channels_df)
    return stop_df_2, stop_channels_df_2, stop_amplitude_df_2, stop_onset_df_2, stop_duration_df_2

