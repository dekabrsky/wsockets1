import aiohttp
from aiohttp import web


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':  # проверяем, не хотят ли закрыть соединение
                await ws.close()
            else:
                with open(msg.data, 'r') as txtfile:  # ожидается, что в сообщении будет передано имя файла
                    file_string = txtfile.read()  # считываем файл

                await ws.send_str(file_string)  # все наши файлы - текст
                # реализация вебсокета в aio позволяет отправлять текст, json или байты в отдельных корутинах,
                # таких как send_str
        elif msg.type == aiohttp.WSMsgType.ERROR:  # обработка ошибок
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws


async def getfile(request):
    return web.FileResponse(str(request.url).split("/")[3])
    # получаем адрес файла - последнюю часть урла,
    # полученного в запросе


app = web.Application()  # запускаем веб-приложение

# все файлы получим с помощью одного метода - getFile
app.add_routes([web.get("/myfile1.txt", getfile)])
app.add_routes([web.get("/README.rst", getfile)])
app.add_routes([web.get("/aioserver.py", getfile)])  # вместо myserver

# путь для получения всего содержимого папки (статических файлов)
app.router.add_static("/directory", path="*полный путь на машине*/wsockets1", show_index=True)
# TODO записать свой путь на локальной машине до папки

# а теперь через вебсокет
app.add_routes([web.get("/ws", websocket_handler)])

web.run_app(app)
