class TrafficManager:
    def __init__(self):
        self.occupied_vertices = {}  # Tracks which vertex is occupied and by which robot

    def request_vertex(self, robot_id, vertex_index):
        if vertex_index in self.occupied_vertices:
            print(f"Vertex {vertex_index} is currently occupied by Robot {self.occupied_vertices[vertex_index]}.")
            return False
        self.occupied_vertices[vertex_index] = robot_id
        print(f"Robot {robot_id} occupied vertex {vertex_index}.")
        return True

    def release_vertex(self, vertex_index):
        if vertex_index in self.occupied_vertices:
            print(f"Vertex {vertex_index} released by Robot {self.occupied_vertices[vertex_index]}.")
            del self.occupied_vertices[vertex_index]
