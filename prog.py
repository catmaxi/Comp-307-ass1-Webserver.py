import socket
import sys

IP = sys.argv[1]
PORT = int(sys.argv[2])
path_to_root = sys.argv[3]


def receive(client_connection):
    request_data = b''
    while True:
        request_data += client_connection.recv(4098)
        if b'\r\n\r\n' in request_data:
            break

    parts = request_data.split(b'\r\n\r\n', 1)
    header = parts[0]
    body = parts[1]

    if b'Content-Length' in header:
        headers = header.split(b'\r\n')
        for h in headers:
            if h.startswith(b'Content-Length'):
                blen = int(h.split(b' ')[1])
                break
    else:
        blen = 0

    while len(body) < blen:
        body += client_connection.recv(4098)

    print('header =========')
    print(header.decode('utf-8', 'replace'), flush=True)
    print('body ===========')
    print(body.decode('utf-8', 'replace'), flush=True)

    return header, body


# HOST, PORT = '127.0.0.1', 8888
HOST, PORT = IP, PORT

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print(f'Serving HTTP on port {PORT} ...')
while True:
    client_connection, client_address = listen_socket.accept()
    header, body = receive(client_connection)
    list_header = header.split()
    file = list_header[1].decode()

    # print(header.decode().find('Firefox'))

    if(header.decode().find('Firefox') > -1):
        print("this is firefox")
        http_response = """\
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8

<html>
<body>
<h1><b>Please switch to another browser as Firefox is not secure!!!</b></h1>
</body>
</html>
"""
        http_response = http_response.replace('\n', '\r\n')
        http_response = http_response.encode(encoding='UTF-8')
        client_connection.sendall(http_response)
        client_connection.close()
        # break;

    else:
        print("this is not firefox")
        print(file.split("."))
        file_ext = file.split(".")[1]
        print("file is " + file)
        print(file_ext)

        if(file_ext == "jpg"):
            http_response = """\
HTTP/1.1 200 OK
Content-Type: image/jpeg

"""
        elif(file_ext == "html"):
            http_response = """\
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8

"""
        elif(file_ext == "png"):
            http_response = """\
HTTP/1.1 200 OK
Content-Type: image/png

"""

        if(file_ext != "ico"):
            http_response = http_response.replace('\n', '\r\n')
            http_response = http_response.encode(encoding='UTF-8')
            with open(path_to_root + file, 'rb') as fh:
                http_response += fh.read()
            client_connection.sendall(http_response)
            client_connection.close()
