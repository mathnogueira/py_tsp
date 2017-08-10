from graphviz import Graph
from copy import copy

class DrawGraph:
    """
    Classe é responsável pelo desenho de grafos juntamente com uma solução.

    """
    def __init__(self):
        self.name = None


    def get_edges(self, graph, solution, map_node_index):
        """
        Recupera o conjunto de arestas contidas na solução, utilizando o 
        formato em tupla (x, y) para definir uma aresta do nó de índice x 
        para o de índice y, onde x < y.

        :param graph: grafo
        :param solution: solução para o grafo
        :param map_node_index: mapeamento dos nós do grafo para seus 
            respectivos índices
        :return: conjunto de arestas contidas na solução
        """
        edges = set()
        solution_cp = copy(solution)
        solution_cp.append(solution_cp[0])
        N = len(solution_cp)-1
        for index in range(N):
            edge = map_node_index[solution_cp[index]], map_node_index[solution_cp[index+1]]
            if edge[0] > edge[1]:
                edge = edge[1], edge[0]
            edges.add(edge)

        return edges


    def draw(self, graph, solution, solution_name):
        """
        Desenha o grafo mostrando a solução

        :param graph: grafo
        :param solution: solução para o grafo
        :param solution_name: nome da solução
        """
        dot_graph = Graph(solution_name, None, None, None, 'svg', 'dot')
        #dot_graph.graph_attr['rankdir'] = 'LR'
        for (index, node) in enumerate(solution):
            name = str(index)
            label = '(%d, %d)' % (node.prize, node.penality)
            dot_graph.node(name, label)

        N = len(solution)
        for index in range(N-1):
            node = solution[index]
            destination = solution[index+1]
            cost = node.get_cost_to(destination)
            start_node_name = str(index)
            end_node_name = str(index+1)
            label =  str(int(cost))
            dot_graph.edge(start_node_name, end_node_name, label)

        if N > 1:
            node = solution[N-1]
            destination = solution[0]
            cost = node.get_cost_to(destination)
            start_node_name = str(N-1)
            end_node_name = str(0)
            label = str(int(cost))
            dot_graph.edge(start_node_name, end_node_name, label)

    
        # for (index, node) in enumerate(graph.nodes):
        #     name = str(index)
        #     label = '(%d, %d)' % (node.prize, node.penality)
        #     if node == solution[0]:
        #         dot_graph.node(name, label, color='red', style="filled")
        #     else:
        #         dot_graph.node(name, label)

        # map_node_index = self.get_map_nodes_index(graph)
        # edges = self.get_edges(graph, solution, map_node_index)

        # for (index, node) in enumerate(graph.nodes):
        #     for link in node.links:
        #         index_dest = map_node_index[link.destination]
        #         if index < index_dest: 
        #             start_node_name = str(index)
        #             end_node_name = str(index_dest)
        #             label = str(link.cost)
        #             if (index, index_dest) in edges:
        #                 dot_graph.edge(start_node_name, end_node_name, label)
                    #else:
                        #dot_graph.edge(start_node_name, end_node_name, label, color='red')

        dot_graph.save(solution_name + '.dot')
        dot_graph.render(solution_name, None, False, True)

        # for (index, node) in enumerate(graph.nodes):
        #     for link in node.links:
        #         index_dest = map_node_index[link.destination]
        #         if index < index_dest: 
        #             start_node_name = 'n' + str(index)
        #             end_node_name = 'n' + str(index_dest)
        #             label = str(link.cost)
        #             if (index, index_dest) not in edges:
        #                 dot_graph.edge(start_node_name, end_node_name, label, color='red')

        # solution_name += "Compl"
        # dot_graph.save(solution_name + '.dot')
        # dot_graph.render(solution_name, None, True, True)
