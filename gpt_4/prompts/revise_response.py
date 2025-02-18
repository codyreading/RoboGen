import pickle
from gpt_4.query import query
import json

def get_missing_objects(task, objects, temperature, model):
    system = """You are a helpful assistant that identifies ALL objects mentioned in tasks that are not already in a current list of objects.
When analyzing tasks, identify every physical object that appears in the text, including:
- Objects that need to be manipulated (e.g., picked up, opened, used)
- Containers, furniture, or storage locations (e.g., cupboards, drawers, tables)
- Tools or instruments needed for the task
- Background or environment objects

Be extremely thorough. Don't miss any objects in the task description and any objects that might be needed to complete the task.
"""

    # Construct the prompt for the LLM
    prompt = f"""
Task: {task}

Current list of objects: {objects}

Please identify ALL objects mentioned in the task that are not already in the current list of objects.
Return your answer as a JSON list of strings.  If no new objects need to be added, return an empty list.

Example output:
["object1", "object2"]
"""
    response = query(system,
                     user_contents=[prompt],
                     assistant_contents=[],
                     temperature=temperature,
                     model=model)
    missing_objects = []

    # Try to parse the result as JSON
    try:
        missing_objects = json.loads(response)
    except json.JSONDecodeError:
        # Look for anything that might be a list in the response
        if '[' in result and ']' in result:
            list_part = result[result.find('['):result.rfind(']')+1]
            try:
                missing_objectss = json.loads(list_part)
            except:
                print("Could not extract list from response. Returning empty list.")
    return missing_objects


def revise_response(task, object_category, task_names, task_descriptions, additional_objects, links, joints, temperature, model):
    # Get any missing objects
    new_object_list = []
    for objs in additional_objects:
        objects = f"{object_category}, {objs}"
        missing_objects = get_missing_objects(task=task, objects=objects, model=model, temperature=temperature)

        # Update the original list
        new_objects = objs.split(", ")
        new_objects = set(new_objects)
        new_objects.update(missing_objects)
        new_objects = list(new_objects)
        new_objects = ', '.join(new_objects)

        new_object_list.append(new_objects)


    return task_names, task_descriptions, new_object_list, links, joints