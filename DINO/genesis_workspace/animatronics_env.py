import torch
import numpy as np
import math
import genesis as gs
from genesis.utils.geom import quat_to_xyz, transform_by_quat, inv_quat, transform_quat_by_quat
import os

def gs_rand_float(lower, upper, shape, device):
    return (upper - lower) * torch.rand(size=shape, device=device) + lower


class AnimatronicsEnv:
    def __init__(self, num_envs, env_cfg, obs_cfg, reward_cfg, command_cfg, show_viewer=True, device="cuda"):
        self.num_envs = num_envs
        self.num_obs = obs_cfg["num_obs"]
        self.num_privileged_obs = None
        self.num_actions = env_cfg["num_actions"]
        self.num_commands = command_cfg["num_commands"]
        self.device = gs.device

        self.simulate_action_latency = True  # there is a 1 step latency on real robot
        self.dt = 0.02  # control frequency on real robot is 50hz
        self.max_episode_length = math.ceil(env_cfg["episode_length_s"] / self.dt)

        self.env_cfg = env_cfg
        self.obs_cfg = obs_cfg
        self.reward_cfg = reward_cfg
        self.command_cfg = command_cfg

        self.obs_scales = obs_cfg["obs_scales"]
        self.reward_scales = reward_cfg["reward_scales"]

        # create scene
        self.scene = gs.Scene(
            sim_options=gs.options.SimOptions(dt=self.dt, substeps=30),
            viewer_options=gs.options.ViewerOptions(
                max_FPS=int(0.5 / self.dt),
                camera_pos=(2.0, 0.0, 2.5),
                camera_lookat=(0.0, 0.0, 0.5),
                camera_fov=40,
            ),
            vis_options=gs.options.VisOptions(rendered_envs_idx=list(range(1))),
            rigid_options=gs.options.RigidOptions(
                dt=self.dt,
                constraint_solver=gs.constraint_solver.Newton,
                enable_collision=True,
                enable_self_collision=True,
                enable_joint_limit=True,
            ),
            show_viewer=show_viewer,
        )

        # add plain
        self.scene.add_entity(gs.morphs.URDF(file="urdf/plane/plane.urdf", fixed=True))

        # add robot
        self.base_init_pos = torch.tensor(self.env_cfg["base_init_pos"], device=gs.device)
        self.base_init_quat = torch.tensor(self.env_cfg["base_init_quat"], device=gs.device)
        self.inv_base_init_quat = inv_quat(self.base_init_quat)
        
        # Path to the URDF file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        urdf_path = os.path.join(script_dir, "../animatronics_urdf_description/animatronics_urdf_description_standalone.urdf")

        self.robot = self.scene.add_entity(
            gs.morphs.URDF(
                file=urdf_path,
                pos=self.base_init_pos.cpu().numpy(),
                quat=self.base_init_quat.cpu().numpy(),
                merge_fixed_links=True,
                batch_fixed_verts=True,
            ),
        )

        # Set high friction for feet to prevent slipping (use merged group names instead)
        for name in ["XM,H,D-540.N101.I101_v5_4", "XM,H,D-540.N101.I101_v5_8"]:
            self.robot.get_link(name).set_friction(1.0)

        # build
        self.scene.build(n_envs=num_envs)

        # names to indices
        print("AVAILABLE JOINTS:", [j.name for j in self.robot.joints])
        self.motors_dof_idx = [self.robot.get_joint(name).dof_start for name in self.env_cfg["joint_names"]]

        # IMU links (using proxies since fixed links are merged)
        # imu_link 1 -> LegEnd_v9_1
        # imu_link 2 -> LegEnd_v9_2
        # imu_link 3 -> base
        self.imu_links = [
            self.robot.get_link("XM,H,D-540.N101.I101_v5_4"),
            self.robot.get_link("XM,H,D-540.N101.I101_v5_8"),
            self.robot.get_link("base"),
            self.robot.get_link("Head_Joint_v6_1"),
        ]

        # PD control parameters
        self.robot.set_dofs_kp([self.env_cfg["kp"]] * self.num_actions, self.motors_dof_idx)
        self.robot.set_dofs_kv([self.env_cfg["kd"]] * self.num_actions, self.motors_dof_idx)
        
        # Set joint force range to 10Nm
        self.robot.set_dofs_force_range(
            lower=[-10.0] * self.num_actions,
            upper=[10.0] * self.num_actions,
            dofs_idx_local=self.motors_dof_idx
        )

        # prepare reward functions and multiply reward scales by dt
        self.reward_functions, self.episode_sums = dict(), dict()
        for name in self.reward_scales.keys():
            self.reward_scales[name] *= self.dt
            self.reward_functions[name] = getattr(self, "_reward_" + name)
            self.episode_sums[name] = torch.zeros((self.num_envs,), device=gs.device, dtype=gs.tc_float)

        # initialize buffers
        self.base_lin_vel = torch.zeros((self.num_envs, 3), device=gs.device, dtype=gs.tc_float)
        self.base_ang_vel = torch.zeros((self.num_envs, 3), device=gs.device, dtype=gs.tc_float)
        self.projected_gravity = torch.zeros((self.num_envs, 3), device=gs.device, dtype=gs.tc_float)
        self.global_gravity = torch.tensor([0.0, 0.0, -1.0], device=gs.device, dtype=gs.tc_float).repeat(
            self.num_envs, 1
        )
        self.obs_buf = torch.zeros((self.num_envs, self.num_obs), device=gs.device, dtype=gs.tc_float)
        self.rew_buf = torch.zeros((self.num_envs,), device=gs.device, dtype=gs.tc_float)
        self.reset_buf = torch.ones((self.num_envs,), device=gs.device, dtype=gs.tc_int)
        self.episode_length_buf = torch.zeros((self.num_envs,), device=gs.device, dtype=gs.tc_int)
        self.commands = torch.zeros((self.num_envs, self.num_commands), device=gs.device, dtype=gs.tc_float)
        self.commands_scale = torch.tensor(
            [self.obs_scales["lin_vel"], self.obs_scales["lin_vel"], self.obs_scales["ang_vel"]],
            device=gs.device,
            dtype=gs.tc_float,
        )
        self.actions = torch.zeros((self.num_envs, self.num_actions), device=gs.device, dtype=gs.tc_float)
        self.last_actions = torch.zeros_like(self.actions)
        self.dof_pos = torch.zeros_like(self.actions)
        self.dof_vel = torch.zeros_like(self.actions)
        self.last_dof_vel = torch.zeros_like(self.actions)
        self.base_pos = torch.zeros((self.num_envs, 3), device=gs.device, dtype=gs.tc_float)
        self.base_quat = torch.zeros((self.num_envs, 4), device=gs.device, dtype=gs.tc_float)
        self.default_dof_pos = torch.tensor(
            [self.env_cfg["default_joint_angles"][name] for name in self.env_cfg["joint_names"]],
            device=gs.device,
            dtype=gs.tc_float,
        )
        self.extras = dict()  # extra information for logging
        self.extras["observations"] = dict()

        # Initialize imu_quats to avoid AttributeError before first step
        # 4 links: LegEnd1, LegEnd2, Base, Head
        self.imu_quats = [torch.tensor([1.0, 0.0, 0.0, 0.0], device=gs.device).repeat(self.num_envs, 1) for _ in range(4)]
        self.imu_pos = [torch.zeros((self.num_envs, 3), device=gs.device) for _ in range(4)]

        # Initialize action scales based on URDF limits
        dof_limits = self.robot.get_dofs_limit(self.motors_dof_idx)
        lower_limits = dof_limits[0]
        upper_limits = dof_limits[1]
        
        # Calculate scale to cover the range from default (0) to limits
        # scale = max(abs(lower), abs(upper))
        # Handle continuous joints (inf) by setting a default scale (e.g., 1.0)
        self.action_scales = torch.max(torch.abs(lower_limits), torch.abs(upper_limits))
        self.action_scales[torch.isinf(self.action_scales)] = 1.0 # Default for continuous joints
        
        print(f"Action scales: {self.action_scales}")

    def _resample_commands(self, envs_idx):
        self.commands[envs_idx, 0] = gs_rand_float(*self.command_cfg["lin_vel_x_range"], (len(envs_idx),), gs.device)
        self.commands[envs_idx, 1] = gs_rand_float(*self.command_cfg["lin_vel_y_range"], (len(envs_idx),), gs.device)
        self.commands[envs_idx, 2] = gs_rand_float(*self.command_cfg["ang_vel_range"], (len(envs_idx),), gs.device)

    def step(self, actions):
        self.actions = torch.clip(actions, -self.env_cfg["clip_actions"], self.env_cfg["clip_actions"])
        exec_actions = self.last_actions if self.simulate_action_latency else self.actions
        
        # Use per-joint action scales
        target_dof_pos = exec_actions * self.action_scales + self.default_dof_pos
        
        self.robot.control_dofs_position(target_dof_pos, self.motors_dof_idx)
        self.scene.step()

        # update buffers
        self.episode_length_buf += 1
        self.base_pos[:] = self.robot.get_pos()
        self.base_quat[:] = self.robot.get_quat()
        rel_quat = transform_quat_by_quat(self.base_quat, self.inv_base_init_quat)
        self.base_euler = quat_to_xyz(
            rel_quat,
            rpy=True,
            degrees=False,
        )
        inv_base_quat = inv_quat(self.base_quat)
        self.base_lin_vel[:] = transform_by_quat(self.robot.get_vel(), inv_base_quat)
        self.base_ang_vel[:] = transform_by_quat(self.robot.get_ang(), inv_base_quat)
        self.projected_gravity = transform_by_quat(self.global_gravity, inv_base_quat)
        self.dof_pos[:] = self.robot.get_dofs_position(self.motors_dof_idx)
        self.dof_vel[:] = self.robot.get_dofs_velocity(self.motors_dof_idx)

        # resample commands
        envs_idx = (
            (self.episode_length_buf % int(self.env_cfg["resampling_time_s"] / self.dt) == 0)
            .nonzero(as_tuple=False)
            .reshape((-1,))
        )
        self._resample_commands(envs_idx)

        # check termination and reset
        self.reset_buf = self.episode_length_buf > self.max_episode_length
        # Swapped roll/pitch indices to match Robot Y-forward orientation
        # Physical Pitch (lean forward/back) is rotation around X (base_euler[:, 0])
        self.reset_buf |= torch.abs(self.base_euler[:, 0]) > self.env_cfg["termination_if_pitch_greater_than"]
        # Physical Roll (roll left/right) is rotation around Y (base_euler[:, 1])
        self.reset_buf |= torch.abs(self.base_euler[:, 1]) > self.env_cfg["termination_if_roll_greater_than"]

        time_out_idx = (self.episode_length_buf > self.max_episode_length).nonzero(as_tuple=False).reshape((-1,))
        self.extras["time_outs"] = torch.zeros_like(self.reset_buf, device=gs.device, dtype=gs.tc_float)
        self.extras["time_outs"][time_out_idx] = 1.0

        self.reset_idx(self.reset_buf.nonzero(as_tuple=False).reshape((-1,)))

        # compute reward
        self.rew_buf[:] = 0.0
        for name, reward_func in self.reward_functions.items():
            rew = reward_func() * self.reward_scales[name]
            self.rew_buf += rew
            self.episode_sums[name] += rew

        # compute observations
        imu_quats = []
        imu_pos = []
        for link in self.imu_links:
            imu_quats.append(link.get_quat())
            imu_pos.append(link.get_pos())
        
        imu_obs = torch.cat(imu_quats, axis=-1) # (num_envs, 16)
        self.imu_quats = imu_quats 
        self.imu_pos = imu_pos

        # Remap observations to Agent Frame (X=Forward=Robot_Y, Y=Lateral(Left)=Robot_-X)
        remapped_ang_vel = torch.stack([
            self.base_ang_vel[:, 1],  # Agent Roll (around X) = Robot Roll around Y
            -self.base_ang_vel[:, 0], # Agent Pitch (around Y) = Robot Pitch around -X
            self.base_ang_vel[:, 2]   # Agent Yaw (around Z) = Robot Yaw around Z
        ], dim=-1)

        remapped_projected_gravity = torch.stack([
            self.projected_gravity[:, 1],  # Agent Forward = Robot Forward (Y)
            -self.projected_gravity[:, 0], # Agent Lateral = Robot Left (-X)
            self.projected_gravity[:, 2]   # Agent Vertical = Robot Up (Z)
        ], dim=-1)

        self.obs_buf = torch.cat(
            [
                remapped_ang_vel * self.obs_scales["ang_vel"],  # 3
                remapped_projected_gravity,  # 3
                self.commands * self.commands_scale,  # 3
                (self.dof_pos - self.default_dof_pos) * self.obs_scales["dof_pos"],  # num_actions
                self.dof_vel * self.obs_scales["dof_vel"],  # num_actions
                self.actions,  # num_actions
                imu_obs, # 12
            ],
            axis=-1,
        )

        self.last_actions[:] = self.actions[:]
        self.last_dof_vel[:] = self.dof_vel[:]

        self.extras["observations"]["critic"] = self.obs_buf

        return self.obs_buf, self.rew_buf, self.reset_buf, self.extras

    def get_observations(self):
        self.extras["observations"]["critic"] = self.obs_buf
        return self.obs_buf, self.extras

    def get_privileged_observations(self):
        return None

    def reset_idx(self, envs_idx):
        if len(envs_idx) == 0:
            return

        # reset dofs
        self.dof_pos[envs_idx] = self.default_dof_pos
        self.dof_vel[envs_idx] = 0.0
        self.robot.set_dofs_position(
            position=self.dof_pos[envs_idx],
            dofs_idx_local=self.motors_dof_idx,
            zero_velocity=False,
            envs_idx=envs_idx,
        )
        self.robot.set_dofs_velocity(
            velocity=torch.zeros_like(self.dof_pos[envs_idx]),
            dofs_idx_local=self.motors_dof_idx,
            envs_idx=envs_idx,
        )

        # reset base
        self.base_pos[envs_idx] = self.base_init_pos
        self.base_quat[envs_idx] = self.base_init_quat.reshape(1, -1)
        self.robot.set_pos(self.base_pos[envs_idx], zero_velocity=False, envs_idx=envs_idx)
        self.robot.set_quat(self.base_quat[envs_idx], zero_velocity=False, envs_idx=envs_idx)
        self.base_lin_vel[envs_idx] = 0
        self.base_ang_vel[envs_idx] = 0
        # self.robot.zero_all_dofs_velocity(envs_idx)

        # reset buffers
        self.last_actions[envs_idx] = 0.0
        self.last_dof_vel[envs_idx] = 0.0
        self.episode_length_buf[envs_idx] = 0
        self.reset_buf[envs_idx] = True

        # fill extras
        self.extras["episode"] = {}
        for key in self.episode_sums.keys():
            self.extras["episode"]["rew_" + key] = (
                torch.mean(self.episode_sums[key][envs_idx]).item() / self.env_cfg["episode_length_s"]
            )
            self.episode_sums[key][envs_idx] = 0.0

        self._resample_commands(envs_idx)

    def reset(self):
        self.reset_buf[:] = True
        self.reset_idx(torch.arange(self.num_envs, device=gs.device))
        return self.obs_buf, None

    # ------------ reward functions----------------
    def _reward_tracking_lin_vel(self):
        # Tracking of linear velocity commands (remapped to Agent Frame)
        # Agent Forward (X) command matches Robot Physical Y velocity
        # Agent Lateral (Y) command matches Robot Physical -X velocity
        robot_vel_remapped = torch.stack([self.base_lin_vel[:, 1], -self.base_lin_vel[:, 0]], dim=-1)
        lin_vel_error = torch.sum(torch.square(self.commands[:, :2] - robot_vel_remapped), dim=1)
        return torch.exp(-lin_vel_error / self.reward_cfg["tracking_sigma"])

    def _reward_tracking_ang_vel(self):
        # Tracking of angular velocity commands (yaw)
        ang_vel_error = torch.square(self.commands[:, 2] - self.base_ang_vel[:, 2])
        return torch.exp(-ang_vel_error / self.reward_cfg["tracking_sigma"])

    def _reward_lin_vel_z(self):
        # Penalize z axis base linear velocity
        return torch.square(self.base_lin_vel[:, 2])

    def _reward_action_rate(self):
        # Penalize changes in actions
        return torch.sum(torch.square(self.last_actions - self.actions), dim=1)

    def _reward_similar_to_default(self):
        # Penalize joint poses far away from default pose
        return torch.sum(torch.abs(self.dof_pos - self.default_dof_pos), dim=1)

    def _reward_base_height(self):
        # Penalize base height away from target
        return torch.square(self.base_pos[:, 2] - self.reward_cfg["base_height_target"])

    def _reward_body_orientation(self):
        # Penalize if body (IMU 3 / base) is not horizontal
        # imu_quats[2] is base (IMU 3)
        base_quat = self.imu_quats[2]
        inv_base_quat = inv_quat(base_quat)
        projected_gravity = transform_by_quat(self.global_gravity, inv_base_quat)
        # Penalize xy components (should be 0 if horizontal)
        return torch.sum(torch.square(projected_gravity[:, :2]), dim=1)

    def _reward_feet_orientation(self):
        # Penalize if feet (IMU 1 & 2) are not horizontal
        # imu_quats[0] is LegEnd_v9_1 (IMU 1)
        # imu_quats[1] is LegEnd_v9_2 (IMU 2)
        
        penalties = 0.0
        for i in [0, 1]:
            foot_quat = self.imu_quats[i]
            inv_foot_quat = inv_quat(foot_quat)
            projected_gravity = transform_by_quat(self.global_gravity, inv_foot_quat)
            penalties += torch.sum(torch.square(projected_gravity[:, :2]), dim=1)
            
        return penalties

    def _reward_alive(self):
        # Reward for staying alive (not terminating)
        return torch.ones(self.num_envs, device=gs.device)

    def _reward_head_height(self):
        # Penalize if head (IMU 4 / imu_pos[3]) is too low (touching ground)
        # Target head height should be at least some value (e.g. 0.2m)
        head_height = self.imu_pos[3][:, 2]
        # Quadratic penalty if below target
        target_height = 0.25
        penalty = torch.square(torch.clamp(target_height - head_height, min=0.0))
        return penalty
