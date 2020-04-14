from .views import APIClientView, IndexView, WSClientView, WSOPCView 


ROUTES = (
    ("/", "*", IndexView),
    ("/ws/opc", "*", WSOPCView),
    ("/ws/client", "*", WSClientView),
    ("/api/client", "*", APIClientView),
)