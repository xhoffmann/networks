"""Functions for generating synthetis networks.

2021, Xavier R. Hoffmann <xrhoffmann@gmail.com>
"""

import copy
import random


def configuration_model(*, degrees, max_trials=10, max_fails=1000):
    """Configuration model from degree list.

    Generates simple graph: no self-loops nor multiedges.

    Args:
        degrees: Degree list.
        max_trials: Max number of trials with this degree sequence.
        max_fails: Max number of fails (not added pair) in a trial.

    Returns:
        adjacency: Adjacency list with tuples of pairs (n1, n2), with
            n1 < n2.

    Raises:
        ValueError: If the sum of degrees is uneven.
    """
    # check if sum of stubs is even
    if sum(degrees) % 2 != 0:
        err = f"Sum of degrees ({sum(degrees)}) must be even."
        raise ValueError(err)

    # backup stubs and edges
    stubs_bu = []
    edges_bu = {}
    for i, el in enumerate(degrees):
        aux = [i] * el
        stubs_bu += aux[:]
        edges_bu[i] = []

    trials = 0
    while trials < max_trials:
        stubs = copy.copy(stubs_bu)
        edges = copy.deepcopy(edges_bu)
        fails = 0
        while stubs:
            n1 = random.choice(stubs)
            aux = stubs[:]
            aux.remove(n1)
            n2 = random.choice(aux)
            if n1 != n2 and n2 not in edges[n1]:
                edges[n1].append(n2)
                edges[n2].append(n1)
                stubs.remove(n1)
                stubs.remove(n2)
            else:
                fails += 1
                if fails > max_fails:
                    trials += 1
                    break
        adjacency = [(i, j) for i in edges for j in edges[i] if i < j]
        return adjacency
    return []
