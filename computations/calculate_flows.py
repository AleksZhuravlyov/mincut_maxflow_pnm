import sys
import os
import numpy as np
import openpnm as op
current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_path, '../'))

from computations.preprocess_min_cut import preprocess_min_cut
from computations.calculate_min_cut import calculate_edmonds_karp


# calculate absolute permeability using PNM end max-flow
def calculate_flows(net):
    # Creating network dictionary which stores the required properties
    pn = op.network.GenericNetwork()
    pn.update(net)

    # Double-check isolating pores
    h = pn.check_network_health()
    op.topotools.trim(network=pn, pores=h['trim_pores'])

    # Adding required fluid props and calculate hydraulic conductance
    water = op.phases.Water(network=pn)
    water.add_model(propname='throat.hydraulic_conductance',
                    model=op.models.physics.hydraulic_conductance.hagen_poiseuille)

    # Set in/out pressures
    Pout = 101325
    Pin = 2 * Pout
    dP = Pin - Pout

    # Set viscosity
    viscosity = 10e-4
    water['pore.viscosity'] = viscosity
    water['throat.viscosity'] = viscosity

    water['throat.hydraulic_conductance'] = np.pi * pn['throat.diameter'] ** 4 / (
            128 * viscosity * pn['throat.total_length'])

    # Specify boundary conditions and run the solver
    flow = op.algorithms.StokesFlow(network=pn, phase=water)
    key_left = 'left'
    key_right = 'right'
    flow.set_value_BC(pores=pn.pores(key_left), values=Pin)
    flow.set_value_BC(pores=pn.pores(key_right), values=Pout)
    flow.run()

    # Calculate flow length
    Lx = np.amax(pn['pore.coords'][:, 0]) - np.amin(pn['pore.coords'][:, 0])
    L = Lx
    A = Lx * Lx  # since the network is cubic Lx = Ly = Lz

    # Add pore pressure to PN dict
    pn['pore.pressure'] = flow['pore.pressure']

    # Add hydraulic conductance to PN dict
    pn['throat.hydraulic_conductance'] = water['throat.hydraulic_conductance']

    # Calc total flow rate
    Q_pnm = flow.rate(pores=pn.pores('left'))[0]

    # Calc permeability and output flow rate using PNM
    K_pnm = flow.calc_effective_permeability(domain_area=A, domain_length=Lx)[0]
    # print("K_pnm", K_pnm)
    # print("Q_pnm", Q_pnm)

    # Add throat velocities to PN dict
    arias = pn['throat.diameter'] * pn['throat.diameter'] / 4
    presses = flow['pore.pressure']
    conducts = pn['throat.hydraulic_conductance']
    delta_presses = list()
    for pores in pn['throat.conns']:
        delta_presses.append(abs(presses[pores[0]] - presses[pores[1]]))
    pn['throat.velocity'] = np.array(delta_presses) * conducts / arias

    # finding energy loss in whole-network
    water_density = 1000
    friction_const = 32 * pn['throat.total_length'] * viscosity / pn['throat.diameter'] ** 2 / water_density
    energy_loss_throats_net = friction_const * pn['throat.velocity'] ** 2
    energy_loss_throats_av_net = np.sum(energy_loss_throats_net * pn['throat.total_length']) / np.sum(
        pn['throat.total_length'])
    pn['throat.energy_loss'] = energy_loss_throats_net
    pn['throat.energy_loss_by_length'] = energy_loss_throats_net / pn['throat.total_length']

    throats_av_length = np.mean(pn['throat.total_length'])
    energy_loss_throats_av_length_net = energy_loss_throats_av_net / throats_av_length
    # print('energy_loss_throats_av_net', '{:.4e}'.format(energy_loss_throats_av_net))
    # print('energy_loss_throats_av_length_net', '{:.4e}'.format(energy_loss_throats_av_length_net))

    # Provide Edmonds-Karp algorithm
    pores, throats = preprocess_min_cut(pn, water, key_left, key_right)
    R, min_cut = calculate_edmonds_karp(pores, throats, viscosity, A, dP, L)

    # Find which throats in pn correspond to min_cuts
    throats_id = np.arange(len(pn['throat.conns']))
    min_cuts_in_net = np.in1d(throats_id, min_cut['id'])
    min_cuts_in_net = min_cuts_in_net * 1
    pn['throat.min_cuts_in_net'] = min_cuts_in_net

    # Find av length of min-cuts
    mincut_lengths = pn['throat.length'] * min_cuts_in_net
    mincut_lengths = mincut_lengths[mincut_lengths != 0]
    mincut_av_length = np.mean(mincut_lengths)

    # Find energy loss in min-cuts
    energy_loss_mincut = energy_loss_throats_net * min_cuts_in_net
    energy_loss_mincut = energy_loss_mincut[energy_loss_mincut != 0]
    energy_loss_throats_av_mincut = np.sum(energy_loss_mincut * mincut_lengths) / np.sum(
        mincut_lengths)
    energy_loss_throats_av_length_mincut = energy_loss_throats_av_mincut / mincut_av_length
    deviation_energy_loss_throats_av = energy_loss_throats_av_mincut / energy_loss_throats_av_net
    deviation_energy_loss_throats_av_length = energy_loss_throats_av_length_mincut / energy_loss_throats_av_length_net
    # print('energy_loss_throats_av_mincut', '{:.4e}'.format(energy_loss_throats_av_mincut))
    # print('energy_loss_throats_av_length_mincut', '{:.4e}'.format(energy_loss_throats_av_length_mincut))
    # print('deviation_energy_loss_throats_av', deviation_energy_loss_throats_av)
    # print('deviation_energy_loss_throats_av_length', deviation_energy_loss_throats_av_length)

    K_edm = R['in_a']['in_b']['flow'] / A
    Q_edm = R['in_a']['in_b']['flow'] * dP / L / viscosity
    flow_params = np.array([K_pnm, Q_pnm, K_edm, Q_edm])

    # Calculating pore connections
    pore_list = np.arange(len(pn['pore.coords'])).tolist()
    pore_conns = [[] for i in range(len(pore_list))]
    for i in range(len(pore_list)):
        for j in range(len(pn['throat.conns'])):
            if i == pn['throat.conns'][j][0]:
                pore_conns[i].append(pn['throat.conns'][j][1])
            if i == pn['throat.conns'][j][1]:
                pore_conns[i].append(pn['throat.conns'][j][0])

    # Calculating connection number
    conn_number = []
    for i in range(len(pore_list)):
        conn_number.append(len(pore_conns[i]))
    conn_number = np.array(conn_number)

    Dict = {}
    Dict['K_pnm'] = K_pnm
    Dict['Q_pnm'] = Q_pnm
    Dict['K_edm'] = K_edm
    Dict['Q_edm'] = Q_edm

    por_rad_avg = np.average(pn['pore.diameter'][pn['pore.internal']] / 2)
    por_rad_std = np.std(pn['pore.diameter'][pn['pore.internal']] / 2)
    throat_rad_avg = np.average(pn['throat.diameter'][pn['throat.internal']] / 2)
    throat_rad_std = np.std(pn['throat.diameter'][pn['throat.internal']] / 2)
    throat_len_avg = np.average(pn['throat.length'][pn['throat.internal']])
    throat_length_std = np.std(pn['throat.length'][pn['throat.internal']])
    conn_num_avg = np.average(conn_number[pn['pore.internal']])
    conn_num_std = np.std(conn_number[pn['pore.internal']])

    Dict['por_rad_avg'] = por_rad_avg
    Dict['por_rad_std'] = por_rad_std
    Dict['thr_rad_avg'] = throat_rad_avg
    Dict['thr_rad_std'] = throat_rad_std
    Dict['thr_len_avg'] = throat_len_avg
    Dict['thr_len_std'] = throat_length_std
    Dict['conn_num_avg'] = conn_num_avg
    Dict['conn_num_std'] = conn_num_std

    return Dict, min_cut
