import socket


if __name__ == "__main__":


    SERVER_IP = '10.169.25.139'
    PORT = 12345
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORT))


    while True:
        message = "hehehe hahaha"
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        print(f"message recived: {data.decode()}")
    client_socket.close()
    
