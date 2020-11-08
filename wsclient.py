import asyncio
import websockets


async def connection(adr):
    async with websockets.connect(adr) as ws:
       await ws.send(adr)
    data = await ws.recv()
    print("Получены данные: " + data)


adr = input("ws://127.0.0.1:8080/ws/")
asyncio.get_event_loop().run_until_complete(connection(adr))
