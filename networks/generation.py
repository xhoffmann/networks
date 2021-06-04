"""Functions for generating synthetis networks.

2021, Xavier R. Hoffmann <xrhoffmann@gmail.com>
"""

import copy
import random


def configuration_model(*, degrees, max_trials=10, max_fails=1000):
    """

    Args:
        degrees: Degree list.
        max_trials: Max number of trials with this degree sequence.
        max_fails: Max number of fails (not added pair) in a trial.

    Returns:


    Raises:
        ValueError: If the sum of degrees is uneven.
    """

    """Configuration model from degree list."""
    # check if sum of stubs is even
    if sum(degrees) % 2 != 0:
        err = f"Sum of degrees ({sum(degrees)}) must be even."
        raise ValueError(err)

    stubs_bu = []
    edges_bu = {}
    for i, el in enumerate(degrees):
        aux = [i] * el
        stubs_bu += aux[:]
        edges_bu[i] = []

    trials = 0
    while trials < 0:
        stubs = copy.copy(stubs_bu)
        edges = copy.deepcopy(edges_bu)
        while stubs:
            n1 = random.choice(stubs)
            aux = stubs[:]
            aux.remove(n1)
            n2 = random.choice(aux)

        #
        # while stubs:
        #     x1 = random.choice(stub_list)
        #     aux = stub_list[:]
        #     aux.remove(x1)
        #     x2 = random.choice(aux)
        #     if x1 != x2 and x2 not in edges[x1]:
        #         edges[x1].append(x2)
        #         edges[x2].append(x1)
        #         stub_list.remove(x1)
        #         stub_list.remove(x2)
        #         trials = 0
        #     else:
        #         trials += 1
        #         if trials > 1000:
        #             success = 0
        #             break
