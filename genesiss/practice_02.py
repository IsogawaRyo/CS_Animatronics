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

# when loading an entity, you can specify its pose in the morph.
franka = scene.add_entity(
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
    "neckMid_to_neckTop":   "XC430",   # XC430 A/B → XC430 に統一
    "neckTop_to_head":      "XC430",
    "base_to_legBaseR":     "XM540",
    "legBaseR_to_legHutoR": "XM540",
    "legHutoR_to_legSuneR": "XM540",
    "legSuneR_to_footR":    "XM540",
    "base_to_legBaseL":     "XM540",
    "legBaseL_to_legHutoL": "XM540",
    "legHutoL_to_legSuneL": "XM540",
    "legSuneL_to_footL":    "XM540",   # XM54 → XM540 に修正
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

dofs_idx = [franka.get_joint(name).dof_idx_local for name in joint_names]

for i in range(500):
    #franka.set_dofs_position(1, 100)
    positions = []
    for dofs_id in dofs_idx:
        positions.append(100)
    franka.control_dofs_force(
            positions, dofs_idx,
    )
    scene.step()

for i in range(1000):
    scene.step()

