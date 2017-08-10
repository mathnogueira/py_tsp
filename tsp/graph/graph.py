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

    def __init__(self, data):
        self.links = []
        self.prize = data[0]
        self.penality = data[1]
        self.visited = False

    def add_link(self, destination, cost):
        """
        Adiciona uma aresta ao nó.

        :param destination: nó que será alcançado por essa aresta
        :param cost: custo de se movimentar por essa aresta
        """
        link = GraphLink(destination, cost)
        self.links.append(link)

    def get_links(self):
        """
        Retorna as arestas que ligam este nó aos outros nós do grafo.

        :return: arestas que saem deste nó.
        """
        return self.links

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
