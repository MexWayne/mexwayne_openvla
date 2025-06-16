import socket
import time


if __name__ == "__main__":


    SERVER_IP = '10.169.25.139'
    PORT = 12345
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORT))

    coord_action_list = [
                            [210, -5, 120, -175, 0, -45],       # goto cross center
                            [-70, 215, 115, -175, 0, -45]       # goto blue area 
                        ]

    while True:
        message = ""
        for i in range(5):
            message += str(coord_action_list[0][i])
            message += ","
        message +=  str(coord_action_list[0][5])

        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        print(f"message recived: {data.decode()}")
        time.sleep(4)

        message = ""
        for i in range(5):
            message += str(coord_action_list[1][i])
            message += ","
        message +=  str(coord_action_list[1][5])

        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        print(f"message recived: {data.decode()}")
        time.sleep(4)

    
    client_socket.close()
    