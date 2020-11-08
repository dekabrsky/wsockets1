import asyncio
import websockets


async def connection(adr):
    print("hey")
    async with websockets.connect(adr) as ws:  # открываем соединение
       await ws.send(adr)  # отправляем запрос
    data = await ws.recv()  # получаем данные из корутины recv, ожидающей их получение
    print("Получены данные: " + data)


asyncio.get_event_loop().run_until_complete(connection(input("ws://0.0.0.0:8080/ws/")))  # запуск клиента
