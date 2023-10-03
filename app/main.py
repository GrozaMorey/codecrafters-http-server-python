import socket
import re
def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, adress = server_socket.accept()

    with conn:
        request = Request(conn.recv(1024).decode())
        if request.path == "/":
            conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
        elif re.match("/echo/*", request.path):
            path = request.path.replace("/echo/", "")
            response = bytes(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path)}\r\n\r\n{path}", encoding="UTF-8",)
            conn.send(response)
        else:
            conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")


class Request:

    def __init__(self, data):
        data = data.split("\r\n")
        self.path = data[0].split(" ")[1]
        data.pop(0)

        if type(data[-1]) is str:
            self.data = data[-1]

        for i in data:
            try:
                i = i.split(": ")

                setattr(self, i[0].lower().replace(" ", ""), i[1].lower().replace(" ", ""))

            except IndexError:
                continue






while True:
    main()
