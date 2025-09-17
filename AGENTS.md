# Repository Guidelines

## Project Structure & Module Organization
- `src/` holds all ROS 2 packages (e.g., `system_controller`, `motor_controller`, `controller_publisher`, `audio_player`). Each package follows the standard `package_name/package_name` Python layout.
- Shared assets sit at the workspace root: motion bags in `MotionFiles/`, audio clips in `AudioFiles/`, controller mappings in `ControllerMap.json`, and per-motor limits in `Motor_Limits.json`.
- Utility scripts such as `ros2_start.sh`, `setup_genesis_venv.sh`, and tests like `test_motor_states.py` live in the repository root. Keep new tooling alongside these helpers.

## Build, Test, and Development Commands
- `source /opt/ros/jazzy/setup.bash` loads the system ROS 2 environment; run it before any workspace commands.
- `colcon build --symlink-install` (from the repo root) builds every package; prefer `--symlink-install` during development for faster iteration.
- `source install/setup.bash` (after a successful build) overlays the workspace before running executables.
- `ros2 run system_controller system_controller` launches the main control node; pair it with `controller_publisher` and `motor_controller` in separate shells.
- `python test_motor_states.py` exercises the motor state service mock; add similar CLI entry points for new diagnostics.

## Coding Style & Naming Conventions
- Python sources use 4-space indentation, snake_case modules, and CapWords classes; match existing ROS node naming (`SystemController`, `motor_controller`).
- Keep functions under ~100 lines, favour small helpers, and add targeted inline comments where logic is non-obvious.
- Log through `self.get_logger()` with clear prefixes (`Recording START [...]`) so runtime traces stay readable.

## Testing Guidelines
- Provide runnable scripts or `pytest`-compatible modules for new features; name files `test_<feature>.py` and ensure they succeed with `python -m pytest` when applicable.
- For motion or hardware changes, document bench-test steps (e.g., required motors, expected torques) in PR notes or README snippets.

## Commit & Pull Request Guidelines
- Follow the existing concise, present-tense convention (`add hand recording toggle`, `fix motor limits`). Group related changes into a single commit when possible.
- Pull requests should describe the problem, the solution, and manual test evidence (commands run, observed behaviour, screenshots or logs). Link any tracking issues and flag hardware risks or calibration requirements.
- Request reviews from maintainers responsible for the affected packages and wait for CI or manual test acknowledgements before merging.
