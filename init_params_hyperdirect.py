from frontendhelpers import *
from tracetype import *
import copy
import pdb
import numpy as np
import scipy.stats as sp_st


# ----------------------  helper_cellparams FUNCTION  --------------------
# helper_cellparams sets the neuron parameters with either the defaults or
# the values passed as arguments

# inputs:   params = neuronal parameters sent as argument. This is a dataframe and allows setting only a subset of the parameters
#           N : number of receptors on the neuron
#           C : capacitance in nF
#           Taum : membrane time constant in ms
#           RestPot : Neuron rest potential in mV
#           ResetPot : Neuron reset potential in mV
#           Threshold : Neuron threshold potential in mV
#           RestPot_ca : Rest potential for calcium ions
#           Alpha_ca : Amount of increment of [Ca] with each spike discharge. (muM)
#           Tau_ca : Time constant of Ca related conductance
#           Eff_ca : Ca efficacy
#           tauhm : Duration of the burst in ms
#           tauhp : Duration of hyperpolarization necessary to recruit a maximal postinhibitory rebound response in ms.
#           V_h :  Threshold for activation of bursts in mV.
#           V_T :  low-threshold Ca^2+ reversal potential in mV
#           g_T : low-threshold Ca^2+ maximal conductance  in mS/cm^2
#           g_adr_max : Maximum value of the g
#           Vadr_h : Potential for g_adr=0.5g_adr_max
#           Vadr_s : Slop of g_adr at Vadr_h, defining how sharp the shape of g_ard is
#           ADRRevPot : Reverse potential for ADR
#           g_k_max :  Maximun outward rectifying current
#           Vk_h : Potential for g_k=0.5g_k_max
#           Vk_s : Slop of g_k at Vk_h, defining how sharp the shape of g_k is
#           tau_k_max : maximum tau for outward rectifying k current
#           n_k :  gating variable for outward rectifying K channel
#           h :  gating variable for the low-threshold Ca^2+ current
# outputs:  celldefaults = neuron parameters, which are either default
# values or values set by params

def helper_cellparams(params=None):

    celldefaults = ParamSet('celldefaults', {'N': 75,
                                             'C': 0.5,
                                             'Taum': 20,
                                             'RestPot': -70,
                                             'ResetPot': -55,
                                             'Threshold': -50,
                                             'RestPot_ca': -85,
                                             'Alpha_ca': 0.5,
                                             'Tau_ca': 80,
                                             'Eff_ca': 0.0,
                                             'tauhm': 20,
                                             'tauhp': 100,
                                             'V_h': -60,
                                             'V_T': 120,
                                             'g_T': 0,
                                             'g_adr_max': 0,
                                             'Vadr_h': -100,
                                             'Vadr_s': 10,
                                             'ADRRevPot': -90,
                                             'g_k_max': 0,
                                             'Vk_h': -34,
                                             'Vk_s': 6.5,
                                             'tau_k_max': 8,
                                             'n_k': 0,
                                             'h': 1, })

    if params is not None:

        celldefaults = ModifyViaSelector(celldefaults, params)

    return celldefaults


# ----------------------  helper_popspecific FUNCTION  -------------------
# helper_popspecific sets the population specific parameters with either
# the defaults or the values passed as arguments

# inputs:   pops = population parameters sent as argument. This is a dictionary and allows setting only a subset of the parameters
#           LIP:  Lateral intraparietal cortex
#           FSI: Striatal fast-spiking interneurons,
#           GPeP: prototypical-external Globus Pallidus
#           STNE: subthalamic nucleus (STN)
#           LIPI:  lateral intraparietal cortex interneurons
#           Th: Thalamus,
#           N = number of neurons
#           C = Capacitance in nF
#           Taum = membrane time constant in ms
#           g_T =  low-threshold Ca^2+ maximal conductance in mS/cm^2
# outputs:  popspecific = population specific parameters dictionary


def helper_popspecific(pops=dict()):

    popspecific = {'LIP': {'N': 204, 'dpmn_cortex': 1},
                   'FSI': {'C': 0.2, 'Taum': 10},
                   # should be 10 but was 20 due to bug
                   'GPeP': {'N': 500, 'g_T': 0.06, 'Taum': 20}, #N:750 total, 2/3
                   'GPeA': {'N': 250, 'g_T': 0.06, 'Taum': 20}, #1/3
                   'STNE': {'N': 750, 'g_T': 0.06},
                   'LIPI': {'N': 186, 'C': 0.2, 'Taum': 10},
                   'Th': {'Taum': 27.78}}

    if pops is not None:
        for key in pops.keys():
            for item in pops[key].keys():
                popspecific[key][item] = pops[key][item]

    return popspecific


