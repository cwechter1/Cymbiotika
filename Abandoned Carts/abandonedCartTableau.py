import csv
import requests
import time
from datetime import date, timedelta

# Shopify store info
store_url = 'https://mitolife.myshopify.com'
access_token = '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'

headers = {
    "X-Shopify-Access-Token" : "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",
    "Content-Type": "application/json"
}

store_info = requests.get(store_url, headers=headers)

# Start date to collect data
start_date = date(2023, 6, 20)
date = start_date


# Define CSV file
csv_file_path = 'abandoned_carts_daily.csv'
field_names = ['Date', 'Abandoned Carts Percentage']

daily_abandoned_carts = []
daily_total_orders = []
abandoned_carts_percentage = []

while date <= date.today():
    min_time = date.strftime('%Y-%m-%dT00:00:00')
    max_time = date.strftime('%Y-%m-%dT23:59:59-07:00')
    params = {
        'status': 'any',
        'created_at_min': min_time,
        'created_at_max': max_time
    }

    params_orders = {
        'status': 'any',
        'created_at_min': min_time,
        'created_at_max': max_time
    }
    fraud_orders = 0
    fraud_orders_request = requests.get(f"{store_url}/admin/api/2022-07/orders.json", headers=headers, params=params_orders)
    fraud_orders_info = fraud_orders_request.json()
    fraud_orders_count = fraud_orders_info.get('orders', [])
    for order in fraud_orders_count:
        if order['cancel_reason'] == 'fraud':
            fraud_orders += 1
        
    abandoned_checkouts_request = requests.get(f"{store_url}/admin/api/2022-07/checkouts/count.json?", headers=headers, params=params)
    total_orders_request = requests.get(f"{store_url}/admin/api/2022-07/orders/count.json", headers=headers, params=params_orders)

    abandoned_checkouts_count = abandoned_checkouts_request.json().get('count', 0) 
    total_orders_count = total_orders_request.json().get('count', 0) 

    abandoned_carts_percentage_values = ((abandoned_checkouts_count) / (total_orders_count + abandoned_checkouts_count)) * 100
    abandoned_carts_percentage.append(abandoned_carts_percentage_values)
    
    daily_abandoned_carts.append(abandoned_checkouts_count)
    daily_total_orders.append(total_orders_count)

    # formatted_date = date.strftime('%Y-%m-%dT23:59:59-07:00')

    # Transfer to CSV file
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([date, abandoned_checkouts_count, total_orders_count, abandoned_carts_percentage_values])
    print(f"Date: {date}, Abandoned Carts: {abandoned_checkouts_count}, Total Orders: {total_orders_count}, Abandoned Carts Percentage: {abandoned_carts_percentage_values:.2f}%")
    
    date = date + timedelta(days=1)
    time.sleep(1)







# for i in range(len(daily_abandoned_carts)):
#     loop_date = date[i]
#     abandoned = daily_abandoned_carts[i]
#     orders = daily_total_orders[i]
#     percentage = abandoned_carts_percentage[i]
#     writer.writerow([loop_date, abandoned, orders, percentage]) 
    

   
