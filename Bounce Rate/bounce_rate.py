import csv
import time
from datetime import date, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set up the Google Analytics API credentials and service
SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
KEY_FILE_LOCATION = "/Users/cymbiotika/Desktop/CymbiotikaCody/GA/client_secrets.json"
VIEW_ID = "240793260"

credentials = service_account.Credentials.from_service_account_file(KEY_FILE_LOCATION)

analytics = build("analyticsreporting", "v4", credentials=credentials)


def find_urls(start_date, end_date):
    urls = []
    current_date = start_date
    start_date_str = current_date.strftime("%Y-%m-%d")
    end_date_str = start_date_str

    url_response = (
        analytics.reports()
        .batchGet(
            body={
                "reportRequests": [
                    {
                        "viewId": VIEW_ID,
                        "dateRanges": [
                            {"startDate": start_date_str, "endDate": end_date_str}
                        ],
                        "metrics": [{"expression": "ga:pageviews"}],
                        "dimensions": [{"name": "ga:pagePath"}],
                        "orderBys": [
                            {"fieldName": "ga:pageviews", "sortOrder": "DESCENDING"}
                        ],
                        "pageSize": 50,
                    }
                ]
            }
        )
        .execute()
    )

    url_reports = url_response.get("reports", [])
    if url_reports:
        url_report = url_reports[0]
        url_rows = url_report.get("data", {}).get("rows", [])
        if url_rows:
            urls.extend([row.get("dimensions", [])[0] for row in url_rows])
        else:
            print(f"No data found for {start_date_str}")
    else:
        print(f"No data found for {start_date_str}")

    urls = urls[:50]  # Limit the URLs to 50 overall
    return urls


def find_bounce_rate(date, urls):
    formatted_date = date.strftime("%Y-%m-%d")
    print(f"Date: {formatted_date}")
    bounce_rate_data = [[formatted_date]]
    for url in urls:
        response = (
            analytics.reports()
            .batchGet(
                body={
                    "reportRequests": [
                        {
                            "viewId": VIEW_ID,
                            "dateRanges": [
                                {"startDate": formatted_date, "endDate": formatted_date}
                            ],
                            "dimensions": [{"name": "ga:pagePath"}],
                            "orderBys": [
                                {"fieldName": "ga:pagePath", "sortOrder": "ASCENDING"}
                            ],
                            "pageSize": 100000,
                            "dimensionFilterClauses": [
                                {
                                    "filters": [
                                        {
                                            "dimensionName": "ga:pagePath",
                                            "operator": "EXACT",
                                            "expressions": [url],
                                        }
                                    ]
                                }
                            ],
                        }
                    ]
                }
            )
            .execute()
        )

        reports = response.get("reports", [])
        if reports:
            rows = reports[0].get("data", {}).get("rows", [])
            if rows:
                bounce_rate = float(rows[0]["metrics"][0]["values"][0])
                print(f"URL: {url}, Bounce Rate: {bounce_rate:.2f}%")
                bounce_rate_data[0].append(bounce_rate)
            else:
                bounce_rate_data[0].append(0)
        else:
            bounce_rate_data[0].append(0)
    return bounce_rate_data


start_date = date(2023, 6, 1)
end_date = date.today()

urls = find_urls(start_date, end_date)

current_date = start_date
data = []
while current_date < end_date:
    data.extend(find_bounce_rate(current_date, urls))
    current_date += timedelta(days=1)
    time.sleep(5)
csv_file_path = "bounce_rates.csv"
field_names = ["Date"] + urls + ["Average Bounce Rate"]

with open(csv_file_path, "a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(field_names)
    writer.writerows(data)


# import csv
# from datetime import date, timedelta
# from google.oauth2 import service_account
# from googleapiclient.discovery import build

# # Set up the Google Analytics API credentials and service
# SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
# KEY_FILE_LOCATION = '/Users/cymbiotika/Desktop/CymbiotikaCody/GA/client_secrets.json'
# VIEW_ID = '240793260'

# credentials = service_account.Credentials.from_service_account_file(KEY_FILE_LOCATION)

# start_date = date(2023, 1, 1)
# current_date = start_date
# end_date = date.today()
# top_urls = []
# analytics = build('analyticsreporting', 'v4', credentials=credentials)

# def find_urls(start_date, end_date):
#     start_date_str = start_date.strftime('%Y-%m-%d')
#     end_date_str = end_date.strftime('%Y-%m-%d')

#     url_response = analytics.reports().batchGet(
#         body={
#             'reportRequests': [{
#                 'viewId': VIEW_ID,
#                 'dateRanges': [{'startDate': start_date_str, 'endDate': end_date_str}],
#                 'metrics': [{'expression': 'ga:pageviews'}],
#                 'dimensions': [{'name': 'ga:pagePath'}],
#                 'orderBys': [{'fieldName': 'ga:pageviews', 'sortOrder': 'DESCENDING'}],
#                 'pageSize': 51  # Increase the pageSize to 51
#             }]
#         }
#     ).execute()

#     url_reports = url_response.get('reports', [])
#     if url_reports:
#         url_report = url_reports[0]
#         url_rows = url_report.get('data', {}).get('rows', [])
#         if url_rows:
#             urls = [row.get('dimensions', [])[0] for row in url_rows]
#             urls = urls[1:]  # Exclude the first URL
#             top_urls.append(urls)
#             return urls
#         else:
#             print("No data found for URLs")
#     else:
#         print("No data found for URLs")
# def find_bounce_rates(current_date, url):
#     minim = current_date.strftime('%Y-%m-%d')
#     maxim = current_date.strftime('%Y-%m-%d')

#     response = analytics.reports().batchGet(
#         body={
#             'reportRequests': [{
#                 'viewId': VIEW_ID,
#                 'dateRanges': [{'startDate': minim, 'endDate': maxim}],
#                 'metrics': [{'expression': 'ga:bounceRate'}],
#                 'dimensions': [{'name': 'ga:pagePath'}],
#                 'orderBys': [{'fieldName': 'ga:bounceRate'}],
#                 'pageSize': 100000,
#                 'dimensionFilterClauses': [{
#                     'filters': [{
#                         'dimensionName': 'ga:pagePath',
#                         'operator': 'EXACT',
#                         'expressions': [url]
#                     }]
#                 }]
#             }]
#         }
#     ).execute()
#     reports = response.get('reports', [])
#     if reports:
#         rows = reports[0].get('data', {}).get('rows', [])
#         if rows:
#             bounce_rate = float(rows[0]['metrics'][0]['values'][0])
#             return bounce_rate
#         else:
#             print(f"No Rows Found for {url}")
#     else:
#         print(f"No Reports Found for {url}")

# find_urls(start_date, end_date)

# while current_date < date.today():
#     bounce_rate_data = [current_date.strftime('%Y-%m-%d')]
#     for url in top_urls:
#         bounce_rate = find_bounce_rates(current_date, url)
#         bounce_rate_data.extend([url, bounce_rate])
#     average_bounce_rate = sum(bounce_rate_data[2::2]) / len(top_urls) if top_urls else None
#     print(f"Date: {current_date}, URL: {url}, Bounce Rate: {bounce_rate:.2f}%, Average Bounce Rate: {average_bounce_rate:.2f}")
#     current_date += timedelta(days=1)
