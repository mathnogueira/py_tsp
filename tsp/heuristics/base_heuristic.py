class BaseHeuristic:

    def __init__(self):
        self.reset()

    def reset(self):
        """
        Reseta as contagens da heuristica
        """
        self.stop_threshold = 0.5
        self.collected_prize = 0.0
        self.total_cost = 0.0
        self.graph = None
        self.current_node = None
        self.total_prize = 0.0

    def solve(self, graph):
        """
        Inicia as variaveis necessárias para executar a heuristica
        """
        self.reset()
        self.graph = graph
        self.current_node = graph.get_starting_node()
        self.total_prize = self._calculate_total_prize()

    def _calculate_total_prize(self):
        """
        Calcula o prêmio máximo que pode ser obtido no grafo

        :return: 
        """
        total_prize = 0.0
        for node in self.graph.nodes:
            total_prize += node.prize
        return total_prize

    def get_total_penalities(self):
        """
        Calcula as penalidades dos nós não visitados

        :return: soma das penalidades dos nós não visitados
        """
        total_penalities = 0.0
        for node in self.graph.nodes:
            if not node.visited:
                total_penalities += node.penality
        return total_penalities
