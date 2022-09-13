#!/usr/bin/env python


import asyncio

import datetime
#import secrets #if we want a fancy key

import random
import websockets


"""
async def show_time(websocket): #this one works, so we keep it

    while True: #we would like: if changed: send data.js (to html)

        message = datetime.datetime.utcnow().isoformat() + "Z"

        await websocket.send(message)

        await asyncio.sleep(random.random() * 2 + 1)

async def error(websocket,message):
    #send an error message
    event={
        "type": "error",
        "message": message,
    }
    await websocket.send(json.dumps(event))
"""
#idea (Post-methode)

async def get_data(websocket):
    #we would want to append the new data in the js (with time stemp --> change --> send_data to html)
    async for message in websocket:
        event = json.loads(message)
        #we want timestemp for data evaluation and visualisation!!!!!!
        datajs.write(event.data + "\n")#our change
        datajs.close()
        event = {
            "type": "data",
            "data": datajs,
        }
        websocket.send(connected, json.dumps(event))

#this would be for more clients

"""async def join(websocket, join_key):
    try:
        connected = JOIN[join_key]
    except KeyError:
        await error(websocket,"wrong Join_Key")
        return
    connected.add(websocket)
    try:
        await get_data(websocket) #do we need await here?
    finally:
        connected.remove(websocket) #do we want this?

#"""

async def handler(websocket):
    #handle a connection and dispatch it according to who is connecting --> first part only if we have plural clients

    message = await websocket.recv() #value in there?
    event = json.loads(message)
    assert event["type"] == "data"

    try:
        get_data(websocket)
    except Exception:
        print("wrong type name")
    """
    # otherwise this should be it
    await websocket.recv() #value in there? & message = ; but then another parameter in get_data?
    get_data(websocket)
    """


async def main():
    textjs = open (test.js, 'x')#<-- alawys do a new file in each session? different name? --> (test.js,x) ## file_name = datetime.now().strftime(%d-%m-%Y-%H-%M.js)
    textjs.close()
    datajs = open(test.js, 'a')
    #they did a start function...
    #initialise set of WebSocket connections (http?)
    connected = {websocket}
    #join key --> in game for the players who can send and receive
    #join_key = 42777#secrets.token_urlsafe(12)
    #JOIN[join_key] = connected
    #now they send the key to the first player... we want to initialise them manually?

    async with websockets.serve(handler, "", 8001): #(show_time,"localhost",5678)

        await asyncio.Future()  # run forever


if __name__ == "__main__":

    asyncio.run(main())
