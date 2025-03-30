from models.robot import Robot
import logging
import os

log_dir = os.path.join(os.path.dirname(__file__), "../../logs")
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, "fleet_logs.txt")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='a'
)

class FleetManager:
    def __init__(self, gui_scene, traffic_manager, vertices):
        """
        Initialize FleetManager with graphical scene, traffic management, and vertices data.
        :param gui_scene: PyQt graphical scene.
        :param traffic_manager: TrafficManager instance.
        :param vertices: List of vertex data from the navigation graph.
        """
        self.robots = []  # List of robot instances
        self.scene = gui_scene  # PyQt graphical scene
        self.traffic_manager = traffic_manager  # TrafficManager instance
        self.vertices = vertices  # Vertices data from the navigation graph
        self.robot_counter = 0  # Counter to assign unique IDs to robots


    def spawn_robot(self, vertex_index):
        """
        Spawn a robot at the specified vertex.
        :param vertex_index: The index of the vertex where the robot is spawned.
        :return: The created robot instance or None if failed.
        """
        if not self.traffic_manager.request_vertex(None, vertex_index):
            print(f"Vertex {vertex_index} is occupied. Cannot spawn robot.")
            return None

        # Retrieve vertex data using the provided index
        vertex_data = self.vertices[vertex_index]
        x, y = vertex_data[:2]  # Extract coordinates

        # Create and initialize the robot
        robot = Robot(self.robot_counter, vertex_index, self.scene, self.traffic_manager, self.vertices)
        robot.spawn(x, y)
        self.robots.append(robot)
        self.robot_counter += 1
        print(f"Robot {robot.id} spawned at vertex {vertex_index}.")
        return robot


    def assign_task(self, robot_id, path):
        robot = next((r for r in self.robots if r.id == robot_id), None)
        if robot:
            robot.assign_task(path)
            logging.info(f"Assigned task to Robot {robot_id}: Path {path}")
        else:
            logging.error(f"Failed to assign task to robot{robot_id}.Robot not found.")