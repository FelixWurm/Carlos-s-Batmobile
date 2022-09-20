import json
import socket


def get_values_from(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.send(b"exit")
    return json.loads(sock.recv(1024).decode("utf-8"))


def main():
    print(json.dumps(get_values_from("192.168.199.12", 25022), indent=2))


if __name__ == '__main__':
    main()
