import numpy as np
import genesis as gs

########################## init ##########################
gs.init(backend=gs.cuda)

########################## create a scene ##########################
scene = gs.Scene(
    sim_options = gs.options.SimOptions(
        dt = 0.01,
    ),
    viewer_options = gs.options.ViewerOptions(
        camera_pos    = (0, -3.5, 2.5),
        camera_lookat = (0.0, 0.0, 0.5),
        camera_fov    = 30,
        max_FPS       = 60,
    ),
    show_viewer = True,
)

########################## entities ##########################
plane = scene.add_entity(
    gs.morphs.Plane(),
)

raptor = scene.add_entity(
    gs.morphs.URDF(
        file  = '../simple_model.urdf',
        pos   = (1.0, 1.0, 0.8),
        euler = (0, 0, 0),
    ),
)

########################## build ##########################
scene.build()

joint_names = [
    "base_to_armRU",
    "armRU_to_armRL",
    "base_to_armLU",
    "armLU_to_armLL",
    "base_to_neckBottom",
    "neckBottom_to_neckMid",
    "neckMid_to_neckTop",
    "neckTop_to_head",
    "base_to_legBaseR",
    "legBaseR_to_legHutoR",
    "legHutoR_to_legSuneR",
    "legSuneR_to_footR",
    "base_to_legBaseL",
    "legBaseL_to_legHutoL",
    "legHutoL_to_legSuneL",
    "legSuneL_to_footL",
]

JOINT_TO_MODEL = {
    "base_to_armRU":        "XL430",
    "armRU_to_armRL":       "XL430",
    "base_to_armLU":        "XL430",
    "armLU_to_armLL":       "XL430",
    "base_to_neckBottom":   "XM430",
    "neckBottom_to_neckMid":"XL430",
    "neckMid_to_neckTop":   "XC430",
    "neckTop_to_head":      "XC430",
    "base_to_legBaseR":     "XM540",
    "legBaseR_to_legHutoR": "XM540",
    "legHutoR_to_legSuneR": "XM540",
    "legSuneR_to_footR":    "XM540",
    "base_to_legBaseL":     "XM540",
    "legBaseL_to_legHutoL": "XM540",
    "legHutoL_to_legSuneL": "XM540",
    "legSuneL_to_footL":    "XM540",
}

MOTOR_FORCE_RANGE = {
    "XL430": (-40,  40),
    "XC430": (-35,  35),
    "XM430": (-80,  80),
    "XM540": (-120, 120),
}

KP = {j: 1.0 for j in joint_names}
KV = {j: 1.0 for j in joint_names}

def _vec_from_map(keys, m):
    missing = [k for k in keys if k not in m]
    if missing:
        raise ValueError(f"未入力のキーがあります: {missing}")
    return np.array([m[k] for k in keys], dtype=float)

def _force_vecs_from_models(keys, jt2model, model2range):
    lower = []
    upper = []
    not_found = []
    for j in keys:
        model = jt2model.get(j, "")
        if model not in model2range:
            not_found.append((j, model))
            lower.append(0.0); upper.append(0.0)
        else:
            lo, up = model2range[model]
            lower.append(float(lo)); upper.append(float(up))
    if not_found:
        msg = ", ".join([f"{j}→'{m}'" for j, m in not_found])
        raise ValueError(f"MOTOR_FORCE_RANGE に無いモデルがあります: {msg}")
    return np.array(lower), np.array(upper)

kp_vec = _vec_from_map(joint_names, KP)
kv_vec = _vec_from_map(joint_names, KV)
lower_vec, upper_vec = _force_vecs_from_models(joint_names, JOINT_TO_MODEL, MOTOR_FORCE_RANGE)

dofs_idx = [raptor.get_joint(name).dof_idx_local for name in joint_names]

########################## 追加設定 ##########################
# KP/KV
raptor.set_dofs_kp(
    kp             = kp_vec,
    dofs_idx_local = dofs_idx,
)
raptor.set_dofs_kv(
    kv             = kv_vec,
    dofs_idx_local = dofs_idx,
)

# Force Range
raptor.set_dofs_force_range(
    lower          = lower_vec,
    upper          = upper_vec,
    dofs_idx_local = dofs_idx,
)

# 初期姿勢（rad）
q0_rad = np.array([
    1.57,   # base_to_armRU
   -1.10,   # armRU_to_armRL
    1.57,   # base_to_armLU
   -1.10,   # armLU_to_armLL
    0.00,   # base_to_neckBottom
    0.00,   # neckBottom_to_neckMid
    0.00,   # neckMid_to_neckTop
    0.00,   # neckTop_to_head
    0.00,   # base_to_legBaseR
   -0.80,   # legBaseR_to_legHutoR
    1.30,   # legHutoR_to_legSuneR
   -1.50,   # legSuneR_to_footR
    0.00,   # base_to_legBaseL
   -0.80,   # legBaseL_to_legHutoL
    1.30,   # legHutoL_to_legSuneL
   -1.50,   # legSuneL_to_footL
], dtype=float)

qd0_rad = np.zeros_like(q0_rad)

if hasattr(raptor, "reset_dofs_state"):
    raptor.reset_dofs_state(q=q0_rad, qd=qd0_rad, dofs_idx_local=dofs_idx)
else:
    raptor.control_dofs_position(q0_rad, dofs_idx)
    for _ in range(100):
        scene.step()

########################## simulation loop ##########################
for i in range(500):
    # ここで制御を入れるなら franka.control_dofs_force など
    positions = []
    #for dofs_id in dofs_idx:
    #    positions.append(100)
    base_link = raptor.get_link('base_link')
    qpos = raptor.inverse_kinematics(
            link = base_link,
            pos = np.array([0.0, 0.0, 0.5]),
            quat = np.array([0, 1, 0, 0]),
    )

    qpos[:2] = 0.4

    path = raptor.plan_path(
            qpos_goal = qpos,
            num_way_points = 200,
    )

    for waypoint in path:
        raptor.control_dofs_position(waypoint)
        scene.step()

    for i in range(100):
        scene.step()


    raptor.control_dofs_position(qpos[:-2], dofs_idx)

    current_forces = raptor.get_dofs_force(
        dofs_idx,
    )
    print(current_forces)
    scene.step()

for i in range(1000):
    scene.step()
