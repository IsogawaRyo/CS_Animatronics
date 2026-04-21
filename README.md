# CS_Animatronics
ROS 2 workspace for building and testing a dinosaur animatronics stack. The system targets a Raspberry Pi 5 (8 GB, Ubuntu), uses DualSense as the primary controller, and drives Dynamixel XL430/XL330 servos plus auxiliary audio and IMU subsystems.

## Hardware & Software Requirements
- Raspberry Pi 5 or equivalent Linux host with access to up to **three** U2D2 adapters (`/dev/ttyUSB[0-2]`) for high-torque body segments.
- DualSense (or other joystick supported by `pygame`) connected over USB/Bluetooth.
- Dynamixel XL430/XL330 servos powered with per-motor limits defined in `Motor_Limits.json`.
- Optional BNO055 IMU array streamed from the `PICO/code.py` firmware via USB CDC.
- ROS 2 Jazzy: `source /opt/ros/jazzy/setup.bash` before building or running.
- Python 3.8+ with `rclpy`, `pygame`, `numpy`, `serial`, `pygame.mixer`, `rosbag2_py`, `dynamixel_sdk`, and GUI dependencies for Tk (`motion_editor`).
- Optional Genesis + PyTorch tooling for the `genesis_workspace/` environment (see `setup_genesis_venv.sh`).

## Repository Layout
The repository has been restructured into two main top-level directories based on hardware domains:
- **`DINO`**: The main animatronics robot running ROS 2 (upper body).
- **`CAR`**: The separate mobile cart base running independently.

### Important Structure (DINO)
Inside `DINO/` you will find:
- **`src`**: Core ROS 2 packages (`system_controller`, `motor_controller`, etc.)
- **`PICO`**: Submodule/scripts for Raspberry Pi Pico integrations.
- **`ros2_start.sh`**: Centralized startup script that launches all essential ROS 2 nodes.
- **Configurations**: `Motor_Limits.json`, `ControllerMap.json`, `AudioMap.json`
- **Assets**: `AudioFiles/`, `MotionFiles/`, `RecordedLog/`

| Path (Inside DINO/) | Purpose |
| --- | --- |
| `src/` | All ROS 2 packages following the `package_name/package_name` layout. |
| `AudioFiles/`, `AudioMap.json` | Dinosaur audio clips plus ID → filename map used by `audio_player`. |
| `MotionFiles/`, `RecordedLog/` | Hand-recorded motor state bags and archived logs used by `system_controller` & `motion_editor`. |
| `ControllerMap.json` | User-assignable DualSense button → motion mapping. |
| `Motor_Limits.json` | Per-motor initial position, soft limits, acceleration, and velocity caps consumed by controllers. |
| `PICO/` | CircuitPython firmware for the BNO055 IMU multiplexer streaming packets consumed by `imu_receiver`. |
| `genesis_workspace/`, `simple_model.urdf` | Genesis robotics practice environment, training, and evaluation scripts. |
| `ros2_start.sh`, `develop_environment.sh`, `setup_genesis_venv.sh` | Helper scripts for spawning ROS nodes, configuring Git/SSH on new devices, and provisioning the Genesis virtual environment. |
| `test_motor_states.py`, `test_IMU.py` | Standalone diagnostics for the `get_motor_states` service and the IMU visualization pipeline. |

## Setup & Build
1. Source ROS 2: `source /opt/ros/jazzy/setup.bash`.
2. From the repository root run:
   ```bash
   colcon build --symlink-install
   source install/setup.bash
   ```
3. Optional: run `setup_genesis_venv.sh` to create a `genesis_env` virtual environment with PyTorch, Taichi, Genesis, and helper activation scripts (`activate_genesis.sh`, `deactivate_genesis.sh`).
4. Optional: `develop_environment.sh` installs Git, sets the repo identity, and provisions SSH keys on a fresh Ubuntu install.

> **Note:** `ros2_start.sh` deletes `build/ log/ install/` unconditionally, rebuilds, adds the current user to `dialout`, and then spawns every core node in separate `gnome-terminal` windows. Use it only when you expect a clean build and have physical access to confirm the new terminals; otherwise launch nodes manually or via `ros2 launch`.

