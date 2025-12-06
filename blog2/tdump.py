import ast
import bisect
import csv
import datetime
import io
import pickle
import re
import sqlite3
import sys
from pprint import pprint

from xxhash import xxh64

import sl_list


def field_hash(it):
    ho = xxh64()
    match it:
        case str():
            ho.update(it.encode())
        case list():
            bs = pickle.dumps(it)
            ho.update(bs)
        case _:
            raise ValueError
    return ho.hexdigest()


tks = []
comps_changed = False

conn = sqlite3.connect("finance.db")

cursor = conn.cursor()

"""
Use conn.create_function(name, num_args, func) to register your function.
name: The name you want to use for the function in your SQL queries (e.g., 'SQUARE_NUM').
num_args: The number of arguments your Python function expects.
func: The Python function itself.
"""

pre = [
    "ATM Balance Inquiry Fee",
    "ATM Cash Withdrawal",
    "ATM Withdrawal Fee",
    "Card Purch W/ Cash Back",
    "Card Purchase",
    "Cash Load",
    "Deposit",
    "Direct Deposit",
    "Fee for declined ACH debit",
    "Inactivity Fee",
    "Monthly Paper Statement Fee",
    "PIN Purchase",
    "PIN Purchase Transaction Fee",
    "Plan Fee",
    "Preauthorized Payment to PAYPAL for INST XFER",
    "Preauthorized Payment to PAYPAL for RETRY PYMT",
    "Preauthorized Payment to PAYPAL for VERIFYBANK",
    "Refund or Correction",
    "Return",
    "Signature Purchase",
    "Signature Purchase Transaction Fee",
    "Visa Money Transfer",
]
pre.sort(key=lambda t: t.lower())

cursor.execute("""
    CREATE TABLE IF NOT EXISTS transaction_types
    (
    [id]     TEXT PRIMARY KEY,
    [name] TEXT
    )
""")
cursor.execute("""
   DELETE from transaction_types;
""")

for r in pre:
    cursor.execute(
        """
        INSERT OR IGNORE INTO transaction_types (id, name) VALUES (?,?)
    """,
        [field_hash(r), r],
    )

# conn.commit()

pre.sort(reverse=True, key=len)
pprint(pre)


def find_type(d):
    ts = []
    for it in pre:
        if isinstance(it, list):
            for it2 in it:
                if it2.lower() in d.lower():
                    ts.append(it2)
        else:
            if it.lower() in d.lower():
                ts.append(it)
    # if len(ts)>1:
    # print(ts)
    return ts[0] if len(ts) > 0 else ""


def find_type2(d):
    t = find_type(d)
    match t:
        case "Signature Purchase" | "PIN Purchase" | "Card Purchase":
            t = "Debit Card Purchase"
    return t


def del_type(d):
    try:
        t = find_type(d)
        if len(t):
            d = re.sub(r"\s*" + t + r"\s*", " ", d, flags=re.IGNORECASE)
            d = d.strip()
        return d
    except Exception as e:
        print(e)
        raise e


