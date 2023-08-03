from datetime import date, timedelta, datetime
import requests
import time
import csv
import google.auth
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    BigInteger,
    Integer,
    String,
    DateTime,
    Numeric,
    Boolean,
)
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from datetime import datetime

DATABASE_URL = "postgresql://postgres:6vFvzWwpso6K0oCKxpdD@jalen-data.czawitrflbjp.us-east-1.rds.amazonaws.com/postgres"

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=5)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class CYM_sessions(Base):
    __tablename__ = "cym_sessions"

    id = Column(Integer, primary_key=True)

    date = Column(DateTime)
    nonsubscription_orders = Column(Numeric)
    total_sessions = Column(Numeric)


# Shopify store info
store_url = "https://mitolife.myshopify.com"
access_token = "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"

headers = {
    "X-Shopify-Access-Token": "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",
    "Content-Type": "application/json",
}
# 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
store_info = requests.get(store_url, headers=headers)

# Start date to collect data
start_date = date.today()
current_date = start_date - timedelta(days=1)
subscription_current_date = start_date

# Define CSV file
csv_file_path = "sessions.csv"
field_names = [
    "Date",
    "Non-Subscription Orders",
    "Total Sessions",
]

daily_order_count = []
total_daily_count = []
total_subscription_count = []
nonsubscription_count = []
total_sessions_count = []
fraud_test = 0

SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
KEY_FILE_LOCATION = "/Users/cymbiotika/Desktop/CymbiotikaCody/GA/client_secrets.json"
VIEW_ID = "332137414"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_FILE_LOCATION
client = BetaAnalyticsDataClient()
Base.metadata.create_all(engine)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
with Session() as session:
    while current_date < date.today():
        min_time = current_date.strftime("%Y-%m-%dT00:00:00-08:00")
        max_time = current_date.strftime("%Y-%m-%dT23:59:59-08:00")
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
        fraud_test = total_orders + fraud_orders
        while fraud_test % 250 == 0:
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
                fraud_test = total_orders + fraud_orders

        # Find subscription orders
        min_subscription_time = current_date.strftime("%Y-%m-%dT00:00:00-08:00")
        max_subscription_time = current_date.strftime("%Y-%m-%dT00:59:59-08:00")
        params_subscriptions = {
            "status": "any",
            "created_at_min": min_subscription_time,
            "created_at_max": max_subscription_time,
            "limit": 250,
        }
        subscription_page = 1
        subscription_total_orders = 0
        subscription_fraud_orders = 0
        subscription_fraud_test = 0
        subscription_response = requests.get(
            f"{store_url}/admin/orders.json",
            headers=headers,
            params=params_subscriptions,
        )
        subscription_orders_info = subscription_response.json()
        subscription_orders = subscription_orders_info.get("orders", [])
        for order in subscription_orders:
            if order["cancel_reason"] == "fraud":
                subscription_orders.remove(order)
                subscription_fraud_orders += 1
        subscription_total_orders += len(subscription_orders)
        subscription_fraud_test = subscription_total_orders + subscription_fraud_orders

        while subscription_fraud_test % 250 == 0:
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
                subscription_fraud_test = (
                    subscription_total_orders + subscription_fraud_orders
                )

        non_subscription_daily = 0
        # Find nonsubscription orders
        non_subscription_daily = total_orders - subscription_total_orders
        nonsubscription_count.append(non_subscription_daily)

        minim = current_date.strftime("%Y-%m-%d")
        maxim = current_date.strftime("%Y-%m-%d")
        # GA 3 API
        # # Find the daily total sessions
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

        # GA 4 API
        # Find the daily total sessions
        request_api = RunReportRequest(
            property=f"properties/{VIEW_ID}",
            dimensions=[Dimension(name="date")],
            metrics=[Metric(name="sessions")],
            date_ranges=[DateRange(start_date=minim, end_date=maxim)],
        )
        response = client.run_report(request_api)

        total_sessions = 0
        # Get metric_values from response
        for row in response.rows:
            total_sessions = row.metric_values[0].value

        with open(csv_file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([current_date, non_subscription_daily, total_sessions])

        print("Date: {}".format(current_date))
        print("Nonsubscription Orders: {}".format(non_subscription_daily))
        print("Total Sessions: {}".format(total_sessions))
        print("------------------------------")

        data_model = CYM_sessions(
            date=current_date,
            nonsubscription_orders=non_subscription_daily,
            total_sessions=total_sessions,
        )
        session.add(data_model)
        session.commit()

        total_subscription_count.append(subscription_total_orders)
        subscription_total_orders = 0
        non_subscription_daily = 0
        total_sessions_count.append(total_sessions)
        total_sessions = 0
        fraud_test = 0
        subscription_fraud_test = 0

        subscription_current_date += timedelta(days=1)
        current_date += timedelta(days=1)
session.close()
