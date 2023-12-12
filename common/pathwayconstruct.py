from common.popconstruct import *


simplepathways = pd.DataFrame(
    [
        ['LIP', 'D1STR', 'AMPA', 'syn', 1, 0.027],
        ['LIP', 'D1STR', 'NMDA', 'syn', 1, 0.027],
        ['LIP', 'D2STR', 'AMPA', 'syn', 1, 0.027],
        ['LIP', 'D2STR', 'NMDA', 'syn', 1, 0.027],
        ['LIP', 'FSI', 'AMPA', 'all', 1, 0.198],
        ['LIP', 'Th', 'AMPA', 'all', 1, 0.035],
        ['LIP', 'Th', 'NMDA', 'all', 1, 0.035],

        ['D1STR', 'D1STR', 'GABA', 'syn', 0.45, 0.28],
        ['D1STR', 'D2STR', 'GABA', 'syn', 0.45, 0.28],
        ['D1STR', 'GPi', 'GABA', 'syn', 1, 2.09],

        ['D2STR', 'D2STR', 'GABA', 'syn', 0.45, 0.28],
        ['D2STR', 'D1STR', 'GABA', 'syn', 0.5, 0.28],
        ['D2STR', 'GPeP', 'GABA', 'syn', 1, 4.07],

        ['FSI', 'FSI', 'GABA', 'all', 1, 3.25833],
        ['FSI', 'D1STR', 'GABA', 'all', 1, 1.7776],
        ['FSI', 'D2STR', 'GABA', 'all', 1, 1.669867],

        ['GPeP', 'GPeP', 'GABA', 'all', 0.0667, 1.75],
        ['GPeP', 'STNE', 'GABA', 'syn', 0.0667, 0.35],
        ['GPeP', 'GPi', 'GABA', 'syn', 1, 0.06],

        ['STNE', 'GPeP', 'AMPA', 'syn', 0.161668, 0.07],
        ['STNE', 'GPeP', 'NMDA', 'syn', 0.161668, 1.51],
        ['STNE', 'GPi', 'NMDA', 'all', 1, 0.038],

        ['GPi', 'Th', 'GABA', 'syn', 1, 0.3315],

        ['Th', 'D1STR', 'AMPA', 'syn', 1, 0.3825],
        ['Th', 'D2STR', 'AMPA', 'syn', 1, 0.3825],
        ['Th', 'FSI', 'AMPA', 'all', 0.8334, 0.1],
        ['Th', 'LIP', 'NMDA', 'all', 0.8334, 0.03],

        # ramping ctx

        ['LIP', 'LIP', 'AMPA', 'all', 0.4335, 0.0127],
        ['LIP', 'LIP', 'NMDA', 'all', 0.4335, 0.15],
        ['LIP', 'LIPI', 'AMPA', 'all', 0.241667, 0.113],
        ['LIP', 'LIPI', 'NMDA', 'all', 0.241667, 0.525],

        ['LIPI', 'LIP', 'GABA', 'all', 1, 1.75],
        ['LIPI', 'LIPI', 'GABA', 'all', 1, 3.58335],

        ['Th', 'LIPI', 'NMDA', 'all', 0.8334, 0.015],

    ],
    columns=['src', 'dest', 'receptor', 'type', 'con', 'eff']
)
simplepathways = trace(simplepathways, 'init')

#################################3#############################################

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


connectiongrid = constructSquareDf(untrace(popdata['name'].tolist()))
connectiongrid = trace(connectiongrid, 'init')


Connectivity_AMPA = connectiongrid.copy()
MeanEff_AMPA = connectiongrid.copy()
Connectivity_GABA = connectiongrid.copy()
MeanEff_GABA = connectiongrid.copy()
Connectivity_NMDA = connectiongrid.copy()
MeanEff_NMDA = connectiongrid.copy()


for idx, row in pathways.iterrows():
    biselector = row['biselector']
    receptor = row['receptor']
    con = row['con']
    eff = row['eff']
    if receptor == 'AMPA':
        Connectivity_AMPA = FillGridSelection(
            Connectivity_AMPA, popdata, biselector, con)
        MeanEff_AMPA = FillGridSelection(
            MeanEff_AMPA, popdata, biselector, eff)
    if receptor == 'GABA':
        Connectivity_GABA = FillGridSelection(
            Connectivity_GABA, popdata, biselector, con)
        MeanEff_GABA = FillGridSelection(
            MeanEff_GABA, popdata, biselector, eff)
    if receptor == 'NMDA':
        Connectivity_NMDA = FillGridSelection(
            Connectivity_NMDA, popdata, biselector, con)
        MeanEff_NMDA = FillGridSelection(
            MeanEff_NMDA, popdata, biselector, eff)
