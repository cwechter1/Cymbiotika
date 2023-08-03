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

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from datetime import datetime


Base = declarative_base()


class Conversion(Base):
    __tablename__ = "customerdata"

    id = Column(Integer, primary_key=True)

    app_id = Column(String)
    order_date = Column(DateTime)
    order_name = Column(String)
    order_total = Column(Numeric)
    order_status = Column(String)
    discount_name = Column(String)
    discount_amount = Column(Numeric)
    customer_email = Column(String)
    customer_created_date = Column(DateTime)
    customer_order_count = Column(Integer)


class ReCharge(Base):
    __tablename__ = "rechargeorders"

    id = Column(Integer, primary_key=True)

    order_date = Column(DateTime)
    order_id = Column(Numeric)
    shopify_order_id = Column(Numeric)
    email = Column(String)
    address_id = Column(Numeric)
    subtotal = Column(Numeric)
    shipping_price = Column(Numeric)
    total = Column(Numeric)
    discount_code = Column(String)
    discount_amount = Column(Numeric)
    order_type = Column(String)


class CymInventory(Base):
    __tablename__ = "cyminventory"

    id = Column(Integer, primary_key=True)

    time = Column(DateTime)
    sku = Column(String)
    name = Column(String)
    on_Hand = Column(Numeric)
    in_Transit = Column(Numeric)
    available = Column(Numeric)
    allocated = Column(Numeric)


class CymShipped(Base):
    __tablename__ = "cymshipped"

    id = Column(Integer, primary_key=True)

    ship_date = Column(DateTime)
    sku = Column(String)
    product = Column(String)
    quantity = Column(Numeric)
    order_name = Column(String)
    is_subscription = Column(String)
    created_date = Column(DateTime)
    customer = Column(String)
    warehouse = Column(String)
    batch = Column(Numeric)
    order_type = Column(String)


class AUS_Queued_Subs(Base):
    __tablename__ = "aus_queued_subs"

    id = Column(Integer, primary_key=True)

    scheduled_at = Column(DateTime)
    product = Column(String)
    orders = Column(Numeric)
    quantity = Column(Numeric)
    total = Column(Numeric)


class CA_Queued_Subs(Base):
    __tablename__ = "ca_queued_subs"

    id = Column(Integer, primary_key=True)

    scheduled_at = Column(DateTime)
    product = Column(String)
    orders = Column(Numeric)
    quantity = Column(Numeric)
    total = Column(Numeric)


class GAportal(Base):
    __tablename__ = "gaportal"

    id = Column(Integer, primary_key=True)

    day = Column(String)
    email = Column(String)
    shopify_id = Column(Numeric)
    unique_visits = Column(String)
    time_on_page = Column(String)
    page = Column(String)
    cx_cancel = Column(Boolean)
    status = Column(String)
    created_at = Column(DateTime)


class Churn_by_Tier(Base):
    __tablename__ = "churn_by_tier"

    id = Column(Integer, primary_key=True)

    churn_date = Column(DateTime)
    email = Column(String)
    shopify_id = Column(Numeric)
    tier = Column(Numeric)
    tier_id = Column(Numeric)
    date_earned = Column(DateTime)
    created_at = Column(DateTime)


class GA_PA(Base):
    __tablename__ = "ga_pa"

    id = Column(Integer, primary_key=True)

    day = Column(String)
    email = Column(String)
    shopify_id = Column(Numeric)
    unique_visits = Column(String)
    time_on_page = Column(String)
    page = Column(String)
    cx_cancel = Column(Boolean)
    status = Column(String)
    churned = Column(Boolean)
    tier = Column(String)


class Tiers(Base):
    __tablename__ = "tiers"

    id = Column(Integer, primary_key=True)

    tier_id = Column(Numeric)
    customer_id = Column(Numeric)
    tier = Column(Numeric)
    date_earned = Column(DateTime)
    shopify_id = Column(Numeric)


class Tier_Count(Base):
    __tablename__ = "tier_count"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    blank = Column(Numeric)
    member = Column(Numeric)
    insider = Column(Numeric)
    elite = Column(Numeric)
    vip = Column(Numeric)
    total = Column(Numeric)


class Active_by_Tier(Base):
    __tablename__ = "active_by_tier"

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime)
    email = Column(String)
    shopify_id = Column(String)
    tier = Column(Numeric)
    tier_id = Column(Numeric)
    date_earned = Column(DateTime)


