from django.shortcuts import render
import asyncio
import datetime

# def seelog(request):
#     return render(request, 'interactive.txt','')

# def logs(request):
#     return render(request, 'log.html','')

def salida(request):
    async def display_date(loop):
        end_time = loop.time() + 100.0
        while True:
            archivo = open('interactive.txt', 'r')
            context = {
                timer = print(datetime.datetime.now())
                output = print(archivo.read())
            }
            if (loop.time() + 1.0) >= end_time:
                break
            await asyncio.sleep(1)

    loop = asyncio.get_event_loop()
    # Blocking call which returns when the display_date() coroutine is done
    loop.run_until_complete(display_date(loop))
    loop.close()
    return render(request,'log.html', context )