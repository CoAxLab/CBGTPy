
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
def define_reward(conflict,  actionchannels, n_trials=100, reward_mu=1, reward_std=0):
    #print(actionchannels)
    trial_index = np.arange(n_trials)
    
    # define suboptimal choice reward probability
    opt_p = conflict[0]
    subopt_p = conflict[1]#1 - opt_p
    probs = conflict
    #print("conflict",(opt_p,subopt_p))
    print("conflict",probs)
    # sample rewards
    reward_values = np.random.normal(loc=reward_mu, scale=reward_std, size=n_trials)
    

    # calculate n_trials based on probabilities
    n_opt_reward_trials = int(opt_p * n_trials)
    n_subopt_reward_trials = int(subopt_p * n_trials)
    n_probs_trials = [ int(x*n_trials)  for x in probs]
    
    print("sum",sum(probs))
    if sum(probs) == 1: # all probabilities sum upto 1
        rew_idx = []
        for i in np.arange(len(probs)):
            if len(rew_idx) == 0:
                temp_idx = np.random.choice(trial_index, size=n_probs_trials[i], replace=False)
                rew_idx.append(temp_idx)
            else:
                used_idx = np.hstack(rew_idx)
                temp_idx = np.setxor1d(trial_index, used_idx)
                rew_idx.append(temp_idx)
    else:
        rew_idx = []
        for i in np.arange(len(probs)):
            temp_idx = np.random.choice(trial_index, size=n_probs_trials[i], replace=False)
            rew_idx.append(temp_idx)
        
        
    # find indices for optimal and suboptimal choices
    opt_reward_idx = np.random.choice(trial_index, size=n_opt_reward_trials, replace=False)
    # return the sorted, unique values that are in only one (not both) of the
    # input arrays
    if subopt_p == (1-opt_p):
        subopt_reward_idx = np.setxor1d(trial_index, opt_reward_idx)
    else:
        subopt_reward_idx = np.random.choice(trial_index, size=n_subopt_reward_trials, replace=False)

    # intialize reward vectors
    reward = np.zeros((n_trials, len(actionchannels)))
    #reward_t1, reward_t2 = np.zeros((n_trials)), np.zeros((n_trials))

    # assign rewards
    #reward[opt_reward_idx, 0] = reward_values[opt_reward_idx]
    #reward[subopt_reward_idx, 1] = reward_values[subopt_reward_idx]
    for i in np.arange(len(probs)):
        reward[rew_idx[i],i] = reward_values[rew_idx[i]]
    
    reward = pd.DataFrame(reward)
    channel_dict = dict()
    for i in np.arange(len(actionchannels)):
        channel_dict[i] = actionchannels.iloc[i]["action"]
        
    reward = reward.rename(columns = channel_dict)
    #print(reward)
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
    
    if cp_lambda == None: # No change points , volatility parameter is moot
        cp_indicator = np.zeros(n_trials)
        cp_idx = []
        return cp_idx, cp_indicator
        
    
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




def calc_reward(conflict,block_len,reward_mu,reward_std,actions):
    trial_index = np.arange(block_len)
    reward_values = np.random.normal(loc=reward_mu, scale=reward_std, size=block_len)
    print("conflict",conflict)

    if isinstance(conflict,tuple):
        n_probs_trials = [ int(x*block_len)  for x in conflict]
    elif isinstance(conflict,float):
        n_probs_trials = [ int(conflict*block_len) ]
        conflict = [conflict]
    else:
        n_probs_trials = [int(1.0*block_len)] # Hopefully this condition is never accessed
    print("sum",sum(conflict))
    print("n_prob_trials",n_probs_trials)
    
    if sum(conflict) == 1: # all probabilities sum upto 1
        rew_idx = []
        for i in np.arange(len(conflict)):
            if len(rew_idx) == 0:
                temp_idx = np.random.choice(trial_index, size=n_probs_trials[i], replace=False)
                rew_idx.append(temp_idx)
            else:
                used_idx = np.hstack(rew_idx)
                temp_idx = np.random.choice(np.setxor1d(trial_index, used_idx),size=n_probs_trials[i],replace=False)
                rew_idx.append(temp_idx)
    else:
        rew_idx = []
        for i in np.arange(len(conflict)):
            temp_idx = np.random.choice(trial_index, size=n_probs_trials[i], replace=False)
            rew_idx.append(temp_idx)

    reward = np.zeros((block_len, len(actions)))
    #reward_t1, reward_t2 = np.zeros((n_trials)), np.zeros((n_trials))

    # assign rewards
    #reward[opt_reward_idx, 0] = reward_values[opt_reward_idx]
    #reward[subopt_reward_idx, 1] = reward_values[subopt_reward_idx]
    for i in np.arange(len(conflict)):
        reward[rew_idx[i],i] = reward_values[rew_idx[i]]
    
    reward = pd.DataFrame(reward)
    channel_dict = dict()
    for i in np.arange(len(actions)):
        channel_dict[i] = actions[i]
        
    reward = reward.rename(columns = channel_dict)
    print("calc_rew",reward)
    return reward #reward_t1, reward_t2

    



# def define_epochs(n_trials, reward, cp_idx, conflict, actionchannels,reward_mu=1, reward_std=0):  #reward_t1, reward_t2,
def define_epochs(n_trials, cp_idx, conflict, actionchannels,reward_mu=1, reward_std=0):  #reward_t1, reward_t2,
    
    #print("define_epochs")
    #print(actionchannels)
    #print("reward",reward)
    t1_epochs = []
    t2_epochs = []
    t_epochs_list = dict()
    


    volatile_pattern = []
    
