#import all the required libraries

from __future__ import division
import sypy
import matplotlib.pyplot as plt
import networkx as nx
from itertools import permutations
import numpy as np
from operator import itemgetter

#create sybil region
sybil_region = sypy.Region(
        graph = sypy.PowerLawGraph(num_nodes=80,node_degree=2,prob_triad=0.03,seed=1),
        name = "SybilCompleteGraph",is_sybil=True)
nx.set_node_attributes(sybil_region.graph.structure, 'Node_type', 'Sybil_node')
#print sybil_region.graph.structure.nodes(data='True')
#sybil_region.visualize()

#create honest region
honest_region = sypy.Region(
        graph=sypy.PowerLawGraph(num_nodes=100,node_degree=2,prob_triad=0.03,seed=1),
        name="HonestPowerLawGraph")
honest_region.pick_random_honest_nodes(num_nodes=10)
nx.set_node_attributes(honest_region.graph.structure, 'Node_type', 'Honest_node')
#print honest_region.graph.structure.nodes(data='True')
#honest_region.visualize()

#create online scial network
social_network = sypy.Network(left_region=honest_region,right_region=sybil_region,name="OnlineSocialNetwork")
social_network.random_pair_stitch(num_edges=10)
social_network.visualize()

G = social_network.graph.structure
#print G.nodes(data='True')
nx.draw(G)
plt.show()

#create edgelist
nx.write_edgelist(G, "edgelistfinal.txt")

#find the diameter and radius
dia=nx.diameter(G,e=None)
#print (dia)
print ("Diameter = %d" % (dia))
rad=dia/2 
print ("Radius = %f " % (rad))
#print (rad)
#create a function to find the efficiency
def efficiency(G, u, v):
	return 1 / nx.shortest_path_length(G, u, v)
def global_efficiency(G):
	n = len(G)
	denom = n * (n - 1)
	return sum(efficiency(G, u, v) for u, v in permutations(G, 2)) / denom
def local_efficiency(G):
	return sum(global_efficiency(G) for v in G) / len(G)
#read edgelist from the B-matrix output
mat=np.loadtxt('outputBmatrix.txt',delimiter=' ')
arrmat=np.array(mat)
s=0
#implement a loop to calculate the B-matrix efficiency
for k in range(1,180):
	for l in range(1,8):
		s=s+((k/l)*arrmat[l][k])
#print s
#implement a loop to calculate the efficiency of the sub-graph
N_D=list()
#H=list()
N=list()
p=list()
Bmatrix_efficiency=list()

for i in range(180):
	
	N_D.append(G.degree([i]).values())
	
	H=(nx.ego_graph(G,i,radius=rad,center=False,undirected=True,distance= None))
	
	N.append(nx.number_of_nodes(H))
	#print N
	
	p.append(local_efficiency(H))
	nx.draw(H)
	#plt.savefig('egograph:'+ str(i)+'.png')
	#plt.close()
	nx.write_edgelist(H,"edgelist:"+str(i) +".txt")
	
	Bmatrix_efficiency.append(s/(N[i]*(N[i]-1)))
print ("Node_Degree :")
print(N_D[0:])
	
print ("Number_of_nodes:")
print (N[0:])

print ("local efficiency")
print (p[0:])

print ("Bmatrix_efficiency:")
print (Bmatrix_efficiency)

#print ("local efficiency of node %d = %f \t\t Bmatrix_efficiency = %f \t\t Node_degree = %d" % (i,p,Bmatrix_efficiency,N_D))

#Plotting Graphs:
plt.plot(N_D,p)
plt.show()
plt.plot(N_D,Bmatrix_efficiency)
plt.show()
plt.plot(Bmatrix_efficiency,p)
plt.show()



