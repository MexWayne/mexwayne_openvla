"""
verify_openvla.py

Given an HF-exported OpenVLA model, attempt to load via AutoClasses, and verify forward() and predict_action().
"""

import time

import numpy as np
import torch
from PIL import Image
from transformers import AutoModelForVision2Seq, AutoProcessor
from transformers import BitsAndBytesConfig
import cv2
import socket





# === Verification Arguments
MODEL_PATH = "openvla/openvla-7b"
SYSTEM_PROMPT = (
    "A chat between a curious user and an artificial intelligence assistant. "
    "The assistant gives helpful, detailed, and polite answers to the user's questions."
)
#INSTRUCTION = "put spoon on towel"
INSTRUCTION = "pick up the cubic"


def get_openvla_prompt(instruction: str) -> str:
    if "v01" in MODEL_PATH:
        return f"{SYSTEM_PROMPT} USER: What action should the robot take to {instruction.lower()}? ASSISTANT:"
    else:
        return f"In: What action should the robot take to {instruction.lower()}?\nOut:"


@torch.inference_mode()
def verify_openvla() -> None:
    print(f"[*] Verifying OpenVLAForActionPrediction using Model `{MODEL_PATH}`")
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

    # Load Processor & VLA
    print("[*] Instantiating Processor and Pretrained OpenVLA")
    processor = AutoProcessor.from_pretrained(MODEL_PATH, trust_remote_code=True)

    # === BFLOAT16 + FLASH-ATTN MODE ===
    print("[*] Loading in BF16 with Flash-Attention Enabled")
    vla = AutoModelForVision2Seq.from_pretrained(
        MODEL_PATH,
        attn_implementation="flash_attention_2",
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
    ).to(device)


    # === 8-BIT QUANTIZATION MODE (`pip install bitsandbytes`) :: [~9GB of VRAM Passive || 10GB of VRAM Active] ===
    #print("[*] Loading in 8-Bit Quantization Mode")
    #vla = AutoModelForVision2Seq.from_pretrained(
    #    MODEL_PATH,
    #    #attn_implementation="flash_attention_2",
    #    torch_dtype=torch.float16,
    #    quantization_config=BitsAndBytesConfig(load_in_8bit=True),
    #    low_cpu_mem_usage=True,
    #    trust_remote_code=True,
    #)

    # === 4-BIT QUANTIZATION MODE (`pip install bitsandbytes`) :: [~6GB of VRAM Passive || 7GB of VRAM Active] ===
    # print("[*] Loading in 4-Bit Quantization Mode")
    # vla = AutoModelForVision2Seq.from_pretrained(
    #     MODEL_PATH,
    #     attn_implementation="flash_attention_2",
    #     torch_dtype=torch.float16,
    #     quantization_config=BitsAndBytesConfig(load_in_4bit=True),
    #     low_cpu_mem_usage=True,
    #     trust_remote_code=True,
    # )

    if False:
        print("[*] Iterating with Randomly Generated Images")
        for _ in range(100):
            prompt = get_openvla_prompt(INSTRUCTION)
            image = Image.fromarray(np.asarray(np.random.rand(256, 256, 3) * 255, dtype=np.uint8))

            # === BFLOAT16 MODE ===
            inputs = processor(prompt, image).to(device, dtype=torch.bfloat16)

            # === 8-BIT/4-BIT QUANTIZATION MODE ===
            # inputs = processor(prompt, image).to(device, dtype=torch.float16)

            # Run OpenVLA Inference
            start_time = time.time()
            action = vla.predict_action(**inputs, unnorm_key="bridge_orig", do_sample=False)
            print(f"\t=>> Time: {time.time() - start_time:.4f} || Action: {action}")

    
    if True:
        print("[*] Iterating with Randomly Generated Images")
        cam_r = cv2.VideoCapture(2)  # /dev/video2

        SERVER_IP = '10.169.25.139'
        PORT = 12345
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, PORT))

        while(True):
            ret_r, frame_r = cam_r.read()  # ret==True/False: read successfully or not; frame: image
            if not ret_r:
                print("Failed to read the image from right camera.")
                break

            # === display image ===
            cv2.imshow('Video_from_right', frame_r)
            prompt = get_openvla_prompt(INSTRUCTION)
            resize_img = cv2.resize(frame_r, (256, 256))
            image = Image.fromarray(np.asarray(resize_img, dtype=np.uint8))

            # === BFLOAT16 MODE ===
            inputs = processor(prompt, image).to(device, dtype=torch.bfloat16)

            # Run OpenVLA Inference
            start_time = time.time()
            action = vla.predict_action(**inputs, unnorm_key="bridge_orig", do_sample=False)
            print(f"\t=>> Time: {time.time() - start_time:.4f} || Action: {action}")


            # === send message === 
            message = ""
            for i in range(5):
                if i < 2:
                    #message += str(action[i] * 2000)
                    message += str(action[i] * 1200)
                elif i == 2:
                    message += str(action[i] * 1200)
                else:
                    message += str(action[i])
                message += ","
            message +=  str(action[5])
            client_socket.sendall(message.encode())
            data = client_socket.recv(1024)
            print(f"message recived: {data.decode()}")

            # press ESC key to exit
            key_r = cv2.waitKey(1)
            if key_r == 27:
                break

    cam_r.release()
    client_socket.close()


if __name__ == "__main__":
    verify_openvla()
