import matplotlib.pyplot as plt
import networkx as nx

def visualize_erd():
    # Create the ERD graph
    G = nx.DiGraph()

    # Entities (tables) for the ERD
    entities = [
        "User", "UserPortfolio", "Holding", "Stock", "Sector",
        "Document", "ValuationModel", "Transaction", "Configuration",
        "HistoricalMetric", "HistoricalPrice", "Dividend"
    ]

    for entity in entities:
        G.add_node(entity)

    # Relationships between entities
    edges = [
        ("User", "UserPortfolio"),
        ("User", "Configuration"),
        ("UserPortfolio", "Holding"),
        ("UserPortfolio", "Transaction"),
        ("Holding", "Stock"),
        ("Stock", "Holding"),
        ("Stock", "HistoricalMetric"),
        ("Stock", "HistoricalPrice"),
        ("Stock", "Dividend"),
        ("Stock", "Document"),
        ("Stock", "ValuationModel"),
        ("Stock", "Transaction"),
        ("Sector", "Document"),
        ("Sector", "Stock"),
        ("Stock", "Sector")
    ]

    for edge in edges:
        G.add_edge(*edge)

    # Position nodes for clarity
    fixed_positions = {
        "User": (0, 0),
        "Configuration": (1, 0),
        "UserPortfolio": (0, -1),
        "Holding": (-1, -2),
        "Stock": (0, -2),
        "Sector": (1, -2),
        "Document": (2, -2),
        "ValuationModel": (0, -3),
        "Transaction": (-1, -3),
        "HistoricalMetric": (-2, -3),
        "HistoricalPrice": (0, -4),
        "Dividend": (-1, -4)
    }

    pos = nx.spring_layout(G, pos=fixed_positions, fixed=fixed_positions.keys())

    # Draw the graph
    plt.figure(figsize=(20, 14))
    nx.draw(G, pos, with_labels=True, node_size=6000, node_color="lightblue", font_size=16, 
            width=2.5, edge_color="gray", alpha=0.8, arrowsize=25, arrowstyle='-|>', 
            edgecolors='black', linewidths=1.5)

    # Highlight primary keys for entities
    primary_keys = {
        "User": "id",
        "Configuration": "id",
        "UserPortfolio": "id",
        "Holding": "id",
        "Stock": "id",
        "Sector": "id",
        "Document": "id",
        "ValuationModel": "id",
        "Transaction": "id",
        "HistoricalMetric": "id",
        "HistoricalPrice": "date, stock_id",
        "Dividend": "id"
    }

    for entity, pk in primary_keys.items():
        plt.annotate(f"PK: {pk}", (pos[entity][0], pos[entity][1]-0.075), 
                     color='black', fontsize=10, ha='center')

    # Add title and legend
    plt.title("Entity-Relationship Diagram (ERD)", fontsize=24, pad=20)

    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='Entity', markersize=15, markerfacecolor='lightblue', markeredgewidth=1.5, markeredgecolor='black'),
        plt.Line2D([0], [0], color='gray', label='Relationship', markersize=15, linewidth=2.5)
    ]
    plt.legend(handles=legend_elements, loc='upper right', fontsize=14)

    plt.show()

# Uncomment the following line to run the function and visualize the ERD
# visualize_erd()
