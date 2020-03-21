from .views import CoolerStateView, OPCView


ROUTES = (
    ("/", "*", IndexView)
    ("/{name}", "*", CoolerStateView),
    ("/ws/opc", "*", OPCView),
)