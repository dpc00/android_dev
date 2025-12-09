import csv
import datetime

filename = "bankstatementconverter.com.csv"
statement_time = datetime.datetime(2025, 9, 1).timestamp() * 1000

# with open(filename, 'r', newline='') as csvfile:
#     csv_reader = csv.reader(csvfile)

#     # Read the header row (optional)
#     # header = next(csv_reader)
#     # print(f"Header: {header}")

#     # Iterate over the remaining rows
#     for row in csv_reader:
#         print(row)

# print('-------------------')

cntr = 1


def ridfunc():
    global cntr
    id = statement_time + cntr
    cntr += 1
    return id


with open(filename, "r", newline="") as csvfile:
    dict_reader = csv.DictReader(csvfile)
    income = []
    expense = []
    for row in dict_reader:
        rd = {}
        if "Amount" in row and row["Amount"] != "":
            rd["Amount"] = float(row["Amount"])
            if "Description" in row:
                ts = row["Description"].split(": ")
                if ts[0] == "Debit":
                    rd["Amount"] = -rd["Amount"]
                rd["Description"] = ts[1]
                rd["Date"] = datetime.datetime.strptime(
                    row["ï»¿Date Posted"], "%m/%d/%Y"
                )
            # print(rd)
            if rd["Amount"] < 0:
                rd["TID"] = ridfunc()
                expense.append(rd)
            elif rd["Amount"] > 0:
                rd["TID"] = ridfunc()
                income.append(rd)
    # print('=========')
    print("Income")
    income = sorted(income, key=lambda j: j["Date"])
    for i in income:
        print(i)

    print("Expense")
    expense = sorted(expense, key=lambda j: j["Date"])
    for i in expense:
        print(i)
