import sys

from tsp.graph_builder import GraphBuilder
from tsp.heuristics.greedy import GreedyHeuristic
from tsp.heuristics.insertion import InsertionHeuristic
from tsp.draw_graph import DrawGraph


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Erro: Você deve informar o nome do arquivo de descrição do grafo")
        print("Modo de uso: python main.py <arquivo_descricao_grafo>")
        exit()

    filename = sys.argv[1]

    graph_builder = GraphBuilder()
    graph = graph_builder.build(filename)

    greedy_heuristic = GreedyHeuristic()
    greedy_total_cost = greedy_heuristic.solve(graph)

    graph = graph_builder.build(filename)

    insertion_heuristic = InsertionHeuristic()
    insertion_total_cost = insertion_heuristic.solve(graph)

    draw_graph = DrawGraph()
    index_sep_dir = filename.rindex('/') + 1
    filename_no_dir = filename[index_sep_dir:]
    index_dot = filename_no_dir.index('.')
    filename_no_dir = filename_no_dir[:index_dot]
    solution_name = 'solInsertion' + filename_no_dir
    draw_graph.draw(graph, insertion_heuristic.visitation_order, solution_name)

    print("Custo total do algoritmo guloso: ", greedy_total_cost)
    print("Custo total do algoritmo de inserção: ", insertion_total_cost)
    