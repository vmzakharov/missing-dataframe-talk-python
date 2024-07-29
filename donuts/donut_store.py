import pandas as pd
import numpy as np
import unittest
from datetime import date, timedelta
from math import nan

TODAY = date.today()
YESTERDAY = TODAY + timedelta(days=-1)
TOMORROW = TODAY + timedelta(days=1)


class TestDonutShop(unittest.TestCase):
    def setUp(self):
        self.customers = pd.DataFrame(
            {
                "Name": ["Alice", "Bob", "Carol", "Dave"],
                "Street": ["902 S Pacific St", "405 Main St", "12300 State St", "102 S Main St"],
                "City": ["Las Vegas", "Dallas", "Atlanta", "Phoenix"],
                "State": ["NM", "SD", "MI", "OR"]
            }
        )

        self.menu = pd.DataFrame(
            {
                "Donut": ["Blueberry", "Old Fashioned", "Pumpkin Spice", "Jelly", "Apple Cider"],
                "Price": [1.25, 1.00, 0.75, 1.50, 1.50],
                "DiscountPrice": [1.00, 0.90, 0.65, 1.25, 1.25]
            }
        )

        # self.orders = pd.DataFrame(
        #     {
        #         "Customer": ["Alice", "Alice", "Bob", "Alice", "Alice", "Carol", "Dave", "Alice", "Carol", "Bob"],
        #         "DeliveryDate": [YESTERDAY, YESTERDAY, YESTERDAY, TODAY, TODAY, TODAY,
        #                          TOMORROW, TOMORROW, TOMORROW, TOMORROW],
        #         "Donut": ["Old Fashioned", "Blueberry", "Old Fashioned", "Apple Cider", "Blueberry", "Old Fashioned",
        #                   "Old Fashioned", "Jelly", "Blueberry", "Pumpkin Spice"],
        #         "Quantity": [12, 2, 12, 12, 2, 12, 12, 12, 2, 1]
        #     }
        # )

        self.orders = pd.DataFrame(
            [
                ["Alice", YESTERDAY, "Old Fashioned", 12],
                ["Alice", YESTERDAY, "Blueberry", 2],
                ["Bob",   YESTERDAY, "Old Fashioned", 12],
                ["Alice", TODAY, "Apple Cider", 12],
                ["Alice", TODAY, "Blueberry", 2],
                ["Carol", TODAY, "Old Fashioned", 12],
                ["Dave",  TOMORROW, "Old Fashioned", 12],
                ["Alice", TOMORROW, "Jelly", 12],
                ["Carol", TOMORROW, "Blueberry", 2],
                ["Bob",   TOMORROW, "Pumpkin Spice", 1]
            ],
            columns=["Customer", "DeliveryDate", "Donut", "Quantity"]
        )

    def test_donuts_in_popularity_order(self):
        donuts_by_qty = (self.orders
                         .groupby("Donut")
                         .agg({"Quantity": ["sum"]}))

        print("sdflkjglkdjsgfl;kjgdf;lkhj;ksl'fdgjhlk;fgsjh;ljfgs;lhjl;sfg")
        print(donuts_by_qty.columns)
        print(donuts_by_qty)

        donuts_by_qty.columns = donuts_by_qty.columns.get_level_values(0)
        print(donuts_by_qty.columns)

        popularity_list = (donuts_by_qty.sort_values(["Quantity", "Donut"],
                                                     ascending=[False, True])
                           .index.to_list())

        expected = ["Old Fashioned", "Apple Cider", "Jelly", "Blueberry", "Pumpkin Spice"]

        self.assertListEqual(expected, popularity_list)

    def test_priority_orders_tomorrow(self):
        priority_orders_tomorrow = self.orders[
            (self.orders["DeliveryDate"] == TOMORROW) &
            ((self.orders["Quantity"] >= 12) | (self.orders["Customer"] == "Bob"))
        ].set_index("Customer")

        expected = pd.DataFrame(
            [
                ["Dave",  TOMORROW, "Old Fashioned", 12],
                ["Alice", TOMORROW,         "Jelly", 12],
                ["Bob",   TOMORROW, "Pumpkin Spice",  1]
            ],
            columns=["Customer", "DeliveryDate", "Donut", "Quantity"]
        ).set_index("Customer")

        print(priority_orders_tomorrow)
        print(expected)

        self.assertTrue(expected.equals(priority_orders_tomorrow))

    def test_total_spend_per_customer(self):
        # join orders to menu
        orders_with_prices = self.orders.merge(self.menu, how="left", on="Donut")

        # add order price column
        orders_with_prices["OrderPrice"] = np.where(
            orders_with_prices["Quantity"] < 12,
            orders_with_prices["Price"] * orders_with_prices["Quantity"],
            orders_with_prices["DiscountPrice"] * orders_with_prices["Quantity"]
        )

        # group by and aggregate
        spend_per_customer = orders_with_prices.groupby("Customer").agg({"OrderPrice": ["sum"]})

        spend_per_customer.columns = spend_per_customer.columns.get_level_values(0)

        expected = pd.DataFrame(
            [
                ["Alice", 45.80],
                ["Bob",   11.55],
                ["Carol", 13.30],
                ["Dave",  10.80]
            ],
            columns=["Customer", "OrderPrice"]
        ).set_index("Customer")

        print(spend_per_customer)
        print(type(spend_per_customer))

        print(expected)

        self.assertTrue(expected.equals(spend_per_customer))

    def test_donut_count_per_customer_per_day(self):
        # TODO: use pivot_table
        deliveries_by_cust_by_date = (self.orders
                                      .groupby(["Customer", "DeliveryDate"])
                                      .sum() # only care about Quantity
                                      .reset_index() # flatten all index levels for rows
                                      .pivot(index="Customer", columns="DeliveryDate",
                                             values="Quantity")
                                      )

        expected = pd.DataFrame(
            {
                "Customer": ["Alice", "Bob", "Carol", "Dave"],
                YESTERDAY: [14.0, 12.0, nan, nan],
                TODAY: [14.0, nan, 12.0, nan],
                TOMORROW: [12.0, 1.0, 2.0, 12.0]
            }
        ).set_index("Customer")

        self.assertTrue(expected.equals(deliveries_by_cust_by_date))


if __name__ == "__main__":
    unittest.main()

