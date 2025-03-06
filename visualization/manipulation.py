import os
import yaml
import numpy as np
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from manipulation.utils import build_up_env, take_round_images, save_numpy_as_gif
from utils import io_utils

def visualize(config_path, output_dir):
    env = get_env(config_path, visualize=True, output_dir=output_dir)


def get_env(task_config_path,
            gui=False,
            randomize=False, # whether to randomize the initial state of the environment.
            obj_id=0,
            visualize=False,
            name=None,
            output_dir=None): # which object to use from the list of possible objects.):
    with open(task_config_path, 'r') as file:
        task_config = yaml.safe_load(file)

    solution_path = None
    for obj in task_config:
        if "solution_path" in obj:
            solution_path = obj["solution_path"]
            break

    if not os.path.exists(solution_path):
        os.makedirs(solution_path, exist_ok=True)


    all_substeps = os.path.join(solution_path, "substeps.txt")
    with open(all_substeps, 'r') as f:
        substeps = f.readlines()
    print("all substeps:\n {}".format("".join(substeps)))

    action_spaces = os.path.join(solution_path, "action_spaces.txt")
    with open(action_spaces, 'r') as f:
        action_spaces = f.readlines()
    print("all action spaces:\n {}".format("".join(action_spaces)))

    substep = substeps[0].lstrip().rstrip()
    action_space = action_spaces[0].lstrip().rstrip()
    task_name = substep.replace(" ", "_")

    env, safe_config = build_up_env(
        task_config_path,
        solution_path,
        task_name,
        None,
        return_env_class=False,
        action_space=action_space,
        render=gui,
        randomize=randomize,
        obj_id=obj_id,
        visualize=visualize,
        output_dir=output_dir,
    )
    env.reset()
    return env

def generate_images(env, distance=1.6, num_images=1, elevation=30, azimuth_offset=0):
    center = None
    if env.use_table:
        center = np.array([0, 0, 0.4])
    else:
        for name in env.urdf_ids:
            if name in ['robot', 'plane', 'init_table']:
                continue
            if env.urdf_types[name] != "urdf":
                continue
            object_id = env.urdf_ids[name]
            min_aabb, max_aabb = env.get_aabb(object_id)
            center = (min_aabb + max_aabb) / 2
            break
    if center is None:
        center = np.array([0, 0, 0.4])

    azimuth_interval = int(360 / num_images)
    rgbs, depths = take_round_images(env,
                                     center=center,
                                     distance=distance,
                                     elevation=elevation,
                                     azimuth_interval=azimuth_interval,
                                     azimuth_offset=azimuth_offset,
                                     camera_width=512,
                                     camera_height=512)
    return rgbs

def visualize_image(env, azimuth):
    images = generate_images(env=env,
                             azimuth_offset=azimuth)
    image = images[0].astype(np.uint8)
    return image

def save_images(images, output_path):
    output_path.mkdir(parents=True, exist_ok=True)

    for i, image in enumerate(images):
        path = output_path / f"{i}.jpeg"
        io_utils.save_image(image, path)
