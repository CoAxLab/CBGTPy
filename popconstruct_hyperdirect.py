from frontendhelpers import *
from init_params_hyperdirect import *
import pandas as pd


# ----------------------  helper_popconstruct FUNCTION  ------------------
# helper_popconstruct sets for each population the corrisponding specific
# parameters with either the defaults or the values passed as arguments
# (through the functions implemented in init_params.py)

# inputs:   channels = action channels related parameters - through helper_actionchannels (init_params.py)
#           popspecific = population specific parameters dictionary - through helper_popspecific (init_params.py)
#           celldefaults = neuron parameters, which are either default values or values set by the user - through helper_cellparams (init_params.py)
#           receptordefaults = receptor specific parameters dictionary - through helper_receptor (init_paras.py)
#           basestim = base stimulus parameter dictionary - through helper_basestim (init_params.py)
#           dpmn_defaults = dopamine related parameters dictionary - through helper_dpmn (init_params.py)
#           d1defaults = dopamine related parameters for D1-MSN - through helper_d1 (init_params.py)
# d2defaults = dopamine related parameters for D2-MSN - through helper_d2
# (init_params.py)

# outputs:  popdata = populations dataframe, each one containing the
# corresponding specific parameters

def helper_popconstruct(
        channels,
        popspecific,
        celldefaults,
        receptordefaults,
        basestim,
        dpmndefaults,
        d1defaults,
        d2defaults):

    popdata = pd.DataFrame()

    popdata['name'] = [
        'GPi',
        'STNE',
        'GPeP',
        'GPeA',
        'D1STR',
        'D2STR',
        'LIP',
        'Th',
        'FSI',
        'LIPI',
    ]
    popdata = trace(popdata, 'init')

    popdata = ModifyViaSelector(popdata, channels, SelName(
        ['GPi', 'STNE', 'GPeP','GPeA', 'D1STR', 'D2STR', 'LIP', 'Th']))

    popdata = ModifyViaSelector(popdata, celldefaults)

    for key, data in popspecific.items():
        params = ParamSet('popspecific', data)
        popdata = ModifyViaSelector(popdata, params, SelName(key))

    popdata = ModifyViaSelector(popdata, receptordefaults)

    for key, data in basestim.items():
        params = ParamSet('basestim', data)
        popdata = ModifyViaSelector(popdata, params, SelName(key))

    popdata = ModifyViaSelector(
        popdata, dpmndefaults, SelName(['D1STR', 'D2STR']))
    popdata = ModifyViaSelector(popdata, d1defaults, SelName('D1STR'))
    popdata = ModifyViaSelector(popdata, d2defaults, SelName('D2STR'))
    #print('popdata', popdata)

    return popdata

# ----------------------  helper_poppathways FUNCTION  -------------------
# helper_poppathays sets for each connection between populations the
# corrisponding specific parameters with either the defaults or the values
# passed

# inputs:  popdata = populations dataframe, each one containing the corresponding specific parameters
# newpathways = connectivity parameters sent as argument. This is a
# dataframe and allows setting only a subset of parameters.

# outputs:  pathways = dataframe that defines the source and the
# destination of each connection, which is the type of receptor involved,
# the probability of connection and efficiency


