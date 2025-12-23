import argparse
import os
import pickle
import shutil
from importlib import metadata

os.environ["SETUPTOOLS_USE_DISTUTILS"] = "stdlib"

try:
    try:
        if metadata.version("rsl-rl"):
            raise ImportError
    except metadata.PackageNotFoundError:
        if metadata.version("rsl-rl-lib") != "2.2.4":
            raise ImportError
except (metadata.PackageNotFoundError, ImportError) as e:
    raise ImportError("Please uninstall 'rsl_rl' and install 'rsl-rl-lib==2.2.4'.") from e
from rsl_rl.runners import OnPolicyRunner

import genesis as gs

from animatronics_env import AnimatronicsEnv


def get_train_cfg(exp_name, max_iterations):
    train_cfg_dict = {
        "algorithm": {
            "class_name": "PPO",
            "clip_param": 0.2,
            "desired_kl": 0.01,
            "entropy_coef": 0.01,
            "gamma": 0.99,
            "lam": 0.95,
            "learning_rate": 0.001,
            "max_grad_norm": 1.0,
            "num_learning_epochs": 5,
            "num_mini_batches": 4,
            "schedule": "adaptive",
            "use_clipped_value_loss": True,
            "value_loss_coef": 1.0,
        },
        "init_member_classes": {},
        "policy": {
            "activation": "elu",
            "actor_hidden_dims": [512, 256, 128],
            "critic_hidden_dims": [512, 256, 128],
            "init_noise_std": 1.0,
            "class_name": "ActorCritic",
        },
        "runner": {
            "checkpoint": -1,
            "experiment_name": exp_name,
            "load_run": -1,
            "log_interval": 1,
            "max_iterations": max_iterations,
            "record_interval": -1,
            "resume": False,
            "resume_path": None,
            "run_name": "",
        },
        "runner_class_name": "OnPolicyRunner",
        "num_steps_per_env": 24,
        "save_interval": 100,
        "empirical_normalization": None,
        "seed": 1,
    }

    return train_cfg_dict


def get_cfgs():
    env_cfg = {
        "num_actions": 18,
        # joint/link names
        "default_joint_angles": {  # [rad]
            "Revolute_3": 0.0,
            "Revolute_4": 0.0,
            "Revolute_10": 0.0,
            "Revolute_11": 0.0,
            "Revolute_14": 0.0,
            "Revolute_15": 0.0,
            "Revolute_18": 0.0,
            "Revolute_19": 0.0,
            "Revolute_22": 0.0,
            "Revolute_23": 0.0,
            "Revolute_36": 0.0,
            "Revolute_37": 0.0,
            "Revolute_40": 0.0,
            "Revolute_42": 0.0,
            "Revolute_44": 0.0,
            "Revolute_46": 0.0,
            "Revolute_47": 0.0,
            "Revolute_50": 0.0,
        },
        "joint_names" : [
            "Revolute_3",
            "Revolute_4",
            "Revolute_10",
            "Revolute_11",
            "Revolute_14",
            "Revolute_15",
            "Revolute_18",
            "Revolute_19",
            "Revolute_22",
            "Revolute_23",
            "Revolute_36",
            "Revolute_37",
            "Revolute_40",
            "Revolute_42",
            "Revolute_44",
            "Revolute_46",
            "Revolute_47",
            "Revolute_50",
        ],
        "kp": 15.0,
        "kd": 1.0,
        # termination
        "termination_if_roll_greater_than": 50,  # degree
        "termination_if_pitch_greater_than": 50,
        # base pose
        # base pose
        "base_init_pos": [0.0, 0.05, 0.35], # Shifted 0.05 forward in Y
        "base_init_quat": [0.991, 0.131, 0.0, 0.0], # Approx 15 degrees forward lean
        "episode_length_s": 20.0,
        "resampling_time_s": 4.0,
        "simulate_action_latency": True,
        "clip_actions": 100.0,
    }
    obs_cfg = {
        "num_obs": 79, # 3+3+3 + 18 + 18 + 18 + 16 (IMU) = 79
        "obs_scales": {
            "lin_vel": 2.0,
            "ang_vel": 0.25,
            "dof_pos": 1.0,
            "dof_vel": 0.05,
        },
    }
    reward_cfg = {
        "tracking_sigma": 0.25,
        "base_height_target": 0.3, # Target height slightly lower than initial to allow for stance
        "feet_height_target": 0.0,
        "reward_scales": {
            "tracking_lin_vel": 3.0,
            "tracking_ang_vel": 0.5,
            "lin_vel_z": -0.5,
            "base_height": -0.5,
            "action_rate": -0.01,
            "similar_to_default": 0.0,
            "body_orientation": -10.0, # Increased penalty for non-horizontal torso
            "head_height": -5.0,        # Penalty for head touching ground
            "feet_orientation": -1.0,
            "alive": 1.0,
        },
    }
    command_cfg = {
        "num_commands": 3,
        "lin_vel_x_range": [0.5, 0.5],
        "lin_vel_y_range": [0, 0],
        "ang_vel_range": [0, 0],
    }

    return env_cfg, obs_cfg, reward_cfg, command_cfg


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--exp_name", type=str, default="animatronics-walking")
    parser.add_argument("-B", "--num_envs", type=int, default=4096)
    parser.add_argument("--max_iterations", type=int, default=1000)
    args = parser.parse_args()

    gs.init(logging_level="warning")

    log_dir = f"logs/{args.exp_name}"
    env_cfg, obs_cfg, reward_cfg, command_cfg = get_cfgs()
    train_cfg = get_train_cfg(args.exp_name, args.max_iterations)

    if os.path.exists(log_dir):
        shutil.rmtree(log_dir)
    os.makedirs(log_dir, exist_ok=True)

    pickle.dump(
        [env_cfg, obs_cfg, reward_cfg, command_cfg, train_cfg],
        open(f"{log_dir}/cfgs.pkl", "wb"),
    )

    env = AnimatronicsEnv(
        num_envs=args.num_envs, env_cfg=env_cfg, obs_cfg=obs_cfg, reward_cfg=reward_cfg, command_cfg=command_cfg
    )

    runner = OnPolicyRunner(env, train_cfg, log_dir, device=gs.device)

    runner.learn(num_learning_iterations=args.max_iterations, init_at_random_ep_len=True)


if __name__ == "__main__":
    main()
