import socket

#KEK
def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, adress = server_socket.accept()

    with conn:
        conn.send(b"HTTP/1.1 200 OK\r\n\r\n")


if __name__ == "__main__":
    main()