class GA_Cancel_Flow(Base):
    __tablename__ = "ga_cancel_flow"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    event_action = Column(String)
    experiment_group = Column(String)
    experiment_variant = Column(String)
    address_id = Column(Numeric)
    email = Column(String)
    tier = Column(String)
    status = Column(String)


class CYM_Order_Total(Base):
    __tablename__ = "cym_order_total"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    order_total = Column(Numeric)
    refund_total = Column(Numeric)
    total = Column(Numeric)


class Portal_PV(Base):
    __tablename__ = "portal_pv"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    page_id = Column(String)
    unique_page_views = Column(String)
    avg_time_on_page = Column(String)
    page = Column(String)


class CA_Order_Total(Base):
    __tablename__ = "ca_order_total"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    order_total = Column(Numeric)
    refund_total = Column(Numeric)
    total = Column(Numeric)


class AUS_Order_Total(Base):
    __tablename__ = "aus_order_total"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    order_total = Column(Numeric)
    refund_total = Column(Numeric)
    total = Column(Numeric)


class RYA_Order_Total(Base):
    __tablename__ = "rya_order_total"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    order_total = Column(Numeric)
    refund_total = Column(Numeric)
    total = Column(Numeric)


class WS_Order_Total(Base):
    __tablename__ = "ws_order_total"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    order_total = Column(Numeric)
    refund_total = Column(Numeric)
    total = Column(Numeric)


class CYM_Subs_Count(Base):
    __tablename__ = "cym_subs_count"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    sub_count = Column(Numeric)


class CA_Subs_Count(Base):
    __tablename__ = "ca_subs_count"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    sub_count = Column(Numeric)


class CA_Cust_Count(Base):
    __tablename__ = "ca_cust_count"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    sub_count = Column(Numeric)


class RYA_Cust_Count(Base):
    __tablename__ = "rya_cust_count"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    sub_count = Column(Numeric)


class RYA_Sub_Count(Base):
    __tablename__ = "rya_sub_count"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    sub_count = Column(Numeric)


class AUS_Sub_Count(Base):
    __tablename__ = "aus_sub_count"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    sub_count = Column(Numeric)


class AUS_Cust_Count(Base):
    __tablename__ = "aus_cust_count"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    sub_count = Column(Numeric)


class CYM_Queued_Subs(Base):
    __tablename__ = "cym_queued_subs"

    id = Column(Integer, primary_key=True)

    scheduled_at = Column(DateTime)
    product = Column(String)
    orders = Column(Numeric)
    quantity = Column(Numeric)
    total = Column(Numeric)


class CYM_Run_Rate(Base):
    __tablename__ = "cym_run_rate"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    product = Column(String)
    quantity = Column(Numeric)
    avg = Column(Numeric)


class CAShipped(Base):
    __tablename__ = "cashipped"

    id = Column(Integer, primary_key=True)

    ship_date = Column(DateTime)
    sku = Column(String)
    product = Column(String)
    quantity = Column(Numeric)
    order_name = Column(String)
    is_subscription = Column(String)
    created_date = Column(DateTime)
    customer = Column(String)
    warehouse = Column(String)
    batch = Column(Numeric)
    order_type = Column(String)


class CA_Run_Rate(Base):
    __tablename__ = "ca_run_rate"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    product = Column(String)
    quantity = Column(Numeric)
    avg = Column(Numeric)


class CA_ReCharge(Base):
    __tablename__ = "ca_recharge"

    id = Column(Integer, primary_key=True)

    order_date = Column(DateTime)
    order_id = Column(Numeric)
    shopify_order_id = Column(Numeric)
    email = Column(String)
    address_id = Column(Numeric)
    subtotal = Column(Numeric)
    shipping_price = Column(Numeric)
    total = Column(Numeric)
    discount_code = Column(String)
    discount_amount = Column(Numeric)
    order_type = Column(String)


class CAInventory(Base):
    __tablename__ = "cainventory"

    id = Column(Integer, primary_key=True)

    time = Column(DateTime)
    sku = Column(String)
    name = Column(String)
    on_Hand = Column(Numeric)
    in_Transit = Column(Numeric)
    available = Column(Numeric)
    allocated = Column(Numeric)


class CYM_Queued(Base):
    __tablename__ = "cym_queued"

    id = Column(Integer, primary_key=True)

    scheduled_at = Column(DateTime)
    order_count = Column(Numeric)
    customers = Column(Numeric)
    discount = Column(Numeric)
    subtotal = Column(Numeric)
    tax = Column(Numeric)
    shipping = Column(Numeric)
    total = Column(Numeric)


