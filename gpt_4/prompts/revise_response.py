import pickle
from gpt_4.query import query, query_vlm
import json
from utils import io_utils

def separate_and_items(items):
    """
    Separate items that are joined by 'and' or '&' into individual items.

    Args:
        items (list): A list of strings that may contain items separated by 'and' or '&'

    Returns:
        list: A list of individual items with separators split
    """
    separated_items = []
    for item in items:
        # Replace & with 'and' to standardize splitting
        item = item.replace('&', ' and ')

        # Check if 'and' is in the item
        if ' and ' in item:
            # Split the item by 'and' and strip whitespace
            split_items = [i.strip() for i in item.split(' and ')]
            separated_items.extend(split_items)
        else:
            # If no 'and', add the item as is
            separated_items.append(item)

    return separated_items

def remove_words(items):
    """
    Remove items that are entirely 'floor' (case-insensitive).

    Args:
        items (list): A list of strings to process

    Returns:
        list: A list of items with 'floor' entries removed, regardless of capitalization
    """
    words = ["floor", "hands", "hand", "table"]
    cleaned_items = [item for item in items if item.lower() not in words]

    return cleaned_items

def get_objects_from_text(response):
    missing_objects = []

    # Try to parse the response as JSON
    try:
        missing_objects = json.loads(response)
    except json.JSONDecodeError:
        # Look for anything that might be a list in the response
        if '[' in response and ']' in response:
            list_part = response[response.find('['):response.rfind(']')+1]
            try:
                missing_objectss = json.loads(list_part)
            except:
                print("Could not extract list from response. Returning empty list.")

    missing_objects = separate_and_items(missing_objects)
    missing_objects = remove_words(missing_objects)
    return missing_objects


def get_missing_objects_llm(task, objects, temperature, model):
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

Current list of objects: {', '.join(objects)}

IMPORTANT INSTRUCTIONS:
- Return ONLY specific, individual items
- DO NOT return categories or general classes of items
- Each item must be a concrete, individual object

For example:
- CORRECT: ["wooden broom", "dustpan", "vacuum cleaner"]
- INCORRECT: ["cleaning tools", "kitchen utensils", "gardening equipment"]

Please identify ALL objects mentioned in the task that are not already in the current list of objects.
Return your answer as a list of strings. Ensure that each item in the list is a specific item. If no new objects need to be added, return an empty list.

Example output:
["object1", "object2"]
"""
    response = query(system,
                     user_contents=[prompt],
                     assistant_contents=[],
                     temperature=temperature,
                     model=model)
    missing_objects = get_objects_from_text(response)
    return missing_objects


def get_missing_objects_vlm(task, objects, image_path, model, temperature):
    system = "You are a helpful assistant that identifies objects shown in an image that are not already in a current list of objects"

    # Construct the prompt for the LLM
    prompt = f"""
Task: {task}

Current list of objects: {', '.join(objects)}

IMPORTANT INSTRUCTIONS:
- Return ONLY specific, individual items
- DO NOT return categories or general classes of items
- Each item must be a concrete, individual object

For example:
- CORRECT: ["wooden broom", "plastic dustpan", "vacuum cleaner"]
- INCORRECT: ["cleaning tools", "kitchen utensils", "gardening equipment"]

Please identify ALL objects in the image that are not already in the current list of objects.
Return your answer as a list of strings. Ensure that each item in the list is a single item, and not a collection of items. If no new objects need to be added, return an empty list.

Example output:
["object1", "object2"]
"""
    image = io_utils.load_image(image_path)
    response = query_vlm(system=system, images=[image], prompt=prompt, model=model, temperature=temperature)
    missing_objects = get_objects_from_text(response)
    return missing_objects


def revise_response(task, object_category, task_names, task_descriptions, additional_objects, links, joints, temperature_dict, model_dict, image_dir=None):

    # Get any missing objects
    new_object_list = []
    for objs in additional_objects:
        new_objects = objs.split(", ")
        new_objects = separate_and_items(new_objects) # Remove objects that are combined
        new_objects = remove_words(new_objects)
        new_objects = set(new_objects)

        objects_all = [object_category] + list(new_objects)
        missing_objects_llm = get_missing_objects_llm(task=task,
                                                      objects=objects_all,
                                                      model=model_dict["llm_missing_objects"],
                                                      temperature=temperature_dict["llm_missing_objects"])
        new_objects.update(missing_objects_llm)

        if image_dir is not None:
            objects_all = [object_category] + list(new_objects)

            missing_objects_vlm = get_missing_objects_vlm(task=task,
                                                          objects=objects_all,
                                                          image_path=image_dir / f"{object_category}.png",
                                                          model=model_dict["vlm_missing_objects"],
                                                          temperature=temperature_dict["vlm_missing_objects"])
            new_objects.update(missing_objects_vlm)

        new_objects = list(new_objects)
        new_objects = ', '.join(new_objects)
        new_object_list.append(new_objects)


    return task_names, task_descriptions, new_object_list, links, joints