from frontendhelpers import *
from init_params_nchoice import *
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
        'STN',
        'GPe',
        'dSPN',
        'iSPN',
        'Cx',
        'Th',
        'FSI',
        'CxI',
    ]
    popdata = trace(popdata, 'init')

    popdata = ModifyViaSelector(popdata, channels, SelName(
        ['GPi', 'STN', 'GPe', 'dSPN', 'iSPN', 'Cx', 'Th']))

    popdata = ModifyViaSelector(popdata, celldefaults)

    for key, data in popspecific.items():
        params = ParamSet('popspecific', data)
        popdata = ModifyViaSelector(popdata, params, SelName(key))

    popdata = ModifyViaSelector(popdata, receptordefaults)

    for key, data in basestim.items():
        params = ParamSet('basestim', data)
        popdata = ModifyViaSelector(popdata, params, SelName(key))

    popdata = ModifyViaSelector(
        popdata, dpmndefaults, SelName(['dSPN', 'iSPN']))
    popdata = ModifyViaSelector(popdata, d1defaults, SelName('dSPN'))
    popdata = ModifyViaSelector(popdata, d2defaults, SelName('iSPN'))

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


def helper_poppathways(popdata,number_of_choices,newpathways=None):

    if newpathways is None:
        newpathways = pd.DataFrame()

    dpmn_ratio = 0.5
    dpmn_implied = 0.7
    if number_of_choices >1:
        scaling_conn = 2./float(number_of_choices)
        scaling_wts = 1
    else:
        scaling_conn = 1
        scaling_wts = 2./float(number_of_choices)
        
        
    print("scaling_conn",scaling_conn)
    print("scaling_wts",scaling_wts)
    # phenotype study's values
    simplepathways = pd.DataFrame(
        [
            ['Cx', 'dSPN', 'AMPA', 'syn', 1, 0.015, True],#
            ['Cx', 'dSPN', 'NMDA', 'syn', 1, 0.02, False],#
            ['Cx', 'iSPN', 'AMPA', 'syn', 1, 0.015, True],#
            ['Cx', 'iSPN', 'NMDA', 'syn', 1, 0.02, False],#
#             ['Cx', 'FSI', 'AMPA', 'all', 1, 0.198, False],#
            ['Cx', 'FSI', 'AMPA', 'all', 1*scaling_conn, 0.19*scaling_wts, False],#            
            ['Cx', 'Th', 'AMPA', 'syn', 1, 0.025, False],#
#             ['Cx', 'Th', 'NMDA', 'syn', 1, 0.05, False],# For str lesion to work, corticothalamic regime
            ['Cx', 'Th', 'NMDA', 'syn', 1, 0.029, False],# correct values for plasticity

            ['dSPN', 'dSPN', 'GABA', 'syn', 0.45, 0.28, False],#
            ['dSPN', 'iSPN', 'GABA', 'syn', 0.45, 0.28, False],#
            ['dSPN', 'GPi', 'GABA', 'syn', 1, 2.09, False],

            ['iSPN', 'iSPN', 'GABA', 'syn', 0.45, 0.28, False],#
            ['iSPN', 'dSPN', 'GABA', 'syn', 0.5, 0.28, False],#
            ['iSPN', 'GPe', 'GABA', 'syn', 1, 4.07, False],#

            
            ['FSI', 'FSI', 'GABA', 'all', 1, 3.25833, False],#
#             ['FSI', 'dSPN', 'GABA', 'all', 1, 1.77760, False],#
#             ['FSI', 'iSPN', 'GABA', 'all', 1, 1.66987, False],#
            ['FSI', 'dSPN', 'GABA', 'all', 1, 1.2, False],#
            ['FSI', 'iSPN', 'GABA', 'all', 1, 1.1, False],#
            

            ['GPe', 'GPe', 'GABA', 'all', 0.0667*scaling_conn, 1.75*scaling_wts, False],#
            ['GPe', 'STN', 'GABA', 'syn', 0.0667, 0.35, False],#
            ['GPe', 'GPi', 'GABA', 'syn', 1, 0.058, False],#

            ['STN', 'GPe', 'AMPA', 'syn', 0.161666, 0.07, False],#
            ['STN', 'GPe', 'NMDA', 'syn', 0.161666, 1.51, False],#
            ['STN', 'GPi', 'NMDA', 'all', 1*scaling_conn, 0.0380*scaling_wts, False],#

            ['GPi', 'Th', 'GABA', 'syn', 1, 0.3315, False],#

            ['Th', 'dSPN', 'AMPA', 'syn', 1, 0.3825, False],#
            ['Th', 'iSPN', 'AMPA', 'syn', 1, 0.3825, False],#
            ['Th', 'FSI', 'AMPA', 'all', 0.8334*scaling_conn, 0.1*scaling_wts, False],#
            ['Th', 'Cx', 'NMDA', 'all', 0.8334*scaling_conn, 0.03*scaling_wts, False],#

            # ramping ctx

            ['Cx', 'Cx', 'AMPA', 'syn', 0.13, 0.0127, False],#
            ['Cx', 'Cx', 'NMDA', 'syn', 0.13, 0.08, False],#
            ['Cx', 'CxI', 'AMPA', 'all', 0.0725*scaling_conn, 0.113*scaling_wts, False],#
            ['Cx', 'CxI', 'NMDA', 'all', 0.0725*scaling_conn, 0.525*scaling_wts, False],#

            ['CxI', 'Cx', 'GABA', 'all', 0.5, 1.05, False],#
            ['CxI', 'CxI', 'GABA', 'all', 1, 1.075, False],#

            ['Th', 'CxI', 'NMDA', 'all', 0.8334*scaling_conn, 0.015*scaling_wts, False],#

        ],
        columns=['src', 'dest', 'receptor', 'type', 'con', 'eff', 'plastic']
    )

    simplepathways = trace(simplepathways, 'init')

    if len(newpathways) != 0:
#         print("newpathways not NONE")
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
#     print(pathways.loc[pathways["src"]=="dSPN"][["src","dest","eff"]])
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
