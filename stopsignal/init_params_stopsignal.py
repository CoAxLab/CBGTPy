from common.frontendhelpers import *
from common.tracetype import *
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

    celldefaults = ParamSet('celldefaults', params)

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

    popspecific = pops

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

    receptordefaults = ParamSet('receptordefaults', receps)

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
    basestim = base

    # ejn
    # basestim = {'FSI': {
    #     'FreqExt_AMPA': 3.6,
    #     'MeanExtEff_AMPA': 1.55,
    #     'MeanExtCon_AMPA': 800},
    #     'CxI': {
    #     'FreqExt_AMPA': 1.05,
    #     'MeanExtEff_AMPA': 0.6,#1.2,
    #     'MeanExtCon_AMPA': 640},
    #     'GPi': {
    #     'FreqExt_AMPA': 0.8,
    #     'MeanExtEff_AMPA': 5.9,
    #     'MeanExtCon_AMPA': 800},
    #     'STN': {
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
    #     'dSPN': {
    #     'FreqExt_AMPA': 1.3,
    #     'MeanExtEff_AMPA': 4,
    #     'MeanExtCon_AMPA': 800},
    #     'iSPN': {
    #     'FreqExt_AMPA': 1.3,
    #     'MeanExtEff_AMPA': 4,
    #     'MeanExtCon_AMPA': 800},
    #     'Cx': {
    #     'FreqExt_AMPA': 2.2,
    #     'MeanExtEff_AMPA': 2,
    #     'MeanExtCon_AMPA': 800},
    #     'Th': {
    #     'FreqExt_AMPA': 2.2,
    #     'MeanExtEff_AMPA': 2.5,
    #     'MeanExtCon_AMPA': 800}, }

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

    dpmndefaults = ParamSet('dpmndefaults', dpmns)


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

    d1defaults = ParamSet('d1defaults', d1)

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

    d2defaults = ParamSet('d2defaults', d2)

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

