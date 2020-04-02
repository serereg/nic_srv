from .views import IndexView, WSClientView, WSOPCView 


ROUTES = (
    ("/", "*", IndexView),
    ("/ws/opc", "*", WSOPCView),
    ("/ws/client", "*", WSClientView),
)