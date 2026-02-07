import os
import sys
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analyzer import SalesAnalyzer
from generate_data import generate_sales_data


def main():
    print("=" * 60)
    print("SALES ANALYTICS PLATFORM")
    print("=" * 60)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    raw_data_path = os.path.join(data_dir, "sales_data.csv")
    if not os.path.exists(raw_data_path):
        print("Generating data...")
        generate_sales_data(200, raw_data_path)
    else:
        print("Using existing data")

    analyzer = SalesAnalyzer(output_dir=output_dir)
    analyzer.load_data(raw_data_path)
    analyzer.clean_data_pipeline()

    clean_data_path = os.path.join(data_dir, "sales_clean.csv")
    analyzer.export_clean_data(clean_data_path)
    analytics = analyzer.run_basic_analytics()
    print("\nKey insights")
    print(f"Total Revenue: ${analytics['total_revenue']:,.2f}")
    print(f"Average Order Value: ${analytics['average_order_value']:,.2f}")
    print(f"Customer Count: {analytics['customer_count']}")
    print(f"Repeat Customer Rate: {analytics['repeat_customer_rate']:.1f}%")
    print(f"Top Category: {analytics['most_profitable_category']['name']}")

    json_path = os.path.join(output_dir, "analytics.json")
    analyzer.export_analytics_json(json_path)

    frontend_public = os.path.abspath(
        os.path.join(base_dir, "..", "frontend", "public")
    )
    if os.path.isdir(frontend_public):
        shutil.copyfile(json_path, os.path.join(frontend_public, "analytics.json"))

    print("\nDone")
    print(f"Output: {output_dir}")
    return analytics


if __name__ == "__main__":
    main()
