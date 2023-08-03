from datetime import date, timedelta, datetime
import requests
import time
import csv
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
import os

import pandas as pd

# from sqlalchemy import create_engine
# from db.models import Base, CYM_Abandoned_Cart
# from sqlalchemy.orm import sessionmaker

# Shopify store info
store_url = "https://mitolife.myshopify.com"
access_token = "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"

headers = {
    "X-Shopify-Access-Token": "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",
    "Content-Type": "application/json",
}

store_info = requests.get(store_url, headers=headers)

# Start date to collect data
start_date = date.today() - timedelta(days=5)
current_date = start_date
subscription_current_date = start_date

# Define CSV file
csv_file_path = "nonsubscription_orders.csv"
field_names = [
    "Date",
    "Total Sessions",
    "Adds to Cart",
    "Non-Subscription Orders",
    "Abandoned Cart Rate",
]

daily_order_count = []
total_daily_count = []
total_subscription_count = []
nonsubscription_count = []
add_to_carts_count = []
abandoned_cart_rate = []
total_sessions_count = []

SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
KEY_FILE_LOCATION = "/Users/cymbiotika/Desktop/CymbiotikaCody/GA/client_secrets.json"
VIEW_ID = "332137414"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_FILE_LOCATION

client = BetaAnalyticsDataClient()
while current_date < date.today():
    min_time = current_date.strftime("%Y-%m-%dT00:00:00-07:00")
    max_time = current_date.strftime("%Y-%m-%dT23:59:59-07:00")
    params = {
        "status": "any",
        "created_at_min": min_time,
        "created_at_max": max_time,
        "limit": 250,
    }
    page = 1
    total_orders = 0
    fraud_orders = 0
    response = requests.get(
        f"{store_url}/admin/orders.json", headers=headers, params=params
    )
    orders_info = response.json()
    orders = orders_info.get("orders", [])
    for order in orders:
        if order["cancel_reason"] == "fraud":
            orders.remove(order)
            fraud_orders += 1
    total_orders += len(orders)
    print(total_orders)
    while total_orders + fraud_orders % 250 == 0:
        if "Link" in response.headers:
            head = response.headers["Link"]
            link = head.split(" ")
            if 'rel="next"' not in head:
                break
            next_url = link[link.index('rel="next"') - 1]
            # Remove "<" and ">" from next_url
            l = next_url[1:-2]
            page += 1
        else:
            break
        while "next" in head:
            next_page = requests.get(l, headers=headers)
            next_page_info = next_page.json()
            next_page_orders = next_page_info.get("orders", [])
            head = next_page.headers["Link"]
            link = head.split(" ")
            next_url = link[-2]
            l = next_url[1:-2]
            fraud_orders = 0
            for order in next_page_orders:
                if order["cancel_reason"] == "fraud":
                    next_page_orders.remove(order)
                    fraud_orders += 1
            total_orders += len(next_page_orders)

    # Find subscription orders
    min_subscription_time = current_date.strftime("%Y-%m-%dT01:00:00-07:00")
    max_subscription_time = current_date.strftime("%Y-%m-%dT01:59:59-07:00")
    params_subscriptions = {
        "status": "any",
        "created_at_min": min_subscription_time,
        "created_at_max": max_subscription_time,
        "limit": 250,
    }
    subscription_page = 1
    subscription_total_orders = 0
    subscription_fraud_orders = 0
    subscription_response = requests.get(
        f"{store_url}/admin/orders.json", headers=headers, params=params_subscriptions
    )
    subscription_orders_info = subscription_response.json()
    subscription_orders = subscription_orders_info.get("orders", [])
    for order in subscription_orders:
        if order["cancel_reason"] == "fraud":
            subscription_orders.remove(order)
            subscription_fraud_orders += 1
    subscription_total_orders += len(subscription_orders)

    while subscription_total_orders + subscription_fraud_orders % 250 == 0:
        if "Link" in subscription_response.headers:
            subscription_head = subscription_response.headers["Link"]
            subscription_link = subscription_head.split(" ")
            if 'rel="next"' not in subscription_head:
                break
            subscription_next_url = subscription_link[
                subscription_link.index('rel="next"') - 1
            ]
            # Remove "<" and ">" from next_url
            subscription_l = subscription_next_url[1:-2]
            subscription_page += 1
        else:
            break
        while "next" in subscription_head:
            subscription_next_page = requests.get(subscription_l, headers=headers)
            subscription_next_page_info = subscription_next_page.json()
            subscription_next_page_orders = subscription_next_page_info.get(
                "orders", []
            )
            subscription_head = subscription_next_page.headers["Link"]
            subscription_link = subscription_head.split(" ")
            subscription_next_url = subscription_link[-2]
            subscription_l = subscription_next_url[1:-2]
            subscription_fraud_orders = 0
            for order in subscription_next_page_orders:
                if order["cancel_reason"] == "fraud":
                    subscription_next_page_orders.remove(order)
                    subscription_fraud_orders += 1
            subscription_total_orders += len(subscription_next_page_orders)

    non_subscription_daily = 0
    # Find nonsubscription orders
    non_subscription_daily = total_orders - subscription_total_orders
    nonsubscription_count.append(non_subscription_daily)

    minim = current_date.strftime("%Y-%m-%d")
    maxim = current_date.strftime("%Y-%m-%d")

    # response = (
    #     analytics.reports()
    #     .batchGet(
    #         body={
    #             "reportRequests": [
    #                 {
    #                     "viewId": VIEW_ID,
    #                     "dateRanges": [{"startDate": minim, "endDate": maxim}],
    #                     "metrics": [{"expression": "ga:uniqueEvents"}],
    #                     "dimensions": [
    #                         {"name": "ga:eventCategory"},
    #                         {"name": "ga:eventAction"},
    #                         {"name": "ga:eventLabel"},
    #                         {"name": "ga:date"},
    #                     ],
    #                     "dimensionFilterClauses": [
    #                         {
    #                             "filters": [
    #                                 {
    #                                     "operator": "EXACT",
    #                                     "dimensionName": "ga:eventAction",
    #                                     "expressions": ["add_to_cart"],
    #                                 }
    #                             ]
    #                         }
    #                     ],
    #                     "pageSize": 10000,
    #                 }
    #             ]
    #         }
    #     )
    #     .execute()
    # )

    # reports = response.get("reports", [])
    # if reports:
    #     rows = reports[0].get("data", {}).get("rows", [])
    #     if rows:
    #         unique_events = int(rows[0]["metrics"][0]["values"][0])
    #         cart_count = unique_events
    #     else:
    #         print("No Rows Found")
    # else:
    #     print("No Reports Found")

    # Find the daily cart count
    request_api = RunReportRequest(
        property="properties/332137414",
        dimensions=[Dimension(name="date")],
        metrics=[Metric(name="add_to_cart")],
        date_ranges=[DateRange(start_date=minim, end_date=maxim)],
    )
    response = client.run_report(request=request_api)
    for row in response.rows:
        cart_count = row.metric_values[0].value

    # Find the daily total sessions
    # response = (
    #     analytics.reports()
    #     .batchGet(
    #         body={
    #             "reportRequests": [
    #                 {
    #                     "viewId": VIEW_ID,
    #                     "dateRanges": [{"startDate": minim, "endDate": maxim}],
    #                     "metrics": [
    #                         {"expression": "ga:sessions"},
    #                     ],
    #                     "dimensions": [
    #                         {"name": "ga:date"},
    #                     ],
    #                     "pageSize": 10000,
    #                 }
    #             ]
    #         }
    #     )
    #     .execute()
    # )
    # total_sessions = 0
    # reports = response.get("reports", [])
    # if reports:
    #     rows = reports[0].get("data", {}).get("rows", [])
    #     if rows:
    #         total_sessions = int(rows[0]["metrics"][0]["values"][0])
    #     else:
    #         print("No Rows Found")
    # else:
    #     print("No Reports Found")

    request_api = RunReportRequest(
        property="properties/332137414",
        dimensions=[Dimension(name="date")],
        metrics=[Metric(name="sessions")],
        date_ranges=[DateRange(start_date=minim, end_date=maxim)],
    )
    response = client.run_report(request=request_api)
    for row in response.rows:
        total_sessions = row.metric_values[0].value

    # Find the daily abandoned cart rate
    abandoned_cart_rate_count = 1 - (non_subscription_daily / cart_count)
    abandoned_cart_rate_percentage = "{:.2%}".format(abandoned_cart_rate_count)

    with open(csv_file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(field_names)
        writer.writerow(
            [
                current_date,
                total_sessions,
                cart_count,
                non_subscription_daily,
                abandoned_cart_rate_percentage,
            ]
        )

    print("Date: {}".format(current_date))
    print("Total Sessions: {}".format(total_sessions))
    print("Adds to Cart: {}".format(cart_count))
    print("Nonsubscription Orders: {}".format(non_subscription_daily))
    print("Abandoned Cart Rate: {:.2%}".format(abandoned_cart_rate_count))
    print("------------------------------")

    # engine = create_engine('postgresql://postgres:6vFvzWwpso6K0oCKxpdD@jalen-data.czawitrflbjp.us-east-1.rds.amazonaws.com:5432/postgres')
    # Session = sessionmaker(bind=engine)
    # session = Session()

    # data_model = CYM_Abandoned_Cart(date=current_date, total_sessions=total_sessions, adds_to_cart=cart_count, nonsubscription_orders=non_subscription_daily, abandoned_cart_rate=abandoned_cart_rate_count)
    # session.add(data_model)
    # session.commit()

    total_subscription_count.append(subscription_total_orders)
    subscription_total_orders = 0
    non_subscription_daily = 0
    add_to_carts_count.append(cart_count)
    cart_count = 0
    total_sessions_count.append(total_sessions)
    total_sessions = 0
    abandoned_cart_rate.append(abandoned_cart_rate_count)
    abandoned_cart_rate_count = 0
    subscription_current_date += timedelta(days=1)

    current_date += timedelta(days=1)

# session.close()