class CA_Queued(Base):
    __tablename__ = "ca_queued"

    id = Column(Integer, primary_key=True)

    scheduled_at = Column(DateTime)
    order_count = Column(Numeric)
    customers = Column(Numeric)
    discount = Column(Numeric)
    subtotal = Column(Numeric)
    tax = Column(Numeric)
    shipping = Column(Numeric)
    total = Column(Numeric)


class AUS_Queued(Base):
    __tablename__ = "aus_queued"

    id = Column(Integer, primary_key=True)

    scheduled_at = Column(DateTime)
    order_count = Column(Numeric)
    customers = Column(Numeric)
    discount = Column(Numeric)
    subtotal = Column(Numeric)
    tax = Column(Numeric)
    shipping = Column(Numeric)
    total = Column(Numeric)


class RYA_Queued(Base):
    __tablename__ = "rya_queued"

    id = Column(Integer, primary_key=True)

    scheduled_at = Column(DateTime)
    order_count = Column(Numeric)
    customers = Column(Numeric)
    discount = Column(Numeric)
    subtotal = Column(Numeric)
    tax = Column(Numeric)
    shipping = Column(Numeric)
    total = Column(Numeric)


class CYM_Processed_Subs(Base):
    __tablename__ = "cym_processed_subs"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    recurring_orders = Column(Numeric)
    recurring_customers = Column(Numeric)
    recurring_sales = Column(Numeric)
    recurring_units = Column(Numeric)
    checkout_orders = Column(Numeric)
    checkout_customers = Column(Numeric)
    checkout_sales = Column(Numeric)
    checkout_units = Column(Numeric)


class CYM_Rech_Refunds(Base):
    __tablename__ = "cym_rech_refunds"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    recurring_orders = Column(Numeric)
    recurring_customers = Column(Numeric)
    recurring_refunds = Column(Numeric)
    checkout_orders = Column(Numeric)
    checkout_customers = Column(Numeric)
    checkout_refunds = Column(Numeric)


class CA_Processed_Subs(Base):
    __tablename__ = "ca_processed_subs"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    recurring_orders = Column(Numeric)
    recurring_customers = Column(Numeric)
    recurring_sales = Column(Numeric)
    recurring_units = Column(Numeric)
    checkout_orders = Column(Numeric)
    checkout_customers = Column(Numeric)
    checkout_sales = Column(Numeric)
    checkout_units = Column(Numeric)


class AUS_Processed_Subs(Base):
    __tablename__ = "aus_processed_subs"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    recurring_orders = Column(Numeric)
    recurring_customers = Column(Numeric)
    recurring_sales = Column(Numeric)
    recurring_units = Column(Numeric)
    checkout_orders = Column(Numeric)
    checkout_customers = Column(Numeric)
    checkout_sales = Column(Numeric)
    checkout_units = Column(Numeric)


class RYA_Processed_Subs(Base):
    __tablename__ = "rya_processed_subs"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    recurring_orders = Column(Numeric)
    recurring_customers = Column(Numeric)
    recurring_sales = Column(Numeric)
    recurring_units = Column(Numeric)
    checkout_orders = Column(Numeric)
    checkout_customers = Column(Numeric)
    checkout_sales = Column(Numeric)
    checkout_units = Column(Numeric)


class CA_Rech_Refunds(Base):
    __tablename__ = "ca_rech_refunds"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    recurring_orders = Column(Numeric)
    recurring_customers = Column(Numeric)
    recurring_refunds = Column(Numeric)
    checkout_orders = Column(Numeric)
    checkout_customers = Column(Numeric)
    checkout_refunds = Column(Numeric)


class AUS_Rech_Refunds(Base):
    __tablename__ = "aus_rech_refunds"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    recurring_orders = Column(Numeric)
    recurring_customers = Column(Numeric)
    recurring_refunds = Column(Numeric)
    checkout_orders = Column(Numeric)
    checkout_customers = Column(Numeric)
    checkout_refunds = Column(Numeric)


class RYA_Rech_Refunds(Base):
    __tablename__ = "rya_rech_refunds"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    recurring_orders = Column(Numeric)
    recurring_customers = Column(Numeric)
    recurring_refunds = Column(Numeric)
    checkout_orders = Column(Numeric)
    checkout_customers = Column(Numeric)
    checkout_refunds = Column(Numeric)


class CYM_Abandoned_Cart(Base):
    __tablename__ = "cym_abandoned_cart"

    id = Column(Integer, primary_key=True)

    date = Column(DateTime)
    total_sessions = Column(Numeric)
    adds_to_cart = Column(Numeric)
    nonsubscription_orders = Column(Numeric)
    abandoned_cart_rate = Column(Numeric)


