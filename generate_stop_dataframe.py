import numpy as np
import random
import pandas as pd
from tracetype import *


def define_stop(stop_signal_probability, actionchannels, n_trials, pop_names, stop_signal_channel, stop_signal_amplitude, stop_signal_onset, stop_signal_duration, stop_signal_present, stop_signal_population ):
    #print(actionchannels)

    
    stop_df = pd.DataFrame() 
    
    assert isinstance(stop_signal_probability,list)
    assert isinstance(stop_signal_present,list)
    assert isinstance(stop_signal_amplitude,list)
    assert isinstance(stop_signal_onset,list)
    assert isinstance(stop_signal_duration,list)
    assert isinstance(stop_signal_channel,list)
    assert isinstance(stop_signal_population,list)
    
    lengths = {
        len(stop_signal_probability),
        len(stop_signal_present),
        len(stop_signal_amplitude),
        len(stop_signal_onset),
        len(stop_signal_duration),
        len(stop_signal_channel),
        len(stop_signal_population),
    }
    assert len(lengths) == 1, "not all stop signal lists are same length"
    
    
    stop_df["stop_signal_present"] = stop_signal_present
    stop_df["stop_signal_probability"] = stop_signal_probability
    stop_df["stop_signal_channel"] = stop_signal_channel
    stop_df["stop_signal_population"] = stop_signal_population
    
    
    stop_amplitude_dfs = []
    stop_onset_dfs = []
    stop_duration_dfs = []
    stop_channels_dfs = []
    stop_populations_dfs = []
    stop_list_trials_list = []
    
    
    for i in np.arange(len(stop_signal_population)):
    
        trial_index = np.arange(n_trials)

        stop_amplitude_df = pd.DataFrame()
        stop_onset_df = pd.DataFrame()
        stop_duration_df = pd.DataFrame()

        stop_amplitude_df = pd.DataFrame(columns=list(actionchannels.action.values)+["trial_num"])
        stop_amplitude_df["trial_num"] = trial_index
        for act in list(actionchannels.action.values):
            stop_amplitude_df[act] = stop_signal_amplitude[i]

        stop_onset_df = pd.DataFrame(columns=list(actionchannels.action.values)+["trial_num"])
        stop_onset_df["trial_num"] = trial_index
        for act in list(actionchannels.action.values):
            stop_onset_df[act] = stop_signal_onset[i]

        stop_duration_df = pd.DataFrame(columns=list(actionchannels.action.values)+["trial_num"])
        stop_duration_df["trial_num"] = trial_index
        for act in list(actionchannels.action.values):
            stop_duration_df[act] = stop_signal_duration[i]

        stop_channels_df = pd.DataFrame(columns=list(actionchannels.action.values)+["trial_num"])
        stop_channels_df["trial_num"] = trial_index
        for act in list(actionchannels.action.values):
            stop_channels_df[act] = False

        pops = [ untrace(x) for x in pop_names]
    #     print(pops)
        stop_populations_df = pd.DataFrame(columns=pops+["trial_num"])
        stop_populations_df["trial_num"] = trial_index
        for pop in pops:
            stop_populations_df[pop] = False



        trial_indices = np.zeros(n_trials)
        if isinstance(stop_signal_probability[i],float) == True:
            trials_with_stop_signal = np.random.choice(trial_index,int(n_trials*stop_signal_probability[i]), replace=False)
        elif type(stop_signal_probability[i]) == list:
            trials_with_stop_signal = stop_signal_probability[i]

        stop_list_trials = trials_with_stop_signal

        print(trials_with_stop_signal)        

        for n in np.arange(n_trials):

            if stop_signal_channel[i] == "any":
                channels_stop = np.random.choice(list(actionchannels.action.values),1, replace=False)
            elif stop_signal_channel[i] == "all":
                if stop_signal_population[i] not in ['FSI','CxI']:
                    channels_stop = list(actionchannels.action.values)
                else:
                    channels_stop = np.nan
            elif stop_signal_channel[i] in list(actionchannels.action.values):
                if stop_signal_population[i] not in ['FSI','CxI']:
                    channels_stop = [stop_signal_channel[i]]
                else:
                    channels_stop = np.nan
            elif isinstance(stop_signal_channel[i],(list,tuple)):
                if stop_signal_population[i] not in ['FSI','CxI']:
                    channels_stop = list(stop_signal_channel[i])
                else:
                    channels_stop = np.nan

            if n in trials_with_stop_signal:
                for col in channels_stop:
                    stop_channels_df.loc[n,col] = True

                for pop in stop_signal_population[i]:
                    #print("pop stop_1",pop)
                    stop_populations_df.loc[n,pop] = True
                    #print(stop_populations_df.loc[n,pop])
        
        stop_amplitude_dfs.append(stop_amplitude_df)
        stop_onset_dfs.append(stop_amplitude_df)
        stop_duration_dfs.append(stop_duration_df)
        stop_channels_dfs.append(stop_channels_df)
        stop_populations_dfs.append(stop_populations_df)
        stop_list_trials_list.append(stop_list_trials)
    
          
    print("stop_amplitude_dfs",stop_amplitude_dfs)
    
    return stop_df, stop_channels_dfs, stop_amplitude_dfs, stop_onset_dfs, stop_duration_dfs, stop_populations_dfs, stop_list_trials_list 


def GenStopSchedule(stop_signal_probability, actionchannels, n_trials, popdata, stop_signal_channel, stop_signal_amplitude, stop_signal_onset, stop_signal_duration, stop_signal_present, stop_signal_population):
    
    stop_df, stop_channels_dfs, stop_amplitude_dfs, stop_onset_dfs, stop_duration_dfs, stop_populations_dfs, stop_list_trials_list = define_stop(stop_signal_probability, actionchannels, n_trials, popdata, stop_signal_channel, stop_signal_amplitude, stop_signal_onset, stop_signal_duration, stop_signal_present, stop_signal_population)
    
    return stop_df, stop_channels_dfs, stop_amplitude_dfs, stop_onset_dfs, stop_duration_dfs, stop_populations_dfs, stop_list_trials_list
