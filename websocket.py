import asyncio
import enum
import json
import socket
import struct
import subprocess
import websockets
from dataclasses import dataclass


class State(enum.Enum):
    KEEP_ALIVE = 0
    FORWARD = 1
    BACKWARDS = 2
    ROTATE_LEFT = 3
    ROTATE_RIGHT = 4


STATE = State.KEEP_ALIVE
UPDATE_EVENT = asyncio.Event()
POSITION_EVENT = asyncio.Event()


@dataclass
class Position:
    x: int
    y: int


POSITION = []

SPEED = 100
CHANNEL = 0

CARLOS_NAMES = []

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
            while True:
                data, address = sock.recvfrom(1500)

                if data[0] == 14:
                    x, y = struct.unpack("!dd", data[1:])
                    if POSITION[CHANNEL].x != x or POSITION[CHANNEL].y != y:
                        POSITION[CHANNEL] = Position(x, y)
                        POSITION_EVENT.set()

                if data[0] == 10:
                    resend_connect_request = True
        except socket.error:
            pass

        if resend_connect_request:
            request = struct.pack("!B", int(4))
            sock.sendto(request, (get_ip(CARLOS_NAMES[CHANNEL]), port))
            print("Sent connection request")

        data = []
        if type(SPEED) != float and type(SPEED) != int:
            continue
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


async def position_handler(websocket):
    try:
        while True:
            await asyncio.wait_for(POSITION_EVENT.wait(), timeout=None)
            event = {"type": "position", "channel": CHANNEL,
                     "data": {"x": POSITION[CHANNEL].x, "y": POSITION[CHANNEL].y}}
            await websocket.send(json.dumps(event))
            POSITION_EVENT.clear()
    except Exception as e:
        print(e)


async def handler(websocket):
    global STATE
    global SPEED
    global CHANNEL

    asyncio.create_task(position_handler(websocket))

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
    with open("hosts") as hosts:
        CARLOS_NAMES = hosts.readlines()
        CARLOS_NAMES = [line.rstrip() for line in CARLOS_NAMES]
        CARLOS_NAMES = list(filter(None, CARLOS_NAMES))

    subprocess.call(["killall", "webrtc_server"])
    print(CARLOS_NAMES)
    enum_hosts = enumerate(CARLOS_NAMES)
    for i, host in enum_hosts:
        webrtc_port = 57770 + i
        print(webrtc_port)
        subprocess.Popen(
            ["./webrtc-server/webrtc_server", "--rtsp-server-ip=" + host + ":8554", "--port=" + str(webrtc_port)])

    if len(CARLOS_NAMES) < 10:
        for i in range(10 - len(CARLOS_NAMES)):
            CARLOS_NAMES.append(CARLOS_NAMES[0])

    for i in range(len(CARLOS_NAMES)):
        POSITION.append(Position(x=0, y=0))
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
