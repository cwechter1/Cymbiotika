from datetime import datetime
import pandas as pd
from db.models import Base, CYM_Returning_Customers
from db import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, DateTime, Numeric

print("Start")

df = pd.read_csv(
    "/Users/cymbiotika/Desktop/CymbiotikaCody/Returning Customer Rate/returning_customer_rate.csv"
)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

with Session() as session:
    for i, row in df.iterrows():
        # Skip rows with column names
        if row["Date"] == "Date":
            continue

        Date = datetime.strptime(row["Date"], "%Y-%m-%d").date()
        returning_customer_rate = row["returning_customer_rate"]
        nonsubscription_return_rate = row["nonsubscription_return_rate"]

        returning_customer = CYM_Returning_Customers(
            date=Date,
            returning_customer_rate=returning_customer_rate,
            nonsubscription_return_rate=nonsubscription_return_rate,
        )
        session.add(returning_customer)

    session.commit()

print("End")
