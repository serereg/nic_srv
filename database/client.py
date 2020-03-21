from .models import Cooler


class DBClient:
    def __init__(self, dsn, db):
        self.db = db
        self.dsn = dsn

    async def connect(self):
        await self.db.set_bind(self.dsn)
        await self.db.gino.create_all()

    async def close(self):
        await self.db.pop_bind().close()

    async def add_fixtures(self, fixtures):
        for fixture in fixtures:
            try:
                await fixture["model"].create(**fixture["fields"])
            except:
                pass

    async def create_cooler(self, name, description=None):
        return await Cooler.create(name=name, description=description)

    async def get_cooler(self, id=None, name=None):
        condition = True
        if id is not None:
            condition = condition and Cooler.id == id
        if name is not None:
            condition = condition and Cooler.name == name
        return await Cooler.query.where(condition).gino.first()
