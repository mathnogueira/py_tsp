"""
Módulo que contém as classes necessárias para representar um grafo
"""

class Graph:
    """
    Classe que representa um grafo
    """

    def __init__(self):
        self.nodes = []
        self.start_node = None

    def __str__(self):
        self_str = ''
        for (index, node) in enumerate(self.nodes):
            self_str += '%f - %s\n' % (index, str(node))
        self_str += '\n'
        map_node_index = self.get_map_nodes_index()
        for (index_a, node) in enumerate(self.nodes):
            for link in node.get_links():
                index_b = map_node_index[link.destination]
                if index < index_b:
                    self_str += '(%f, %f) - %f\n' % (index, index_b, link.cost)
        return self_str

    def __repr__(self):
        return str(self)


    def get_map_nodes_index(self):
        """
        Realiza um mapeamento dos nós do grafo para seus respectivos índices

        :param graph: grafo
        :return: mapeamento de nós para índices
        """
        map_node_index = dict()
        for (index, node) in enumerate(graph.nodes):
            map_node_index[node] = index
        return map_node_index

    def add_node(self, node):
        """
        Adiciona um nó ao grafo

        :param node: nó a ser adicionado
        """
        self.nodes.append(node)

    def apply_costs(self, costs):
        """
        Aplica os custos das arestas do grafo. Cada posição do array de
        custos deve conter outro array que indica o custo de se mover para
        cada outro nó do grafo.

        Exemplo: Para o array de custo de um nó qualquer: [0,2,3]
        Esse array indica que o grafo tem os custos:
        0 para ir ao nó 0,
        2 para ir ao nó 1,
        3 para ir ao nó 2,

        :param costs: matriz de custos onde cada linha representa os custos para
        as arestas que saem de um nó
        """

        for graph_links in zip(self.nodes, costs):
            for (index, cost) in enumerate(graph_links[1]):
                node = graph_links[0]
                destination_node = self.nodes[index]
                if node != destination_node:
                    node.add_link(destination_node, cost)

    
    def set_starting_node(self, node):
        """
        Define o nó inicial do grafo

        :param node: nó inicial do grafo
        """
        self.start_node = node

    def get_starting_node(self):
        """
        Retorna o nó inicial do grafo.

        :return: nó inicial do grafo
        """
        return self.start_node

    def number_nodes(self):
        """
        Retorna o número de nós contidos no grafo

        :return: número de nós contidos no grafo
        """
        return len(self.nodes)

class GraphNode:
    """
    Classe que representa um nó do grafo.
    """

    count_index = 0

    def __init__(self, data):
        self.index = GraphNode.count_index
        GraphNode.count_index += 1
        self.links_map = dict()
        self.links = []
        self.prize = data[0]
        self.penality = data[1]
        self.visited = False

    def __str__(self):
        return '(%f, %f)' % (self.prize, self.penality)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return self.index

    def __eq__(self, other):
        return isinstance(other, GraphNode) and self.index == other.index

    def add_link(self, destination, cost):
        """
        Adiciona uma aresta ao nó.

        :param destination: nó que será alcançado por essa aresta
        :param cost: custo de se movimentar por essa aresta
        """
        self.links_map[destination] = cost
        link = GraphLink(destination, cost)
        self.links.append(link)

    def get_links(self):
        """
        Retorna as arestas que ligam este nó aos outros nós do grafo.

        :return: arestas que saem deste nó.
        """
        return self.links

    def get_links_mean(self):
        mean = 0
        for link in self.links:
            mean += link.cost
        return mean / len(self.links)


    def get_cost_to(self, node):
        """
        Retorna o custo da aresta que conecta esse nó com o outro especificado.

        :return: custo da aresta que conecta o nó com o nó especificado.
        """
        return self.links_map[node]

    def get_link_to(self, node):
        """
        Retorna a aresta que conecta esse nó com o outro especificado.

        :return: aresta que conecta o nó com o nó especificado.
        """
        for link in self.links:
            if link.destination == node:
                return link

        return None


class GraphLink:
    """
    Classe que representa um aresta do grafo.
    """

    def __init__(self, destination, cost):
        self.destination = destination
        self.cost = cost

    def __str__(self):
        return '(%f, %f)' % (self.destination, self.cost)

    def __repr__(self):
        return str(self)