class CYM_Refunds(Base):
    __tablename__ = "cym_refunds"

    id = Column(Integer, primary_key=True)

    date = Column(DateTime)
    order_name = Column(String)
    email = Column(String)
    order_count = Column(Numeric)
    total_spent = Column(Numeric)
    refund_amount = Column(Numeric)
    order_total = Column(Numeric)
    net_sales = Column(Numeric)
    refund_type = Column(String)
    status = Column(String)


class UAE_Order_Total(Base):
    __tablename__ = "uae_order_total"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    order_total = Column(Numeric)
    refund_total = Column(Numeric)
    total = Column(Numeric)


class UAE_Cust_Count(Base):
    __tablename__ = "uae_cust_count"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    cust_count = Column(Numeric)


class UAE_Sub_Count(Base):
    __tablename__ = "uae_sub_count"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    sub_count = Column(Numeric)


class UAE_Processed_Subs(Base):
    __tablename__ = "uae_processed_subs"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    recurring_orders = Column(Numeric)
    recurring_customers = Column(Numeric)
    recurring_sales = Column(Numeric)
    recurring_units = Column(Numeric)
    checkout_orders = Column(Numeric)
    checkout_customers = Column(Numeric)
    checkout_sales = Column(Numeric)
    checkout_units = Column(Numeric)


class UAE_Rech_Refunds(Base):
    __tablename__ = "uae_rech_refunds"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    recurring_orders = Column(Numeric)
    recurring_customers = Column(Numeric)
    recurring_refunds = Column(Numeric)
    checkout_orders = Column(Numeric)
    checkout_customers = Column(Numeric)
    checkout_refunds = Column(Numeric)


class UAE_Queued(Base):
    __tablename__ = "uae_queued"

    id = Column(Integer, primary_key=True)

    scheduled_at = Column(DateTime)
    order_count = Column(Numeric)
    customers = Column(Numeric)
    discount = Column(Numeric)
    subtotal = Column(Numeric)
    tax = Column(Numeric)
    shipping = Column(Numeric)
    total = Column(Numeric)


class CYM_Returning_Customers(Base):
    __tablename__ = "cym_returning_customers"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    returning_customer_rate = Column(Numeric)
    nonsubscription_return_rate = Column(Numeric)


class WS_Customers(Base):
    __tablename__ = "ws_customers"

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime)
    email = Column(String)
    name = Column(String)
    order_count = Column(Numeric)
    total_spent = Column(Numeric)
    last_order_name = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)


class WS_Orders(Base):
    __tablename__ = "ws_orders"

    id = Column(Integer, primary_key=True)

    order_date = Column(DateTime)
    order_name = Column(String)
    customer_email = Column(String)
    order_total = Column(Numeric)
    order_status = Column(String)
    discount_amount = Column(Numeric)
    city = Column(String)
    state = Column(String)
    country = Column(String)


class CYM_Insubs(Base):
    __tablename__ = "cym_insubs"

    id = Column(Integer, primary_key=True)

    cancelled_at = Column(DateTime)
    product = Column(String)
    subscriptions = Column(Numeric)
    quantity = Column(Numeric)
    status = Column(String)
    total = Column(Numeric)


class CYM_Newsubs(Base):
    __tablename__ = "cym_newsubs"

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime)
    product = Column(String)
    subscriptions = Column(Numeric)
    quantity = Column(Numeric)
    status = Column(String)
    total = Column(Numeric)


class Day_Of_Churn(Base):
    __tablename__ = "day_of_churn"

    id = Column(Integer, primary_key=True)

    cancelled_at = Column(DateTime)
    email = Column(String)
    customer_id = Column(Numeric)
    cancel_reason = Column(String)
    created_at = Column(DateTime)


class Day_Of_Cancelled_Subs(Base):
    __tablename__ = "day_of_cancelled_subs"

    id = Column(Integer, primary_key=True)

    cancelled_at = Column(DateTime)
    address_id = Column(Numeric)
    email = Column(String)
    product_title = Column(String)
    product_id = Column(Numeric)
    quantity = Column(Numeric)
    cancel_reason = Column(String)
    created_at = Column(DateTime)


class Day_Of_New(Base):
    __tablename__ = "day_of_new"

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime)
    email = Column(String)
    customer_id = Column(Numeric)
    new_subscriptions = Column(Numeric)


class CYM_Sold_Products(Base):
    __tablename__ = "cym_sold_products"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    product = Column(String)
    product_id = Column(Numeric)
    total_sales = Column(Numeric)
    customers = Column(Numeric)
    quantity = Column(Numeric)


