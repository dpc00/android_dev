from datetime import date, timedelta


def days_left():
    d1 = date.today()
    d2 = d1.replace(day=28)
    d3 = d2 - d1
    if d3.days < 0:
        d2 = d2.replace(month=d2.month + 1)
        d3 = d2 - d1
    print(d3)


f()
