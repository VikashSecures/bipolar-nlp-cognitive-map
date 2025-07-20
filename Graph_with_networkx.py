import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load your CSV file into a DataFrame
file_path = 'G:/NMIT/research project a/CODE/bipolar_knowledge_graph.csv'  # Update with your actual file path
df = pd.read_csv(file_path)

# Initialize an empty directed graph for the complete data
G_complete = nx.DiGraph()

# Loop through the DataFrame and add triples to the graph for the complete data
for index, row in df.iterrows():
    head, relation, tail = row['Head'], row['Relation'], row['Tail']

    # Add nodes and edges to the complete graph
    G_complete.add_edge(head, tail, label=relation)

# Plotting the complete graph
plt.figure(figsize=(25, 25), dpi=300)
pos_complete = nx.spring_layout(G_complete, k=2, iterations=50, seed=0)  # Adjust layout for better visualization
nx.draw_networkx_nodes(G_complete, pos_complete, node_size=5000, node_color='skyblue')
nx.draw_networkx_edges(G_complete, pos_complete, edge_color='gray', width=2)
nx.draw_networkx_labels(G_complete, pos_complete, font_size=12)

# Draw edge labels for the complete graph
edge_labels_complete = nx.get_edge_attributes(G_complete, 'label')
nx.draw_networkx_edge_labels(G_complete, pos_complete, edge_labels=edge_labels_complete, font_size=12)

plt.title('Complete Knowledge Graph')
plt.axis('off')
plt.show()

# Creating a smaller subgraph with a subset of nodes (first 5 rows as an example)
G_subset = nx.DiGraph()

# Loop through a subset of the DataFrame (first 5 rows for simplicity)
for index, row in df.head(5).iterrows():
    head, relation, tail = row['Head'], row['Relation'], row['Tail']

    # Add nodes and edges to the subset graph
    G_subset.add_edge(head, tail, label=relation)

# Plotting the smaller subset graph
plt.figure(figsize=(10, 8), dpi=300)
pos_subset = nx.spring_layout(G_subset, k=2, iterations=50, seed=0)  # Positioning the graph for better visualization
nx.draw_networkx_nodes(G_subset, pos_subset, node_size=2000, node_color='lightgreen')
nx.draw_networkx_edges(G_subset, pos_subset, edge_color='gray', width=2)
nx.draw_networkx_labels(G_subset, pos_subset, font_size=10)

# Draw edge labels for the subset graph
edge_labels_subset = nx.get_edge_attributes(G_subset, 'label')
nx.draw_networkx_edge_labels(G_subset, pos_subset, edge_labels=edge_labels_subset, font_size=10)

plt.title('Subset of Knowledge Graph')
plt.axis('off')
plt.show()
