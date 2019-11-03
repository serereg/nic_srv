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
                cur_cooler.SetSP(request.rel_url.query['val'+ str(t)])
                print(str(t)+"/"+cur_cooler.sp)
                return web.Response(text='OK')
            elif ('cmd'+str(t)) in request.rel_url.query.keys():
                if request.rel_url.query['cmd' + str(t)] == 'YOn':
                    cur_cooler.YOn()
                    return web.Response(text='OK')
            elif ('cmd'+str(t)) in request.rel_url.query.keys():
                if request.rel_url.query['cmd' + str(t)] == 'YOff':
                    cur_cooler.YOff()
                    return web.Response(text='OK')
            elif len(request.rel_url.query.keys())==0:
                strpv = ""
                strsp = ""
                for k in range(1,12):
                    strpv = strpv+str(list_Cooler[k].GetPV())+";"
                    strsp = strsp+str(list_Cooler[k].sp)+";"
                return web.Response(text=strpv+strsp)
async def ws_browser_handler(self, request):
        pass

    
app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}',handle)])

if __name__ == '__main__':
    for i in range(1,16):
        list_Cooler.append(Cooler(i))


    web.run_app(app)

