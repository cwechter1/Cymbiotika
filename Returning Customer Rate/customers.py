import requests
from datetime import datetime, timedelta, date
import csv
from sqlalchemy import create_engine
from db.models import Base, CYM_Returning_Customers
from sqlalchemy.orm import sessionmaker

# Shopify store info
store_url = 'https://mitolife.myshopify.com'
access_token = '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'

headers = {
    "X-Shopify-Access-Token": "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",
    "Content-Type": "application/json"
}

store_info = requests.get(store_url, headers=headers)

start_date = date.today() - timedelta(days=1)
current_date = start_date

csv_file_path = 'returning_customer_rate.csv'
field_names = ['Date', 'Returning Customer Rate', 'Non-Subscription Return Rate']

total_customer_count = []
created_customer_count = []
nonsubscription_count = []

while current_date < date.today():
    min_time = current_date.strftime('%Y-%m-%dT00:00:00-07:00')
    max_time = current_date.strftime('%Y-%m-%dT23:59:59-07:00')
    
    params = {
        'status': 'any',
        'created_at_min': min_time,
        'created_at_max': max_time,
        'limit': 250
    }
    customer_params = {
        'status': 'any',
        'created_at_min': min_time,
        'created_at_max': max_time,
        'limit': 250
    }
    page = 1
    total_customers = 0
    response = requests.get(f"{store_url}/admin/orders.json", headers=headers, params=params)
    orders_info = response.json()
    orders = orders_info.get('orders', [])
    total_customers += len(orders)

    while total_customers % 250 == 0:
        if 'Link' in response.headers:
            head = response.headers['Link']
            link = head.split(' ')
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
            next_page_orders = next_page_info.get('orders', [])
            head = next_page.headers['Link']
            link = head.split(' ')
            next_url = link[-2]
            l = next_url[1:-2]
            total_customers += len(next_page_orders)

    total_customer_count.append(total_customers)
    
    # Find subscription orders
    min_subscription_time = current_date.strftime('%Y-%m-%dT01:00:00-07:00')
    max_subscription_time = current_date.strftime('%Y-%m-%dT01:59:59-07:00')
    params_subscriptions = {
        'status': 'any',
        'created_at_min': min_subscription_time,
        'created_at_max': max_subscription_time,
        'limit': 250
    }
    subscription_page = 1
    subscription_total_orders = 0
    subscription_response = requests.get(f"{store_url}/admin/orders.json", headers=headers, params=params_subscriptions)
    subscription_orders_info = subscription_response.json()
    subscription_orders = subscription_orders_info.get('orders', [])

    subscription_total_orders += len(subscription_orders)

    while subscription_total_orders % 250 == 0:
        if 'Link' in subscription_response.headers:
            subscription_head = subscription_response.headers['Link']
            subscription_link = subscription_head.split(' ')
            if 'rel="next"' not in subscription_head:
                break
            subscription_next_url = subscription_link[subscription_link.index('rel="next"') - 1]
            # Remove "<" and ">" from next_url
            subscription_l = subscription_next_url[1:-2]
            subscription_page += 1
        else:
            break
        while "next" in subscription_head:
            subscription_next_page = requests.get(subscription_l, headers=headers)
            subscription_next_page_info = subscription_next_page.json()
            subscription_next_page_orders = subscription_next_page_info.get('orders', [])
            subscription_head = subscription_next_page.headers['Link']
            subscription_link = subscription_head.split(' ')
            subscription_next_url = subscription_link[-2]
            subscription_l = subscription_next_url[1:-2]
            subscription_total_orders += len(subscription_next_page_orders)

    non_subscription_daily = 0
    non_subscription_daily = total_customers - subscription_total_orders
    nonsubscription_count.append(non_subscription_daily)

    new_page = 1
    new_response = requests.get(f"{store_url}/admin/customers.json", headers=headers, params=customer_params)
    new_customer_info = new_response.json()
    new_customers = new_customer_info.get('customers', [])

    new_customers_count = len(new_customers)
    while new_customers_count % 250 == 0:
        if 'Link' in new_response.headers:
            new_head = new_response.headers['Link']
            new_link = new_head.split(' ')
            if 'rel="next"' not in new_head:
                break
            new_next_url = new_link[new_link.index('rel="next"') - 1]
            # Remove "<" and ">" from next_url
            new_l = new_next_url[1:-2]
            new_page += 1
        else:
            break
        while "next" in new_head:
            new_next_page = requests.get(new_l, headers=headers)
            new_next_page_info = new_next_page.json()
            new_next_page_orders = new_next_page_info.get('customers', [])
            new_head = new_next_page.headers['Link']
            new_link = new_head.split(' ')
            new_next_url = new_link[-2]
            new_l = new_next_url[1:-2]
            new_customers_count += len(new_next_page_orders)
    
    created_customer_count.append(new_customers_count)

    returning_customers = total_customers - new_customers_count
    returning_customer_rate = returning_customers / total_customers

    non_subscription_returning_customers = returning_customers - subscription_total_orders
    non_subscription_return_rate = non_subscription_returning_customers / non_subscription_daily

    with open(csv_file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_date, returning_customer_rate, non_subscription_return_rate])
            # 'Total Customers': total_customers,
            # 'Non-Subscription Customers': non_subscription_daily,
            # 'New Customers': new_customers_count,

    print ("Date: {}".format(current_date))
    print("Total Customers: {}".format(total_customers))
    print("Non-Subscription Customers: {}".format(non_subscription_daily))
    print("New Customers: {}".format(new_customers_count))
    print("Returning Customer Rate: {:.2%}".format(returning_customer_rate))
    print("Non-Subscription Return Rate: {:.2%}".format(non_subscription_return_rate))

    total_customers = 0
    new_customers_count = 0
    returning_customers = 0
    non_subscription_daily = 0

    engine = create_engine('postgresql://postgres:6vFvzWwpso6K0oCKxpdD@jalen-data.czawitrflbjp.us-east-1.rds.amazonaws.com:5432/postgres')
    Session = sessionmaker(bind=engine)
    session = Session()

    data_model = CYM_Returning_Customers(date=current_date, returning_customer_rate=returning_customer_rate, nonsubscription_return_rate=non_subscription_return_rate)
    session.add(data_model)
    session.commit()

    current_date += timedelta(days=1)

session.close()