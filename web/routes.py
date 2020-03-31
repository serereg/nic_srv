from .views import IndexView, WSClientView, WSOPCView 


ROUTES = (
    ("/", "*", IndexView),
    ("ws/opc", "*", OPCView),
    ("ws/client", "*", ClientView),
)