"""Functions for generating synthetis networks.

2021, Xavier R. Hoffmann <xrhoffmann@gmail.com>
"""

import copy
import random
from typing import List, Sequence, Tuple, Dict

from scipy import special as sp_special  # type: ignore


def configuration_model(
    *, degrees: Sequence[int], max_trials: int = 10, max_fails: int = 1000
) -> List[Tuple[int, int]]:
    """Configuration model from degree list.

    Generates simple graph: no self-loops nor multiedges.
    Returns empty list if not feasible.

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
    edges_bu: Dict[int, List[int]] = {}
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


def sample_powerlaw_with_natural_cutoff(
    *, gamma: float, nodes: int, k_min: int = 2
) -> List[int]:
    """Sample degrees from a powerlaw with natural cutoff.

    Args:
        gamma: Powerlaw exponent (larger than 2).
        nodes: Total number of nodes.
        k_min: Minimum degree.

    Returns:
        degrees: Degree sequence.

    Raises:
        ValueError: If exponent is smaller or equal than 2.
        ValueError: If k_min is smaller than 1.
    """
    if gamma <= 2:
        err = f"Exponent ({gamma}) should be larger than 2."
        raise ValueError(err)
    if k_min < 1:
        err = f"Mimimum degree ({k_min}) should be larger than 0."

    k0 = k_min
    x0 = float(k0)
    # compute natural cut-off
    k_cut = int(x0 * nodes ** (1.0 / (gamma - 1.0)))
    # compute normalization constant
    norm_discrete = sp_special.zeta(gamma, k0) - sp_special.zeta(gamma, k_cut + 1)
    norm_continuous = (gamma - 1.0) * x0 ** (gamma - 1.0)

    def discrete(k):
        return k ** (-gamma) / norm_discrete

    def continuous(x):
        return norm_continuous * x ** (-gamma)

    degrees = []
    count = 0
    coef = discrete(k0) / continuous(x0 + 1)
    while count < nodes:
        u = random.random()
        x = x0 * u ** (1.0 / (1.0 - gamma))
        k = int(x)
        if k <= k_cut and random.random() * coef * continuous(x) <= discrete(k):
            degrees.append(k)
            count += 1

    return degrees


def degree_random_regular_network(*, nodes, k, **kwargs) -> List[Tuple[int, int]]:
    """Generate adjacency list for random degree-regular network.

    Generates simple graph: no self-loops nor multiedges.
    Returns empty list if not feasible.

    Args:
        nodes: Number of nodes.
        k: Fixed degree.
        **kwargs: Keyword arguments for function configuration_model.

    Returns:
        Adjacency list.
    """
    degrees = [k] * nodes
    return configuration_model(degrees=degrees, **kwargs)


def scale_free_network(
    *, nodes, gamma, k_min, max_random: int = 10, **kwargs
) -> List[Tuple[int, int]]:
    """Generate adjacency list for scale-free network.

    Generates simple graph: no self-loops nor multiedges.
    Returns empty list if not feasible.

    Args:
        nodes: Number of nodes.
        gamma: Powerlaw exponent.
        k_min: Minimum degree.
        max_random: Maximum randomizations of degree sequence.
        **kwargs:  Keyword arguments for function configuration_model.

    Returns:
        Adjacency list.
    """
    randomization = 0
    while randomization < max_random:
        degrees = sample_powerlaw_with_natural_cutoff(
            gamma=gamma, nodes=nodes, k_min=k_min
        )
        adjacency = configuration_model(degrees=degrees, **kwargs)
        if adjacency:
            return adjacency
        else:
            randomization += 1
    return []
