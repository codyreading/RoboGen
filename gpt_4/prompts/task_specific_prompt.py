def get_task_specific_prompt():
    prompt = """
I will give you an articulated object, with its articulation tree and semantics. I will also give you a basic task description that a robotic arm can perform with this articulated object in a household scenario. Your goal is to fully describe the task in a specific format. You can think of the robotic arm as a Franka Panda robot. The task will be built in a simulator for the robot to learn it.

The task will focus on manipulation or interaction with the object itself. Sometimes the object will have functions, e.g., a microwave can be used to heat food, in these cases, feel free to include other objects that are needed for the task. Sometimes the task description will specify additonal objects, make sure all of these objects are included as Additional Objects.

Please write in the following format:
Task name: the name of the task.
Description: some basic descriptions of the tasks.
Additional Objects: Additional objects other than the provided articulated object required for completing the task.
Links: Links of the articulated objects that are required to perform the task.
- Link 1: reasons why this link is needed for the task
- Link 2: reasons why this link is needed for the task
- …
Joints: Joints of the articulated objects that are required to perform the task.
- Joint 1: reasons why this joint is needed for the task
- Joint 2: reasons why this joint is needed for the task
- …


Example Input:

```Oven articulation tree
links:
base
link_0
link_1
link_2
link_3
link_4
link_5
link_6
link_7

joints:
joint_name: joint_0 joint_type: revolute parent_link: link_7 child_link: link_0
joint_name: joint_1 joint_type: continuous parent_link: link_7 child_link: link_1
joint_name: joint_2 joint_type: continuous parent_link: link_7 child_link: link_2
joint_name: joint_3 joint_type: continuous parent_link: link_7 child_link: link_3
joint_name: joint_4 joint_type: continuous parent_link: link_7 child_link: link_4
joint_name: joint_5 joint_type: continuous parent_link: link_7 child_link: link_5
joint_name: joint_6 joint_type: continuous parent_link: link_7 child_link: link_6
joint_name: joint_7 joint_type: fixed parent_link: base child_link: link_7
```

```Oven semantics
link_0 hinge door
link_1 hinge knob
link_2 hinge knob
link_3 hinge knob
link_4 hinge knob
link_5 hinge knob
link_6 hinge knob
link_7 heavy oven_body
```

```Task
Open the oven door
```

Example output:

Task Name: Open Oven Door
Description: The robotic arm will open the oven door.
Additional Objects: None
Links:
- link_0: from the semantics, this is the door of the oven. The robot needs to approach this door in order to open it.
Joints:
- joint_0: from the articulation tree, this is the revolute joint that connects link_0. Therefore, the robot needs to actuate this joint for opening the door.

Can you do the same for the following object and task:
"""
    return prompt