import numpy as np
from common.tracetype import *

def CreateSynapses(popdata, cons, effs, plasticity):
    connection = np.zeros((len(popdata),len(popdata))).tolist()
    efficacy = np.zeros((len(popdata),len(popdata))).tolist()

    for idx1,row1 in popdata.iterrows():
        for idx2,row2 in popdata.iterrows():
            con = cons.iloc[idx1,idx2]

            if con == 0.0:
                efficacy[idx1][idx2] = None
                connection[idx1][idx2] = None
                continue

            eff = effs.iloc[idx1,idx2]

            condata = None
            if con == 1.0:
                if plasticity.iloc[idx1][idx2] or True: # disable broadcast-based compression
                    condata = np.ones((popdata['N'].loc[idx1],popdata['N'].loc[idx2]))
                else:
                    condata = np.ones((popdata['N'].loc[idx1],1))
            else:
                condata = (np.random.rand(popdata['N'].loc[idx1],popdata['N'].loc[idx2]) < con).astype(int)

            effdata = condata * untrace(eff)

            connection[idx1][idx2] = condata
            efficacy[idx1][idx2] = effdata

            #print(idx1,idx2,con)
    return connection,efficacy


#
def CreateAuxiliarySynapseData(popdata, cons):
    auxdata = np.zeros((len(popdata),len(popdata))).tolist()
    for idx1,row1 in popdata.iterrows():
        for idx2,row2 in popdata.iterrows():
            if cons.iloc[idx1,idx2] == 0.0:
                auxdata[idx1][idx2] = None
                continue
            auxdata[idx1][idx2] = np.ones((popdata['N'].loc[idx1],popdata['N'].loc[idx2]))
            # print(idx1,idx2)
    return auxdata

#
def expandParamByCell(popdata,param,defaultvalue=np.nan):

    databypop = []

    if param not in popdata.columns:
        #print(param + " not found, initializing to " + str(defaultvalue))
        pass

    for idx1,row1 in popdata.iterrows():

        fillvalue = defaultvalue
        if param in popdata.columns:
            if not row1[param].is_nan():
                fillvalue = untrace(row1[param])

        array = np.ones(row1['N']) * fillvalue
        databypop.append(array)
    return databypop


#
def expandParamByCell2D(popdata,param,fillvalue=np.nan):

    databypop = []


    if param not in popdata.columns:
        print(param + " not found, initializing to " + str(fillvalue))

    for idx1,row1 in popdata.iterrows():

        if param not in popdata.columns:
            array = np.ones(row1['N']) * fillvalue
            databypop.append(array)
            continue


        value = row1[param]
        if value.is_nan():
            value = fillvalue
        else:
            value = untrace(value)
        array = [value]*untrace(row1['N'])
        databypop.append(np.array(array))
        continue

    return databypop
#
class NullClass():
    pass
#
def initializeAgent(popdata):
    agent = NullClass()

    propertylist = [
        'FreqExt_AMPA',
        'FreqExt_AMPA_basestim',
        'FreqExt_GABA',
        'FreqExt_NMDA',
        'MeanExtEff_AMPA',
        'MeanExtEff_GABA',
        'MeanExtEff_NMDA',
        'MeanExtCon_AMPA',
        'MeanExtCon_GABA',
        'MeanExtCon_NMDA',
        'Tau_AMPA',
        'Tau_GABA',
        'Tau_NMDA',
        'ExtS_AMPA',
        'ExtS_GABA',
        'ExtS_NMDA',
        'LS_AMPA',
        'LS_GABA',
        'LS_NMDA',
        'timesincelastspike',
        'Ptimesincelastspike',
        'g_rb',
        'V',
        'V_h',
        'h',
        'tauhp',
        'tauhm',
        'g_T',
        'Threshold',
        'ResetPot',
        'RefrState',
        'g_adr_max',
        'Vadr_h',
        'Vadr_s',
        'g_k',
        'g_k_max',
        'tau_k_max',
        'Vk_h',
        'Vk_s',
        'n_k',
        'g_ahp',
        'Taum',
        'RestPot',
        'C',
        'ADRRevPot',
        'V_T',
        'Ca',
        'Vk',
        'Tau_ca',
        'RevPot_AMPA',
        'RevPot_GABA',
        'RevPot_NMDA',
        'alpha_ca',
        'dpmn_DAp',
        'dpmn_tauDOP',
        'dpmn_APRE',
        'dpmn_dPRE',
        'dpmn_tauPRE',
        'dpmn_APOST',
        'dpmn_dPOST',
        'dpmn_tauPOST',
        'dpmn_E',
        'dpmn_tauE',
        'dpmn_m',
        'dpmn_DAt',
        'dpmn_taum',
        'dpmn_type',
        'dpmn_wmax',
        'dpmn_alphaw',
        'dpmn_fDA_D1',
        'dpmn_fDA_D2',
        'dpmn_x_fda',
        'dpmn_y_fda',
        'dpmn_d2_DA_eps',
        
        ###
        'ExtMuS_AMPA',
        'ExtMuS_GABA',
        'ExtMuS_NMDA',
        'ExtSigmaS_AMPA',
        'ExtSigmaS_GABA',
        'ExtSigmaS_NMDA',
        'cond',
        'g_adr',
        'dv',
        'tau_n',
        'n_inif',
        'Vaux',
        'N',
        ###
        'dpmn_XPRE',
        'dpmn_XPOST',
        'dpmn_cortex',

    ]

    for prop in propertylist:
        setattr(agent, prop, expandParamByCell(popdata,prop,0))

    agent.spikes = []
    for i in range(len(popdata)):
        agent.spikes.append([])

    agent.dt = 0.2 # ms
    #agent.dt = 0.05 # ms

    agent.bufferlength = 300 #50 # 10ms averaging window / 0.2ms dt
    agent.bufferpointer = 0
    agent.rollingbuffer = np.zeros((len(popdata),agent.bufferlength))

    return agent