# ----------------------  helper_receptor FUNCTION  ----------------------
# helper_receptor sets the receptor specific parameters with either the
# defaults or the values passed as arguments

# inputs:   receps = receptor parameters sent as argument. This is a dataframe and allows setting only a subset of the parameters
#           Tau_AMPA: Time constant AMPA
#           RevPot_AMPA: Reversal potential, AMPA
#           Tau_GABA: Time constant GABA
#           RevPot_GABA: Reversal potential, GABA
#           Tau_NMDA: Time constant NMDA
#           RevPot_NMDA: Reversal potential, NMDA
# outputs:  receptordefaults = receptor specific parameters dictionary


def helper_receptor(receps=None):

    receptordefaults = ParamSet('receptordefaults', {'Tau_AMPA': 2,
                                                     'RevPot_AMPA': 0,
                                                     'Tau_GABA': 5,
                                                     'RevPot_GABA': -70,
                                                     'Tau_NMDA': 100,
                                                     'RevPot_NMDA': 0, })

    if receps is not None:
        receptordefaults = ModifyViaSelector(receptordefaults, receps)

    return receptordefaults


# ----------------------  helper_basestim FUNCTION  ----------------------
# helper_basestim sets the baseline stimulation parameters for all the
# populations with either the defaults or the values passed as arguments

# inputs:   base = baseline stimulation parameters sent as argument. This is a dictionary and allows setting only a subset of the parameters
#           Each population has three stimulation parameters:
#           FreqExt_AMPA: Input firing rate to AMPA receptors
#           MeanExtEff_AMPA: AMPA conductance
#           MeanExtCon_AMPA:  AMPA connection Probability
#           FreqExt_GABA: Input firing rate to GABA receptors
#           MeanExtEff_GABA: GABA conductance
#           MeanExtCon_GABA:  GABA connection Probability
# outputs:  basestim = base stimulus parameter dictionary