class CYM_Active_Yest(Base):
    __tablename__ = "cym_active_yest"

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime)
    email = Column(String)
    shopify_id = Column(String)
    tier = Column(Numeric)
    tier_id = Column(Numeric)
    date_earned = Column(DateTime)


class CYM_Churn(Base):
    __tablename__ = "cym_churn"

    id = Column(Integer, primary_key=True)

    churn_date = Column(DateTime)
    email = Column(String)
    external_id = Column(Numeric)


class CYM_Tiers_DoD(Base):
    __tablename__ = "cym_tiers_dod"

    id = Column(Integer, primary_key=True)

    day = Column(DateTime)
    from_member_to_insider = Column(Numeric)
    from_member_to_elite = Column(Numeric)
    from_member_to_vip = Column(Numeric)
    from_member_to_blank = Column(Numeric)
    from_insider_to_member = Column(Numeric)
    from_insider_to_elite = Column(Numeric)
    from_insider_to_vip = Column(Numeric)
    from_insider_to_blank = Column(Numeric)
    from_elite_to_member = Column(Numeric)
    from_elite_to_insider = Column(Numeric)
    from_elite_to_vip = Column(Numeric)
    from_elite_to_blank = Column(Numeric)
    from_vip_to_member = Column(Numeric)
    from_vip_to_insider = Column(Numeric)
    from_vip_to_elite = Column(Numeric)
    from_vip_to_blank = Column(Numeric)
    from_blank_to_member = Column(Numeric)
    from_blank_to_insider = Column(Numeric)
    from_blank_to_elite = Column(Numeric)
    from_blank_to_vip = Column(Numeric)
    new_member = Column(Numeric)
    new_insider = Column(Numeric)
    new_elite = Column(Numeric)
    new_vip = Column(Numeric)
    new_blank = Column(Numeric)
    stayed_member = Column(Numeric)
    stayed_insider = Column(Numeric)
    stayed_elite = Column(Numeric)
    stayed_vip = Column(Numeric)
    stayed_blank = Column(Numeric)


class CYM_Habitual_Active_Customers(Base):
    __tablename__ = "cym_habitual_active_customers"

    id = Column(Integer, primary_key=True)

    pull_date = Column(DateTime)
    created_at = Column(DateTime)
    email = Column(String)
    shopify_id = Column(Numeric)
    tier = Column(Numeric)


class CA_conversions(Base):
    __tablename__ = "ca_conversions"

    id = Column(Integer, primary_key=True)

    app_id = Column(String)
    order_date = Column(DateTime)
    order_name = Column(String)
    order_total = Column(Numeric)
    order_status = Column(String)
    discount_name = Column(String)
    discount_amount = Column(Numeric)
    customer_email = Column(String)
    customer_created_date = Column(DateTime)
    customer_order_count = Column(Integer)


class CYM_New_Subs_by_Active(Base):
    __tablename__ = "cym_new_subs_by_active"

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime)
    email = Column(String)
    address_id = Column(Numeric)
    tier = Column(Numeric)
    shopify_product_id = Column(Numeric)
    product_title = Column(String)
    sku = Column(String)
    quantity = Column(Numeric)
    price = Column(Numeric)


class CYM_ReCh_Cust(Base):
    __tablename__ = "cym_rech_cust"

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime)
    rech_id = Column(Numeric)
    shopify_id = Column(Numeric)
    email = Column(String)


class CYM_Token(Base):
    __tablename__ = "cym_token"

    id = Column(Integer, primary_key=True)

    reward = Column(String)
    email = Column(String)
    shopify_id = Column(Numeric)
    tier = Column(Numeric)
    redeemed = Column(String)
    claimed_nft = Column(String)
    date_earned = Column(DateTime)
    date_redeemed = Column(DateTime)
    db_id = Column(Numeric)
    db_cust_id = Column(Numeric)


class Queued_Revenue_by_Tier(Base):
    __tablename__ = "queued_revenue_by_tier"

    id = Column(Integer, primary_key=True)

    scheduled_at = Column(DateTime)
    email = Column(String)
    total_price = Column(Numeric)
    charge_id = Column(Numeric)
    tier = Column(Numeric)


class Active_by_Created_At(Base):
    __tablename__ = "active_by_created_at"

    id = Column(Integer, primary_key=True)

    date = Column(String)
    creation_date = Column(DateTime)
    active_customers = Column(Numeric)
    inactive_customers = Column(Numeric)
