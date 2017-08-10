from tsp.heuristics.base_heuristic import BaseHeuristic
from copy import copy

class InsertionHeuristic(BaseHeuristic):
    """
    Heuristica que resolve o problema utilizando um algoritmo guloso.
    """

    def __init__(self): 
        super(InsertionHeuristic, self).__init__()
        self.visitation_order = []

    def solve(self, graph):
        """
        Encontra a solução do problema usando o método de inserção de valores para
        minimizar o custo.

        :param graph: grafo que será resolvido.
        """
        super(InsertionHeuristic, self).solve(graph)
        self.visitation_order = [self.current_node]
        cost_is_decreasing = False
        previous_iteration_cost = float("inf")
        current_iteration_cost = 0
        best_insertion_order = None
        number_tries = 0

        while self.should_continue() or cost_is_decreasing:
            best_insertion = self.get_best_insertion()
            self.calculate_collected_prize()

            current_iteration_cost = best_insertion[1]
            cost_is_decreasing = current_iteration_cost < previous_iteration_cost
            if cost_is_decreasing:
                previous_iteration_cost = current_iteration_cost
                best_insertion_order = copy(self.visitation_order)
                number_tries = 0
            else:
                number_tries += 1
            
            # Limita o número de tentativas de melhora, se foi executada 50 iteraçoes
            # consecutivas e o custo do grafo não abaixou, para a execução.
            if number_tries >= 50:
                break

            self.visitation_order.insert(best_insertion[0][1], best_insertion[0][0])

            print("Current cost:", current_iteration_cost)

        return self.calculate_visitation_cost(best_insertion_order)

    def get_best_insertion(self):
        """
        Encontra qual nó deve ser inserido no sub-grafo para minimizar o custo
        de visitar os nós do grafo original e o insere na lista de nós visitados.
        """
        possible_nodes = [node for node in self.graph.nodes if node not in self.visitation_order]
        best_insertion = None
        best_insertion_cost = float("inf")

        for node in possible_nodes:
            # Evita inserção de nós já presentes no sub-grafo
            if node in self.visitation_order:
                continue

            for position in range(len(self.visitation_order) + 1):
                best_insertion_candidate = copy(self.visitation_order)
                best_insertion_candidate.insert(position, node)
                best_insertion_candidate.append(best_insertion_candidate[0])
                cost = self.calculate_visitation_cost(best_insertion_candidate)
                if cost < best_insertion_cost:
                    best_insertion_cost = cost
                    best_insertion = (node, position)

        return (best_insertion, cost)

    def should_continue(self):
        """
        Define se o algoritmo deve continuar executando ou deve parar nesse momento.

        :return: True, se deve continuar, False se não deve continuar
        """
        necessary_prize_to_stop = self.total_prize * self.stop_threshold

        print("Collected:", self.collected_prize, "Necessary:", necessary_prize_to_stop)
        return self.collected_prize < necessary_prize_to_stop

    def calculate_collected_prize(self):
        """
        Calcula a quantidade de premios coletados até o momento.

        :return: total de premios coletados nos nós visitados.
        """
        self.collected_prize = 0.0
        for node in self.visitation_order:
            self.collected_prize += node.prize

    def calculate_visitation_cost(self, visitation_order):
        """
        Calcula o custo total do sub-grafo informado.

        :param visitation_order: sub-grafo que terá o custo calculado.
        :return: custo do grafo informado
        """
        total_penalities = 0.0
        unvisited_nodes = [node for node in self.graph.nodes if node not in visitation_order]

        for unvisited_node in unvisited_nodes:
            total_penalities += unvisited_node.penality

        total_cost = 0.0

        for (index, node) in enumerate(visitation_order):
            if index < len(visitation_order) - 1:
                next_node = visitation_order[index+1]
                link_next_node = node.get_link_to(next_node)
                total_cost += link_next_node.cost
            

        return total_penalities + total_cost
