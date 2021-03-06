# 1. IMPORTING SCRIPTS

import cbgt as cbgt
from frontendhelpers import *
from tracetype import *
import init_params as par
import popconstruct as popconstruct
import qvalues as qval
import generateepochs as gen
from agentmatrixinit import *
from agent_timestep import timestep_mutator, multitimestep_mutator
import pipeline_creation as pl_creat

# 2. TIMESTEP LOOP

def mega_loop(self):
    self.AMPA_con,self.AMPA_eff = CreateSynapses(self.popdata,self.connectivity_AMPA,self.meaneff_AMPA,self.plastic_AMPA)
    self.GABA_con,self.GABA_eff = CreateSynapses(self.popdata,self.connectivity_GABA,self.meaneff_GABA,self.plastic_GABA)
    self.NMDA_con,self.NMDA_eff = CreateSynapses(self.popdata,self.connectivity_NMDA,self.meaneff_NMDA,self.plastic_NMDA)

    popdata = self.popdata
    actionchannels = self.actionchannels
    agent = initializeAgent(popdata)
    self.agent = agent

    popdata['column'] = popdata.index

    agent.AMPA_con,agent.AMPA_eff = self.AMPA_con,self.AMPA_eff
    agent.GABA_con,agent.GABA_eff = self.GABA_con,self.GABA_eff
    agent.NMDA_con,agent.NMDA_eff = self.NMDA_con,self.NMDA_eff
    agent.LastConductanceNMDA = CreateAuxiliarySynapseData(popdata,self.connectivity_NMDA)


    agent.phase = 0
    agent.basestim_reached = 0
    agent.globaltimer = 0
    agent.phasetimer = 0
    agent.stoptimer = 0
    agent.opttimer = 0

    agent.motor_queued = None
    agent.dpmn_queued = None
    agent.gain = np.ones(len(actionchannels))
    agent.extstim = np.zeros(len(actionchannels))
    agent.ramping_extstim = np.zeros(len(actionchannels))
    agent.in_popids = np.where(popdata['name'] == 'LIP')[0]
    print(agent.in_popids)
    agent.out_popids = np.where(popdata['name'] == 'Th')[0]
    agent.str_popids = np.where(untrace(popdata)['name'].str.contains("STR"))[0]
    agent.d1_popids = np.where(popdata['name'] == 'D1STR')[0]
    agent.d2_popids = np.where(popdata['name'] == 'D2STR')[0]
    agent.stop_popids = np.where(popdata['name'] == 'STNE')[0]
    
    agent.opt_popids = np.where(untrace(popdata)['name'].str.contains(self.opt_signal_population[0]))[0]
    agent.ramping_stopstim_current = np.zeros(len(actionchannels))
    agent.ramping_optstim_current = np.zeros(len(actionchannels))
    agent.ramping_stopstim_target = np.zeros(len(actionchannels))
    agent.ramping_optstim_target = np.zeros(len(actionchannels))
    agent.stopsignal_applied = np.zeros(len(actionchannels))
    agent.optstim_applied = np.zeros(len(actionchannels))

    presented_stimulus = 1
    self.chosen_action = None

    for action_idx in range(len(actionchannels)):
        popid = agent.in_popids[action_idx]
        agent.FreqExt_AMPA_basestim[popid] = agent.FreqExt_AMPA[popid]
        #print("agent.FreqExt_AMPA_basestim[popid]",agent.FreqExt_AMPA_basestim[popid])

    for action_idx in range(len(actionchannels)):
        popid = agent.in_popids[action_idx]
        agent.FreqExt_AMPA[popid] = np.zeros(len(agent.FreqExt_AMPA[popid]))
        #print("agent.FreqExt_AMPA[popid]",agent.FreqExt_AMPA[popid])
        
        
    for action_idx in range(len(actionchannels)):
        popid = agent.opt_popids[action_idx]
        agent.ramping_optstim_current[action_idx] = np.mean(agent.FreqExt_AMPA[popid])
        agent.ramping_optstim_target[action_idx] = np.mean(agent.FreqExt_AMPA[popid])
        

    multitimestep_mutator(agent,popdata,5000)
    agent.FRs = [agent.rollingbuffer.mean(1) / untrace(list(popdata['N'])) / agent.dt * 1000]

    agent.hist_E = []
    agent.hist_DAp = []
    agent.hist_fDA_D1 = []
    agent.hist_fDA_D2 = []
    
    agent.hist_Apre = []
    agent.hist_Apost = []
    agent.hist_Xpre = []
    agent.hist_Xpost = []
    
    agent.hist_w = []
    #agent.hist_w_all = []
    agent.hist_w_std = []
    agent.hist_w_min = []
    agent.hist_w_max = []
    agent.inp = []

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
        else:
            agent.extstim = agent.gain * presented_stimulus * self.maxstim  # TODO: make 3.0 a param
            agent.ramping_extstim = agent.extstim
        #print("agent.gain",agent.gain)
        #print("agent.phase",agent.phase)
        #print("agent.ramping_extstim",agent.ramping_extstim)
        
        for action_idx in range(len(actionchannels)):
            popid = agent.in_popids[action_idx]
            #print("agent.FreqExt_AMPA_basestim[popid]",agent.FreqExt_AMPA_basestim[popid].mean())
            agent.FreqExt_AMPA[popid] = agent.FreqExt_AMPA_basestim[popid] + np.ones(len(agent.FreqExt_AMPA[popid])) * agent.ramping_extstim[action_idx]
            #print("agent.FreqExt_AMPA[popid]",agent.FreqExt_AMPA[popid].mean())

            
        # Ramping for STOP signal
        agent.ramping_optstim_current = agent.ramping_optstim_current * 0.9 + agent.ramping_optstim_target * 0.1
        for action_idx in range(len(actionchannels)):
            popid = agent.opt_popids[action_idx]
            agent.FreqExt_AMPA[popid] = np.ones(len(agent.FreqExt_AMPA[popid])) * agent.ramping_optstim_current[action_idx]

            
            
        multitimestep_mutator(agent,popdata,5)

        #for action_idx in range(len(actionchannels)):
        #    popid = agent.in_popids[action_idx]
            #print("after timestep mutator")
            #print("agent.FreqExt_AMPA[popid]",agent.FreqExt_AMPA[popid].mean())
        
        agent.phasetimer += 1 # 1 ms = 5 * dt
        agent.globaltimer += 1 # 1 ms = 5 * dt
        agent.stoptimer += 1
        agent.opttimer += 1
        agent.FRs = np.concatenate((agent.FRs,[agent.rollingbuffer.mean(1) / untrace(list(popdata['N'])) / agent.dt * 1000]))

        agent.hist_E.append([agent.dpmn_E[popid].mean() for popid in agent.str_popids])
        agent.hist_DAp.append([agent.dpmn_DAp[popid].mean() for popid in agent.str_popids])
        agent.hist_fDA_D1.append([ agent.dpmn_fDA_D1[popid].mean() for popid in agent.d1_popids])
        agent.hist_fDA_D2.append([ agent.dpmn_fDA_D2[popid].mean() for popid in agent.d2_popids])
        
            
        agent.hist_w.append([[agent.AMPA_eff[src][targ].mean() for targ in agent.str_popids if agent.AMPA_eff[src][targ] is not None] for src in agent.in_popids])
        agent.inp.append([ agent.FreqExt_AMPA[popid].mean()  for popid in agent.in_popids   ])
