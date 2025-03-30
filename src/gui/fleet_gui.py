import sys
from PyQt5.QtWidgets import (
    QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QComboBox
)
from PyQt5.QtGui import QPen, QFont, QBrush, QColor
from PyQt5.QtCore import Qt
from models.nav_graph import NavGraph
from controllers.fleet_manager import FleetManager
from controllers.traffic_manager import TrafficManager
from utils.helpers import a_star_pathfinding


class FleetGUI(QWidget):
    def __init__(self, nav_graph_path):
        super().__init__()
        self.setWindowTitle("Improved Fleet Management System")
        self.setGeometry(100, 100, 1400, 800)

        # Main Layout
        self.layout = QVBoxLayout(self)

        # Graphics View and Scene
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.layout.addWidget(self.view)

        # Load Navigation Graph
        self.nav_graph = NavGraph(nav_graph_path)
        self.vertices = self.nav_graph.get_vertices()
        self.lanes = self.nav_graph.get_lanes()
        self.neighbors = self.compute_neighbors()
        # Controllers
        self.traffic_manager = TrafficManager()  # Initialize TrafficManager
        self.fleet_manager = FleetManager(self.scene, self.traffic_manager, self.vertices)  # Pass vertices to FleetManager

        # Robot Limit
        self.max_robots = 10  # Maximum number of robots allowed
        self.robot_count = 0  # Current number of robots

        # Selection State
        self.selected_vertex = None
        self.selected_robot = None

        # UI Controls
        self.init_ui_controls()

        # Draw Graph
        self.draw_graph()
    def compute_neighbors(self):
        """Generate a mapping of vertices to their neighbors based on lanes."""
        neighbors = {i: [] for i in range(len(self.vertices))}
        for lane in self.lanes:
            src, dest = lane[0], lane[1]
            neighbors[src].append(dest)
            neighbors[dest].append(src)  # Assuming undirected lanes
        return neighbors

    def init_ui_controls(self):
        """Initialize UI buttons and dropdowns."""
        controls = QHBoxLayout()

        # Spawn Robot Button
        self.spawn_robot_button = QPushButton("Spawn Robot")
        self.spawn_robot_button.clicked.connect(self.spawn_robot)
        controls.addWidget(self.spawn_robot_button)

        # Robot Selection Dropdown
        self.robot_selector = QComboBox()
        self.robot_selector.addItem("Select a robot")
        self.robot_selector.currentIndexChanged.connect(self.select_robot_from_list)
        controls.addWidget(self.robot_selector)

        # Assign Destination Button
        self.assign_task_button = QPushButton("Assign Destination")
        self.assign_task_button.clicked.connect(self.assign_task)
        controls.addWidget(self.assign_task_button)

        # Stop Robot Button
        self.stop_robot_button = QPushButton("Stop Robot")
        self.stop_robot_button.clicked.connect(self.stop_robot)
        controls.addWidget(self.stop_robot_button)

        # Logs Label
        self.logs_label = QLabel("Logs: Ready for interaction.")
        controls.addWidget(self.logs_label)

        self.layout.addLayout(controls)

    def draw_graph(self):
        """Draw the vertices and lanes."""
        for lane in self.lanes:
            src, dest = lane[:2]
            src_vertex, dest_vertex = self.vertices[src], self.vertices[dest]
            line = QGraphicsLineItem(
                src_vertex[0] * 50, src_vertex[1] * 50,
                dest_vertex[0] * 50, dest_vertex[1] * 50
            )
            line.setPen(QPen(Qt.gray, 2))
            self.scene.addItem(line)

        for idx, vertex in enumerate(self.vertices):
            x, y, attr = vertex[0], vertex[1], vertex[2]
            ellipse = QGraphicsEllipseItem(x * 50, y * 50, 20, 20)
            ellipse.setBrush(Qt.blue if attr.get("is_charger", False) else Qt.lightGray)
            ellipse.setToolTip(f"Vertex {idx} - {attr.get('name', '')}")
            self.scene.addItem(ellipse)
            ellipse.setData(0, idx)
            ellipse.mousePressEvent = lambda e, v=ellipse: self.select_vertex(v)

    def select_vertex(self, vertex_item):
        """Select a vertex."""
        self.selected_vertex = vertex_item.data(0)
        self.logs_label.setText(f"Selected Vertex: {self.selected_vertex}")

    def select_robot_from_list(self):
        """Handle robot selection from the dropdown."""
        index = self.robot_selector.currentIndex()
        if index == 0:
            self.selected_robot = None
            self.logs_label.setText("No robot selected.")
        else:
            self.selected_robot = index - 1
            self.logs_label.setText(f"Selected Robot: {self.selected_robot}")

    def spawn_robot(self):
        """Spawn a robot at the selected vertex."""
        if self.robot_count >= self.max_robots:
            self.logs_label.setText("Robot limit reached! Cannot spawn more robots.")
            return

        if self.selected_vertex is not None:
            # Attempt to spawn a robot
            robot = self.fleet_manager.spawn_robot(self.selected_vertex)
            if robot is None:
                self.logs_label.setText(f"Failed to spawn robot at Vertex {self.selected_vertex}. It might be occupied.")
                return

            # Retrieve vertex coordinates and create the robot's graphical label
            x, y = self.vertices[self.selected_vertex][:2]
            label = self.scene.addText(f"R{robot.id}", QFont("Arial", 10))
            label.setPos(x * 50 + 15, y * 50 - 15)

            # Add robot to dropdown for selection
            self.robot_selector.addItem(f"Robot {robot.id}")
            self.robot_count += 1
            robot.item.mousePressEvent = lambda e, r=robot.id: self.select_robot(r)
            self.logs_label.setText(f"Spawned Robot {robot.id} at Vertex {self.selected_vertex}.")
        else:
            self.logs_label.setText("Select a vertex to spawn a robot.")

    def assign_task(self):
        """Assign a task to the selected robot."""
        if self.selected_robot is not None and self.selected_vertex is not None:
            robot = self.fleet_manager.robots[self.selected_robot]
            start_vertex = robot.current_vertex

            # Ensure the destination is free
            if not self.traffic_manager.request_vertex(self.selected_robot, self.selected_vertex):
                self.logs_label.setText(f"Vertex {self.selected_vertex} is occupied. Robot {self.selected_robot} cannot proceed.")
                return

            # Find the path using A* pathfinding
            path = a_star_pathfinding(start_vertex, self.selected_vertex, self.vertices, self.neighbors)
            if path:
                self.fleet_manager.assign_task(self.selected_robot, path)
                self.logs_label.setText(f"Assigned task to Robot {self.selected_robot}: Path -> {path}")
            else:
                self.logs_label.setText("No valid path available.")

    def stop_robot(self):
        """Stop the selected robot."""
        if self.selected_robot is not None:
            # Get the selected robot
            robot = self.fleet_manager.robots[self.selected_robot]

            # Stop the robot's movement
            robot.timer.stop()
            robot.status = "stopped"

            # Release the vertex occupied by the robot
            self.traffic_manager.release_vertex(robot.current_vertex)

            self.logs_label.setText(f"Robot {self.selected_robot} has been stopped and released vertex {robot.current_vertex}.")
            print(f"Robot {self.selected_robot} has been stopped and released vertex {robot.current_vertex}.")
        else:
            self.logs_label.setText("Select a robot to stop.")

