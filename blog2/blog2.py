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
            ),
            id=anm,
        )
        # ao.labelinput = lblin
        yield lblin


def find_yesterdays_ending_balances():
    global conn, cursor
    c1 = cursor.execute("""
        select asset_id from asset;
    """)
    rows = c1.fetchall()
    ydd = datetime.date.today() - datetime.timedelta(days=8)
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
    sdd = datetime.date.today() - datetime.timedelta(days=8)
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


def update_asset_balance(ao):
    global conn, cursor
    row = cursor.execute(
        """
            select * from asset where asset_id = ?;
        """,
        [ao.id],
    ).fetchone()
    if row:
        rcb = row["current_balance"]
        if rcb != ao.balance:
            cursor.execute(
                """
                   update asset set current_balance = ?
                   where asset_id = ?
                """,
                [ao.balance, ao.id],
            )
            conn.commit()


def update_asset_balances():
    global conn, cursor
    for anm in drows.keys():
        ao = drows[anm]
        update_asset_balance(ao)


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
        width: 80%;
        margin: 1;
        layout: horizontal;
        height: 4;
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

    def __init__(self, label: Label, input: Input, id=None) -> None:
        self.label = label
        self.input = input
        self.init_value = input.value
        self.num = Num(round(float(input.value), 2))
        super().__init__(id=id)

    def compose(self) -> ComposeResult:
        yield self.label
        yield self.input
        yield self.num

    def key_escape(self):
        self.input.value = self.init_value
        self.num.num = float(self.init_value)


rex1 = r"([+\-]?\s*(?:[0-9,]*)(?:[\.][0-9]*)?)"
rex2 = r"([a-z]{2})"
rex3 = "(?:" + rex1[1:] + "|(?:" + rex2[1:]


def validNumSet(iv):
    res1 = txtpa(iv)
    return not any([type(n) != float for n in res1])


def txtp(txt):
    def f1(a, c):
        print(f"HEY! {a=} {type(a)=}")
        print(f"HEY! {c=} {type(c)=}")
        return a + c

    return reduce(f1, txtpa(txt), 0)


nt = {
    "cr": 1,
    "de": 2,
    "ti": 3,
    "to": 4,
    "rr": 5,
}

ntc = 0


class CR(float):
    pass


class DE(float):
    pass


class TI(float):
    pass


class TO(float):
    pass


class RR(float):
    pass


def txtpa(txt):
    def f1(s):
        global ntc
        print(f"txtpa {txt=}")
        if type(s) == tuple:
            raise ValueError()
        s = re.sub(r"\s+", "", s)
        s = re.sub(r",", "", s)
        print(f"{s=} {rex2=}")
        if re.match(rex2, s):
            if s in nt:
                ntc = nt[s]
            return None
        if s == "":
            return None
        val = None
        try:
            val = round(float(s), 2)
            print(f"{val=} {ntc=}")
            ntc2, ntc = ntc, 0
            match ntc2:
                case 0:
                    if val > 0:
                        return CR(val)
                    elif val < 0:
                        return DE(val)
                    else:
                        return None
                case 1:
                    return CR(val)
                case 2:
                    return DE(val)
                case 3:
                    return TI(val)
                case 4:
                    return TO(val)
                case 5:
                    return RR(val)
        except Exception as e:
            print(f"{e=}")
            return None

    def f2(n):
        return n is not None and math.isfinite(n)

    if not txt:
        return []
    ntc = 0
    txt = txt.strip()
    res1 = re.findall(rex3, txt)
    print(f"{res1=}")
    res1 = map(f1, res1)
    res1 = filter(f2, res1)
    return res1


lv = DataTable()


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
    Button {
        align: center bottom;
    }
    """
    total_assets = Reactive(0)

    def compute_total_assets(self):
        lis = self.query(LabeledInput)
        ta = 0
        for li in lis:
            if li.id in drows:
                ta += li.num.num
        return ta

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
        li = ev.input.parent
        if li.id in drows:
            li.num.num = txtp(ev.input.value)
            self.ta.num = self.total_assets

    def update_labeledinput(self, anm):
        ao = drows[anm]
        if ao.balance:
            fvl = f"{ao.balance:>6.2f}"
        else:
            fvl = ""
        li = self.query_one("#" + anm, LabeledInput)
        li.input.value = fvl
        li.num.num = ao.balance

    def on_button_pressed(self, msg):
        if msg.button.id == "data_save":
            self.log_balance_changes()
            lv_update()

    def log_balance_changes(self):
        global conn, cursor
        lis = self.query(LabeledInput)
        for li in lis:
            if li.id not in drows:
                continue
            ao = drows[li.id]
            cin = li.input
            ai = list(txtpa(cin.value))
            if ai is None or len(ai) == 0:
                continue
            acc = ai[0]
            # see if initial/prev bal in, enter if not
            row = cursor.execute(
                """
                select * from blog where asset_id = ? order by time desc;
            """,
                [ao.id],
            ).fetchone()
            if row is None:
                t = datetime.datetime.now()
                cursor.execute(
                    """
                        insert into blog (time, asset_id, amount, balance) values (?,?,?,?);
                    """,
                    [t, ao.id, 0, round(acc, 2)],
                )
                conn.commit()
            elif row["balance"] != acc:
                if round(row["balance"], 2) != acc:
                    t = datetime.datetime.now()
                    cursor.execute(
                        """
                        insert into blog (time, asset_id, amount, balance) values (?,?,?,?);
                    """,
                        [t, ao.id, acc - row["balance"], round(acc, 2)],
                    )
                    conn.commit()
                    ao.balance = round(acc, 2)
                    update_asset_balance(ao)
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
                ao.balance = round(acc, 2)
                update_asset_balance(ao)
            self.update_labeledinput(li.id)


if __name__ == "__main__":
    app = CompoundApp()
    app.run()
