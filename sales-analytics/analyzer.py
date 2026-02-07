import json
import os
from typing import Any, Dict, List, Optional

import pandas as pd


class SalesAnalyzer:
    def __init__(self, data_path: Optional[str] = None, output_dir: str = "output"):
        self.data_path = data_path
        self.output_dir = output_dir
        self._data: Optional[pd.DataFrame] = None
        self._analytics: Dict[str, Any] = {}

        if data_path:
            self.load_data(data_path)

    def load_data(self, path: str) -> pd.DataFrame:
        self.data_path = path
        df = pd.read_csv(path)
        if "order_date" in df.columns:
            df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
        if "status" in df.columns:
            df["status"] = df["status"].fillna("pending").astype(str).str.lower()
        for col in ["order_amount", "unit_price", "quantity"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        self._data = df
        return df

    def get_data(self) -> pd.DataFrame:
        if self._data is None:
            raise ValueError("No data loaded")
        return self._data

    def _completed(self, df: pd.DataFrame) -> pd.DataFrame:
        if "status" not in df.columns:
            return df
        return df[df["status"] == "completed"]

    def run_basic_analytics(self) -> Dict[str, Any]:
        df = self.get_data()
        completed = self._completed(df)

        total_revenue = float(completed["order_amount"].sum()) if "order_amount" in completed.columns else 0.0
        average_order_value = float(completed["order_amount"].mean()) if len(completed) else 0.0
        customer_count = int(df["customer_id"].nunique()) if "customer_id" in df.columns else 0
        order_count = int(len(df))

        revenue_by_category = {}
        if {"product_category", "order_amount"}.issubset(completed.columns):
            revenue_by_category = (
                completed.groupby("product_category")["order_amount"].sum().sort_values(ascending=False).to_dict()
            )

        most_profitable_category = {"name": "", "revenue": 0.0}
        if revenue_by_category:
            top_name = next(iter(revenue_by_category))
            most_profitable_category = {"name": top_name, "revenue": float(revenue_by_category[top_name])}

        monthly_revenue = {}
        monthly_growth = {}
        if "order_date" in completed.columns and "order_amount" in completed.columns:
            monthly = completed.dropna(subset=["order_date"]).copy()
            monthly["month"] = monthly["order_date"].dt.to_period("M").astype(str)
            monthly_series = monthly.groupby("month")["order_amount"].sum().sort_index()
            monthly_revenue = {k: float(v) for k, v in monthly_series.items()}
            growth = monthly_series.pct_change() * 100
            monthly_growth = {k: float(round(v, 2)) for k, v in growth.dropna().items()}

        order_status_distribution = {"count": {}, "percentage": {}}
        if "status" in df.columns:
            counts = df["status"].value_counts()
            percentages = (counts / len(df) * 100).round(2)
            order_status_distribution = {
                "count": counts.to_dict(),
                "percentage": percentages.to_dict(),
            }

        top_customers: List[Dict[str, Any]] = []
        if {"customer_id", "order_amount"}.issubset(completed.columns):
            stats = completed.groupby("customer_id").agg(
                lifetime_value=("order_amount", "sum"),
                order_count=("order_amount", "count"),
            )
            stats["avg_order_value"] = stats["lifetime_value"] / stats["order_count"]
            top_customers = (
                stats.sort_values("lifetime_value", ascending=False)
                .head(10)
                .reset_index()
                .to_dict(orient="records")
            )

        top_products: List[Dict[str, Any]] = []
        if {"product_category", "product_name", "order_amount", "quantity"}.issubset(completed.columns):
            prod_stats = completed.groupby(["product_category", "product_name"]).agg(
                revenue=("order_amount", "sum"),
                quantity=("quantity", "sum"),
                order_count=("order_amount", "count"),
            )
            top_products = (
                prod_stats.sort_values("revenue", ascending=False)
                .head(10)
                .reset_index()
                .to_dict(orient="records")
            )

        repeat_customer_rate = 0.0
        if "customer_id" in completed.columns:
            orders_per_customer = completed.groupby("customer_id").size()
            if len(orders_per_customer):
                repeat = int((orders_per_customer > 1).sum())
                repeat_customer_rate = float(repeat / len(orders_per_customer) * 100)

        analytics: Dict[str, Any] = {
            "total_revenue": round(total_revenue, 2),
            "average_order_value": round(average_order_value, 2),
            "customer_count": customer_count,
            "order_count": order_count,
            "repeat_customer_rate": round(repeat_customer_rate, 2),
            "most_profitable_category": {
                "name": most_profitable_category["name"],
                "revenue": round(float(most_profitable_category["revenue"]), 2),
            },
            "revenue_by_category": {k: round(float(v), 2) for k, v in revenue_by_category.items()},
            "monthly_revenue": {k: round(float(v), 2) for k, v in monthly_revenue.items()},
            "monthly_growth": monthly_growth,
            "order_status_distribution": order_status_distribution,
            "top_customers": top_customers,
            "top_products": top_products,
        }

        self._analytics = analytics
        return analytics

    def export_analytics_json(self, output_path: Optional[str] = None) -> str:
        if not self._analytics:
            self.run_basic_analytics()

        if output_path is None:
            output_path = os.path.join(self.output_dir, "analytics.json")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self._analytics, f, indent=2, default=str)

        return output_path