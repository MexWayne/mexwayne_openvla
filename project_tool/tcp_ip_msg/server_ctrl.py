import socket
import os
import ipywidgets.widgets as widgets
from IPython.display import display
import time
import threading
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle

def reset_joints():
    mc.send_angles([0, 0, 0, 0, 0, -45], 50)
    mc.set_gripper_value(100, 50)
    coord = mc.get_coords()
    print("get coord:" + str(coord))

def message_to_list(message_data):
    data_list = message_data.split(",")
    return [float(x) for x in data_list]

if __name__ == "__main__":

    mc = MyCobot('/dev/ttyUSB0', 1000000)
    g_speed = 50

    HOST = '0.0.0.0'
    PORT = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)


    reset_joints()


    print(f" waiting for action from client ctrl...")

    conn, addr = server_socket.accept()
    print(f"client connected, addr: {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"recieved: {data.decode()}")
        conn.sendall(b"server recived coordinate action: " + data)

        message_data = data.decode()
        ctrl_coord = message_to_list(message_data)
        print("data_list:" + str(ctrl_coord))
        
        print("get the coords:" + str(ctrl_coord))
        mc.send_coords(ctrl_coord, g_speed)
        print("-----------------")
        time.sleep(3)



    conn.close()
    server_socket.close()