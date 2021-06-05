# networks
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Network generation and analysis.

2021, Xavier R. Hoffmann <xrhoffmann@gmail.com>



## `generation`

Module to generate synthetic networks.

All functions are straightforward, except `sample_powerlaw_with_natural_cutoff`.

This function samples N values of a power law with exponent gamma, restricted from k_min to k_max = floor( k_min * N ** [1 / (gamma - 1)]). It samples the corresponding continuous distribution and uses a simple rejection method to sample the target discrete distribution. See docs for details.

## `analysis`

Module to analyze networks.

The function `breadth-first` checks if the networks has a single component or not. It can be adapted to compute other cluster-related properties.
