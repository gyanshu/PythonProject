import heapq
from collections import defaultdict


class CurrencyConverter:
    def __init__(self, rates):
        """
        Initialize the conversion graph.
        :param rates: List of conversion rates in format ["USD:CAD:DHL:5", "USD:GBP:FEDX:10"]
        """
        self.graph = defaultdict(list)
        for rate in rates:
            src, tgt, method, cost = rate.split(':')
            cost = float(cost)  # Ensure cost is treated as a number
            self.graph[src].append((tgt, method, cost))

    def convert_direct(self, src, tgt, amount):
        """ Converts directly from src to tgt if a direct conversion exists. """
        for neighbor, method, cost in self.graph[src]:
            if neighbor == tgt:
                return amount * cost, [method]
        return None  # No direct conversion available

    def convert_with_one_hop(self, src, tgt, amount):
        """ Finds the minimum cost conversion with at most 1 extra hop. """
        min_cost = float('inf')
        best_path = None

        # Try direct conversion
        direct = self.convert_direct(src, tgt, amount)
        if direct:
            return direct

        # Try 1-hop conversion
        for intermediate, method1, rate1 in self.graph[src]:
            for neighbor, method2, rate2 in self.graph[intermediate]:
                if neighbor == tgt:
                    total_cost = amount * rate1 * rate2
                    if total_cost < min_cost:
                        min_cost = total_cost
                        best_path = [method1, method2]

        return (min_cost, best_path) if best_path else None

    def convert_with_two_hops(self, src, tgt, amount):
        """ Finds the minimum cost conversion with at most 2 extra hops. """
        min_cost = float('inf')
        best_path = None

        # Try direct conversion
        direct = self.convert_direct(src, tgt, amount)
        if direct:
            return direct

        # Try 1-hop conversion
        one_hop = self.convert_with_one_hop(src, tgt, amount)
        if one_hop:
            return one_hop

        # Try 2-hop conversion
        for intermediate1, method1, rate1 in self.graph[src]:
            for intermediate2, method2, rate2 in self.graph[intermediate1]:
                for neighbor, method3, rate3 in self.graph[intermediate2]:
                    if neighbor == tgt:
                        total_cost = amount * rate1 * rate2 * rate3
                        if total_cost < min_cost:
                            min_cost = total_cost
                            best_path = [method1, method2, method3]

        return (min_cost, best_path) if best_path else None

    def convert_with_exactly_one_hop(self, src, tgt, amount):
        """ Finds the minimum cost conversion that requires exactly 1 intermediate currency. """
        min_cost = float('inf')
        best_path = None

        for intermediate, method1, rate1 in self.graph[src]:
            for neighbor, method2, rate2 in self.graph[intermediate]:
                if neighbor == tgt:
                    total_cost = amount * rate1 * rate2
                    if total_cost < min_cost:
                        min_cost = total_cost
                        best_path = [method1, method2]

        return (min_cost, best_path) if best_path else None

    def convert_with_dijkstra(self, src, tgt, amount):
        """
        Dijkstra's Algorithm to find the minimum-cost conversion allowing infinite hops.
        Returns (min cost, shipping methods) or None if no path exists.
        """
        pq = [(0, src, amount, [])]  # (total_cost, current_currency, converted_amount, path)
        min_costs = {src: 0}  # Track minimum cost to reach each node
        best_paths = {src: []}  # Track paths

        while pq:
            curr_cost, curr, curr_amount, path = heapq.heappop(pq)

            if curr == tgt:
                return curr_amount, path  # Found the cheapest path

            for neighbor, method, rate in self.graph[curr]:
                new_amount = curr_amount * rate
                new_cost = curr_cost + rate  # Total cost accumulates

                if neighbor not in min_costs or new_cost < min_costs[neighbor]:
                    min_costs[neighbor] = new_cost
                    best_paths[neighbor] = path + [method]
                    heapq.heappush(pq, (new_cost, neighbor, new_amount, path + [method]))

        return None  # No valid path found


rates = [
    "USD:CAD:DHL:1.25",
    "USD:GBP:FEDX:0.75",
    "CAD:GBP:UPS:0.8",
    "GBP:EUR:DHL:1.2",
    "CAD:EUR:FEDX:1.1",
]

converter = CurrencyConverter(rates)

# Direct conversion (no extra hops)
print(converter.convert_direct("USD", "CAD", 100))  # (125.0, ['DHL'])

# At most 1 extra hop
print(converter.convert_with_one_hop("USD", "EUR", 100))  # (USD -> GBP -> EUR)

# At most 2 extra hops
print(converter.convert_with_two_hops("USD", "EUR", 100))  # (USD -> CAD -> GBP -> EUR)

# Exactly 1 extra hop
print(converter.convert_with_exactly_one_hop("USD", "EUR", 100))  # (USD -> GBP -> EUR)

# Infinite hops (Dijkstra's Algorithm)
print(converter.convert_with_dijkstra("USD", "EUR", 100))
