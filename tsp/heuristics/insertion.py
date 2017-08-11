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
        self.collected_prize = self.current_node.prize
        self.current_cost = self.get_total_penalities() - self.current_node.penality
        
        cost_is_decreasing = False
        best_cost = float("inf")
        current_iteration_cost = self.current_cost
        best_insertion_order = None        
        should_continue = self.should_continue()
        number_tries = 0

        while should_continue or (number_tries < 50 and len(self.visitation_order) < self.graph.number_nodes()):
            # recupera o melhor nó para inserir no momento
            best_insertion = self.get_best_insertion()
            current_iteration_cost = best_insertion[1]
            self.visitation_order.insert(best_insertion[0][1], best_insertion[0][0])
            # atualiza o custo atual e o prêmio
            self.collected_prize += best_insertion[0][0].prize
            self.current_cost = current_iteration_cost
            cost_is_decreasing = current_iteration_cost < best_cost

            if cost_is_decreasing:
                best_cost = current_iteration_cost
                best_insertion_order = copy(self.visitation_order)
                number_tries = 0
            else:
                number_tries += 1

            should_continue = self.should_continue()

        self.visitation_order = best_insertion_order
        return self.calculate_visitation_cost(best_insertion_order)

    def get_best_insertion(self):
        """
        Encontra qual nó deve ser inserido no sub-grafo para minimizar o custo
        de visitar os nós do grafo original e o insere na lista de nós visitados.
        """
        possible_nodes = [node for node in self.graph.nodes if node not in self.visitation_order]
        best_insertion = None
        best_insertion_cost = float("inf")
        N = len(self.visitation_order)

        # salva em uma lista os custos das arestas dos nós do índice atual para o anterior 
        if N > 1:
            cost_cache = [ self.visitation_order[0].get_cost_to(self.visitation_order[N-1]) ]
        else:
            cost_cache = [ 0 ]
        for index in range(N-1):
            cost_cache.append(self.visitation_order[index].get_cost_to(self.visitation_order[index+1]))

        for node in possible_nodes:
            for position in range(N):
                cost_to_1 = node.get_cost_to(self.visitation_order[position])
                cost_to_2 = node.get_cost_to(self.visitation_order[position-1])
                # calcula o custo após a inserção do nó node na posição position
                cost = self.current_cost - cost_cache[position]
                cost += cost_to_1
                cost += cost_to_2
                cost -= node.penality
                if cost < best_insertion_cost:
                    best_insertion_cost = cost
                    best_insertion = (node, position)

        return (best_insertion, best_insertion_cost)

    def should_continue(self):
        """
        Define se o algoritmo deve continuar executando ou deve parar nesse momento.

        :return: True, se deve continuar, False se não deve continuar
        """
        necessary_prize_to_stop = self.total_prize * self.stop_threshold

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

        visitation_order.append(visitation_order[0])

        for (index, node) in enumerate(visitation_order):
            if index < len(visitation_order) - 1:
                next_node = visitation_order[index+1]
                link_next_node = node.get_link_to(next_node)
                total_cost += link_next_node.cost
        
        visitation_order.pop()

        return total_penalities + total_cost
