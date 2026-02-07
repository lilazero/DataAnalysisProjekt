import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


class SalesAnalyzer:
    def __init__(self, data_path: Optional[str] = None, output_dir: str = "output"):
        self.data_path = data_path
        self.output_dir = output_dir
        self._data: Optional[pd.DataFrame] = None
        self._clean_data: Optional[pd.DataFrame] = None
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

    def inspect_data(self) -> Dict[str, Any]:
        df = self.get_data()
        info = {
            "shape": df.shape,
            "columns": list(df.columns),
            "missing_values": df.isnull().sum().to_dict(),
            "duplicates": int(df.duplicated().sum()),
        }
        return info

    def clean_data_pipeline(self) -> pd.DataFrame:
        df = self.get_data().copy()

        if "status" in df.columns:
            df["status"] = df["status"].fillna("pending").astype(str).str.lower().str.strip()

        for col in ["product_category", "product_name", "customer_id", "order_id"]:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()

        for col in ["order_amount", "unit_price", "quantity"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        if "quantity" in df.columns:
            df = df[df["quantity"] > 0]

        if "order_amount" in df.columns:
            df = df[df["order_amount"] >= 0]

        if "order_date" in df.columns:
            df = df[df["order_date"].notna()]

        if "order_id" in df.columns:
            df = df.drop_duplicates(subset=["order_id"])

        self._clean_data = df
        return df

    def export_clean_data(self, path: Optional[str] = None) -> str:
        if self._clean_data is None:
            raise ValueError("No clean data available")

        if path is None:
            base_dir = os.path.dirname(self.data_path) if self.data_path else self.output_dir
            path = os.path.join(base_dir, "sales_clean.csv")

        os.makedirs(os.path.dirname(path), exist_ok=True)
        self._clean_data.to_csv(path, index=False)
        return path

    def get_data(self) -> pd.DataFrame:
        if self._clean_data is not None:
            return self._clean_data
        if self._data is None:
            raise ValueError("No data loaded")
        return self._data

    def _completed(self, df: pd.DataFrame) -> pd.DataFrame:
        if "status" not in df.columns:
            return df
        return df[df["status"] == "completed"]

    def get_revenue_by_category(self) -> pd.Series:
        df = self.get_data()
        completed = self._completed(df)
        if {"product_category", "order_amount"}.issubset(completed.columns):
            return (
                completed.groupby("product_category")["order_amount"]
                .sum()
                .sort_values(ascending=False)
            )
        return pd.Series(dtype=float)

    def get_monthly_revenue(self) -> pd.Series:
        df = self.get_data()
        completed = self._completed(df).copy()
        if "order_date" not in completed.columns or "order_amount" not in completed.columns:
            return pd.Series(dtype=float)
        completed = completed.dropna(subset=["order_date"])
        completed["month"] = completed["order_date"].dt.to_period("M")
        return completed.groupby("month")["order_amount"].sum().sort_index()

    def _count_outliers(self, df: pd.DataFrame, column: str = "order_amount") -> int:
        if column not in df.columns or df[column].empty:
            return 0
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        if iqr == 0:
            return 0
        low = q1 - 2.0 * iqr
        high = q3 + 2.0 * iqr
        return int(df[(df[column] < low) | (df[column] > high)].shape[0])

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

        avg_order_size_by_category = {}
        if {"product_category", "quantity"}.issubset(completed.columns):
            avg_order_size_by_category = (
                completed.groupby("product_category")["quantity"].mean().round(2).to_dict()
            )

        customer_segments = {"customer_count": {}, "total_revenue": {}, "avg_spending": {}}
        if {"customer_id", "order_amount"}.issubset(completed.columns):
            spending = completed.groupby("customer_id")["order_amount"].sum()
            if len(spending):
                p70 = spending.quantile(0.70)
                p90 = spending.quantile(0.90)

                def tier(value: float) -> str:
                    if value >= p90:
                        return "Premium"
                    if value >= p70:
                        return "Regular"
                    return "Low"

                segments = spending.apply(tier)
                customer_segments = {
                    "customer_count": segments.value_counts().to_dict(),
                    "total_revenue": spending.groupby(segments).sum().to_dict(),
                    "avg_spending": spending.groupby(segments).mean().to_dict(),
                }

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
            "avg_order_size_by_category": avg_order_size_by_category,
            "customer_segments": customer_segments,
            "top_customers": top_customers,
            "top_products": top_products,
            "outlier_count": self._count_outliers(completed),
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

    def export_top_lists(self, output_dir: Optional[str] = None) -> List[str]:
        if not self._analytics:
            self.run_basic_analytics()

        if output_dir is None:
            output_dir = self.output_dir

        os.makedirs(output_dir, exist_ok=True)
        exported: List[str] = []

        customers_path = os.path.join(output_dir, "top_customers.csv")
        pd.DataFrame(self._analytics.get("top_customers", [])).to_csv(
            customers_path, index=False
        )
        exported.append(customers_path)

        products_path = os.path.join(output_dir, "top_products.csv")
        pd.DataFrame(self._analytics.get("top_products", [])).to_csv(
            products_path, index=False
        )
        exported.append(products_path)

        return exported

    def generate_summary_report(self, output_path: Optional[str] = None) -> str:
        if not self._analytics:
            self.run_basic_analytics()

        analytics = self._analytics
        lines = [
            "=" * 60,
            "SALES ANALYTICS SUMMARY",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 60,
            "",
            f"Total Revenue: ${analytics['total_revenue']:,.2f}",
            f"Average Order Value: ${analytics['average_order_value']:,.2f}",
            f"Total Customers: {analytics['customer_count']}",
            f"Total Orders: {analytics['order_count']}",
            f"Repeat Customer Rate: {analytics['repeat_customer_rate']:.1f}%",
            "",
            f"Top Category: {analytics['most_profitable_category']['name']} (${analytics['most_profitable_category']['revenue']:,.2f})",
            "",
            "Order Status:",
        ]

        for status, count in analytics["order_status_distribution"]["count"].items():
            pct = analytics["order_status_distribution"]["percentage"][status]
            lines.append(f"  {status}: {count} ({pct:.1f}%)")

        lines.append("")
        lines.append(f"Outlier Orders: {analytics['outlier_count']}")

        text = "\n".join(lines)

        if output_path is None:
            output_path = os.path.join(self.output_dir, "summary_report.txt")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

        return text

    def create_visualizations(self, output_dir: Optional[str] = None) -> List[str]:
        if output_dir is None:
            output_dir = os.path.join(self.output_dir, "figures")

        os.makedirs(output_dir, exist_ok=True)
        plt.style.use("seaborn-v0_8-darkgrid")

        files = [
            self._create_category_bar_chart(output_dir),
            self._create_monthly_line_chart(output_dir),
            self._create_order_histogram(output_dir),
            self._create_category_boxplot(output_dir),
        ]
        return [path for path in files if path]

    def _create_category_bar_chart(self, output_dir: str) -> str:
        revenue_by_cat = self.get_revenue_by_category()
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = plt.cm.get_cmap("viridis")(np.linspace(0.2, 0.8, len(revenue_by_cat)))
        ax.bar(revenue_by_cat.index, revenue_by_cat.values, color=colors)
        ax.set_xlabel("Product Category")
        ax.set_ylabel("Revenue ($)")
        ax.set_title("Revenue by Product Category")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        path = os.path.join(output_dir, "revenue_by_category.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def _create_monthly_line_chart(self, output_dir: str) -> str:
        monthly = self.get_monthly_revenue()
        fig, ax = plt.subplots(figsize=(12, 6))
        x_labels = [str(m) for m in monthly.index]
        ax.plot(x_labels, monthly.values, marker="o", linewidth=2, color="#2E86AB")
        ax.fill_between(x_labels, monthly.values, alpha=0.3, color="#2E86AB")
        ax.set_xlabel("Month")
        ax.set_ylabel("Revenue ($)")
        ax.set_title("Monthly Revenue Trend")
        plt.xticks(rotation=45, ha="right")
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        plt.tight_layout()
        path = os.path.join(output_dir, "monthly_revenue_trend.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def _create_order_histogram(self, output_dir: str) -> str:
        df = self.get_data()
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(
            df["order_amount"], bins=30, color="#E94560", edgecolor="white", alpha=0.7
        )
        ax.set_xlabel("Order Amount ($)")
        ax.set_ylabel("Frequency")
        ax.set_title("Distribution of Order Values")
        plt.tight_layout()
        path = os.path.join(output_dir, "order_value_distribution.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def _create_category_boxplot(self, output_dir: str) -> str:
        df = self.get_data()
        if "product_category" not in df.columns or "order_amount" not in df.columns:
            return ""

        categories = df["product_category"].dropna().unique()
        data = [df[df["product_category"] == c]["order_amount"].values for c in categories]

        fig, ax = plt.subplots(figsize=(10, 6))
        bp = ax.boxplot(data, labels=categories, patch_artist=True)
        colors = plt.cm.get_cmap("Set2")(np.linspace(0, 1, len(categories)))
        for patch, color in zip(bp["boxes"], colors):
            patch.set_facecolor(color)

        ax.set_xlabel("Product Category")
        ax.set_ylabel("Order Amount ($)")
        ax.set_title("Order Amount by Category")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        path = os.path.join(output_dir, "category_boxplot.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path