from .views import IndexView, CoolerStateView, OPCView


ROUTES = (
    ("/", "*", IndexView),
    ("/status", "*", IndexView),
    ("/{name}", "*", CoolerStateView),
    ("/ws/opc", "*", OPCView),
)