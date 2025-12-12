import datetime
import math
import re
import sqlite3
from functools import reduce

from textual.app import App, ComposeResult
from textual.reactive import Reactive
from textual.widget import Widget
from textual.widgets import Button, DataTable, Input, Label


drows = {}

dayrows = []

dbstarted = False


def dbstart():
    global conn, cursor, dbstarted
    if not dbstarted:
        conn = sqlite3.connect("finance.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        dbstarted = True


dbstart()


class AssetObj:
    def __init__(self, name, balance, id):
        self.name = name
        self.balance = balance
        self.id = id
        self.labelinput = None


def load_asset_balances():
    global conn, cursor
    rows = cursor.execute("""
        select * from asset order by name;
    """).fetchall()
    for ass in rows:
        name = ass["name"]
        aid = ass["asset_id"]
        anm = name.replace(" ", "")
        balance = ass["current_balance"]
        drows[anm] = AssetObj(name, balance, aid)

def gen_widgets():
    for anm in drows.keys():
        ao = drows[anm]
        balance = ao.balance
        if balance:
            fvl = f"{balance:>4.2f}"
        else:
            fvl = ""
        lblin = LabeledInput(
            Label(ao.name),
            Input(
                value=fvl,
                id=anm,
            ),
        )
        ao.labelinput = lblin
        yield lblin


def find_yesterdays_ending_balances():
    global conn, cursor
    c1 = cursor.execute("""
        select asset_id from asset;
    """)
    rows = c1.fetchall()
    ydd = datetime.date.today() - datetime.timedelta(days=5)
    db = {}
    for ass in rows:
        aid = ass["asset_id"]
        sr = cursor.execute(
            """
            select * from blog
            where date(time)<? and asset_id=?
            order by time desc
            """,
            [ydd, aid],
        )
        r = sr.fetchone()
        db[aid] = r["balance"]
    return db


def get_todays_transactions():
    global conn, cursor
    sdd = datetime.date.today() - datetime.timedelta(days=5)
    sr = cursor.execute(
        """
        select * from blog
        where date(time)>=?
        order by time asc;
    """,
        [sdd],
    )
    rws = sr.fetchall()
    trs = []
    for r in rws:
        aid = r["asset_id"]
        amt = r["amount"]
        bal = r["balance"]
        tt = datetime.datetime.fromisoformat(r["time"])
        amt = round(amt, 2)
        trs.append((aid, tt, amt, bal))
    return trs


def update_asset_balances():
    global conn, cursor
    for anm in drows.keys():
        ao = drows[anm]
        row = cursor.execute(
            """
            select * from asset where asset_id = ?;
        """,
            [ao.id],
        ).fetchone()
        if row:
            rcb = row["current_balance"]
            print(
                f"current_balance {rcb} {type(rcb)} ao.balance {ao.balance} {type(ao.balance)}"
            )
            if rcb != ao.balance:
                print(f"row {ao.id}:{ao.name} needs update {rcb}->{ao.balance}")
                cursor.execute(
                    """
                   update asset set current_balance = ?
                   where asset_id = ?
                """,
                    [ao.balance, ao.id],
                )
                conn.commit()


class Num(Label):
    num = Reactive(0, layout=True)

    def __init__(self, val, **kwargs):
        super().__init__(f"{val}", **kwargs)
        self.num = val

    def render(self):
        return f"{self.num:>8.2f}"


class LabeledInput(Widget):
    """An input with a label."""

    DEFAULT_CSS = """
    LabeledInput {
        layout: horizontal;
        height: auto;
    }
    LabeledInput Label {
        padding: 1;
        width: 12;
        text-align: left;
    }
    LabeledInput Input {
        width: 1fr;
        text-align: right;
    }
    """

    def __init__(self, label: Label, input: Input) -> None:
        self.label = label
        self.input = input
        self.init_value = input.value
        self.num = Num(round(float(input.value), 2))
        super().__init__()

    def compose(self) -> ComposeResult:
        yield self.label
        yield self.input
        yield self.num

    def key_escape(self):
        self.input.value = self.init_value
        self.num.num = float(self.init_value)


rex = r"([+\-]?\s*(?:[0-9,]*)(?:[\.][0-9]*)?)"


def validNumSet(iv):
    res1 = txtpa(iv)
    return not any([type(n) != float for n in res1])


def txtp(txt):
    def f1(a, c):
        return a + c

    return reduce(f1, txtpa(txt), 0)


def txtpa(txt):
    def f1(s):
        s = re.sub(r"\s+", "", s)
        s = re.sub(r",", "", s)
        try:
            return round(float(s), 2)
        except Exception as e:
            return None

    def f2(n):
        return n is not None and math.isfinite(n)

    if not txt:
        return []
    txt = txt.strip()
    res1 = re.findall(rex, txt)
    res1 = map(f1, res1)
    res1 = filter(f2, res1)
    return res1


class TransactionDataTable(DataTable):
    pass


lv = TransactionDataTable()


def lv_update():
    lv.clear()
    lis = get_todays_transactions()
    for li in lis:
        lv.add_row(
            f"{li[0]:>3}",
            f"{li[1]:%c}",
            f"{li[2]:>8.2f}",
            f"{li[3]:>8.2f}",
        )
    lv.refresh()


class CompoundApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    LabeledInput {
        width: 80%;
        margin: 1;
    }
    Button {
        align: center bottom;
    }
    """
    total_assets = Reactive(0)

    def compute_total_assets(self):
        return sum(ao.labelinput.num.num for ao in drows.values())

    def on_load(self):
        load_asset_balances()

    def compose(self) -> ComposeResult:
        global lv
        self.composing = True
        for l in gen_widgets():
            yield l
        yield Button("Save", id="data_save")
        self.ta = Num(0)
        yield self.ta
        yield lv
        self.composing = False

    def on_mount(self):
        lv.add_column("asset")
        lv.add_column("time")
        lv.add_column("amount")
        lv.add_column("balance")
        lv_update()
        self.ta.num = self.total_assets
        

    def on_input_changed(self, ev):
        if self.composing:
            return
        eid = ev.input.id
        eiv = ev.input.value
        if eiv == "":
            eiv = None
        eiv2 = txtp(eiv)
        ao = drows[eid]
        if eiv2 != ao.balance:
            print(f"{ao.name} changed {ao.balance}->{eiv2}")
            ao.balance = eiv2
            ao.labelinput.num.num = eiv2
            # self.notify(str(ao.balance), timeout=2)
            self.ta.num = self.total_assets
        
    def on_button_pressed(self, msg):
        if msg.button.id == "data_save":
            update_asset_balances()
            self.log_balance_changes()
            for anm in drows.keys():
                ao = drows[anm]
                if ao.balance:
                    fvl = f"{ao.balance:>6.2f}"
                else:
                    fvl = ""
                ao.labelinput.input.value = fvl
                ao.labelinput.num.num = ao.balance
            lv_update()

    def log_balance_changes(self):
        global conn, cursor
        for anm in drows.keys():
            ao = drows[anm]
            cin = ao.labelinput.input
            ai = txtpa(cin.value)
            ai = list(ai)
            if ai is None or len(ai) == 0:
                return
            acc = ai[0]
            # see if initial/prev bal in, enter if not
            row = cursor.execute(
                """
                select * from blog where asset_id = ? order by time desc;
            """,
                [ao.id],
            ).fetchone()
            if row is not None:
                print(
                    f"{row['balance']=}, {acc=} row['balance']==acc {row['balance'] == acc}"
                )
            if row is None or row["balance"] != acc:
                if row is None or round(row["balance"], 2) != acc:
                    t = datetime.datetime.now()
                    cursor.execute(
                        """
                        insert into blog (time, asset_id, amount, balance) values (?,?,?,?);
                    """,
                        [t, ao.id, acc - row["balance"], round(acc, 2)],
                    )
                    conn.commit()
            for i in range(1, len(ai)):
                acc += ai[i]
                t = datetime.datetime.now()
                cursor.execute(
                    """
                    insert into blog (time, asset_id, amount, balance) values (?,?,?,?);
                """,
                    [t, ao.id, ai[i], round(acc, 2)],
                )
                conn.commit()


if __name__ == "__main__":
    app = CompoundApp()
    app.run()