#         agent.hist_Apre.append([agent.dpmn_APRE[popid].mean() for popid in agent.str_popids])
#         agent.hist_Apost.append([agent.dpmn_APOST[popid].mean() for popid in agent.str_popids])
        
#         agent.hist_Xpre.append([agent.dpmn_XPRE[popid].mean() for popid in agent.str_popids])
#         agent.hist_Xpost.append([agent.dpmn_XPOST[popid].mean() for popid in agent.str_popids])
        
        
        #agent.hist_w_all.append([[agent.AMPA_eff[src][targ] for targ in agent.str_popids if agent.AMPA_eff[src][targ] is not None] for src in agent.in_popids])
        agent.hist_w_std.append([[agent.AMPA_eff[src][targ].std() for targ in agent.str_popids if agent.AMPA_eff[src][targ] is not None] for src in agent.in_popids])
        agent.hist_w_min.append([[agent.AMPA_eff[src][targ].min() for targ in agent.str_popids if agent.AMPA_eff[src][targ] is not None] for src in agent.in_popids])
        agent.hist_w_max.append([[agent.AMPA_eff[src][targ].max() for targ in agent.str_popids if agent.AMPA_eff[src][targ] is not None] for src in agent.in_popids])

        if agent.phase == 0:
            gateFRs = agent.rollingbuffer[agent.out_popids].mean(1) / untrace(list(popdata['N'][agent.out_popids])) / agent.dt * 1000
            thresholds_crossed = np.where(gateFRs > 30)[0]
            if len(thresholds_crossed) > 0 or agent.phasetimer > 1000:

                print('phasetimer',agent.phasetimer)
                print('globaltimer',agent.globaltimer)
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
                    print("other_action",agent.other_action)
                    
                    datatables_decision = agent.motor_queued

                    agent.gain[agent.motor_queued] = self.sustainedfraction # sustained fraction in old network
                    #agent.gain[agent.other_action] = self.sustainedfraction*0.9
                    #agent.gain[agent.other_action] *= 0.9
                else:
                    agent.motor_queued = -1

                

                
        if agent.phase == 1:
            #agent.gain[agent.other_action] *= 0.1
            #print("agent.gain",agent.gain)
            if agent.phasetimer > 300:
                agent.phase = 2
                print('phasetimer',agent.phasetimer)
                print('globaltimer',agent.globaltimer)
                print('trial_num',self.trial_num)
                agent.phasetimer = 0
                agent.gain = np.zeros(len(actionchannels))
                print(actionchannels)
                datatables_rewardtime = agent.globaltimer
                datatables_decisiondurationplusdelay = agent.globaltimer - datatables_stimulusstarttime
                if agent.motor_queued == -1:
                    #self.chosen_action = None
                    self.chosen_action = "none"
                else:
                    self.chosen_action = untrace(actionchannels.iloc[agent.motor_queued,0])
                datatables_decision = self.chosen_action
                datatables_correctdecision = self.block[self.trial_num]
                print("chosen_action",self.chosen_action)
                agent.motor_queued = None

                
                
        if agent.phase == 2:

            if agent.phasetimer > 600:
                self.dpmndefaults['dpmn_DAp'] = 0
                self.trial_num += 1
                agent.phase = 0
                agent.basestim_reached = 0
                agent.phasetimer = 0
                agent.stoptimer = 0
                agent.opttimer = 0
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
             
            #else:
            #    agent.gain[thresholds_crossed[0]] = -self.sustainedfraction
                    
                

        if agent.phase == 0 and self.trial_num == self.n_trials:
            break

            
            
        if self.opt_signal_present:    
            # stop signal
            if agent.phase == 0 or agent.phase == 1:
                #print("0 self.trial_num",self.trial_num)

                for action_idx in range(len(actionchannels)):
                    action = untrace(actionchannels.iloc[action_idx,0])
                    trial_wise_opt_onset = self.opt_onset_df.iloc[self.trial_num][action]
                    trial_wise_opt_amplitude = self.opt_amplitude_df.iloc[self.trial_num][action]
                    trial_wise_opt_channel = self.opt_channels_df.iloc[self.trial_num][action]

                    if agent.opttimer < trial_wise_opt_onset or agent.optstim_applied[action_idx] == 1 :
                        continue

                    if trial_wise_opt_channel == True:
                        agent.ramping_optstim_target[action_idx] += trial_wise_opt_amplitude
                        agent.optstim_applied[action_idx] = 1
                    #print("0 stopsignal_applied",agent.stopsignal_applied)
                    #print("0 agent.ramping_stopstim_target",agent.ramping_stopstim_target)
                    #print("0 agent.stoptimer",agent.stoptimer)
                    #print("0 trial_wise_stop_amplitude",trial_wise_stop_amplitude)
                    #print("0 trial_wise_stop_onset",trial_wise_stop_onset)
                    #print("0 agent.phase",agent.phase)



            else:
                #print("2 self.trial_num",self.trial_num)
                for action_idx in np.where(agent.optstim_applied==1)[0]:
                    action = untrace(actionchannels.iloc[action_idx,0])
                    trial_wise_opt_amplitude = self.opt_amplitude_df.iloc[self.trial_num][action]
                    agent.ramping_optstim_target[action_idx] -= trial_wise_opt_amplitude
                    agent.optstim_applied[action_idx] = 0
                    #print("2 stopsignal_applied",agent.stopsignal_applied)
                    #print("2 agent.ramping_stopstim_target",agent.ramping_stopstim_target)
                    #print("2 agent.stoptimer",agent.stoptimer)
                    #print("2 agent.phase",agent.phase)




        # environment
        #if self.chosen_action is None:
        #    self.chosen_action = np.array(["left","right"])[np.random.randint(0,2,1)[0]]
        if self.chosen_action is not None:
            #self.reward_val = qval.get_reward_value(self.t1_epochs,self.t2_epochs,self.chosen_action,self.trial_num)
            self.reward_val = qval.get_reward_value(self.t_epochs,self.chosen_action,self.trial_num)
            datatables_reward = np.sign(self.reward_val)
            self.Q_support_params = qval.helper_update_Q_support_params(self.Q_support_params,self.reward_val,self.chosen_action)
            (self.Q_df, self.Q_support_params, self.dpmndefaults) = qval.helper_update_Q_df(self.Q_df,self.Q_support_params,self.dpmndefaults,self.trial_num)
            print("self.dpmndefaults['dpmn_DAp'].values[0]",self.dpmndefaults['dpmn_DAp'].values[0])
            
            # Shouldn't this be just for chosen action ?
            
            for popid in agent.str_popids:
                agent.dpmn_DAp[popid] *=0
                agent.dpmn_DAp[popid] += self.dpmndefaults['dpmn_DAp'].values[0] #* agent.dt
            self.chosen_action = None

            
            
    self.popfreqs = pd.DataFrame(agent.FRs)
    self.popfreqs['Time (ms)'] = self.popfreqs.index
