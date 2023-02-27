
import numpy as np
import random
import pandas as pd

np.random.seed(0)

# ----------------------  define_reward FUNCTION  ----------------------------
# define_reward function builds different arrays reward, one per each
# possible choice. The code only supports 2 different chooses, t1 and t2.
# The rewards are probabilistic; that is, when an action is selected,
# there is a probability of the reward being delivered or not. We call t1
# being the optimal choice (the preferred one) and t2 the suboptimal. The
# rewards are normally distributed with mean 'reward_mu' and standard
# deviation 'reward_std'.

# inputs:   opt_p = probability of the preferred choice (value from 0 to 1)
#           n_trials = number of trials being performed (must be an integer). Default value is 100.
#           reward_mu = the mean for the magnitude of the reward. Default value is 1.
# reward_std = the std for the magnitude of the reward. Default value is 0.

# outputs:  reward_t1 = array of n_trial length containing the amount of the reward associated to action t1. Each position on the array stands for a different trial
# reward_t2 = array of n_trial length containing the amount of the reward
# associated to action t2. Each position on the array stands for a
# different trial
def define_reward(opt_p,  actionchannels, n_trials=100, reward_mu=1, reward_std=0):
    #print(actionchannels)
    trial_index = np.arange(n_trials)

    # define suboptimal choice reward probability
    subopt_p = 1 - opt_p

    # sample rewards
    reward_values = np.random.normal(loc=reward_mu, scale=reward_std, size=n_trials)
    print("reward_values",reward_values)

    # calculate n_trials based on probabilities
    n_opt_reward_trials = int(opt_p * n_trials)
    n_subopt_reward_trials = int(subopt_p * n_trials)

    # find indices for optimal and suboptimal choices
    opt_reward_idx = np.random.choice(
        trial_index, size=n_opt_reward_trials, replace=False)
    # return the sorted, unique values that are in only one (not both) of the
    # input arrays
    subopt_reward_idx = np.setxor1d(trial_index, opt_reward_idx)

    # intialize reward vectors
    reward = np.zeros((n_trials, len(actionchannels)))
    #reward_t1, reward_t2 = np.zeros((n_trials)), np.zeros((n_trials))

    # assign rewards
    reward[opt_reward_idx, 0] = reward_values[opt_reward_idx]
    #reward_t1[opt_reward_idx] = reward_values[opt_reward_idx]
    #reward_t2[subopt_reward_idx] = reward_values[subopt_reward_idx]
    reward[subopt_reward_idx, 1] = reward_values[subopt_reward_idx]
        
    reward = pd.DataFrame(reward)
    reward = reward.rename(columns = {0 : actionchannels.iloc[0]["action"], 1: actionchannels.iloc[1]["action"]})
    
    return reward #reward_t1, reward_t2


# ----------------------  define_changepoints FUNCTION  ------------------
# define_changepoints function switches the prefered reward value if a
# change point is given. Change points are randomly setted according to a
# Poisson distribution. If a change point occurs, the prefered action
# becames the subpotimal and viceversa, so the amount of the reward needs
# to change. This function changes it.

# inputs:   n_trials = number of trials being performed (must be an integer).
#           reward_t1 = array of n_trial length containing the amount of the reward associated to action t1. Each position on the array stands for a different trial
#           reward_t2 = array of n_trial length containing the amount of the reward associated to action t2. Each position on the array stands for a different trial
# cp_lambda = frequency of changing points (Poisson distribution
# parameter).

# outputs:  cp_idx = array of arbitrary length containing the number of the trial where a change point occurs.
# cp_indicator = array of length n_trials to track wether there is a
# change point (1) or not (0)

