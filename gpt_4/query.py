import openai
import os
import time
import json
import base64
import cv2

def encode_images_to_base64(images, quality=90):
    base64_images = []

    for image in images:
        # Convert BGR to RGB (if needed, since OpenCV loads images in BGR by default)
        bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

       # Encode the image to JPEG format
        _, buffer = cv2.imencode(".jpg", bgr_image)

        # Convert the image to base64
        encoded_image = base64.b64encode(buffer).decode("utf-8")

        # Append to list
        base64_images.append(f"data:image/jpeg;base64,{encoded_image}")

    return base64_images

def query(system, user_contents, assistant_contents, model='gpt-4', save_path=None, temperature=1, debug=False):

    if os.environ["OPENAI_API_KEY"] == "":
        raise ValueError("Invalid OPENAI_API_KEY. Please set export OPENAI_API_KEY=$KEY")

    for user_content, assistant_content in zip(user_contents, assistant_contents):
        user_content = user_content.split("\n")
        assistant_content = assistant_content.split("\n")

        for u in user_content:
            print(u)
        print("=====================================")
        for a in assistant_content:
            print(a)
        print("=====================================")

    for u in user_contents[-1].split("\n"):
        print(u)

    if debug:
        import pdb; pdb.set_trace()
        return None

    print("=====================================")

    start = time.time()
    num_assistant_mes = len(assistant_contents)
    messages = []

    messages.append({"role": "system", "content": "{}".format(system)})
    for idx in range(num_assistant_mes):
        messages.append({"role": "user", "content": user_contents[idx]})
        messages.append({"role": "assistant", "content": assistant_contents[idx]})
    messages.append({"role": "user", "content": user_contents[-1]})

    openai.api_key = os.environ["OPENAI_API_KEY"]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature
    )

    result = ''
    for choice in response.choices:
        result += choice.message.content

    end = time.time()
    used_time = end - start

    print(result)
    if save_path is not None:
        with open(save_path, "w") as f:
            json.dump({"used_time": used_time, "res": result, "system": system, "user": user_contents, "assistant": assistant_contents}, f, indent=4)

    return result

def query_vlm(system, images, prompt, model='gpt-4o', temperature=0.3):
    images_64 = encode_images_to_base64(images)
    text_dict = {"type": "text", "text": prompt}
    content = [text_dict]

    for image_64 in images_64:
        image_dict = {"type": "image_url", "image_url": {"url": image_64, "detail": "low"}}
        content.append(image_dict)

    messages = [{
        "role": "user",
        "content": content
    }]


    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature
    )

    result = ''
    for choice in response.choices:
        result += choice.message.content

    print(result)
    return result