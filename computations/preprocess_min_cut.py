import numpy as np
import pandas as pd


def preprocess_min_cut(pore_network, liq_model, key_left, key_right, save_to_csv=False):
    pores = pd.DataFrame(columns=['id', 'x', 'y', 'z', 'left', 'right'])
    pores.id = np.arange(len(pore_network['pore.coords']))
    pores.x = pore_network['pore.coords'][:, 0]
    pores.y = pore_network['pore.coords'][:, 1]
    pores.z = pore_network['pore.coords'][:, 2]
    pores.left = pore_network['pore.' + key_left]
    pores.right = pore_network['pore.' + key_right]
    pores.index = pores.id
    if save_to_csv:
        pores.to_csv('pores.csv', index=False)

    throats = pd.DataFrame(columns=['id', 'pore_a', 'pore_b', 'conductance',
                                    'length', 'radius', 'velocity'])
    throats.id = np.arange(len(pore_network['throat.conns']))
    throats.pore_a = pore_network['throat.conns'][:, 0]
    throats.pore_b = pore_network['throat.conns'][:, 1]
    throats.conductance = liq_model['throat.hydraulic_conductance']
    throats.index = throats.id
    throats.length = pore_network['throat.total_length']
    throats.radius = pore_network['throat.diameter'] / 2.
    throats.velocity = pore_network['throat.velocity']
    if save_to_csv:
        throats.to_csv('throats.csv', index=False)

    return pores, throats
