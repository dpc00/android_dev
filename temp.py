import subprocess
import sys
from datetime import date, timedelta
import json

result = subprocess.run(
    ["go/bin/plaid-cli", "accounts", "ns"], capture_output=True, text=True
)
ja = json.loads(result.stdout)

print(ja[0]["balances"])
print()


d2 = date.today()
d1 = d2 - timedelta(days=2)

result = subprocess.run(
    [
        "go/bin/plaid-cli",
        "transactions",
        "ns",
        "--from",
        str(d1),
        "--to",
        str(d2),
        "--output-format",
        "json",
    ],
    capture_output=True,
    text=True,
)

trans = json.loads(result.stdout)

tot = {}

for item in trans:
    amnt = item["amount"]
    if amnt > 0:
        d = item["date"]
        if d in tot:
            tot[d] += amnt
        else:
            tot[d] = amnt
        print(
            item["date"],
            "$" + str(item["amount"]),
            item["merchant_name"],
            item["category"],
        )
        print()

print()

for d, a in tot.items():
    print(d, a)
