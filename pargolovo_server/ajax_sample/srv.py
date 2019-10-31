from aiohttp import web
from Cooler import Cooler

paraml = 'ddd'

list_Cooler = []


async def handle(request):
    name = request.match_info.get('name',"Anonymous__")
    text = "Hello, " + name
    for k in request.rel_url.query.keys():
        print(k+"="+request.rel_url.query[k])
    if name == 'index.html':
        return web.FileResponse(name)
    else:
        for t in range(1,16):
            cur_cooler = list_Cooler[t]
            if ('val'+str(t)) in request.rel_url.query.keys():
                list_Cooler[t].SetSP(request.rel_url.query['val'+ str(t)])
                print(str(t)+"/"+list_Cooler[t].sp)
                return web.Response(text='OK')
            elif ('cmd'+str(t)) in request.rel_url.query.keys():
                if request.rel_url.query['cmd' + str(t)] == 'YOn':
                    list_Cooler[t].YOn()
                    return web.Response(text='OK')
            elif ('cmd'+str(t)) in request.rel_url.query.keys():
                if request.rel_url.query['cmd' + str(t)] == 'YOff':
                    list_Cooler[t].YOff()
                    return web.Response(text='OK')
            elif len(request.rel_url.query.keys())==0:
                return web.Response(text="21;22;23;"+str(list_Cooler[1].sp)+';'+str(list_Cooler[2].sp)+';'+str(list_Cooler[3].sp))
                #return web.Response(text= str(cur_cooler.GetPV()))
            list_Cooler[t] = cur_cooler
async def ws_browser_handler(self, request):
        pass

    
app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}',handle)])

if __name__ == '__main__':
    for i in range(1,16):
        list_Cooler.append(Cooler(i))


    web.run_app(app)