def define_changepoints(n_trials,volatility):  #reward_t1, reward_t2,
    

    cp_lambda = volatility[0]
    change_point_type = volatility[1] # "exact" or "poisson"
    # find approximate number of change points
    
    
    n_cps = int(n_trials / cp_lambda)
    #cp_base = np.cumsum(np.random.poisson(lam=cp_lambda,size=n_cps))  # calculate cp indices
    
    
    # Just to test, deterministic blocks
    #print("cp_base",cp_base)
    # cumsum - return the cumulative sum of the elements along a given axis
    if change_point_type == "exact":
        cp_base = np.arange(cp_lambda,n_trials-1+cp_lambda,cp_lambda) 
    elif change_point_type == "poisson":
        cp_base = np.cumsum(np.random.poisson(lam=cp_lambda,size=n_cps))
    else:
        print("error")
    cp_idx = np.insert(cp_base, 0, 0)  # add 0
    cp_idx = np.append(cp_idx, n_trials - 1)  # add 0
    
#     print("cp_idx",cp_idx)
    
    cp_idx = cp_idx[cp_idx < n_trials]
    print("change points:",cp_idx)
    #cp_idx = cp_idx.sort()
       
    # to remove possible equal elements
    cp_idx = list(set(cp_idx))
    cp_idx = sorted(cp_idx)
    
    cp_indicator = np.zeros(n_trials)
    cp_indicator[cp_idx] = 1

    return cp_idx, cp_indicator


# WE MIGHT NEED TO CLEAN THE FOLLOWING FUNCTION! ASK MATT WHICH VARIABLES
# SHOULD IT RETURN

# ----------------------  define_epochs FUNCTION  ----------------------------
# define_epochs function created two different vectors containing the
# delivered rewards in case of action t1 or action t2 is performed
# considering both the reward values associated to the trial and if a
# change point has occured and so the preferred choice changed.

# inputs:   n_trials = number of trials being performed (must be an integer).
#           reward_t1 = array of n_trial length containing the amount of the reward associated to action t1. Each position on the array stands for a different trial
#           reward_t2 = array of n_trial length containing the amount of the reward associated to action t2. Each position on the array stands for a different trial
#           cp_idx = array of arbitrary length containing the number of the trial where a change point occurs.
#           opt_p = probability of the preferred choice (value from 0 to 1)

# outputs:
#           t1_epochs = array of n_trials length where each position i contains the reward value that will be delivered at the trial i if the t1 action is performed
#           t2_epochs = array of n_trials length where each position i contains the reward value that will be delivered at the trial i if the t2 action is performed
#           noisy_pattern = array of n_trials length where each position i contains if the delivered reward at trial i is considered to be noise (reward value) or not (1). We consider noise if the reward value is smaller than 1e-5
# volatile_pattern =  list of n trials indicating which action (0 or 1) is
# the best action for that epoch

def define_epochs(n_trials, reward, cp_idx, opt_p, actionchannels):  #reward_t1, reward_t2,
    
    #print("define_epochs")
    #print(actionchannels)
    #print("reward",reward)
    t1_epochs = []
    t2_epochs = []

    

    epoch_number = []
    epoch_trial = []
    epoch_length = []

    reward_p = []

    volatile_pattern = []

    subopt_p = 1 - opt_p

    block = []  # female greeble is always first
    # returns an integer representing the unicode character
