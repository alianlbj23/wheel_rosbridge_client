# wheel_rosbridge_client
A simple Python-based client for controlling wheel speeds through a ROS (Robot Operating System) Bridge connection using keyboard input.

## Overview
This client allows you to control a robot's wheel speeds by sending commands to a ROS Bridge server. It uses a terminal-based UI for displaying the current wheel speeds and accepting keyboard input for movement control.

## Requirements
- Python 3
- `roslibpy` (1.8.0): For connecting to ROS Bridge
- `urwid` (2.5.16): For the terminal-based UI
- A running ROS Bridge server on the robot or target system

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/wheel_rosbridge_client.git
   cd wheel_rosbridge_client
   ```

2. Install dependencies using requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```

   Or install dependencies manually:
   ```bash
   pip install roslibpy==1.8.0 urwid==2.5.16
   ```

## Usage

Run the client by providing the IP address of the ROS Bridge server:

```bash
python wheel_test.py IP_ADDRESS
```

Example:
```bash
python wheel_test.py 192.168.1.100
```

You can also specify a custom port (default is 9090):
```bash
python wheel_test.py 192.168.1.100 -p 9091
```

## Controls

| Key | Action |
|-----|--------|
| W | Forward (all wheels forward) |
| S | Backward (all wheels backward) |
| A | Rotate left |
| D | Rotate right |
| E | Alternate rotation left |
| R | Alternate rotation right |
| Z | Stop (all wheels zero) |
| ESC | Exit the program |