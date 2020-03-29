from .views import IndexView, CoolerStateView, CoolerAllStatesView, CoolerCommandView, OPCView


ROUTES = (
    # ("api/opc/coolers", "*", opc.CoolersView),                # opc.CoolersView: get получает информацию о всех кулерах
                                                                #                  put создаёт новый кулер
    # ("api/opc/coolers/{id}", "*", opc.CoolerView),            # opc.CoolerView: get получает информацию о кулере с id
    # ("api/opc/coolers/state", "*", opc.CoolersStateView),     # opc.CoolersStateView: get ws отправляет состояние кулеров

    # ("api/client/coolers", "*", client.CoolersView)           # client.CoolersView: get получает информацию и состояния всех кулерах
    # ("api/client/coolers/{id}", "*", client.CoolerView)       # client.CoolerView: get получает информацию и состояние кулера с id
                                                                #                    post отправляет команду для кулера с id

    ("/", "*", IndexView),
    ("/states", "*", CoolerAllStatesView),
    ("/command", "*", CoolerCommandView),
    ("/{name}", "*", CoolerStateView),
    ("/ws/opc", "*", OPCView),
)