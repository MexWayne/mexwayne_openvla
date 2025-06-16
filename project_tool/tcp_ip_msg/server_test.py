import socket


if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f" waiting for connect the client...")

    conn, addr = server_socket.accept()
    print(f"client connected, addr: {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"recieved: {data.decode()}")
        conn.sendall(b"server recived: messsage:" + data)

    conn.close()
    server_socket.close()