#     first_block = np.random.randint(0,2,1)
    first_block = [0]
    second_block = list(set(np.arange(0,2))-set(first_block))

    #first_block = [1]
    #second_block = list(set(np.arange(0,2))-set(first_block))
    reward_t1 = np.array(reward[actionchannels.iloc[first_block[0]]['action']])
    reward_t2 = np.array(reward[actionchannels.iloc[second_block[0]]['action']])
    
    action1 = actionchannels.iloc[first_block[0]]['action']
    action2 = actionchannels.iloc[second_block[0]]['action']
    
    # remove or not? not needed for the moment
    p_id_solution = []  # female greeble is always first
    # returns an integer representing the unicode character
    f_greeble = ord('f')
    m_greeble = ord('m')

    current_target = True
    # treat all the changepoints except for the last one
    for i in range(len(cp_idx) - 1):
        if current_target:
            volatile_pattern.append(np.repeat(0., cp_idx[i + 1] - cp_idx[i]))
            t1_epochs.append(reward_t1[cp_idx[i]:cp_idx[i + 1]])
            t2_epochs.append(reward_t2[cp_idx[i]:cp_idx[i + 1]])
            block.append(np.repeat(action1, cp_idx[i+1]-cp_idx[i]))
            #reward_p.append(np.repeat(opt_p, cp_idx[i+1]-cp_idx[i]))
            #p_id_solution.append(np.repeat(f_greeble, cp_idx[i+1]-cp_idx[i]))
        else:
            volatile_pattern.append(np.repeat(1., cp_idx[i + 1] - cp_idx[i]))
            t1_epochs.append(reward_t2[cp_idx[i]:cp_idx[i + 1]])
            t2_epochs.append(reward_t1[cp_idx[i]:cp_idx[i + 1]])
            block.append(np.repeat(action2, cp_idx[i+1]-cp_idx[i]))
            #reward_p.append(np.repeat(subopt_p, cp_idx[i+1]-cp_idx[i]))
            #p_id_solution.append(np.repeat(m_greeble, cp_idx[i+1]-cp_idx[i]))

        #epoch_number.append(np.repeat(i, cp_idx[i+1]-cp_idx[i]))

        current_target = not(current_target)
        
        # consider the last changepoint
        if i == len(cp_idx) - 2:
            if current_target:
                volatile_pattern.append(
                    np.repeat(0., cp_idx[i + 1] - cp_idx[i]))
                t1_epochs.append(reward_t1[cp_idx[i + 1]:])
                t2_epochs.append(reward_t2[cp_idx[i + 1]:])
                block.append(action1)
                # reward_p.append(opt_p)
                # p_id_solution.append(f_greeble)
            else:
                volatile_pattern.append(
                    np.repeat(1., cp_idx[i + 1] - cp_idx[i]))
                t1_epochs.append(reward_t2[cp_idx[i + 1]:])
                t2_epochs.append(reward_t1[cp_idx[i + 1]:])
                block.append(action2)
                # reward_p.append(subopt_p)
                # p_id_solution.append(m_greeble)

            # epoch_number.append(i+1)

    # save flaten arrays
    #epoch_number = np.hstack(epoch_number).astype('float')
    t1_epochs = np.hstack(t1_epochs)
    t2_epochs = np.hstack(t2_epochs)
    #reward_p = np.hstack(reward_p).astype('float')
    #p_id_solution = np.hstack(p_id_solution)
    volatile_pattern = np.hstack(volatile_pattern)
    noisy_pattern = [min([.00001, abs(x)]) * 100000 for x in t1_epochs]
    
    t_epochs = pd.DataFrame()
    t_epochs[actionchannels.iloc[0]['action']] = t1_epochs
    t_epochs[actionchannels.iloc[1]['action']] = t2_epochs
    # volatile_pattern = [x%2 for x in epoch_number] - if we need to compute
    # epoch_number

    # , epoch_number, reward_p, p_id_solution, t1_epochs, t2_epochs,
    return  t_epochs, noisy_pattern, volatile_pattern, np.hstack(block)


def GenRewardSchedule(n_trials, volatility, conflict, reward_mu, reward_std, actionchannels):
    
    #reward_t1, reward_t2
    reward = define_reward(
        conflict, actionchannels, n_trials, reward_mu, reward_std)
    cp_idx, cp_indicator = define_changepoints(
        n_trials, volatility)
    #t1_epochs, t2_epochs
    t_epochs, noisy_pattern, volatile_pattern, block = define_epochs(
        n_trials, reward, cp_idx, conflict, actionchannels) #reward_t1, reward_t2
    return volatile_pattern, cp_idx, cp_indicator, noisy_pattern, t_epochs,block #t1_epochs, t2_epochs
