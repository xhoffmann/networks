"""Functions for analyzing networks.

2021, Xavier R. Hoffmann <xrhoffmann@gmail.com>
"""

from collections import defaultdict


def breadth_first(*, adjacency):
	"""Runs breadth first algorithm to check single component.

	Args:
		adjacency: Adjacency list with tuples of pairs (n1, n2), with
			n1 < n2.

	Returns:
		True (single component) or False (2 or more components).
	"""
	# create linking dictionary
	links = defaultdict(list)
	for el in adjacency:
		links[el[0]].append(el[1])
		links[el[1]].append(el[0])
	nodes = set(links.keys())
	burned = set()
	num_clus = 0
	while nodes:
		num_clus += 1
		seed = min(nodes)
		pocket = [seed]
		burned.update({seed})
		while pocket:
			seed = pocket.pop()
			# all neighbors
			new_list = set(links[seed])
			# only newly burned
			new_list = new_list.difference(burned)
			# add newly burned to total burned
			burned.update(new_list)
			# add newly burned to pocket
			pocket = [*pocket, *new_list]
		nodes = nodes.difference(burned)
	if num_clus == 1:
		return True
	else:
		return False
