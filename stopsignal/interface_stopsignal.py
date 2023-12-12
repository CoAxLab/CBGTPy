# 1. IMPORTING SCRIPTS

import common.cbgt as cbgt
from common.frontendhelpers import *
from common.tracetype import *
import stopsignal.init_params_stopsignal as par
import stopsignal.popconstruct_stopsignal as popconstruct
import common.qvalues as qval
from common.agentmatrixinit import *
from common.agent_timestep_stop_signal import timestep_mutator, multitimestep_mutator

# 2. TIMESTEP LOOP

def mega_loop(self):
    self.AMPA_con,self.AMPA_eff = CreateSynapses(self.popdata,self.connectivity_AMPA,self.meaneff_AMPA,self.plastic_AMPA)
    self.GABA_con,self.GABA_eff = CreateSynapses(self.popdata,self.connectivity_GABA,self.meaneff_GABA,self.plastic_GABA)
    self.NMDA_con,self.NMDA_eff = CreateSynapses(self.popdata,self.connectivity_NMDA,self.meaneff_NMDA,self.plastic_NMDA)

    popdata = self.popdata
    actionchannels = self.actionchannels
    agent = initializeAgent(popdata)
    self.agent = agent
    stop_iter = np.arange(len(self.stop_signal_population))
    opt_iter = np.arange(len(self.opt_signal_population))


    popdata['column'] = popdata.index

    agent.AMPA_con,agent.AMPA_eff = self.AMPA_con,self.AMPA_eff
    agent.GABA_con,agent.GABA_eff = self.GABA_con,self.GABA_eff
    agent.NMDA_con,agent.NMDA_eff = self.NMDA_con,self.NMDA_eff
    agent.LastConductanceNMDA = CreateAuxiliarySynapseData(popdata,self.connectivity_NMDA)


    agent.phase = 0
    agent.basestim_reached = 0
    agent.globaltimer = 0
    agent.phasetimer = 0
    agent.stoptimer = [ 0 for i in stop_iter]
    agent.opttimer = [ 0 for i in opt_iter]

    agent.motor_queued = None
    agent.dpmn_queued = None
    agent.gain = np.ones(len(actionchannels))
    agent.extstim = np.zeros(len(actionchannels))
    agent.ramping_extstim = np.zeros(len(actionchannels))

    agent.in_popids = np.where(popdata['name'] == 'Cx')[0]
    agent.out_popids = np.where(popdata['name'] == 'Th')[0]
    agent.str_popids = np.where(untrace(popdata)['name'].str.contains("SPN"))[0]
    
    agent.stop_popids = [ np.where(untrace(popdata)['name'].str.contains(self.stop_signal_population[i]))[0] for i in stop_iter]

    print("agent.stop_popids",agent.stop_popids)

    agent.opt_popids = [ np.where(untrace(popdata)['name'].str.contains(self.opt_signal_population[i]))[0] for i in opt_iter]

    #print("agent.stop_popids", agent.stop_popids)
    #print("agent.opt_popids",agent.opt_popids)

    agent.optstim_backup_basestim = [ np.zeros(len(agent.opt_popids[i])) for i in opt_iter]
    agent.stopstim_backup_basestim = [ np.zeros(len(agent.stop_popids[i])) for i in stop_iter]

    agent.stopstim_applied = [ np.zeros(len(actionchannels)) for i in stop_iter]
    agent.optstim_applied = [ np.zeros(len(actionchannels)) for i in opt_iter]


    trial_wise_stop_duration = [ self.stop_signal_duration[i] for i in stop_iter]
    stop_amp = [ self.stop_signal_amplitude[i] for i in stop_iter]
    stop_onset = [ self.stop_signal_onset[i] for i in stop_iter]

    trial_wise_opt_duration = [ self.opt_signal_duration[i] for i in opt_iter]
    opt_amp = [ self.opt_signal_amplitude[i] for i in opt_iter]
    opt_onset = [ self.opt_signal_onset[i] for i in opt_iter]

    presented_stimulus = 1
    self.chosen_action = None

    for action_idx in range(len(actionchannels)):
        popid = agent.in_popids[action_idx]
        agent.FreqExt_AMPA_basestim[popid] = agent.FreqExt_AMPA[popid]

    for action_idx in range(len(actionchannels)):
        popid = agent.in_popids[action_idx]
        agent.FreqExt_AMPA[popid] = np.zeros(len(agent.FreqExt_AMPA[popid]))

    #Stop STN
    #for action_idx in range(len(actionchannels)):
        #popid = agent.stop_popids[action_idx]
        #agent.ramping_stopstim_current[action_idx] = np.mean(agent.FreqExt_AMPA[popid])
        #agent.ramping_stopstim_target[action_idx] = np.mean(agent.FreqExt_AMPA[popid])

    #Stop D2STR
    #for action_idx in range(len(actionchannels)):
        #popid = agent.stop_popids_2[action_idx]
        #agent.ramping_stopstim_current_2[action_idx] = np.mean(agent.FreqExt_AMPA[popid])
        #agent.ramping_stopstim_target_2[action_idx] = np.mean(agent.FreqExt_AMPA[popid])

    #Opto
    for i in opt_iter:
        for action_idx in range(len(agent.opt_popids[i])):
            popid = agent.opt_popids[i][action_idx]
            agent.FreqExt_AMPA_basestim[popid] = agent.FreqExt_AMPA[popid]

        for action_idx in range(len(agent.opt_popids[i])):
            popid = agent.opt_popids[i][action_idx]
            agent.optstim_backup_basestim[i][action_idx] = np.mean(agent.FreqExt_AMPA_basestim[popid])

    #Stop
    for i in stop_iter:
        for action_idx in range(len(agent.stop_popids[i])):
            popid = agent.stop_popids[i][action_idx]
            agent.FreqExt_AMPA_basestim[popid] = agent.FreqExt_AMPA[popid]

        for action_idx in range(len(agent.stop_popids[i])):
            popid = agent.stop_popids[i][action_idx]
            agent.stopstim_backup_basestim[i][action_idx] = np.mean(agent.FreqExt_AMPA_basestim[popid])

            
    multitimestep_mutator(agent,popdata,5000)
    agent.FRs = [agent.rollingbuffer.mean(1) / untrace(list(popdata['N'])) / agent.dt * 1000]

    agent.hist_E = []
    agent.hist_DAp = []

    agent.hist_Apre = []
    agent.hist_Apost = []
    agent.hist_Xpre = []
    agent.hist_Xpost = []

    agent.hist_w = []
    agent.hist_w_std = []
    agent.hist_w_min = []
    agent.hist_w_max = []

    agent.inp = []
    agent.stop_inp = [[] for i in stop_iter]
    agent.opt_inp = [[] for i in opt_iter]

    datatables_decision = None
    datatables_stimulusstarttime = agent.globaltimer
    datatables_decisiontime = None
    datatables_decisionduration = None
    datatables_decisiondurationplusdelay = None
    datatables_rewardtime = None
    datatables_correctdecision = None
    datatables_reward = None

    self.datatables = pd.DataFrame([], columns=["decision", "stimulusstarttime", "decisiontime", "decisionduration", "decisiondurationplusdelay", "rewardtime", "correctdecision", "reward"])
    self.datatables.index.name = 'trial'


    while self.trial_num < self.n_trials:
        
        if agent.phase == 0:
            agent.extstim = agent.gain * presented_stimulus * self.maxstim  # TODO: make 3.0 a param
            agent.ramping_extstim = agent.ramping_extstim * 0.9 + agent.extstim * 0.1
            #agent.ramping_stopstim_current = agent.ramping_stopstim_current * 0.9 + agent.ramping_stopstim_target * 0.1
            #agent.ramping_stopstim_current_2 = agent.ramping_stopstim_current_2 * 0.9 + agent.ramping_stopstim_target_2 * 0.1

        else:
            agent.extstim = agent.gain * presented_stimulus * self.maxstim  # TODO: make 3.0 a param
            agent.ramping_extstim = agent.extstim

        for action_idx in range(len(actionchannels)):
            popid = agent.in_popids[action_idx]
            agent.FreqExt_AMPA[popid] = agent.FreqExt_AMPA_basestim[popid] + np.ones(len(agent.FreqExt_AMPA[popid])) * agent.ramping_extstim[action_idx]


        #Stop
        for i in stop_iter:
            if self.stop_signal_present[i] == True:
                if isinstance(self.stop_duration_dfs[i].iloc[0][0],(float,int)):
                    if agent.stoptimer[i] == stop_onset[i] and self.trial_num in self.stop_list_trials_list[i]:

                        print("stop stim started")

                        for action_idx in range(len(agent.stop_popids[i])):
                            if self.stop_channels_dfs[i].iloc[self.trial_num][action_idx]:
                                popid = agent.stop_popids[i][action_idx]
                                agent.FreqExt_AMPA[popid] = agent.FreqExt_AMPA_basestim[popid] + stop_amp[i]
                elif isinstance(self.stop_duration_dfs[i].iloc[0][0],str):
                    if self.trial_num in self.stop_list_trials_list[i]:
                        which_phase_df = self.stop_duration_dfs[i].iloc[self.trial_num]
                        for action_idx in range(len(agent.stop_popids[i])):                    
    #                       print(which_phase_df[action_idx])
                            which_phase = which_phase_df[action_idx].split(' ')
                            if which_phase[0] == "phase" and int(which_phase[1]) in [0,1,2]:
    #                           print("inside phase")
                                if agent.phase == int(which_phase[1]):
    #                               print("stop stim started")
                                    #for action_idx in range(len(agent.opt_popids[i])):
                                    if self.stop_channels_dfs[i].iloc[self.trial_num][action_idx]:
                                        popid = agent.stop_popids[i][action_idx]
                                        agent.FreqExt_AMPA[popid] = agent.FreqExt_AMPA_basestim[popid] + stop_amp[i]
                else:
                    raise Exception("duration not passed correctly: It should be a numeric or string in format: phase 0")

                                
        #Opto
        for i in opt_iter:
            if self.opt_signal_present[i] == True:
                if isinstance(self.opt_duration_dfs[i].iloc[0][0],(float,int)):
