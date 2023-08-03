import requests
from datetime import timedelta, datetime, date

# Shopify store info
store_url = 'https://mitolife.myshopify.com'
access_token = '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'

headers = {
    "X-Shopify-Access-Token" : "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",
    "Content-Type": "application/json"
}

store_info = requests.get(store_url, headers=headers)

# Start date to collect data
start_date = date(2023, 1, 1)

daily_order_count = []

min_time = start_date.strftime('%Y-%m-%dT00:00:00-07:00')
max_time = start_date.strftime('%Y-%m-%dT23:59:59-07:00')

params = {
    'status': 'any',
    'created_at_min': min_time,
    'created_at_max': max_time,
    'limit': 250
}
page = 1
page_orders = 0

response = requests.get(f"{store_url}/admin/orders.json", headers=headers, params=params)
orders_info = response.json()
orders = orders_info.get('orders', [])

print(orders)
length = len(orders)
daily_order_count.append(len(orders))
while length == 250:
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
        # if 'rel="next"' not in head:
        #     break
        next_url = link[-2]
        l = next_url[1:-2]
        daily_order_count.append(len(next_page_orders))

        length = len(next_page_orders)

print(daily_order_count)
total_daily_orders = sum(daily_order_count)
# print(orders_info)
print(total_daily_orders)


