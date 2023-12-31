import socket
import re
import threading
import sys
import os

def handle_client(conn, adress):
    print("connect by", adress)

    with conn:
        request = Request(conn.recv(1024).decode())
        if request.path == "/":
            conn.send(b"HTTP/1.1 200 OK\r\n\r\n")

        elif re.match("/echo/*", request.path):
            path = request.path.replace("/echo/", "")
            Response(path).send(conn)

        elif re.match("/user-agent/*", request.path):
            Response(request.user_agent).send(conn)

        elif re.match("/files/*", request.path):
            directory = sys.argv[-1]
            filename = request.path.split("/")[-1]

            if os.path.exists(directory + filename):
                file = open(directory + filename, "rb")
                response = Response(file.read().decode("utf-8"))
                response.content_type = "application/octet-stream"
                response.send(conn)
                file.close()

            elif request.method == "POST":
                file_dir = os.path.join(directory, filename)
                with open(file_dir, "w") as file:
                    file.write(request.data)
                response = Response(code=201)
                response.send(conn)

            else:
                conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        else:
            conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")


class Request:
    def __init__(self, data):
        data = data.split("\r\n")
        self.path = data[0].split(" ")[1]
        self.method = data[0].split(" ")[0]
        data.pop(0)

        if type(data[-1]) is str:
            self.data = data[-1]

        for i in data:
            try:
                i = i.split(": ")

                setattr(self, i[0].lower().replace(" ", "").replace("-", "_"), i[1].replace(" ", ""))

            except IndexError:
                continue


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=False)

    while True:
        conn, adress = server_socket.accept()
        tread = threading.Thread(target=handle_client, args=(conn,adress))
        tread.start()


class Response:

    def __init__(self, body=None, code=200):
        self.code = code
        self.body = body
        if type(body) is str:
            self.content_type = "text/plain"

        if body:
            self.content_length = len(body)


    def send(self, conn):

        code = {
            200: "OK",
            404: "NOT FOUND",
            201: "CREATED",
        }

        print("response sending...")
        if self.body:
            conn.send(f"HTTP/1.1 {self.code} {code[self.code]}\r\n"
                      f"Content-Type: {self.content_type}\r\n"
                      f"Content-Length: {self.content_length}\r\n\r\n{self.body}".encode()
                      )

        else:
            conn.send(f"HTTP/1.1 {self.code} {code[self.code]}\r\n\r\n".encode())
        print("response was success send")


if __name__ == "__main__":
    main()
