from orator import DatabaseManager, Model

config = {
    'sqlite': {
        'driver': 'sqlite',
        'database': '/sdcard/budata.db'
    },
}

db = DatabaseManager(config)
Model.set_connection_resolver(db)


class Item(Model):
    __table__ = 'Item'
    __timestamps__ = False


ar = db.table('Item').where('type', '=', 'dir').update({'type': 'fileset'})
print(ar)