def helper_basestim(base=dict()):

    # mixture
    basestim = {'FSI': {
        'FreqExt_AMPA': 4.8,  # 3.0,
        'MeanExtEff_AMPA': 1.55,
        'MeanExtCon_AMPA': 800},
        'LIPI': {
        'FreqExt_AMPA': 3.7,
        # 'FreqExt_AMPA': 1.05,
        'MeanExtEff_AMPA': 1.2,  # 0.6,
        'MeanExtCon_AMPA': 640},
        'GPi': {
        'FreqExt_AMPA': 0.8,
        'MeanExtEff_AMPA': 5.9,
        'MeanExtCon_AMPA': 800},
        'STNE': {
        'FreqExt_AMPA': 4.15, #4.45 last  # 5.2,
        'MeanExtEff_AMPA': 1.65,
        'MeanExtCon_AMPA': 800},
        'GPeP': {
        'FreqExt_AMPA': 4.1, #last 4 # 5,
        'MeanExtEff_AMPA': 2,
        'MeanExtCon_AMPA': 800,
        'FreqExt_GABA': 2,
        'MeanExtEff_GABA': 2,
        'MeanExtCon_GABA': 2000},
        'GPeA': {
        'FreqExt_AMPA': 4,  # 4,
        'MeanExtEff_AMPA': 2,
        'MeanExtCon_AMPA': 800,
        'FreqExt_GABA': 2,
        'MeanExtEff_GABA': 2,
        'MeanExtCon_GABA': 2000},       
        'D1STR': {
        'FreqExt_AMPA': 1.3,
        'MeanExtEff_AMPA': 4,
        'MeanExtCon_AMPA': 800},
        'D2STR': {
        'FreqExt_AMPA': 1.3,
        'MeanExtEff_AMPA': 4,
        'MeanExtCon_AMPA': 800},
        'LIP': {
        'FreqExt_AMPA': 2.5,  # 2.5,
        'MeanExtEff_AMPA': 2,
        'MeanExtCon_AMPA': 800},
        'Th': {
        'FreqExt_AMPA': 2.2,
        'MeanExtEff_AMPA': 2.5,
        'MeanExtCon_AMPA': 800}, }

    # ejn
    # basestim = {'FSI': {
    #     'FreqExt_AMPA': 3.6,
    #     'MeanExtEff_AMPA': 1.55,
    #     'MeanExtCon_AMPA': 800},
    #     'LIPI': {
    #     'FreqExt_AMPA': 1.05,
    #     'MeanExtEff_AMPA': 0.6,#1.2,
    #     'MeanExtCon_AMPA': 640},
    #     'GPi': {
    #     'FreqExt_AMPA': 0.8,
    #     'MeanExtEff_AMPA': 5.9,
    #     'MeanExtCon_AMPA': 800},
    #     'STNE': {
    #     'FreqExt_AMPA': 4.45,
    #     'MeanExtEff_AMPA': 1.65,
    #     'MeanExtCon_AMPA': 800},
    #     'GPeP': {
    #     'FreqExt_AMPA': 4,
    #     'MeanExtEff_AMPA': 2,
    #     'MeanExtCon_AMPA': 800,
    #     'FreqExt_GABA': 2,
    #     'MeanExtEff_GABA': 2,
    #     'MeanExtCon_GABA': 2000},
    #     'D1STR': {
    #     'FreqExt_AMPA': 1.3,
    #     'MeanExtEff_AMPA': 4,
    #     'MeanExtCon_AMPA': 800},
    #     'D2STR': {
    #     'FreqExt_AMPA': 1.3,
    #     'MeanExtEff_AMPA': 4,
    #     'MeanExtCon_AMPA': 800},
    #     'LIP': {
    #     'FreqExt_AMPA': 2.2,
    #     'MeanExtEff_AMPA': 2,
    #     'MeanExtCon_AMPA': 800},
    #     'Th': {
    #     'FreqExt_AMPA': 2.2,
    #     'MeanExtEff_AMPA': 2.5,
    #     'MeanExtCon_AMPA': 800}, }

    if base is not None:
        for key in base.keys():
            for item in base[key].keys():
                basestim[key][item] = base[key][item]

    return basestim

# ----------------------  helper_dpmn FUNCTION  ----------------------------
# helper_dpmn sets dopamine related parameters with either the defaults or
# the values passed as arguments

# inputs:   dpmns = dopamine related parameters sent as argument. This is a dataframe and allows setting only a subset of the parameters
#           dpmn_tauDOP:
#           dpmn_alpha: learning rate
#           dpmn_DAt: tonic dopamine
#           dpmn_taum: decay of motivation
#           dpmn_dPRE: fixed increment to the pre-synaptic spiking (Apre)
#           dpmn_dPOST: fixed increment to the post-synaptic spiking (Apre)
#           dpmn_tauE: eligibility trace decay
#           dpmn_tauPRE: decay time constant for the pre-synaptic spiking (Apre)
#           dpmn_tauPOST: decay time constant for the post-synaptic spiking (Apost)
#           dpmn_wmax: upper bound for the weight w
#           dpmn_w: synaptic weight added to the synaptic conductance during learning
#           dpmn_Q1: expected reward of action 1
#           dpmn_Q2: expected reward of action 2
#           dpmn_m: motivation, modulates strength of dopamne level
#           dpmn_E: eligibility trace
#           dpmn_DAp: phasic dopamine
#           dpmn_APRE: pre-synaptic spiking
#           dpmn_APOST: post-synaptic spiking
#           dpmn_XPRE: pre-synaptic spike time indicators
#           dpmn_XPOST: post-synaptic spike time indicators
# outputs:  dpmndefaults = dopamine realted parameter dictionary


