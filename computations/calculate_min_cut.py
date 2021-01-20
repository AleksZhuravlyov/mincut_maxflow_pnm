import sys
import os

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_path, '../'))

import networkx as nx
from networkx.algorithms.flow import edmonds_karp


def calculate_edmonds_karp(pores, throats, viscosity, A, dP, L):
    edges = list()
    for id in throats.index:
        edges.append((throats.loc[id, 'pore_a'], throats.loc[id, 'pore_b'],
                      {'capacity': throats.loc[id, 'conductance'] * throats.loc[
                          id, 'length'] * viscosity, 'id': id}))

    pores_in = pores.left
    pores_in = pores_in[pores_in]
    for id in pores_in.index:
        edges.append(('in_b', id))
    edges.append(('in_a', 'in_b'))

    pores_out = pores.right
    pores_out = pores_out[pores_out]
    for id in pores_out.index:
        edges.append(('out_a', id))
    edges.append(('out_a', 'out_b'))

    G = nx.Graph()
    G.add_edges_from(edges)
    R = edmonds_karp(G, 'in_a', 'out_b')

    cut_value, partition = nx.minimum_cut(G, 'in_a', 'out_b')

    reachable, non_reachable = partition

    min_cut_node_pairs = set()
    for u, nbrs in ((n, G[n]) for n in reachable):
        min_cut_node_pairs.update((u, v) for v in nbrs if v in non_reachable)

    min_cut_edges_id = list()
    for node_pair in min_cut_node_pairs:
        min_cut_edges_id.append(int(G.adj[node_pair[0]][node_pair[1]]['id']))

    min_cut = dict()
    min_cut['id'] = throats.loc[min_cut_edges_id, 'id']
    min_cut['radius'] = throats.loc[min_cut_edges_id, 'radius']
    min_cut['velocity'] = throats.loc[min_cut_edges_id, 'velocity']

    return R, min_cut
