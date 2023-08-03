# # from db.models import Base, Conversion
# from db import engine
from datetime import datetime
import requests
import json
from datetime import timedelta
from datetime import date

from sqlalchemy.orm import sessionmaker

print("start")

# def get_data(event,lambda_context):

today = date.today()

y = today - timedelta(days=1)

minim = y.strftime("%Y-%m-%dT00:00:00-07:00")
maxim = y.strftime("%Y-%m-%dT23:59:59-07:00")

page = 0

orders = []

url = "https://mitolife.myshopify.com"

headers = {
    "X-Shopify-Access-Token": "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",
    "Content-Type": "application/json",
}

params = {
    "status": "any",
    "processed_at_min": minim,
    "processed_at_max": maxim,
    "limit": 250,
}

response = requests.get(
    f"{url}/admin/api/2023-07/orders.json?", headers=headers, params=params
)

data = response.json()

orders.append(data)

if "Link" in response.headers:
    head = response.headers["Link"]

    link = head.split(" ")

    # print(link)

    lin = link[0]

    l = lin[1:-2]

    page = page + 1

    # print(page)

    while "next" in head:
        # print(True)

        page = page + 1

        # print(page)

        y = requests.get(l, headers=headers)

        datas = y.json()

        orders.append(datas)

        head = y.headers["Link"]

        link = head.split(" ")

        # print(link)

        lin = link[-2]

        l = lin[1:-2]

# print(orders)

# Base.metadata.create_all(engine)

# Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# with Session() as session:
for order in orders:
    o = order["orders"]

    for in_o in o:
        ind = in_o

        cust_id = ind["customer"]["id"]
        app_id = ind["app_id"]
        order_date = ind["created_at"]
        order_date = datetime.strptime(order_date, "%Y-%m-%dT%H:%M:%S%z")
        order_date = order_date - timedelta(hours=7)
        # print(type(order_date), order_date)
        order_name = ind["name"]
        total = ind["total_price"]
        order_status = ind["financial_status"]
        email = ind["contact_email"]

        tags = ind["tags"]

        dis = ind["discount_codes"]

        # print(dis)

        if len(dis) == 0:
            discount = "N/A"
            discount_amount = 0

        if len(dis) != 0:
            for d in dis:
                discount = d["code"]
                discount_amount = d["amount"]

        cust = ind["customer"]

        print(cust)

        email = cust["email"]
        customer_created_date = cust["created_at"]
        customer_created_date = datetime.strptime(
            customer_created_date, "%Y-%m-%dT%H:%M:%S%z"
        )
        customer_created_date = customer_created_date - timedelta(hours=7)
        # print(type(customer_created_date), customer_created_date)

        state = cust["state"]
        # order_count = cust['orders_count']

        cust_response = requests.get(
            f"{url}/admin/api/2023-04/customers/{cust_id}.json",
            headers=headers,
            params=params,
        )
        cust_info = cust_response.json()
        order_count = cust_info["customer"]["orders_count"]

        # c = Conversion(
        #     app_id=app_id,
        #     order_date=order_date,
        #     order_name=order_name,
        #     order_total=total,
        #     order_status=order_status,
        #     discount_name=discount,
        #     discount_amount=discount_amount,
        #     customer_email=email,
        #     customer_created_date=customer_created_date,
        # customer_order_count = order_count
        # )

        #     session.add(c)

        # session.commit()
