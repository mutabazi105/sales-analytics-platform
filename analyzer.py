"""
SalesAnalyzer class for data loading, cleaning, and analysis
"""
import pandas as pd
import numpy as np
from datetime import datetime
from models import EntityFactory


class SalesAnalyzer:
    """Main analyzer class for sales data"""

    def __init__(self, data_path="data/sales_data.csv"):
        self.data_path = data_path
        self.raw_df = None
        self.clean_df = None
        self.factory = EntityFactory()

    def load_data(self):
        """Load CSV data into DataFrame"""
        self.raw_df = pd.read_csv(self.data_path)
        print(f"📊 Loaded {len(self.raw_df)} records from {self.data_path}")
        return self.raw_df

    def inspect_data(self):
        """Inspect data structure and quality"""
        if self.raw_df is None:
            self.load_data()

        print("\n" + "="*40)
        print("DATA INSPECTION")
        print("="*40)

        print(f"Shape: {self.raw_df.shape}")
        print(f"\nColumns: {list(self.raw_df.columns)}")
        print(f"\nData Types:\n{self.raw_df.dtypes}")
        print(f"\nMissing Values:\n{self.raw_df.isnull().sum()}")

        print("\nSample Data (first 3 rows):")
        print(self.raw_df.head(3))

    def clean_data(self):
        """Clean and prepare data for analysis"""
        if self.raw_df is None:
            self.load_data()

        df = self.raw_df.copy()

        print("\n" + "="*40)
        print("DATA CLEANING")
        print("="*40)

        # 1. Handle missing values
        print("1. Handling missing values...")
        df['status'] = df['status'].fillna('pending')

        # 2. Convert data types
        print("2. Converting data types...")
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        df['order_amount'] = pd.to_numeric(df['order_amount'], errors='coerce')
        df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')

        # 3. Remove invalid entries
        print("3. Removing invalid entries...")
        initial_count = len(df)
        df = df[df['order_amount'] > 0]
        df = df[df['quantity'] > 0]
        removed_count = initial_count - len(df)
        print(f"   Removed {removed_count} invalid entries")

        # 4. Remove duplicates
        print("4. Removing duplicates...")
        initial_count = len(df)
        df = df.drop_duplicates(subset=['order_id'], keep='first')
        removed_duplicates = initial_count - len(df)
        print(f"   Removed {removed_duplicates} duplicate orders")

        self.clean_df = df
        print(f"\n✅ Cleaning complete!")
        print(f"   Final shape: {df.shape}")

        return df

    def export_clean_data(self, output_path="data/sales_clean.csv"):
        """Export cleaned data to CSV"""
        if self.clean_df is None:
            self.clean_data()

        self.clean_df.to_csv(output_path, index=False)
        print(f"✅ Clean data exported to {output_path}")
        return output_path

    def calculate_metrics(self):
        """Calculate key business metrics"""
        if self.clean_df is None:
            self.clean_data()

        completed_orders = self.clean_df[self.clean_df['status']
                                         == 'completed']

        metrics = {
            'total_revenue': completed_orders['order_amount'].sum(),
            'total_orders': len(completed_orders),
            'customer_count': self.clean_df['customer_id'].nunique(),
            'avg_order_value': completed_orders['order_amount'].mean(),
            'repeat_customer_rate': self._calculate_repeat_rate(),
            'cancellation_rate': (len(self.clean_df[self.clean_df['status'] == 'cancelled']) / len(self.clean_df)) * 100
        }

        return metrics

    def _calculate_repeat_rate(self):
        """Calculate percentage of customers with multiple orders"""
        order_counts = self.clean_df['customer_id'].value_counts()
        repeat_customers = len(order_counts[order_counts > 1])
        total_customers = len(order_counts)
        return (repeat_customers / total_customers) * 100 if total_customers > 0 else 0

    def get_top_categories(self, n=5):
        """Get top n categories by revenue"""
        completed = self.clean_df[self.clean_df['status'] == 'completed']
        category_revenue = completed.groupby('product_category')[
            'order_amount'].sum()
        return category_revenue.sort_values(ascending=False).head(n)

    def get_top_customers(self, n=10):
        """Get top n customers by total spending"""
        completed = self.clean_df[self.clean_df['status'] == 'completed']
        customer_spending = completed.groupby(
            'customer_id')['order_amount'].sum()
        return customer_spending.sort_values(ascending=False).head(n)

    def analyze_seasonal_trends(self):
        """Analyze monthly sales trends"""
        completed = self.clean_df[self.clean_df['status'] == 'completed']
        completed['month'] = completed['order_date'].dt.to_period('M')
        monthly_sales = completed.groupby('month')['order_amount'].sum()
        return monthly_sales

    def answer_business_questions(self):
        """Answer the 8+ required business questions"""
        metrics = self.calculate_metrics()

        answers = {
            "1. Total Revenue": f"${metrics['total_revenue']:,.2f}",
            "2. Average Order Value": f"${metrics['avg_order_value']:,.2f}",
            "3. Customer Count": metrics['customer_count'],
            "4. Most Profitable Category": self.get_top_categories(1).index[0],
            "5. Top 10 Customers": self.get_top_customers(10).to_dict(),
            "6. Repeat Customer Rate": f"{metrics['repeat_customer_rate']:.1f}%",
            "7. Monthly Sales Trends": self.analyze_seasonal_trends().to_dict(),
            "8. Cancellation Rate": f"{metrics['cancellation_rate']:.1f}%"
        }

        return answers
