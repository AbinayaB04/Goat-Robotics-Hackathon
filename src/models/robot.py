from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QBrush, QColor

class Robot:
    def __init__(self, robot_id, start_vertex, gui_scene, traffic_manager, vertices):
        """
        Initialize the Robot.
        :param robot_id: Unique ID for the robot.
        :param start_vertex: The starting vertex of the robot.
        :param gui_scene: The PyQt graphical scene where the robot is displayed.
        :param traffic_manager: The TrafficManager instance for managing vertex occupancy.
        :param vertices: List of vertex data from the navigation graph.
        """
        self.id = robot_id
        self.current_vertex = start_vertex
        self.scene = gui_scene
        self.traffic_manager = traffic_manager
        self.vertices = vertices  # Store the vertices data
        self.item = None
        self.path = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.move_step)
        self.status = "idle"

    def spawn(self, x, y):
        """Create graphical representation of the robot."""
        color = QColor.fromHsv((self.id * 50) % 360, 255, 255)
        self.item = self.scene.addEllipse(x * 50, y * 50, 20, 20, brush=QBrush(color))
        self.status = "idle"

    def assign_task(self, path):
        """Assign a path for the robot to follow."""
        self.path = path
        self.status = "moving"
        self.timer.start(500)

    def move_step(self):
        """Move the robot along its assigned path."""
        if self.path:
            # Release the current vertex before moving
            self.traffic_manager.release_vertex(self.current_vertex)

            # Move to the next vertex in the path
            next_vertex_index = self.path.pop(0)
            if not self.traffic_manager.request_vertex(self.id, next_vertex_index):
                # Retry logic: Insert the vertex back for the next attempt
                self.path.insert(0, next_vertex_index)
                print(f"Robot {self.id} waiting for vertex {next_vertex_index} to be free.")
                return

            # Update graphical position and mark new vertex as occupied
            self.current_vertex = next_vertex_index
            vertex_data = self.vertices[next_vertex_index]
            x, y = vertex_data[:2]
            self.item.setRect(x * 50, y * 50, 20, 20)  # Move robot graphically

            # If the path is complete, stop the robot and release the vertex
            if not self.path:
                self.traffic_manager.release_vertex(self.current_vertex)
                self.status = "task_complete"
                self.timer.stop()
                print(f"Robot {self.id} completed its task.")
