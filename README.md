# Goat-Robotics-Hackathon

## Fleet Management System
### The system is designed to efficiently manage robot fleets, including navigation, task assignment, and UI functionalities. It provides real-time monitoring, efficient task scheduling, and a user-friendly graphical interface.

## Tech Stack
### Programming Language: Python 3.10+
### Frameworks & Libraries:
### PyQt5 (GUI development)
### JSON (Data storage & navigation graph)
### Logging (For debugging & tracking errors)
### NetworkX (Graph-based pathfinding)
### Threading (Asynchronous task execution)

## Solution Approach
### Navigation System
#### The navigation graph is structured as a JSON file containing nodes and edges representing robot pathways.
### Fleet Management
#### Manages multiple robots with real-time task allocation.
#### Ensures smooth coordination and conflict resolution.
### User Interface
#### PyQt5-based GUI with live robot status updates.
#### Visual representation of the fleet's movement and task progress.
### Logging & Debugging
#### Logs critical events such as errors, navigation updates, and task execution.


## Installation & Setup
### Prerequisites
#### Ensure you have Python 3.10+ installed and the required dependencies.

### Clone the Repository
```
git clone https://github.com/your-repo/Goat-Robotics-Hackathon.git
cd Goat-Robotics-Hackathon
```
### Install dependencies
```
pip install -r requirements.txt
```
### Run the Application
```
python src/main.py
```



