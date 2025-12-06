import datetime
import locale
import math
import re
import sqlite3
import sql3date
from functools import reduce

from textual import on
from textual.app import App, ComposeResult
from textual.containers import CenterMiddle, Horizontal, VerticalScroll
from textual.validation import Function, Number, ValidationResult, Validator
from textual.widget import Widget
from textual.widgets import Button, Input, Label, ListItem, ListView, Pretty

drows = {}

dayrows = []

dbstarted = False


def dbstart():
    global conn, cursor, dbstarted
    if dbstarted:
        return
    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        create table if not exists blog
        (
        time TIMESTAMP primary key default CURRENT_TIMESTAMP,
        asset_id INTEGER,
        balance NUMERIC
     );
    """)
    cursor.execute("""
        create table if not exists blog
        (
        time TIMESTAMP primary key default CURRENT_TIMESTAMP,
        asset_id INTEGER,
        balance NUMERIC
        )
        """)
    dbstarted = True


dbstart()


def load_asset_balances():
    global conn, cursor
    dbstart()
    rows = cursor.execute("""
        select * from asset order by name;
    """).fetchall()
    for ass in rows:
        nm = ass["name"]
        vl = ass["current_balance"]
        # print(f"{vl=} {type(vl)}")
        aid = ass["asset_id"]
        drows[nm.replace(" ", "")] = (nm, vl, aid)


def find_yesterdays_ending_balances():
    ydd = datetime.date.today() - datetime.timedelta(days=1)
    # yydd = datetime.date.today() - datetime.timedelta(days=2)
    sr = cursor.execute(
        """
        select * from blog
        where date(time)<=?
        order by time desc
    """,
        [ydd],
    )
    rws = sr.fetchall()
    db = {}
    for r in rws:
        aid = r["asset_id"]
        if aid not in db:
            db[aid] = r["balance"]
    return db


def get_todays_transactions():
    db = find_yesterdays_ending_balances()
    aacc = db.copy()
    tdd = datetime.date.today()
    sr = cursor.execute(
        """
        select time, asset_id, balance from blog
        where date(time)=?
        order by time asc;
    """,
        [tdd],
    )
    rws = sr.fetchall()
    trs = []
    for r in rws:
        aid = r["asset_id"]
        amt = round(aacc[aid] - r["balance"], 2)
        aacc[aid] = r["balance"]
        tt = r["time"][:16]
        trs.append((aid, tt, amt))
    return trs


def update_asset_balances():
    for anm in drows.keys():
        nm, vl, aid = drows[anm]
        row = cursor.execute(
            """
            select * from asset where asset_id = ?;
        """,
            [aid],
        ).fetchone()
        if row:
            rcb = row["current_balance"]
            print(f"current_balance {rcb} {type(rcb)} vl {vl} {type(vl)}")
            if rcb != vl:
                print(f"row {aid}:{nm} needs update {rcb}->{vl}")
                cursor.execute(
                    """
                   update asset set current_balance = ?
                   where asset_id = ?
                """,
                    [vl, aid],
                )
                conn.commit()


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
        super().__init__()

    def compose(self) -> ComposeResult:
        yield self.label
        yield self.input

    def key_escape(self):
        self.input.value = self.init_value


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


class TransactionListView(ListView):
    def key_backspace(self):
        # find last entry
        c1 = cursor.execute("""
            select rowid, time, asset_id, balance from blog
            order by time desc;
        """)
        mr = c1.fetchone()
        rid = mr["rowid"]
        aid = mr["asset_id"]
        # delete last entry
        c2 = cursor.execute(
            """
            delete from blog
            where rowid = ? and asset_id = ?;
        """,
            [rid, aid],
        )
        conn.commit()
        # rollback balance of asset
        td = datetime.date.today()
        c3 = cursor.execute(
            """
            select * from blog
            where date(time)=? and asset_id=?
            order by time desc;
        """,
            [td, aid],
        )
        rw = c2.fetchone()
        for dr in drows:
            if dr[2] == aid:
                dr[1] = rw["balance"]
        update_asset_balances()


lv = TransactionListView()


def lv_update():
    lv.clear()
    lis = get_todays_transactions()
    for li in lis:
        li1 = Label(str(li[0]) + " " + li[1] + " " + str(li[2]))
        lv.append(ListItem(li1))
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

    def compose(self) -> ComposeResult:
        global lv
        self.composing = True
        load_asset_balances()

        for anm in drows.keys():
            nm, vl, aid = drows[anm]
            if vl:
                vl = f"{vl:>4.2f}"
            yield LabeledInput(
                Label(nm),
                Input(
                    value=vl,
                    id=anm,
                    validators=[Function(validNumSet, "Not a valid amount set!")],
                ),
            )
        yield Pretty([])
        yield Button("Save", id="data_save")
        yield lv
        self.composing = False

    def on_mount(self):
        lv_update()

    def on_input_changed(self, ev):
        if self.composing:
            return
        eid = ev.input.id
        eiv = ev.input.value
        if eiv == "":
            eiv = None
        eiv2 = txtp(eiv)
        nm, vl, aid = drows[eid]
        if eiv2 != vl:
            print(f"{nm} changed {vl}->{eiv2}")
            drows[eid] = (nm, eiv2, aid)
            self.notify(str(eiv2), timeout=2)
        # Updating the UI to show the reasons why validation failed
        if not ev.validation_result.is_valid:
            self.query_one(Pretty).update(ev.validation_result.failure_descriptions)
        else:
            self.query_one(Pretty).update([])

    def on_button_pressed(self, msg):
        if msg.button.id == "data_save":
            update_asset_balances()
            self.log_balance_changes()
            for anm in drows.keys():
                nm, vl, aid = drows[anm]
                if vl:
                    vl = f"{vl:>4.2f}"
                self.query_one("#" + anm, Input).value = vl
            lv_update()

    def log_balance_changes(self):
        global conn, cursor
        for anm in drows.keys():
            cin = self.query_one("#" + anm, Input)
            ai = txtpa(cin.value)
            ai = list(ai)
            if ai is None or len(ai) == 0:
                return
            acc = ai[0]
            aid = drows[anm][2]
            # see if initial/prev bal in, enter if not
            row = cursor.execute(
                """
                select * from blog where asset_id = ? order by time desc;
            """,
                [aid],
            ).fetchone()
            if row is None or row["balance"] != acc:
                t = datetime.datetime.now()
                cursor.execute(
                    """
                    insert into blog (time, asset_id, balance) values (?,?,?);
                """,
                    [t, aid, acc],
                )
            for i in range(1, len(ai)):
                acc += ai[i]
                t = datetime.datetime.now()
                cursor.execute(
                    """
                    insert into blog (time, asset_id, balance) values (?,?,?);
                """,
                    [t, aid, acc],
                )
            conn.commit()


if __name__ == "__main__":
    app = CompoundApp()
    app.run()
