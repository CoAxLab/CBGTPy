import numpy as np
import random
import pandas as pd
from tracetype import *



def define_opt(opt_signal_probability, actionchannels, n_trials, pop_names, opt_signal_channel,opt_signal_amplitude,opt_signal_onset,opt_signal_duration,opt_signal_present,opt_signal_population ):
    #print(actionchannels)


    opt_df = pd.DataFrame()


    assert isinstance(opt_signal_probability,list)
    assert isinstance(opt_signal_present,list)
    assert isinstance(opt_signal_amplitude,list)
    assert isinstance(opt_signal_onset,list)
    assert isinstance(opt_signal_duration,list)
    assert isinstance(opt_signal_channel,list)
    assert isinstance(opt_signal_population,list)

    lengths = {
        len(opt_signal_probability),
        len(opt_signal_present),
        len(opt_signal_amplitude),
        len(opt_signal_onset),
        len(opt_signal_duration),
        len(opt_signal_channel),
        len(opt_signal_population),
    }
    assert len(lengths) == 1, "not all opt signal lists are same length"


    opt_df["opt_signal_present"] = opt_signal_present
    opt_df["opt_signal_probability"] = opt_signal_probability
    opt_df["opt_signal_channel"] = opt_signal_channel
    opt_df["opt_signal_population"] = opt_signal_population


    opt_amplitude_dfs = []
    opt_onset_dfs = []
    opt_duration_dfs = []
    opt_channels_dfs = []
    opt_populations_dfs = []
    opt_list_trials_list = []


    for i in np.arange(len(opt_signal_population)):

        trial_index = np.arange(n_trials)

        opt_amplitude_df = pd.DataFrame()
        opt_onset_df = pd.DataFrame()
        opt_duration_df = pd.DataFrame()

        opt_amplitude_df = pd.DataFrame(columns=list(actionchannels.action.values)+["trial_num"])
        opt_amplitude_df["trial_num"] = trial_index
        for act in list(actionchannels.action.values):
            opt_amplitude_df[act] = opt_signal_amplitude[i]


        opt_onset_df = pd.DataFrame(columns=list(actionchannels.action.values)+["trial_num"])
        opt_onset_df["trial_num"] = trial_index
        for act in list(actionchannels.action.values):
            opt_onset_df[act] = opt_signal_onset[i]

        opt_duration_df = pd.DataFrame(columns=list(actionchannels.action.values)+["trial_num"])
        opt_duration_df["trial_num"] = trial_index
        for act in list(actionchannels.action.values): # Treats the float, int duration value and string "phase 0" etc as same
            opt_duration_df[act] = opt_signal_duration[i] 
    
                

        opt_channels_df = pd.DataFrame(columns=list(actionchannels.action.values)+["trial_num"])
        opt_channels_df["trial_num"] = trial_index
        for act in list(actionchannels.action.values):
            opt_channels_df[act] = False

        pops = [ untrace(x) for x in pop_names]
    #     print(pops)
        opt_populations_df = pd.DataFrame(columns=pops+["trial_num"])
        opt_populations_df["trial_num"] = trial_index
        for pop in pops:
            #if optostim_signal_present:
            opt_populations_df[pop] = False



        trial_indices = np.zeros(n_trials)

        print(type(opt_signal_probability))
        if isinstance(opt_signal_probability[i],(float,int)) == True:
            trials_with_opt_signal = np.random.choice(trial_index,int(n_trials*opt_signal_probability[i]), replace=False)
        elif type(opt_signal_probability[i]) == list or type(opt_signal_probability[i]) == np.ndarray:
            trials_with_opt_signal = opt_signal_probability[i]

        opt_list_trials = trials_with_opt_signal

        print(trials_with_opt_signal)

        for n in np.arange(n_trials):

            if opt_signal_channel[i] == "any":
                channels_opt = np.random.choice(list(actionchannels.action.values),1, replace=False)
            elif opt_signal_channel[i] == "all":
                if opt_signal_population[i] not in ['FSI','LIPI']:
                    channels_opt = list(actionchannels.action.values)
                else:
                    channels_opt = np.nan
            elif opt_signal_channel[i] in list(actionchannels.action.values):
                if opt_signal_population[i] not in ['FSI','CxI']:
                    channels_opt = [opt_signal_channel[i]]
                else:
                    channels_opt = np.nan
            elif isinstance(opt_signal_channel[i],(list,tuple)):
                if opt_signal_population[i] not in ['FSI','CxI']:
                    channels_opt = list(opt_signal_channel[i])
                else:
                    channels_opt = np.nan

            if n in trials_with_opt_signal:
                for col in channels_opt:
                    opt_channels_df.loc[n,col] = True

                for pop in opt_signal_population[i]:
                    print("pop",pop)
                    opt_populations_df.loc[n,pop] = True
                    print(opt_populations_df.loc[n,pop])

        opt_amplitude_dfs.append(opt_amplitude_df)
        opt_onset_dfs.append(opt_amplitude_df)
        opt_duration_dfs.append(opt_duration_df)
        opt_channels_dfs.append(opt_channels_df)
        opt_populations_dfs.append(opt_populations_df)
        opt_list_trials_list.append(opt_list_trials)


    print("opt_amplitude_dfs",opt_amplitude_dfs)

    return opt_df, opt_channels_dfs, opt_amplitude_dfs, opt_onset_dfs,opt_duration_dfs,opt_populations_dfs, opt_list_trials_list #reward_t1, reward_t2


def GenOptSchedule(opt_signal_probability, actionchannels, n_trials,popdata, opt_signal_channel, opt_signal_amplitude, opt_signal_onset,opt_signal_duration, opt_signal_present,opt_signal_population):

    print("begin GenOptSchedule")
    #reward_t1, reward_t2
    opt_df, opt_channels_dfs, opt_amplitude_dfs, opt_onset_dfs,opt_duration_dfs,opt_populations_dfs,opt_list_trials_list = define_opt(
        opt_signal_probability, actionchannels, n_trials,popdata, opt_signal_channel,opt_signal_amplitude, opt_signal_onset,opt_signal_duration,opt_signal_present,opt_signal_population)

    print("opt_df")
    print(opt_df)

    print("opt_channels_df")
    print(opt_channels_dfs)
    return opt_df, opt_channels_dfs, opt_amplitude_dfs, opt_onset_dfs, opt_duration_dfs, opt_populations_dfs, opt_list_trials_list
