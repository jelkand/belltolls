import config.characters as config
import networkx as nx
import numpy as np
import pandas as pd
from networkx.readwrite import json_graph
import json

import matplotlib.pyplot as plt

def read_chapter(chapter_number):
	df = pd.read_csv('./networks/adj_matrices/chapter%s.csv', str(chapter_number), encoding='latin-1')
	return df

def read_master():
	df = pd.read_csv('./networks/master_adj_matrix.csv', encoding='latin-1')
	return df

def build_chapter_graph(chapter_number):
	df = read_chapter(chapter_number)
	matrix = df.as_matrix()


def build_graph(df):
	matrix = df.as_matrix(columns=config.names)
	#matrix = df.values
	cols = list(df.columns.values)
	#drop the empty entry in cols
	del cols[0]
	labels = dict()
	for index, name in enumerate(cols):
		labels[index] = name

	graph = nx.from_numpy_matrix(matrix)
	graph = nx.relabel_nodes(graph, labels, copy=False)
	return graph

def write_json(graph):
	data = json_graph.node_link_data(graph)
	with open('./networks/edge_lists/belltolls.json', 'w') as outfile:
		json.dump(data, outfile)

if __name__ == '__main__':
	data = read_master()
	graph = build_graph(data)
	write_json(graph)
	nx.draw(graph)
	plt.show()

