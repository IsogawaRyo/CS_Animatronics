import genesis as gs
import os
import torch
from animatronics_env import AnimatronicsEnv

def verify_limits():
    gs.init(backend=gs.cuda)
    
    env_cfg = {
        "num_actions": 18,
        "joint_names": [
            "Revolute_3", "Revolute_4", "Revolute_10", "Revolute_11", "Revolute_14", "Revolute_15",
            "Revolute_18", "Revolute_19", "Revolute_22", "Revolute_23", "Revolute_36", "Revolute_37",
            "Revolute_40", "Revolute_42", "Revolute_44", "Revolute_46", "Revolute_47", "Revolute_50"
        ],
        "default_joint_angles": {n: 0.0 for n in [
            "Revolute_3", "Revolute_4", "Revolute_10", "Revolute_11", "Revolute_14", "Revolute_15",
            "Revolute_18", "Revolute_19", "Revolute_22", "Revolute_23", "Revolute_36", "Revolute_37",
            "Revolute_40", "Revolute_42", "Revolute_44", "Revolute_46", "Revolute_47", "Revolute_50"
        ]},
        "kp": 15.0,
        "kd": 1.0,
        "base_init_pos": [0.05, 0.0, 0.35],
        "base_init_quat": [0.985, 0.174, 0.0, 0.0],
        "episode_length_s": 20.0,
        "resampling_time_s": 4.0,
        "simulate_action_latency": True,
        "clip_actions": 100.0,
        "termination_if_roll_greater_than": 50,
        "termination_if_pitch_greater_than": 50,
    }
    
    obs_cfg = {
        "num_obs": 75,
        "obs_scales": {"lin_vel": 2.0, "ang_vel": 0.25, "dof_pos": 1.0, "dof_vel": 0.05},
    }
    
    reward_cfg = {
        "tracking_sigma": 0.25,
        "base_height_target": 0.3,
        "reward_scales": {"tracking_lin_vel": 3.0, "tracking_ang_vel": 0.5, "lin_vel_z": -0.5, "base_height": -0.5, "action_rate": -0.01, "similar_to_default": 0.0, "body_orientation": -2.0, "feet_orientation": -1.0, "alive": 1.0},
    }
    
    command_cfg = {
        "num_commands": 3,
        "lin_vel_x_range": [0.5, 0.5],
        "lin_vel_y_range": [0, 0],
        "ang_vel_range": [0, 0],
    }

    env = AnimatronicsEnv(num_envs=1, env_cfg=env_cfg, obs_cfg=obs_cfg, reward_cfg=reward_cfg, command_cfg=command_cfg, show_viewer=False)
    
    # Get indices for joints
    motors_dof_idx = env.motors_dof_idx
    
    # Check force range (effort limits)
    force_range = env.robot.get_dofs_force_range(motors_dof_idx)
    print("Force Range (Effort Limits):")
    print("Lower:", force_range[0])
    print("Upper:", force_range[1])
    
    expected_lower = -10.0
    expected_upper = 10.0
    
    success = True
    if not torch.allclose(force_range[0], torch.tensor([expected_lower] * len(motors_dof_idx), device=gs.device)):
        print("❌ Lower limits do not match!")
        success = False
    if not torch.allclose(force_range[1], torch.tensor([expected_upper] * len(motors_dof_idx), device=gs.device)):
        print("❌ Upper limits do not match!")
        success = False
        
    if success:
        print("✅ Joint effort limits verified successfully as 10Nm.")
    else:
        print("❌ Verification failed.")
        exit(1)

if __name__ == "__main__":
    verify_limits()