#                     print("float - what is 0th element",self.opt_duration_dfs[i].iloc[0][0])
                    if agent.opttimer[i] == opt_onset[i] and self.trial_num in self.opt_list_trials_list[i]:

                        print("opt stim started")
                        for action_idx in range(len(agent.opt_popids[i])):
                            if self.opt_channels_dfs[i].iloc[self.trial_num][action_idx]:
                                popid = agent.opt_popids[i][action_idx]
                                agent.FreqExt_AMPA[popid] = agent.FreqExt_AMPA_basestim[popid] + opt_amp[i]
            
                elif isinstance(self.opt_duration_dfs[i].iloc[0][0],str):
                    if self.trial_num in self.opt_list_trials_list[i]:
                        which_phase_df = self.opt_duration_dfs[i].iloc[self.trial_num]
                        for action_idx in range(len(agent.opt_popids[i])):                    
    #                         print(which_phase_df[action_idx])
                            which_phase = which_phase_df[action_idx].split(' ')
                            if which_phase[0] == "phase" and int(which_phase[1]) in [0,1,2]:
    #                             print("inside phase")
                                if agent.phase == int(which_phase[1]):
    #                                 print("opt stim started")
                                    #for action_idx in range(len(agent.opt_popids[i])):
                                    if self.opt_channels_dfs[i].iloc[self.trial_num][action_idx]:
                                        popid = agent.opt_popids[i][action_idx]
                                        agent.FreqExt_AMPA[popid] = agent.FreqExt_AMPA_basestim[popid] + opt_amp[i]
                else:
                    raise Exception("duration not passed correctly: It should be a numeric or string in format: phase 0")
                        
                        

        multitimestep_mutator(agent,popdata,5)

        agent.phasetimer += 1 # 1 ms = 5 * dt
        agent.globaltimer += 1 # 1 ms = 5 * dt
        agent.stoptimer = [agent.stoptimer[i] + 1 for i in stop_iter]
