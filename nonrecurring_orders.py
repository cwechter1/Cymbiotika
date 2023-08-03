import requests
import json
from datetime import datetime, timedelta
import time


start_time = datetime(2022, 6, 1)
current_time = start_time
end_time = datetime(2022, 11, 9)


orders = []
recurring_orders = 0
page = 0
l = 250
store_url = "https://api.rechargeapps.com/orders"
while current_time < end_time:
    minim = current_time.strftime("%Y-%m-%dT00:00:00-07:00")
    maxim = current_time.strftime("%Y-%m-%dT23:59:59-07:00")
    headers = {
        "X-Recharge-Access-Token": "sk_1x1_c260e4b1c7889aec8d19c917446e80f4c2861173e13fd51a1a90751b0a34af01"
    }
    params = {
        "page": page,
        "sort_by": "created_at-desc",
        "created_at_min": minim,
        "created_at_max": maxim,
        "limit": 250,
    }
    request = requests.get(store_url, headers=headers, params=params)
    data = request.json()
    l += len(data["orders"])

    for ind in data["orders"]:
        if ind["type"] == "RECURRING":
            recurring_orders += 1
    time.sleep(2)
    print(recurring_orders)
    print(l)
    current_time += timedelta(days=1)


print(recurring_orders)
print(l)
