from flask import Blueprint, render_template, request, make_response, jsonify
import pickle
from datetime import date, timedelta
import config
# import plaidapi

print("-var cfg")
cfg = config.Config("config/development.ini")
# db = transactionsdb.TransactionsDB(cfg.get_dbfile())
# print("-var plaid")
# plaid = plaidapi.PlaidAPI(**cfg.get_plaid_client_config())

# def getbal():
#    print("-getbal")
#    bal = plaid.get_account_balance(cfg.get_account_access_token("NetSpend"))
#    bal = bal[0].balance_current
#    print("NetSpend Balance is",bal)
#    return bal

# def gettrans():
#    print("-gettrans")
#    d2 = date.today()
#    d1 = d2 - timedelta(days=2)
#    ts = plaid.get_transactions(cfg.get_account_access_token("NetSpend"),d1,d2)
#    return list(map(str, ts))

print("-var views")
views = Blueprint("views", __name__)


def days_left(dom):
    print("-days_left")
    d1 = date.today()
    d2 = d1.replace(day=dom)
    d3 = d2 - d1
    if d3.days < 1:
        d2 = d2.replace(month=d2.month + 1)
        d3 = d2 - d1
    # print(d3.days, "days left til", d2)
    return d3.days


print("-var data")
data = {"OAP": 0, "SSI": 0, "SNAP": 0, "DA": 0, "DL1": 0, "DL2": 0, "TR": []}

# def check_bal():
#    global data
#    print("-check_bal")
#    bal = getbal()
#    if data['OAP'] > bal:
#        data['OAP'] = bal


def loaddata():
    global data
    print("-loaddata")
    datapf = "data.pp"
    try:
        with open(datapf, "rb") as fh:
            data = pickle.load(fh)
    except Exception as e:
        print("loaddata failed", e)


def savedata():
    global data
    print("-savedata")
    datapf = "data.pp"
    try:
        with open(datapf, "wb") as fh:
            pickle.dump(data, fh)
    except Exception as e:
        print("savedata failed", e)


def calcDA():
    global data
    print("-calcDA")
    dl1 = days_left(28)
    dl2 = days_left(3)
    data["DA"] = data["OAP"] / dl1 + data["SSI"] / dl2
    data["DA"] = round(data["DA"], 2)
    data["DL1"] = dl1
    data["DL2"] = dl2


# def fetchTR():
#    global data
#    print("-calcTR")
#    data['TR'] = gettrans()


def save(request):
    global data
    print("-save")
    # Print the form data to the console
    for key, value in request.form.items():
        print(f"{key}: {value}")
        data[key] = float(value)
    savedata()


@views.route("/", methods=["GET", "POST"])
def home_page():
    global data
    print("-home_page")
    if request.method == "POST":
        save(request)
    else:
        loaddata()
    # check_bal()
    calcDA()
    # fetchTR()
    h = render_template("home.html", data=data)
    with open("temp.html", "w") as fh:
        fh.write(h)
    return h