ccor = {
    "29 ST M ATM": "29TH ST M ATM",
    "AMANTE COFFEE": "AMANTE UPTOWN COFFEE",
    "AMANTE UPTOWN": "AMANTE UPTOWN COFFEE",
    "AMAZON": "AMAZON.COM",
    "Amazon.com": "AMAZON.COM",
    "ATT PREPAID": "AT&T PREPAID",
    "BLACKJACK PIZ": "BLACKJACK PIZZA",
    "BLACKJACK": "BLACKJACK PIZZA",
    "BURGERKIN": "BURGER KING",
    "CARLS JR.": "CARL'S JR.",
    "CLINICA CAMPESINA FAM": "CLINICA CAMPESINA FAMILY CLINIC",
    "DDS LIQUOR & FO001100": "DDS LIQUOR & FOOD MART",
    "DOMINO'S": "DOMINO'S PIZZA",
    "DOORDASH BLACKJACK": "DOORDASH BLACKJACK PIZZA",
    "DOORDASH BLACKJACK PIZ": "DOORDASH BLACKJACK PIZZA",
    "DOORDASHDOUBLEDASH": "DOORDASH DOUBLEDASH",
    "DOORDASH CARLS JR.": "DOORDASH CARL'S JR.",
    "DUNKIN": "DUNKIN DONUTS",
    "EVERYDAY": "EVERYDAY STORE",
    "FATSHACK": "FAT SHACK",
    "FREDDIES HOT DOGS": "FREDDIE'S HOT DOGS",
    "FRONT RANGE LAUND": "FRONT RANGE LAUNDRY",
    "GOLDENSUN": "GOLDEN SUN",
    "GRUBHUBBLACKJACKPIZZA": "GRUBHUB BLACKJACK PIZZA",
    "GRUBHUBFATSHACK": "GRUBHUB FAT SHACK",
    "GRUBHUBKFC": "GRUBHUB KFC",
    "GRUBHUBMCDONALDS": "GRUBHUB MCDONALD'S",
    "ILLEGAL PETES": "ILLEGAL PETE'S",
    "ILLEGAL PETE S": "ILLEGAL PETE'S",
    "JACK IN THE B": "JACK IN THE BOX",
    "King Soopers": "KING SOOPERS",
    "LOGAN?S ESPRESSO CAFE": "LOGAN'S ESPRESSO CAFE",
    "LOGAN`S ESPRESSO CAFE": "LOGAN'S ESPRESSO CAFE",
    "MASABI RTD": "MASABI LLC RTD",
    "MCDONALDS": "MCDONALD'S",
    "McDonalds": "MCDONALD'S",
    "MUSTARDS LAST STAND": "MUSTARD'S LAST STAND",
    "NOODLES & CO": "NOODLES & COMPANY",
    "NOODLES & COM": "NOODLES & COMPANY",
    "NOODLESCO": "NOODLES & COMPANY",
    "RIPPLE FROZEN YO": "RIPPLE FROZEN YOGURT",
    "ROCKYMOUNTAIN SENIORCA": "ROCKY MOUNTAIN SENIOR CARE",
    "RockyMountain SeniorCa": "ROCKY MOUNTAIN SENIOR CARE",
    "TIERRA Y FUEGO TAQUER": "TIERRA Y FUEGO TAQUERIA",
    "WALGREENS": "WALGREEN'S STORE",
    "WALGREENS STORE": "WALGREEN'S STORE",
    "Walmart.com": "WALMART.COM",
    "WENDY S": "WENDY'S",
    "WENDYS": "WENDY'S",
    "WHOLEFDS": "WHOLE FOODS",
    "YSI Hilltop": "YSI HILLTOP",
}


