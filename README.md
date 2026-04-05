Dual Elevator Parallel LOOK Algorithm Visual Simulator
A graphical visualization program for dual parallel elevators developed with Python's built-in tkinter library. It perfectly implements the classic elevator LOOK scheduling algorithm, supports intelligent call allocation, independent elevator operation, and real-time animation display, intuitively simulating the elevator scheduling logic in real buildings.

📋 Project Overview
Programming Language: Python 3.x
GUI Library: Built-in tkinter (no third-party dependencies required)
Core Algorithm: Elevator LOOK Scheduling Algorithm
Core Features: Dual independent elevators + intelligent dispatching + elegant graphical interface

✨ Key Features
Dual Independent Elevators
Two elevators (Elevator 1: Blue, Elevator 2: Green) run independently with the LOOK algorithm, no interference with each other.
LOOK Algorithm Implementation
Prioritize requests in the current running direction; automatically reverse direction at the endpoint (standard real-world elevator logic).
Intelligent Dispatching System
Automatically assign floor calls to the optimal elevator (prioritize same-direction + closest distance) for maximum efficiency.
Graphical Visualization
Intuitive elevator shaft, smooth moving animation, and highlighted call buttons.
Real-time Status Monitoring
Real-time display of current floor, running direction, and pending request queue at the bottom status bar.

🛠️ System Requirements
Python 3.6 or later
No extra libraries needed (tkinter is a Python standard built-in library)

🚀 Quick Start
Save the code as double_elevator.py
Open the terminal/command prompt and navigate to the project directory
Run the program:

python double_elevator.py

📖 User Guide
Interface Layout
Left: Dual elevator shaft visualization (Blue: Elevator 1, Green: Elevator 2)
Right: Floor call panel (1-10 Floors, Up ▲ / Down ▼ buttons)
Bottom: Real-time status bar for both elevators
Operation Steps
The program initializes automatically; both elevators stop at the 1st floor by default.
Click the Up ▲ or Down ▼ button on any floor to send a call request.
The system dispatches the optimal elevator to respond, with real-time animation during movement.
Buttons reset automatically when the elevator arrives, and the request queue updates synchronously.
Recommended Test Scenarios
Click 10F Up → Elevator 1 moves up to serve
Immediately click 2F Down → Elevator 2 moves down to serve
Observe the parallel operation of two elevators
Test same-direction/opposite-direction calls to verify the LOOK algorithm
🧠 Core Algorithm Principles
1. LOOK Algorithm
The elevator serves all requests in the current running direction sequentially.
Reverse direction immediately when no pending requests exist in the current direction (no empty trips to the top/bottom floor).
Higher efficiency than the SCAN algorithm, matching real elevator usage.
2. Intelligent Dispatching Rules
Prioritize elevators traveling in the same direction as the call.
Select the closest elevator if no same-direction elevator is available.
Minimize passenger waiting time and optimize operating efficiency.

📂 Code Structure
ElevatorLogic Class
Core elevator logic, responsible for:
Maintaining current floor, direction, and request queue
Implementing the LOOK scheduling logic
Controlling elevator movement, stopping, and waiting
DoubleElevatorApp Class
Graphical user interface, responsible for:
Drawing elevator shafts, cars, and floor buttons
Handling user call interactions
Refreshing elevator position and status in real time

⚠️ Compatibility
Fixed compatibility issues for Python 3.12+:
Replaced ttk.Label (unsupported height parameter) with native tk.Label
Fully compatible with all Python 3.x versions

📝 License
This project is open-source and free for learning, teaching, and secondary development.
