import numpy as np
import pandas as pd

celldefaults = {'N': 75,
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
                'h': 1, }

popspecific = {'Cx': {'N': 204, 'dpmn_cortex': 1},
               'FSI': {'C': 0.2, 'Taum': 10},
               # should be 10 but was 20 due to bug
               'GPeP': {'N': 560, 'g_T': 0.06, 'Taum': 20},  # N:750 total, 2/3
               'GPeA': {'N': 190, 'g_T': 0.06, 'Taum': 20},  # 1/3
               'STN': {'N': 750, 'g_T': 0.06},
               'CxI': {'N': 186, 'C': 0.2, 'Taum': 10},
               'Th': {'Taum': 27.78}}


receptordefaults = {'Tau_AMPA': 2,
                    'RevPot_AMPA': 0,
                    'Tau_GABA': 5,
                    'RevPot_GABA': -70,
                    'Tau_NMDA': 100,
                    'RevPot_NMDA': 0, 
                    'RevPot_ChR2': 0, # verify the exact values
                    'RevPot_NpHR':-400
                   }

basestim = {'FSI': {
            'FreqExt_AMPA': 4.8,  # 3.0,
            'MeanExtEff_AMPA': 1.55,
            'MeanExtCon_AMPA': 800},
            'CxI': {
                'FreqExt_AMPA': 3.7,
                # 'FreqExt_AMPA': 1.05,
                'MeanExtEff_AMPA': 1.2,  # 0.6,
                'MeanExtCon_AMPA': 640},
            'GPi': {
                'FreqExt_AMPA': 0.84,  # 0.8
                'MeanExtEff_AMPA': 5.9,
                'MeanExtCon_AMPA': 800},
            'STN': {
                'FreqExt_AMPA': 4.45,  # 4.45 last  # 5.2,
                'MeanExtEff_AMPA': 1.65,
                'MeanExtCon_AMPA': 800},
            'GPeP': {
                'FreqExt_AMPA': 4.,  # last 4.1 # 5,
                'MeanExtEff_AMPA': 2,
                'MeanExtCon_AMPA': 800,
                'FreqExt_GABA': 2,
                'MeanExtEff_GABA': 2,
                'MeanExtCon_GABA': 2000},
            'GPeA': {
                'FreqExt_AMPA': 2.5,  # 2.2,
                'MeanExtEff_AMPA': 2,
                'MeanExtCon_AMPA': 800,
                'FreqExt_GABA': 2,
                'MeanExtEff_GABA': 2,
                'MeanExtCon_GABA': 2000},
            'dSPN': {
                'FreqExt_AMPA': 1.3,
                'MeanExtEff_AMPA': 4,
                'MeanExtCon_AMPA': 800},
            'iSPN': {
                'FreqExt_AMPA': 1.3,
                'MeanExtEff_AMPA': 4,
                'MeanExtCon_AMPA': 800},
            'Cx': {
                'FreqExt_AMPA': 2.5,  # 2.5,
                'MeanExtEff_AMPA': 2,
                'MeanExtCon_AMPA': 800},
            'Th': {
                'FreqExt_AMPA': 2.2,
                'MeanExtEff_AMPA': 2.5,
                'MeanExtCon_AMPA': 800}, }

dpmndefaults = {'dpmn_tauDOP': 2,
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
                'dpmn_XPOST': 0.0}

dSPNdefaults = {'dpmn_type': 1,
              # ??? 80 in original paper, balladron 12, decrease them
              'dpmn_alphaw': (55 / 3.0) * 1.9,
              # 'dpmn_alphaw': (55 / 3.0)*3,  # ??? 80 in original paper, balladron 12, decrease them
              # 'dpmn_alphaw': 12.,
              'dpmn_wmax': 0.06,
              'dpmn_a': 1.0,
              'dpmn_b': 0.1,
              'dpmn_c': 0.05, }

iSPNdefaults = {'dpmn_type': 2,
              # -55 in original paper, balladron = -11
              'dpmn_alphaw': (-45 / 3.0) * 1.9,
              # 'dpmn_alphaw': (-45 / 3.0)*3, # -55 in original paper, balladron = -11
              # 'dpmn_alphaw': -11.,
              'dpmn_wmax': 0.03,
              'dpmn_a': 0.5,
              'dpmn_b': 0.005,
              'dpmn_c': 0.05, }
