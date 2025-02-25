import cv2

video_path = "/mnt/ssds-agent/robotics/datasets/ego4d/v2/full_scale/7aca7552-56d2-4ac0-be30-aed9c5dfc8ea.mp4"
output_image = "data/ego4d/washing_machine.jpeg"
frame_number = 698  # Change this to the frame you want

cap = cv2.VideoCapture(video_path)
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)  # Go to the specific frame
ret, frame = cap.read()


if ret:
    cv2.imwrite(output_image, frame)
    print(f"Saved frame {frame_number} as {output_image}")
else:
    print("Could not extract the frame.")

cap.release()
