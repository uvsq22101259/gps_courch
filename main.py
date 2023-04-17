import json
import heapq

class Graph:
    def __init__(self, graph):
        self.graph = graph
        self.nodes = set(graph.keys())

    def get_shortest_path(self, start_node, end_node):
        distances = {node: float('inf') for node in self.nodes}
        distances[start_node] = 0

        heap = [(0, start_node)]
        while heap:
            (current_distance, current_node) = heapq.heappop(heap)
            if current_node == end_node:
                path = []
                while current_node is not None:
                    path.append(current_node)
                    current_node = distances[current_node][1]
                return path[::-1]

            for neighbor, weight in self.graph[current_node].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = (distance, current_node)
                    heapq.heappush(heap, (distance, neighbor))

        return None

with open('data/data11.json', 'r') as f:
    data = json.load(f)

graph = Graph(data)

start_node = input("Entrez le nœud de départ: ")
end_node = input("Entrez le nœud de fin: ")

shortest_path = graph.get_shortest_path(start_node, end_node)
if shortest_path:
    print("Le chemin le plus court est: ", "->".join(shortest_path))
else:
    print("Il n'y a pas de chemin possible entre ces deux nœuds.")