def helper_dpmn(dpmns=None):

    dpmndefaults = ParamSet('dpmndefaults', {'dpmn_tauDOP': 2,
                                             'dpmn_alpha': 0.3,  # Not used anywhere, maybe should be removed/changed to q_alpha?
                                             'dpmn_DAt': 0.0,
                                             'dpmn_taum': 1e100,
                                             'dpmn_dPRE': 0.8,
                                             # 'dpmn_dPOST': 0.02,
                                             'dpmn_dPOST': 0.04,
                                             'dpmn_tauE': 100.,
                                             'dpmn_tauPRE': 15,
                                             'dpmn_tauPOST': 6,
                                             # 'dpmn_tauPOST': 4,
                                             # 'dpmn_wmax': 0.3,
                                             # 'dpmn_wmax': 0.06,
                                             'dpmn_w': 0.1286,
                                             'dpmn_Q1': 0.0,
                                             'dpmn_Q2': 0.0,
                                             'dpmn_m': 1.0,
                                             'dpmn_E': 0.0,
                                             'dpmn_DAp': 0.0,
                                             'dpmn_APRE': 0.0,
                                             'dpmn_APOST': 0.0,
                                             'dpmn_XPRE': 0.0,
                                             'dpmn_XPOST': 0.0})

    if dpmns is not None:
        dpmnsdefaults = ModifyViaSelector(dpmndefaults, dpmns)

    return dpmndefaults

# ----------------------  helper_d1 FUNCTION  ----------------------------
# helper_d1 sets dopamine related parameters for D1-MSN population with
# either the defaults or the values passed as arguments

# inputs:   d1 = dopamine related parameters for D1-MSNs sent as argument. This is a dataframe and allows setting only a subset of the parameters
#           dpmn_type: 0 = none, 1 = D1, 2 = D2
#           dpmn_alphaw: for weight
#           dpmn_a: parameter for f(DA)
#           dpmn_b: parameter for f(DA)
#           dpmn_c: parameter for f(DA)
# outputs:  d1defaults = dopmaine related parameter for D1-MSN


def helper_d1(d1=None):

    d1defaults = ParamSet('d1defaults', {'dpmn_type': 1,
                                         # ??? 80 in original paper, balladron 12, decrease them
                                         'dpmn_alphaw': (55 / 3.0) * 1.9,
                                         # 'dpmn_alphaw': (55 / 3.0)*3,  # ??? 80 in original paper, balladron 12, decrease them
                                         # 'dpmn_alphaw': 12.,
                                         'dpmn_wmax': 0.06,
                                         'dpmn_a': 1.0,
                                         'dpmn_b': 0.1,
                                         'dpmn_c': 0.05, })
    if d1 is not None:
        d1defaults = ModifyViaSelector(d1defaults, d1)

    return d1defaults

# ----------------------  helper_d2 FUNCTION  ----------------------------
# helper_d2 sets dopamine related parameters for D2-MSN population with
# either the defaults or the values passed as arguments

# inputs:   d2 = dopamine related parameters for D2-MSNs sent as argument. This is a dataframe and allows setting only a subset of the parameters
#           dpmn_type: 0 = none, 1 = D1, 2 = D2
#           dpmn_alphaw: for weight
#           dpmn_a: parameter for f(DA)
#           dpmn_b: parameter for f(DA)
#           dpmn_c: parameter for f(DA)
# outputs:  d2defaults = dopmaine related parameter for D1-MSN


def helper_d2(d2=None):

    d2defaults = ParamSet('d2defaults', {'dpmn_type': 2,
                                         # -55 in original paper, balladron = -11
                                         'dpmn_alphaw': (-45 / 3.0) * 1.9,
                                         # 'dpmn_alphaw': (-45 / 3.0)*3, # -55 in original paper, balladron = -11
                                         # 'dpmn_alphaw': -11.,
                                         'dpmn_wmax': 0.03,
                                         'dpmn_a': 0.5,
                                         'dpmn_b': 0.005,
                                         'dpmn_c': 0.05, })
    if d2 is not None:
        d2defaults = ModifyViaSelector(d2defaults, d2)

    return d2defaults

# ----------------------  helper_actionchannels FUNCTION  ----------------
# helper_actionchannels sets action channel parameters  with either the
# defaults or the values passed as arguments

# inputs:   channels = action channels related parameters sent as argument. This is a dataframe and allows setting only a subset of the parameters
#           action: [ x, y, ...] - number of channels with x, y.. as channel labels. These become the column names in the final network data frame and can be used to access information about the action channels
# outputs:  actionchannels = dictionary with action channels information


def helper_actionchannels(channels=None):

    actionchannels = ParamSet('helper_actionchannels', {'action': [1, 2]},)

    if channels is not None:
        #actionchannels = ModifyViaSelector(actionchannels, channels)
        actionchannels = channels
    # else:
    #    actionchannels = ParamSet('helper_actionchannels', {'action': [1, 2]},)
    return actionchannels

