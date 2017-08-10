"""
Módulo responsável por prover todas as ferramentas necessárias para
converter a definição de um grafo em uma instância do grafo.
"""

from tsp.graph.graph import Graph
from tsp.graph.graph import GraphNode

class GraphBuilder:
    """
    Classe é responsável pela criação de grafos utilizando sua definição em texto

    @author Carlos Pereira
    @author Matheus Nogueira
    @author Pedro Mutter
    @author Raul Manzarraga
    """

    def __init__(self):
        self.name = None

    def build(self, file):
        """
        Cria um grafo a partir de sua definição

        :param file: arquivo que contém a definição do grafo a ser criado
        """
        file_content = self._get_file_content(file)
        formatted_file_content = self._format_file_content(file_content)
        return self._create_graph(formatted_file_content)


    def _create_graph(self, configuration):

        # Converte os valores obtidos em floats
        prizes = [float(prize) for prize in configuration[0].split(' ')]
        penalities = [float(penality) for penality in configuration[1].split(' ')]
        costs = []
        for node_costs in configuration[2:]:
            costs.append([float(cost) for cost in node_costs.split(' ')])

        graph = Graph()

        # Cria todos os nós do grafo
        for node_data in zip(prizes, penalities):
            node = GraphNode(node_data)
            graph.add_node(node)

        # Adiciona os pesos para todas as arestas do grafo
        graph.apply_costs(costs)

        # Define o primeiro nó como sendo o inicial
        graph.set_starting_node(graph.nodes[0])

        return graph
            

    def _get_file_content(self, file):
        """
        Obtém o conteúdo de um arquivo

        :param file: nome do arquivo que terá seu conteúdo extraído.
        :return: lista contendo todas as linhas do arquivo
        """

        file_cursor = open(file)
        return file_cursor.readlines()

    def _format_file_content(self, lines):
        """
        Formata o conteúdo de um arquivo. Esse método é responsável por remover
        qualquer texto que seja desnecessário para a criação de um grafo.

        :param lines: lista contendo linhas do arquivo
        :return: lista de linhas que são úteis para a criação do grafo
        """

        useful_lines = []
        for (line_number, line_content) in enumerate(lines):
            # Remove linhas que só contém o caracter de quebra de linha
            if len(line_content) == 1:
                continue

            # Remove as linhas que contém texto que não contém dados úteis para
            # a geração do grafo
            if line_number in [0, 2, 5, 8]:
                continue

            # Remove espaços em branco extras (transforma n espaços em branco
            # em apenas 1)
            line_content = ' '.join(line_content.split())

            # Adiciona linha que passou em todos os filtros
            useful_lines.append(line_content)

        return useful_lines