## Running the Core Nodes
### Launch file
Use the bundled bringup launch to start the main stack at once:
```bash
ros2 launch system_controller animatronics_bringup.launch.py \
  start_motion_editor:=false \
  start_imu_receiver:=false
```
Set `start_motion_editor`/`start_imu_receiver` to `true` when a display or IMU hardware is available. Other launch arguments (`start_controller_publisher`, `start_system_controller`, `start_motor_controller`, `start_audio_player`) default to `true` but can be toggled per run.

### Manual nodes
Source `install/setup.bash` in every shell, then run:
- `ros2 run controller_publisher controller_publisher` — publishes DualSense input to `controller_input`.
- `ros2 run system_controller system_controller` — consumes joystick input, computes motor commands, triggers audio, and handles motion recording/playback.
- `ros2 run motor_controller motor_controller` — bridges `IdAngle` commands to the Dynamixel buses and exposes the `get_motor_states`/`set_torque` services.
- `ros2 run audio_player audio_player` — plays dinosaur sounds when `system_controller` publishes `play_audio_id`/`play_audio_name`.
- `ros2 run motion_editor motion_editor` — resizable Tk GUI for tweaking recorded motions, mapping controller buttons, and authoring timeline audio cues.
- `ros2 run imu_receiver imu_receiver_node` — converts Pico IMU packets to standard `sensor_msgs/Imu` topics (`imu0`, `imu1`, `imu2`).
- `ros2 run system_monitor system_monitor` — full-screen dashboard with motor/IMU tabs, live current totals for PORT0/1/2, motion assignment shortcuts, and an embedded Motion Editor instance.

## ROS 2 Packages
### `system_controller`
Subscribes to `sensor_msgs/Joy` on `controller_input`, enforces `Motor_Limits.json`, and publishes `motor_commands/IdAngle` messages to `IdAngle`. It provides:
- Mode switching between manual control, assist/test, and torque-off hand recording.
- Motion selection/assignment UI driven by DualSense buttons with defaults defined in `ControllerMap.json`.
- Audio triggers: publishes `std_msgs/Int32` IDs to `play_audio_id`, consumes per-keypose audio metadata from Motion Editor, and auto-roar/breathe cues based on jaw position.
- Motion recording/playback using rosbag2 (`MotionFiles/`) with carry-forward interpolation so partially-specified joints stay smooth.
- Service clients for `get_motor_states` and `set_torque`, plus background sampling timers for recorded motions.

### `motor_controller`
Bridges `IdAngle` to Dynamixel commands via `dynamixel_sdk`, scanning `/dev/ttyUSB[0-2]` (three U2D2 buses) for XL430/XL330 IDs. Features include:
- Live enforcement of `Motor_Limits.json` per motor, including simulation fallback when ports are missing.
- Cached motor-state reporting to reduce serial load.
- `get_motor_states` service returning position, temperature, torque/load, and aggregated current metrics per port and globally.
- `set_torque` service for enabling/disabling torque per ID.

### `controller_publisher`
Uses `pygame` to keep a DualSense connection alive, publishing `sensor_msgs/Joy` packets at 20 Hz. Handles automatic reconnection, axis/button enumeration, and logging when a controller is not detected.

### `audio_player`
Initializes `pygame.mixer`, loads `AudioFiles/` with mappings from `AudioMap.json`, and exposes:
- `play_audio_id` (`std_msgs/Int32`) and `play_audio_name` (`std_msgs/String`) subscribers for playback.
- `stop_audio` subscriber to halt current sounds.
- `audio_status` publisher reporting `PLAYING/FINISHED/ERROR` states.
Includes a default dinosaur sound map and ensures directories exist.

### `motion_editor`
Tkinter GUI backed by a `ROSManager` node that publishes `IdAngle` commands and calls `get_motor_states`. Provides:
- File selection/loading of rosbag motions stored in `MotionFiles/` with resizable panes.
- Per-keypose editing, controller button assignment (updates `ControllerMap.json`), and timeline authoring of audio cues that now preview locally.
- Visual monitors for per-motor position, torque, temperature, error status, and total current across PORT0/PORT1/PORT2.

### `system_monitor`
Tkinter dashboard that opens full-screen, embeds a live Motion Editor tab, plots motor/IMU telemetry, and exposes service buttons for rebooting motors or reconnecting U2D2 ports. Shows controller connectivity, per-port current totals, audio controls, and IMU pose views.