comps = []
comps.append("29 ST M ATM")
comps.append("29TH ST M ATM")
comps.append("7-ELEVEN")
comps.append("AMANTE COFFEE")
comps.append("AMANTE UPTOWN")
comps.append("AMAZON")
comps.append("Amazon Prime")
comps.append("AMAZON.COM")
comps.append("Amazon.com")
comps.append("AMK HC CAFE BCH")
comps.append("AMTRAK")
comps.append("AMZN Mktp")
comps.append("ARAMARK")
comps.append("AT&T PREPAID")
comps.append("ATR AIRSPY")
comps.append("ATT PREPAID")
comps.append("B TOWN WINE + SPIRITS")
comps.append("BA Withdrawal")
comps.append("BASELINE LIQUOR")
comps.append("BESTBUY")
comps.append("BITTERSWEET")
comps.append("BOULDER CONVENIENCE")
comps.append("BOULDER GENERAL STORE")
comps.append("BOULDER ROOT-634825")
comps.append("BOVAS MARKET")
comps.append("BREADWORKS")
comps.append("BREWING MARKET COFFEE")
comps.append("BROADWAY WINE & SPIRIT")
comps.append("BURGERKIN")
comps.append("CELL VILLE")
comps.append("CHASE")
comps.append("Chitester Donald")
comps.append("CIRCLE K")
comps.append("CLINICA CAMPESINA FAM")
comps.append("CLOUDVAPES.COM")
comps.append("COCA COLA")
comps.append("CODHS")
comps.append("COMCAST/XFINITY")
comps.append("CR TG 2 VG")
comps.append("CREDENCE-AMR")
comps.append("DASHMART")
comps.append("DASHPASS")
comps.append("DDS LIQUOR & FO001100")
comps.append("DDS LIQUOR & FOOD MART")
comps.append("Direct Express®")
comps.append("Domestic")
comps.append("DOMINO'S")
comps.append("DOORDASH BLACKJACK")
comps.append("DOORDASH BLACKJACK PIZ")
comps.append("DOORDASH CARLS JR.")
comps.append("DOORDASH JETSPIZZA")
comps.append("DOORDASHDOUBLEDASH")
comps.append("Doozy Duds")
comps.append("DOTS DINER ON THE HILL")
comps.append("DUNKIN")
comps.append("eBay")
comps.append("EFT")
comps.append("EINSTEIN BROS BAGELS")
comps.append("EVERYDAY")
comps.append("EVERYDAY STORE")
comps.append("FAT SHACK")
comps.append("FATSHACK")
comps.append("FORMOSA BAKERY LLC")
comps.append("FREDDIES HOT DOGS")
comps.append("FRONT RANGE LAUND")
comps.append("GOLDENSUN")
comps.append("GOODWILL")
comps.append("GOOGLE MetaCtrl")
comps.append("GOOGLE PLAY")
comps.append("GOOGLE rhmsoft")
comps.append("GOOGLE SpRemote")
comps.append("GREAT CLIPS")
comps.append("GRUBHUBBLACKJACKPIZZA")
comps.append("GRUBHUBFATSHACK")
comps.append("GRUBHUBKFC")
comps.append("GRUBHUBMCDONALDS")
comps.append("HERSHEYS")
comps.append("IHOP")
comps.append("ILLEGAL PETE S")
comps.append("ILLEGAL PETE'S")
comps.append("ILLEGAL PETES")
comps.append("INSTACART")
comps.append("JACK IN THE B")
comps.append("JINNYS MARKET")
comps.append("KFC")
comps.append("KIM'S FOOD TO GO")
comps.append("KING SOOPERS")
comps.append("King Soopers")
comps.append("kroger_ns")
comps.append("LINDSAY'S")
comps.append("LITTLE TIBET")
comps.append("LOGAN?S ESPRESSO CAFE")
comps.append("LOGAN`S ESPRESSO CAFE")
comps.append("LUCKY'S")
comps.append("LYFT")
comps.append("MASABI LLC RTD")
comps.append("MASABI RTD")
comps.append("MCDONALD'S")
comps.append("MCDONALDS")
comps.append("McDonalds")
comps.append("MCGUCKIN HARDWARE")
comps.append("MOE'S BROADWAY BAGEL")
comps.append("MUSTARD'S LAST STAND")
comps.append("MUSTARDS LAST STAND")
comps.append("NETSPEND")
comps.append("NOODLES & CO")
comps.append("NOODLES & COM")
comps.append("NOODLESCO")
comps.append("NORTH BOULDER LIQUOR")
comps.append("NOW MOBILE")
comps.append("OZO COFFEE COMPANY")
comps.append("PAI ISO")
comps.append("PAYPAL DOORDASH")
comps.append("PAYPAL FACEBOOKPAY")
comps.append("PAYPAL for INST XFER")
comps.append("PAYPAL for TRANSFER")
comps.append("PAYPAL for VERIFYBANK")
comps.append("PAYPAL GITHUB")
comps.append("PAYPAL JUSTANSWER")
comps.append("PAYPAL MLEARY")
comps.append("PAYPAL REI")
comps.append("PAYPAL SQUARECIRCU")
comps.append("PEARL CONVENIENCE")
comps.append("PEARL MOBILE-601545")
comps.append("PHARMACA")
comps.append("PIGTRAIN COFFEE")
comps.append("RD CORP")
comps.append("REI #44")
comps.append("RIPPLE FROZEN YO")
comps.append("RockyMountain SeniorCa")
comps.append("RTD BRT BLDR TRANSIT")
comps.append("SANTIAGOS MEXICAN REST")
comps.append("SEI")
comps.append("SHELL")
comps.append("SHELL OIL")
comps.append("SHELL SERVICE STATION")
comps.append("SMOKER FRIENDLY")
comps.append("SNARFS AT THE TABLE")
comps.append("SNARFS BURGER")
comps.append("SNOOZE")
comps.append("Social Security")
comps.append("SPK SPOKEO SEARCH")
comps.append("STARBUCKS")
comps.append("STARBUCKS STORE")
comps.append("SUBWAY")
comps.append("Subway")
comps.append("SWEET COW")
comps.append("TACO BELL")
comps.append("TARGET")
comps.append("TASKER ON TASKRABBIT")
comps.append("TELYRX LLC")
comps.append("THE FITTER")
comps.append("The Fitter")
comps.append("THE UNDERGROUND PIPES")
comps.append("TIERRA Y FUEGO TAQUER")
comps.append("TIERRA Y FUEGO TAQUERIA")
comps.append("TSE K&G")
comps.append("UNIVERSITY HILLS MARKET")
comps.append("US7ELEVEN-FCTI")
comps.append("VILLAGE MOBI-643038")
comps.append("WALGREENS")
comps.append("WALGREENS STORE")
comps.append("Walmart.com")
comps.append("WENDY S")
comps.append("WENDY'S")
comps.append("WENDYS")
comps.append("WG006022")
comps.append("WHOLEFDS")
comps.append("YOUANDMEE")
comps.append("YSI HILLTOP")
comps.append("YSI Hilltop")
comps.sort(key=lambda it: it[0].lower() if type(it) == list else it.lower())
pprint(comps)


