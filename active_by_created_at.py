import requests
import json
from datetime import datetime, timedelta
from db.models import Base, CYM_ReCh_Cust, Active_by_Tier, Active_by_Created_At
from db import engine
from sqlalchemy.orm import sessionmaker

Base.metadata.create_all(engine)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

with Session() as session:
    print("start")
    current_date = datetime.now()
    formatted_date = []
    active_customers_date = []
    dates = [
        date_tuple[0] for date_tuple in session.query(CYM_ReCh_Cust.created_at).all()
    ]
    for date_obj in dates:
        if date_obj:
            date = date_obj.strftime("%Y-%m")
            formatted_date.append(date)

    customer_count_per_month = {}

    for date in formatted_date:
        customer_count_per_month[date] = customer_count_per_month.get(date, 0) + 1

    active_customers = [
        active_tuple[0]
        for active_tuple in session.query(Active_by_Tier.created_at).all()
    ]
    for active_customer in active_customers:
        if active_customer:
            active_date = active_customer.strftime("%Y-%m")
            active_customers_date.append(active_date)

    active_customer_count_per_month = {}
    print("check 1")
    for date in active_customers_date:
        active_customer_count_per_month[date] = (
            active_customer_count_per_month.get(date, 0) + 1
        )

    all_dates = sorted(set(formatted_date) | set(active_customers_date))

    active_count_list = [
        active_customer_count_per_month.get(date, 0) for date in all_dates
    ]
    # Subtract total customers by active customers to get inactive customers
    inactive_count_list = []
    for date in all_dates:
        inactive_count_list.append(
            customer_count_per_month.get(date, 0)
            - active_customer_count_per_month.get(date, 0)
        )
    print("check 2")
    with open("active_customer_counts.csv", "w") as csv_file:
        csv_file.write("Date, Current Date, Active Customers, Inactive Customers\n")
        for date, active_count, inactive_count in zip(
            all_dates, active_count_list, inactive_count_list
        ):
            csv_file.write(
                f"{date}, {current_date}, {active_count}, {inactive_count} \n"
            )
            c = Active_by_Created_At(
                date=date,
                creation_date=current_date,
                active_customers=active_count,
                inactive_customers=inactive_count,
            )
            session.add(c)
        session.commit()

session.close()
