from .views import IndexView, CoolerStateView, OPCView


ROUTES = (
    ("/", "*", IndexView),
    ("/{name}", "*", CoolerStateView),
    ("/ws/opc", "*", OPCView),
)