def flatten_comps():
    global comps
    tmp = []
    for it in comps:
        if type(it) == list:
            for it2 in it:
                tmp.append(it2)
        else:
            tmp.append(it)
    comps = tmp
    comps.sort(key=lambda it: it.lower())
    pprint(comps)


cursor.execute("""
    CREATE TABLE IF NOT EXISTS companies
    (
    [id]     TEXT PRIMARY KEY,
    [name] TEXT
    )
""")


def load_comps_from_csv():
    global comps
    comps.clear()
    with open("finance-companies.csv", "rt", newline="") as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i > 0:
                comps.append(row[1])
    pprint(comps)


def update_comps():
    cursor2 = conn.cursor()
    cursor2.execute("""
    DELETE from companies;
    """)
    for c in comps:
        cn = c if not type(c) == list else str(c)
        cfi = c if not type(c) == list else c[0]
        cursor2.execute(
            """
        INSERT OR IGNORE INTO companies (id, name) VALUES (?, ?)
        """,
            [field_hash(cfi), cn],
        )
    cursor2.close()


# conn.commit()


def write_comps_to_text():
    with open("finance-comps.txt", "wt") as file:
        for c in comps:
            if "[" in c:
                c = ast.literal_eval(c)
            dt = '"' + str(c) + '"' if not type(c) == list else str(c)
            txt = "comps.append(" + dt + ")\n"
            file.write(txt)


ts = []
ts.append(["LEVELUP", "WENDYS", "10498518"])
ts.append(["LEVELUP", "WENDYS", "10512056"])
ts.append(["MASABI", "LLC", "RTD", "DENVER"])
ts.append(["MASABI", "RTD"])
ts.append(["MUSTARD'S", "LAST", "STAND"])
ts.append(["BAGELS", "2445"])
ts.append(["DOORDASH", "DOUBLEDASH"])


def split_tokens(d):
    for l1 in ts:
        t1 = "".join(l1)
        if t1 in d:
            d = d.replace(t1, " ".join(l1), 1)
            return d
    for l1 in ts:
        t1 = "-".join(l1)
        if t1 in d:
            d = d.replace(t1, " ".join(l1), 1)
            return d
    for l1 in ts:
        t1 = "_".join(l1)
        if t1 in d:
            d = d.replace(t1, " ".join(l1), 1)
            return d
    return d


