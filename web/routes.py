from .views import ClientView, IndexView, WSClientView, WSOPCView 


ROUTES = (
    ("/", "*", IndexView),
    ("/ws/opc", "*", WSOPCView),
    ("/ws/client", "*", WSClientView),
    ("/api/client", "*", ClientView),
)