#         agent.stoptimer_2 += 1
        agent.opttimer = [agent.opttimer[i] + 1 for i in opt_iter]
        agent.FRs = np.concatenate((agent.FRs,[agent.rollingbuffer.mean(1) / untrace(list(popdata['N'])) / agent.dt * 1000]))

        #agent.hist_E.append([agent.dpmn_E[popid].mean() for popid in agent.str_popids])
        #agent.hist_DAp.append([agent.dpmn_DAp[popid].mean() for popid in agent.str_popids])
        #agent.hist_w.append([[agent.AMPA_eff[src][targ].mean() for targ in agent.str_popids if agent.AMPA_eff[src][targ] is not None] for src in agent.in_popids])

        if "weight" in self.record_variables:
            agent.hist_w.append([[agent.AMPA_eff[src][targ].mean() for targ in agent.str_popids if agent.AMPA_eff[src][targ] is not None] for src in agent.in_popids])

        if "optogenetic_input" in self.record_variables:
            for i in opt_iter:
                agent.opt_inp[i].append([ agent.FreqExt_AMPA[popid].mean()  for popid in agent.opt_popids[i]])


        if "stop_input" in self.record_variables:
            for i in stop_iter :
                agent.stop_inp[i].append([ agent.FreqExt_AMPA[popid].mean()  for popid in agent.stop_popids[i]])


        agent.inp.append([ agent.FreqExt_AMPA[popid].mean()  for popid in agent.in_popids])


        if agent.phase == 0:
            gateFRs = agent.rollingbuffer[agent.out_popids].mean(1) / untrace(list(popdata['N'][agent.out_popids])) / agent.dt * 1000

            thresholds_crossed = np.where(gateFRs > self.thalamic_threshold)[0]

            

            if len(thresholds_crossed) > 0 or agent.phasetimer > self.choice_timeout:

                print('gateFRs',gateFRs)
                print('thresholds_crossed',thresholds_crossed)
                agent.phase = 1
                agent.phasetimer = 0

                agent.gain = np.zeros(len(actionchannels))
                datatables_decisiontime = agent.globaltimer
                datatables_decisionduration = agent.globaltimer - datatables_stimulusstarttime
                if len(thresholds_crossed) > 0:
                    agent.motor_queued = thresholds_crossed[0]
                    agent.other_action = list(set([0,1]) - set([agent.motor_queued]))[0]

                    datatables_decision = agent.motor_queued

                    agent.gain[agent.motor_queued] = self.sustainedfraction # sustained fraction in old network
                else:
                    agent.motor_queued = -1



        if agent.phase == 1:
            if agent.phasetimer > self.trial_wise_movement_times[self.trial_num]:
                agent.phase = 2
                print('trial_num',self.trial_num)
                agent.phasetimer = 0
                agent.gain = np.zeros(len(actionchannels))
                print(actionchannels)
                datatables_rewardtime = agent.globaltimer
                datatables_decisiondurationplusdelay = agent.globaltimer - datatables_stimulusstarttime
                if agent.motor_queued == -1:
                    self.chosen_action = 'none'
                    for i in stop_iter:
                        if self.stop_signal_present[i] == True:
                        #self.chosen_action = None
                            self.chosen_action = 'stop'
                else:
                    self.chosen_action = untrace(actionchannels.iloc[agent.motor_queued,0])
                datatables_decision = self.chosen_action
                datatables_correctdecision = self.block[self.trial_num]
                print("chosen_action:",self.chosen_action)
                agent.motor_queued = None



        if agent.phase == 2:

            if agent.phasetimer > self.inter_trial_interval:
                self.dpmndefaults['dpmn_DAp'] = 0
                self.trial_num += 1
                agent.phase = 0
                agent.basestim_reached = 0
                agent.phasetimer = 0
                agent.stoptimer = [0 for i in stop_iter]