def all_combs(lst):
    for ni in range(len(lst), 0, -1):
        for i in range(0, len(lst) - ni + 1):
            tl = " ".join(lst[i : i + ni])
            yield tl


def find_comp(d):
    global comps_changed
    # print('-'*10)
    global tks
    try:
        if find_type(d).lower() == "plan fee":
            d = "NETSPEND " + d
        d = del_type(d)
        d = split_tokens(d)
        tks = re.split(r"[\s\*]+", d)

        if len(tks) == 0 or len(tks[0]) == 0:
            return str(tks)
        for cmb in all_combs(tks):
            if cmb in comps:
                # print('match')
                if cmb in ccor:
                    cmb = ccor[cmb]
                return cmb
        rv = sl_list.main(list(all_combs(tks)))
        if rv:
            if not rv in comps:
                comps.append(rv)
                comps.sort(key=lambda it: it.lower())
                update_comps()
            if rv.upper() in ccor:
                rv = ccor[rv.upper()]
            return rv
        else:
            return str(tks)
    except Exception as e:
        print(e)
        raise e


def month(day):
    d = datetime.datetime.strptime(day, "%Y-%m-%d")
    return (d.year - 2016) * 12 + d.month


def week(day):
    i = datetime.datetime.strptime(day, "%Y-%m-%d").isocalendar()
    return (i.year - 2016) * 52 + i.week


def we_date(day):
    i = datetime.datetime.strptime(day, "%Y-%m-%d")
    weekday = i.weekday()
    days_until_saturday = (5 - weekday + 7) % 7  # Adding 7 to handle negative results
    week_ending_date = i + datetime.timedelta(days=days_until_saturday)
    return week_ending_date.strftime("%Y-%m-%d")  # Return only the date part


def income(amt, ttype):
    if amt > 0:
        if ttype == "Cash Load":
            return 0
        return amt
    else:
        return 0


def expense(amt, ttype):
    if amt < 0:
        if ttype == "Card Purch W/ Cash Back":
            return 0
        return amt
    else:
        return 0


conn.create_function("ft", 1, find_type)
conn.create_function("ft2", 1, find_type2)
conn.create_function("dt", 1, del_type)
conn.create_function("fc", 1, find_comp)
conn.create_function("wk", 1, week)
conn.create_function("wed", 1, we_date)
conn.create_function("mth", 1, month)
conn.create_function("inc", 2, income)
conn.create_function("exp", 2, expense)


def dump_table(tbl):
    global ft
    # Get the CREATE TABLE statement
    print("-" * 10 + "Table: " + tbl + "-" * 10, file=ft)

    cursor.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", [tbl]
    )
    create_statement = cursor.fetchone()[0]
    print("-" * 10 + "Create Statement" + "-" * 10, file=ft)
    print(create_statement, file=ft)

    if tbl == "transactions":
        cursor.execute(
            "SELECT sum(amount), fc(description), count(amount) FROM "
            + tbl
            + " group by fc(description), amount<0"
            + " order by sum(amount);"
        )
    else:
        cursor.execute("SELECT * FROM " + tbl + ";")
    dr = list(cursor.description)
    th = []
    for tn in dr:
        th.append(tn[0])
    print("-" * 10 + "Description" + "-" * 10, file=ft)
    pprint(th, stream=ft)

    # print('-'*10 + "CSV" + '-'*10)
    output_buffer = io.StringIO()
    writer = csv.writer(output_buffer)
    writer.writerow(th)
    rows = cursor.fetchall()
    for r in rows:
        writer.writerow(r)
    csv_string = output_buffer.getvalue()
    output_buffer.close()
    # print(csv_string)
    with open(f"finance-{tbl}.csv", "wt") as f:
        f.write(csv_string)


# load_comps_from_csv()

ft = open("finance-tables.txt", "wt")
try:
    dump_table("source")
    dump_table("asset")
    dump_table("transactions")
    dump_table("transaction_types")
    dump_table("companies")
finally:
    ft.close()

# flatten_comps()
update_comps()
write_comps_to_text()

conn.commit()
conn.close()
