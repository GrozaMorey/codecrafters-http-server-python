import socket
import re


def main():
    global conn
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, adress = server_socket.accept()

    with conn:
        request = Request(conn.recv(1024).decode())
        if request.path == "/":
            conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
        elif re.match("/echo/*", request.path):
            path = request.path.replace("/echo/", "")
            response = bytes(
                f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path)}\r\n\r\n{path}",
                encoding="UTF-8", )
            conn.send(response)
        elif re.match("/user-agent/*", request.path):
            Response(request.user_agent).send()
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

                setattr(self, i[0].lower().replace(" ", "").replace("-", "_"), i[1].lower().replace(" ", ""))

            except IndexError:
                continue


class Response:

    def __init__(self, body, code=200):
        if type(body) is str:
            self.code = code

        if body:
            self.content_length = len(body)
            self.body = body

    def send(self):
        conn.send(bytes(f"HTTP/1.1 {self.code} OK\r\n"
                        f"Content-Type: text/plain\r\n"
                        f"Content-Length: {self.content_length}\r\n\r\n{self.body}",
                        encoding="UTF-8", )
                  )


while True:
    main()