def helper_poppathways(popdata, newpathways=None):

    if newpathways is None:
        newpathways = pd.DataFrame()

    dpmn_ratio = 0.5
    dpmn_implied = 0.7

    # phenotype study's values
    simplepathways = pd.DataFrame(
        [
            ['LIP', 'D1STR', 'AMPA', 'syn', 1, 0.020, True], # 0.018 // min 0.008 max 0.022 // 0.027
            ['LIP', 'D1STR', 'NMDA', 'syn', 1, 0.025, False], # min 0.012 max 0.033
            ['LIP', 'D2STR', 'AMPA', 'syn', 1, 0.020, True], # min 0.008 max 0.059 (this)  // 0.027
            ['LIP', 'D2STR', 'NMDA', 'syn', 1, 0.04, False], # 0.04 // min 0.0195 max 0.0885
            ['LIP', 'FSI', 'AMPA', 'all', 1, 0.198, False],
            ['LIP', 'Th', 'AMPA', 'syn', 1, 0.03, False], #0.03
            ['LIP', 'Th', 'NMDA', 'syn', 1, 0.035, False], 

            ['D1STR', 'D1STR', 'GABA', 'syn', 0.45, 0.28, False],#0.28
            ['D1STR', 'D2STR', 'GABA', 'syn', 0.5, 0.28, False], #0.28
            ['D1STR', 'GPi', 'GABA', 'syn', 1, 2.07, False], #2.07 // 1.6/1.7/1.8 min 0.4 max 2.4

            ['D2STR', 'D2STR', 'GABA', 'syn', 0.45, 0.28, False],#0.28
            ['D2STR', 'D1STR', 'GABA', 'syn', 0.5, 0.28, False], #0.28
            ['D2STR', 'GPeP', 'GABA', 'syn', 1, 4.07, False], #1.2 // 2.70 // 4.07 // 2.67 last
            ['D2STR', 'GPeA', 'GABA', 'syn', 0.4, 0.2, False], #0.2 prob = 1 prob 0.8 weight 0.3 Aristieta

            ['FSI', 'FSI', 'GABA', 'all', 1, 3.25833, False],
            ['FSI', 'D1STR', 'GABA', 'all', 1, 1.77760, False], #1.77760
            ['FSI', 'D2STR', 'GABA', 'all', 1, 1.66987, False], #1.66987

            ['GPeP', 'GPeP', 'GABA', 'all', 0.08334, 3., False], #2.5 // prob 0.0667
            ['GPeP', 'STNE', 'GABA', 'syn', 0.08334, 0.35, False], #0.35 // prob 0.0667
            ['GPeP', 'GPi', 'GABA', 'syn', 1, 0.058, False], #0.067 last  min 0.057 max 0.067
            ['GPeP', 'FSI', 'GABA', 'all', 0.4, 0.1, False], # 0.03 // 0.05
            ['GPeP', 'GPeA', 'GABA', 'syn', 0.7, 0.42, False], #prob 1 0.4 last // 0.19 last
            
            ['GPeA', 'GPeP', 'GABA', 'syn', 0.8, 0, False], # 0.05 / prob=0.667
            ['GPeA', 'FSI', 'GABA', 'all', 0.4, 0.01, False], #0.1 // 0.19 #0.35/0.28 - prob < 1
            ['GPeA', 'D2STR', 'GABA', 'syn', 0.42, 0.018, False], # 0.7 // 1.   #0.83/0.8 // 1.7 #1.5 prob < 0.5 - 0.4
            ['GPeA', 'D1STR', 'GABA', 'syn', 0.4, 0.018, False], #0.45 // 0.9/8 - prob 0.4
            ['GPeA', 'GPeA', 'GABA', 'all', 0.8, 1.5, False], # 0.5 last # 3.5 // prob=0.667

            ['STNE', 'GPeP', 'AMPA', 'syn', 0.161666, 0.10, False], #0.15 last // 0.057 // 0.09 last
            ['STNE', 'GPeP', 'NMDA', 'syn', 0.161666, 1.51, False], #1.68 // 1.53 last
            ['STNE', 'GPeA', 'AMPA', 'syn', 0.32333, 0.1, False], #0.002
            ['STNE', 'GPeA', 'NMDA', 'syn', 0.32333, 0.05, False], #0.05
            ['STNE', 'GPi', 'NMDA', 'all', 1, 0.032, False], # 0325 last #0.0295 

            ['GPi', 'Th', 'GABA', 'syn', 1, 0.287, False], #0.285 // 0.29 // control 0.3315

            ['Th', 'D1STR', 'AMPA', 'syn', 1, 0.3825, False],
            ['Th', 'D2STR', 'AMPA', 'syn', 1, 0.3825, False],
            ['Th', 'FSI', 'AMPA', 'all', 0.8334, 0.1, False],
            ['Th', 'LIP', 'NMDA', 'all', 0.8334, 0.03, False],

            # ramping ctx

            ['LIP', 'LIP', 'AMPA', 'syn', 0.13, 0.0127, False],
            ['LIP', 'LIP', 'NMDA', 'syn', 0.13, 0.1, False],
            ['LIP', 'LIPI', 'AMPA', 'all', 0.0725, 0.113, False],
            ['LIP', 'LIPI', 'NMDA', 'all', 0.0725, 0.525, False],

            ['LIPI', 'LIP', 'GABA', 'all', 0.5, 1.05, False],
            ['LIPI', 'LIPI', 'GABA', 'all', 1, 1.075, False],

            ['Th', 'LIPI', 'NMDA', 'all', 0.8334, 0.015, False],

        ],
        columns=['src', 'dest', 'receptor', 'type', 'con', 'eff', 'plastic']
    )


    simplepathways = trace(simplepathways, 'init')

    if len(newpathways) != 0:

        simplepathways.update(newpathways)

    pathways = simplepathways.copy()
    pathways['biselector'] = None
    for idx, row in pathways.iterrows():
        if row['type'] == 'syn':
            pathways.loc[idx, 'biselector'] = NamePathwaySelector(
                row['src'], row['dest'], 'action')
        elif row['type'] == 'all':
            pathways.loc[idx, 'biselector'] = NamePathwaySelector(
                row['src'], row['dest'])
    pathways = trace(pathways, 'auto')

    return pathways

# ----------------------  helper_connectivity FUNCTION  ------------------
# helper_connectivity sets three connectivity grids defining,
# correspondingly, the probability of connection, the mean synaptic
# efficacy and the plasticity of connections between each population,
# referring only to AMPA receptors. With plasticity of connection it is
# meant whether or not the weights of that connection could ever change -
# particularly, referring to the Ctx-STR connections modulated by AMPA
# receptors.

# inputs:  receptor = which type of receptor involved (AMPA, GABA, NMDA)
#          popdata = populations dataframe, each one containing the corresponding specific parameters
# pathways = dataframe defining the source and the destination of each
# connection, which is the type of receptor involved, the probability of
# connection and efficiency

# outputs:  connectivity = connectivity matrix defining the probability of connection between each population
#           meanEff = connectivity matrix defining the mean synaptic efficacy of each connection between populations
# plasticity = connectivity matrix defining the plasticity of connections
# between each population (true or false, 0 if not applicable)


def helper_connectivity(receptor, popdata, pathways):

    connectiongrid = constructSquareDf(untrace(popdata['name'].tolist()))
    connectiongrid = trace(connectiongrid, 'init')
    #print('conngrid', connectiongrid)

    connectivity = connectiongrid.copy()
    meanEff = connectiongrid.copy()
    plasticity = connectiongrid.copy()

    for idx, row in pathways.iterrows():
        if row['receptor'] == receptor:
            biselector = row['biselector']
            receptor = row['receptor']
            con = row['con']
            eff = row['eff']
            plastic = row['plastic']

            connectivity = FillGridSelection(
                connectivity, popdata, biselector, con)
            meanEff = FillGridSelection(
                meanEff, popdata, biselector, eff)
            plasticity = FillGridSelection(
                plasticity, popdata, biselector, plastic)

    return connectivity, meanEff, plasticity