#     opt_p = conflict[0]
#     subopt_p = conflict[1]#1 - opt_p

    probs = conflict
    print("conflict",(probs))
    
    reward = np.zeros((n_trials, len(actionchannels)))
    reward_values = np.random.normal(loc=reward_mu, scale=reward_std, size=n_trials)
    #n_probs_trials = [ int(x*n_trials)  for x in probs]
    
    if isinstance(probs,list): # More than one channel, 
        for i in np.arange(len(probs)):
            reward[:,i] = reward_values[:]
    elif isinstance(probs,float):
        reward[:,0] = reward_values[:]
    
    reward = pd.DataFrame(reward)
    channel_dict = dict()
    for i in np.arange(len(actionchannels)):
        channel_dict[i] = actionchannels.iloc[i]["action"]
        
    reward = reward.rename(columns = channel_dict)
    

    block = []  # female greeble is always first

    block_nums = np.arange(0,len(actionchannels))

    #print("block_nums",block_nums)
    
    
    reward_list = []
    actions = []
    for i in np.arange(len(actionchannels)):
        actions.append(actionchannels.iloc[block_nums[i]]['action'])
    
    for i in np.arange(len(actionchannels)):
        reward_list.append(reward[actions[i]])
        t_epochs_list[actions[i]] = np.zeros((n_trials))
    
    #print("t_epochs_list",t_epochs_list)

    #print("actions",actions)
    if len(cp_idx) > 0:
        k = 0
        for i in range(len(cp_idx)):
            if k == len(probs):
                k = k%len(probs)

            if i < len(cp_idx)-1: 
                block_len = cp_idx[i+1] - cp_idx[i]
                reward_list = calc_reward(conflict,block_len,reward_mu,reward_std,actions)
                print("reward_list", reward_list)

                for ac in actions:           
                    t_epochs_list[ac][cp_idx[i]:cp_idx[i + 1]] = reward_list[ac]#[cp_idx[i]-cp_idx[i-1]:cp_idx[i + 1]-cp_idx[i-1]]
                    block.append(np.repeat(ac, cp_idx[i+1]-cp_idx[i]))
                k+=1
            elif i == len(cp_idx)-1:
                block_len = n_trials-1 - cp_idx[i]
                if block_len> 0:
                    reward_list = calc_reward(conflict,block_len,reward_mu,reward_std,actions)
                    for ac in actions:
                        t_epochs_list[ac][cp_idx[i]:] = reward_list[ac]#[cp_idx[i]-cp_idx[i-1]:]
                        block.append(np.repeat(ac, n_trials-cp_idx[i]))
                    k+=1               

            # for every change point/ block change, move one position to right while assigning reward probabilities
            # eg. actions = ["A","B","C"], conflict = (0.5, 0.3, 0.2)
            # 1st block: A = 0.5, B = 0.3, C = 0.2, 2nd block: B = 0.5, C = 0.3, A = 0.2, 3rd block: C = 0.5, A = 0.3, B = 0.2 ...
            actions = np.roll(actions,-1)
    else:
        block_len = n_trials
        reward_list = calc_reward(conflict,block_len,reward_mu,reward_std,actions)
        print("reward_list", reward_list)
        for ac in actions:           
            t_epochs_list[ac][:] = reward_list[ac]#[cp_idx[i]-cp_idx[i-1]:cp_idx[i + 1]-cp_idx[i-1]]
            block.append(np.repeat(ac, n_trials))
        
        
    #volatile_pattern = np.hstack(volatile_pattern)
    noisy_pattern = [min([.00001, abs(x)]) * 100000 for x in t1_epochs]
    
    #print("t_epochs_list",t_epochs_list)
    
    t_epochs = pd.DataFrame()
    if isinstance(probs,tuple):
        for i in np.arange(len(probs)):
            if len(t_epochs_list[actions[i]]) > 0:
                t_epochs[actions[i]] = np.hstack(t_epochs_list[actions[i]])
    elif isinstance(probs,float):
        t_epochs[actions[0]] = np.hstack(t_epochs_list[actions[0]])
    # epoch_number
    #print("t_epochs",t_epochs)
    # , epoch_number, reward_p, p_id_solution, t1_epochs, t2_epochs,
    return  t_epochs, noisy_pattern, volatile_pattern, np.hstack(block)



def GenRewardSchedule(n_trials, volatility, conflict, reward_mu, reward_std, actionchannels):
    
    #reward_t1, reward_t2
    #reward = define_reward(
    #    conflict, actionchannels, n_trials, reward_mu, reward_std)
    cp_idx, cp_indicator = define_changepoints(
        n_trials, volatility)
    #t1_epochs, t2_epochs
#     t_epochs, noisy_pattern, volatile_pattern, block = define_epochs(n_trials, reward, cp_idx, conflict,actionchannels,reward_mu,reward_std) #reward_t1, reward_t2
    t_epochs, noisy_pattern, volatile_pattern, block = define_epochs(n_trials, cp_idx, conflict,actionchannels,reward_mu,reward_std) #reward_t1, reward_t2

    return volatile_pattern, cp_idx, cp_indicator, noisy_pattern, t_epochs,block #t1_epochs, t2_epochs