### `motor_commands`
Pure interface package defining shared message/service types:
- `msg/IdAngle.msg`
- `srv/GetMotorStates.srv`
- `srv/SetTorque.srv`

### `imu_receiver`
Consumes the Pico serial stream defined in `PICO/code.py`, parses BNO055 quaternion/accel/gyro data, and publishes three `sensor_msgs/Imu` topics. Converts Euler angles to quaternions, validates `NaN`s, and throttles with a 50 Hz timer.

### Additional Content
- `audio_player/test`, `motor_controller/test`, and other package-specific tests live under their respective `test/` directories.
- `src/DeepLabCut/` holds DeepLabCut projects (`Animatronics-Ryo-2024-12-17`, `animatronics-ryo-2024-12-18`), captured videos, and `DeepLabCutAnalysis.py` bootstrap code for creating new DLC projects.
- `genesis_workspace/` contains reinforcement-learning practice scripts (`go2_env.py`, `go2_train.py`, `go2_eval.py`, `practice_0x.py`) that rely on Genesis, PyTorch, and the provided `simple_model.urdf`.

## Messages & Services
- `motor_commands/msg/IdAngle`: `uint8[] ids`, `int32[] angles`.
- `motor_commands/srv/GetMotorStates`: request `ids`; response includes `ids`, `positions`, `temperatures`, `torques`, `error_status`, and aggregate current stats.
- `motor_commands/srv/SetTorque`: request `ids` + `enable`; response `success` and `message`.

## Assets & Configuration
- `MotionFiles/`: rosbag2 recordings produced by torque-off hand-guided sessions; accessible through `system_controller` and `motion_editor`.
- `RecordedLog/`: archival motion logs kept for regression analysis.
- `ControllerMap.json`: maps button indices (Cross, Circle, etc.) to motion files or actions; `system_controller` exposes in-controller assignment UI.
- `Motor_Limits.json`: stringified ints describing each servo’s initial position, min/max bounds, acceleration, and velocity. Controllers convert to ints on load and enforce before sending.
- `AudioFiles/` & `AudioMap.json`: lookup library for roars, growls, hisses, etc. Extend `AudioMap.json` to introduce new IDs.
- `PICO/code.py`: CircuitPython script multiplexing three BNO055 sensors over a TCA9548A, packaging Euler/accel/gyro triples, and sending them at ~50 Hz over USB CDC.
- `simple_model.urdf`: simplified robot description used by the Genesis environment and can be referenced by other simulators.

## Diagnostics & Testing
- `python test_motor_states.py`: exercises the `get_motor_states` service, prints per-motor telemetry, and highlights suspicious readings.
- `python test_IMU.py`: standalone IMU packet visualizer that draws cubes representing the three IMU orientations using Matplotlib.
- Package-level tests under `src/*/test/` can be run with `colcon test` once dependencies are satisfied.
- For joystick or audio issues, run the corresponding nodes (`controller_publisher`, `audio_player`) individually and inspect their `self.get_logger()` output.

## Optional Tooling
- `ros2_start.sh`: end-to-end launcher that cleans previous builds (`build/`, `log/`, `install/`), rebuilds, and starts all primary nodes in separate terminals. Requires a graphical session due to `gnome-terminal`.
- `setup_genesis_venv.sh`: creates `genesis_env`, installs CUDA-capable PyTorch when available, Taichi, Genesis dependencies, clones the Genesis repo if absent, and generates activation/deactivation scripts plus `genesis_requirements_installed.txt`.
- `develop_environment.sh`: bootstrap Git + SSH credentials on a fresh Ubuntu install (`apt install git`, configure user/email, generate keys).
- `genesis_workspace/go2_train.py`, `go2_eval.py`, `go2_env.py`: reinforcement-learning workflow for the simple URDF, leveraging Genesis for multi-environment simulation.
- `test_IMU.py` + `PICO/code.py`: use together for validating IMU packet integrity before integrating with ROS.

With these components in place, you can record hand-guided motions, map them to controller inputs, stream IMU telemetry, and use Genesis/DeepLabCut tooling for offline experimentation—all from this single repository.
