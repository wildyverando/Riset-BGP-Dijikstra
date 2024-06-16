import networkx as nx
import matplotlib.pyplot as plt
import random
import heapq

# >> Beberapa AS number sebagai contoh
as_numbers = [
    1734, 2914, 3320, 3356, 3491, 5511, 6453, 6461, 6762, 6830, 7018, 701, 1299, 1239, 7922
]

# >> Draw Graf dari Nodes AS
G = nx.Graph()
G.add_nodes_from(as_numbers)

# >> Menghubungkan AS Secara Acak dari Nilai AS yang telah ditentukan.
for i in range(len(as_numbers)):
    for j in range(i + 1, len(as_numbers)):
        if random.random() < 0.3:
            G.add_edge(as_numbers[i], as_numbers[j])

# >> Loop dan tambahkan metrik BGP secara Acak
for u, v in G.edges():
    G[u][v]['weight'] = random.randint(1, 10)  # >> Acak panjang AS_PATH dari 1-10

# >> Implementasi Algoritma Dijkstra
def dijkstra(graph, source):
    distances = {node: float('inf') for node in graph.nodes()}
    distances[source] = 0
    priority_queue = [(0, source)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_distance > distances[current_node]:
            continue
        for neighbor, edge_data in graph[current_node].items():
            distance = current_distance + edge_data['weight']
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

# >> Visualisasi graf BGP
fig, ax = plt.subplots(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_size=800, font_size=8, node_color='skyblue', ax=ax)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
ax.set_title('Visualisasi BGP Terdekat dari AS7018 ke AS1239')

# >> Analisis jalur AS dengan Dijkstra (contoh: AS7018 ke AS1239)
source_as = 7018
target_as = 1239

distances = dijkstra(G, source_as)
if target_as in distances:
    # >> Menelusuri jalur terpendek
    path = [target_as]
    while path[-1] != source_as:
        for neighbor, edge_data in G[path[-1]].items():
            if distances[neighbor] + edge_data['weight'] == distances[path[-1]]:
                path.append(neighbor)
                break
    path.reverse()

    # >> Menampilkan jalur terpendek di plt show
    path_str = " -> ".join([f"AS{node}" for node in path])
    ax.text(0.5, -0.1, path_str, ha='center', va='top', transform=ax.transAxes)

plt.show()
