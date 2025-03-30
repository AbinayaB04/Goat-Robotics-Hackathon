import json

class NavGraph:
    def __init__(self, file_path):
        """Initialize NavGraph by loading vertices and lanes from JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            self.vertices = data["levels"]["l1"]["vertices"]
            self.lanes = data["levels"]["l1"]["lanes"]
        except Exception as e:
            print(f"Error loading navigation graph: {e}")
            self.vertices = []
            self.lanes = []

    def get_vertices(self):
        """Return the vertices of the graph."""
        return self.vertices

    def get_lanes(self):
        """Return the lanes of the graph."""
        return self.lanes

    def get_neighbors(self, vertex_index):
        """Get all neighboring vertices for a given vertex."""
        neighbors = []
        for lane in self.lanes:
            if lane[0] == vertex_index:
                neighbors.append(lane[1])
            elif lane[1] == vertex_index:
                neighbors.append(lane[0])
        return neighbors

# Standalone Function to Load Navigation Graph
def load_navigation_graph(file_path):
    """Load and return the navigation graph from a JSON file."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load navigation graph: {e}")
        return None
