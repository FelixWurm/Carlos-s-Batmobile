import asyncio
import enum
import json
import socket
import struct

import websockets


class State(enum.Enum):
    KEEP_ALIVE = 0
    FORWARD = 1
    BACKWARDS = 2
    ROTATE_LEFT = 3
    ROTATE_RIGHT = 4


STATE = State.KEEP_ALIVE
UPDATE_EVENT = asyncio.Event()

SPEED = 100
CHANNEL = 0

CARLOS_NAMES = ["192.168.199.105", "192.168.199.104", "carlos-3.local", "carlos-4.local"]

DNS_CACHE = {}


def get_ip(domain):
    return domain


async def carlos_controller():
    prev_channel = -1
    port = 50000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)

    while True:
        try:
            await asyncio.wait_for(UPDATE_EVENT.wait(), timeout=0.1)
            UPDATE_EVENT.clear()
        except asyncio.exceptions.TimeoutError:
            pass

        resend_connect_request = False

        request = struct.pack("!B", int(4))
        # Todo: Wait for connection accept
        sock.sendto(request, (get_ip(CARLOS_NAMES[CHANNEL]), port))

        if prev_channel != CHANNEL:
            request = struct.pack("!B", int(4))
            # Todo: Wait for connection accept
            sock.sendto(request, (get_ip(CARLOS_NAMES[CHANNEL]), port))
            if prev_channel != -1:
                # Send stop signal to previous channel
                data = struct.pack("!B", int(6))
                sock.sendto(data, (get_ip(CARLOS_NAMES[prev_channel]), port))
                sock.sendto(data, (get_ip(CARLOS_NAMES[prev_channel]), port))
            prev_channel = CHANNEL

        try:
            resp = sock.recvfrom(1500)
            if resp[0] == 10:
                resend_connect_request = True
                print("Resend connection request")
        except socket.error:
            pass

        if resend_connect_request:
            request = struct.pack("!B", int(4))
            # Todo: Wait for connection accept
            sock.sendto(request, (get_ip(CARLOS_NAMES[CHANNEL]), port))

        data = []
        if type(SPEED) != float and type(SPEED) != int:
            continue
        print(STATE)
        if STATE == State.FORWARD:
            data = struct.pack("!Bf", int(1), SPEED)
        if STATE == State.BACKWARDS:
            data = struct.pack("!Bf", int(1), -SPEED)
        if STATE == State.KEEP_ALIVE:
            data = struct.pack("!B", int(6))
        if STATE == State.ROTATE_RIGHT:
            data = struct.pack("!Bf", int(2), -SPEED)
        if STATE == State.ROTATE_LEFT:
            data = struct.pack("!Bf", int(2), SPEED)

        sock.sendto(data, (get_ip(CARLOS_NAMES[CHANNEL]), port))


async def handler(websocket):
    global STATE
    global SPEED
    global CHANNEL

    async for message in websocket:
        event = json.loads(message)
        if event["type"] == "keyPress":
            key = event["key"]

            if key == 'a':
                STATE = State.ROTATE_LEFT
            if key == 'w':
                STATE = State.FORWARD
            if key == 's':
                STATE = State.BACKWARDS
            if key == 'd':
                STATE = State.ROTATE_RIGHT
            if key == 'no_key':
                STATE = State.KEEP_ALIVE
        if event["type"] == "speed":
            SPEED = event["speed"]
        if event["type"] == "channel":
            CHANNEL = event["channel"]

        UPDATE_EVENT.set()


async def websocket_server():
    async with websockets.serve(handler, "localhost", 8888):
        await asyncio.Future()


async def main():
    await asyncio.gather(websocket_server(), carlos_controller())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
