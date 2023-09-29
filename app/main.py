import socket

#KEK
def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, adress = server_socket.accept()

    with conn:
        data = conn.recv(1024).decode()
        head = data.split("\r\n")[0].split(" ")
        path = head[1]

        if path == "/":
            conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
        else:
            conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")


if __name__ == "__main__":
    main()
