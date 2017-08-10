from tsp.heuristics.base_heuristic import BaseHeuristic

class GreedyHeuristic(BaseHeuristic):
    """
    Heuristica que resolve o problema utilizando um algoritmo guloso.
    """

    def __init__(self): 
        super(GreedyHeuristic, self).__init__()


    def solve(self, graph):
        super(GreedyHeuristic, self).solve(graph)
        
        while self.should_continue():
            self.current_node.visited = True
            best_path = self.get_best_path()
            if best_path == None:
                break
            self.total_cost += best_path.cost
            self.current_node = best_path.destination
            self.collected_prize += self.current_node.prize

        # Peso para voltar para o nó inicial
        link_to_starting_node = self.current_node.get_link_to(self.graph.get_starting_node())
        return self.total_cost + link_to_starting_node.cost + self.get_total_penalities()

    def get_best_path(self):
        best_penality_over_cost = 0.0
        possible_paths = self.current_node.get_links()
        penalities_over_costs = [path.destination.penality / path.cost for path in possible_paths]

        for (path, penality_over_cost) in zip(possible_paths, penalities_over_costs):
            node = path.destination
            if not node.visited and penality_over_cost > best_penality_over_cost:
                best_penality_over_cost = penality_over_cost

        if (best_penality_over_cost == 0.0):
            return None

        index_best = penalities_over_costs.index(best_penality_over_cost)
        return possible_paths[index_best]

    def should_continue(self):
        possible_paths = self.current_node.get_links()
        penalities_over_costs = [path.destination.penality / path.cost for path in possible_paths]

        necessary_prize_to_stop = self.total_prize * self.stop_threshold

        #return max(penalities_over_costs) > 1 and self.collected_prize < necessary_prize_to_stop
        return self.collected_prize < necessary_prize_to_stop or max(penalities_over_costs) > 1