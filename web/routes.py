from .views import IndexView, CoolerStateView, CoolerAllStatusesView, CoolerCommandView, OPCView


ROUTES = (
    ("/", "*", IndexView),
    ("/status", "*", CoolerAllStatusesView),
    ("/command", "*", CoolerCommandView),
    ("/{name}", "*", CoolerStateView),
    ("/ws/opc", "*", OPCView),
)