#                 agent.stoptimer_2 = 0
                agent.opttimer = [0 for i in opt_iter]
                agent.gain = np.ones(len(actionchannels))

                datatablesrow = pd.DataFrame([[
                    datatables_decision,
                    datatables_stimulusstarttime,
                    datatables_decisiontime,
                    datatables_decisionduration,
                    datatables_decisiondurationplusdelay,
                    datatables_rewardtime,
                    datatables_correctdecision,
                    datatables_reward,
                ]], columns=["decision", "stimulusstarttime", "decisiontime", "decisionduration", "decisiondurationplusdelay", "rewardtime", "correctdecision", "reward"])
                datatablesrow.index.name = 'trial'

                self.datatables = pd.concat([self.datatables,datatablesrow], ignore_index=True)

                datatables_decision = None
                datatables_stimulusstarttime = agent.globaltimer
                datatables_decisiontime = None
                datatables_decisionduration = None
                datatables_decisiondurationplusdelay = None
                datatables_rewardtime = None
                datatables_correctdecision = None
                datatables_reward = None


        if agent.phase == 0 and self.trial_num == self.n_trials:
            break



        #Stop 1
        for i in stop_iter:
            if self.stop_signal_present[i]:
                if isinstance(self.stop_duration_dfs[i].iloc[0][0],(float,int)):
                    if agent.stoptimer[i] >= trial_wise_stop_duration[i] + stop_onset[i]:
                        for action_idx in range(len(agent.stop_popids[i])):
                            popid = agent.stop_popids[i][action_idx]
                            agent.FreqExt_AMPA[popid] = agent.FreqExt_AMPA_basestim[popid]
                
                elif isinstance(self.stop_duration_dfs[i].iloc[0][0],str):
                    if self.trial_num in self.stop_list_trials_list[i]:
                        which_phase_df = self.stop_duration_dfs[i].iloc[self.trial_num]
                        for action_idx in range(len(agent.stop_popids[i])):                    
    #                         print(which_phase_df)
                            #print(which_phase_df[action_idx])
                            which_phase = which_phase_df[action_idx].split(' ')
                            if agent.phase != int(which_phase[1]): # Stop stimulation if the phase is over
                                popid = agent.stop_popids[i][action_idx]
                                agent.FreqExt_AMPA[popid] = agent.FreqExt_AMPA_basestim[popid]
                            

        #Opto
        for i in opt_iter:
            if self.opt_signal_present[i]:
                if isinstance(self.opt_duration_dfs[i].iloc[0][0],(float,int)):
                    if agent.opttimer[i] >= trial_wise_opt_duration[i] + opt_onset[i]:
                        for action_idx in range(len(agent.opt_popids[i])):
                            popid = agent.opt_popids[i][action_idx]
                            agent.FreqExt_AMPA[popid] = agent.FreqExt_AMPA_basestim[popid]
                            
                elif isinstance(self.opt_duration_dfs[i].iloc[0][0],str):
                    if self.trial_num in self.opt_list_trials_list[i]:
                        which_phase_df = self.opt_duration_dfs[i].iloc[self.trial_num]
                        for action_idx in range(len(agent.opt_popids[i])):                    
    #                       print(which_phase_df)
                            #print(which_phase_df[action_idx])
                            which_phase = which_phase_df[action_idx].split(' ')
                            if agent.phase != int(which_phase[1]): # Stop stimulation if the phase is over
                                popid = agent.opt_popids[i][action_idx]
                                agent.FreqExt_AMPA[popid] = agent.FreqExt_AMPA_basestim[popid]
                            
                            
                            
                            
        #Environment

        if self.chosen_action is not None:

            if self.chosen_action != 'stop' and self.chosen_action != 'none':

                self.reward_val = qval.get_reward_value(self.t_epochs,self.chosen_action,self.trial_num)
                datatables_reward = np.sign(self.reward_val)
                self.Q_support_params = qval.helper_update_Q_support_params(self.Q_support_params,self.reward_val,self.chosen_action)
                (self.Q_df, self.Q_support_params, self.dpmndefaults) = qval.helper_update_Q_df(self.Q_df,self.Q_support_params,self.dpmndefaults,self.trial_num)
                #print("scaled dopamine signal",self.dpmndefaults['dpmn_DAp'].values[0])


                #for popid in agent.str_popids:
                    #agent.dpmn_DAp[popid] *=0
                    #agent.dpmn_DAp[popid] += untrace(self.dpmndefaults['dpmn_DAp'].values[0]) #* agent.dt
                #self.chosen_action = None

            else:

                self.reward_val = 0
                datatables_reward = np.sign(self.reward_val)
                self.Q_support_params = qval.helper_update_Q_support_params(self.Q_support_params,self.reward_val,self.chosen_action)
                (self.Q_df, self.Q_support_params, self.dpmndefaults) = qval.helper_update_Q_df(self.Q_df,self.Q_support_params,self.dpmndefaults,self.trial_num)


                self.chosen_action = None

    self.popfreqs = pd.DataFrame(agent.FRs)
    self.popfreqs['Time (ms)'] = self.popfreqs.index
