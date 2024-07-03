import logging
import os
import PySpice
from PySpice.Spice.Parser import SpiceParser
from PySpice.Spice.Netlist import Circuit, SubCircuitFactory
from PySpice.Unit import *

import json


logging.basicConfig(filename='./logs/read_netlist.log', format= '%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

weights = {'Capacitor': [1,1], 'Resistor' : [1,1], 'Inductor':[1,1], 'Voltage Source': [1,1]}

class Parser:
    def __init__(self,dir):
        self.directory = dir
        self.edges = {}
        self.nodes = []
        self.graph = {}

    def parseData(self):
        parser = SpiceParser(path=self.directory)
        self.circuit = parser.build_circuit()
        print(self.circuit)
        nodes = []
        edges = {}
        for component in self.circuit.element_names:
            nodes.append(component)
            element = self.circuit[component].nodes
            
            edge = []
            for node in element:
                edge.append(int(str(node)))
            edges[component] = edge
        self.nodes = nodes
        self.edges = edges
    
    def jsonify(self):
        #Converts Data and adds weights to the edges
        self.graph['nodes'] = []
        for node in self.nodes:
            inst_type = 'Resistor'
            value = 1
            if node[0] == 'L':
                inst_type = 'Inductor'
                #value = self.circuit[node].inductance
            elif node[0] == 'V':
                inst_type = 'Voltage Source'
                #value = self.circuit[node].voltage
            elif node[0] == 'C':
                inst_type = 'Capacitor'
                #value = self.circuit[node].capacitance
            else:
                
                #value = self.circuit[node].resistance
                pass


            weight = weights[inst_type]

            

            self.graph['nodes'].append({
                'id': node,
                'inst_type':inst_type,
                'ports':self.edges[node],
                'value':value,
                'edge_weight': weight

            })


        #print(self.graph)
        self.graph['edges'] = []
        

        filename = (self.directory.split('/')[-1]).split('.')[0]
        with open('./graph/{}.json'.format(filename), 'w') as outfile:
             #   print(filename)
            json.dump(self.graph, outfile)
    
    def checkSubset(self,list1: list, list2: list):
        for i in list1:
            if i not in list2:
                return False
        return True


if __name__ == '__main__':
    logger.debug("Program loaded")
    file_dir = input("Enter file directory(absolute or relative wrt program location) :")
    if os.path.isfile(file_dir):
        logger.debug("file found.")
        fp = open(file_dir, 'r')
        file_parser = Parser(file_dir)
        logger.info("Parsing file data.")
        file_parser.parseData()
        file_parser.jsonify()

    else:
        logger.critical("File not found.. exiting the program.")
    
    