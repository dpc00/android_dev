from tinydb import TinyDB, Query

db = TinyDB("test2.json", sort_keys=False, indent=4, separators=(",", ": "))
db.purge_table("opdep")
tbl = db.table("opdep")

tbl.insert(
    {
        "op": "gitbackup",
        "di": "git",
        "si": "scrdev",
        "dd": "git",
        "sd": "scrdev",
        "options": {"add": True, "commit": True},
    }
)

for row in tbl.all():
    print(row)

db.close()
