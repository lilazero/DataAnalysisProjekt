'use client';

import { useEffect, useState } from 'react';
import { BarChart3, TrendingUp } from 'lucide-react';
import StatCard from '@/components/StatCard';
import CategoryChart from '@/components/CategoryChart';
import RevenueChart from '@/components/RevenueChart';
import StatusChart from '@/components/StatusChart';
import TopCustomers from '@/components/TopCustomers';
import TopProducts from '@/components/TopProducts';

interface Analytics {
  total_revenue: number;
  average_order_value: number;
  customer_count: number;
  order_count: number;
  repeat_customer_rate: number;
  most_profitable_category: { name: string; revenue: number };
  revenue_by_category: Record<string, number>;
  top_customers: Array<{
    customer_id: string;
    lifetime_value: number;
    order_count: number;
    avg_order_value: number;
  }>;
  monthly_revenue: Record<string, number>;
  monthly_growth: Record<string, number>;
  order_status_distribution: {
    count: Record<string, number>;
    percentage: Record<string, number>;
  };
  top_products: Array<{
    product_category: string;
    product_name: string;
    revenue: number;
    quantity: number;
    order_count: number;
  }>;
}

export default function Home() {
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/analytics.json')
      .then((res) => res.json())
      .then((data) => {
        setAnalytics(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Error loading analytics:', err);
        setLoading(false);
      });
  }, []);

  const formatCurrency = (value: number) => {
    return value.toLocaleString('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-animated-gradient flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-400 text-lg">Loading analytics...</p>
        </div>
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="min-h-screen bg-animated-gradient flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-400 text-lg">Failed to load analytics data</p>
          <p className="text-gray-500 mt-2">Make sure to run the Python backend first!</p>
        </div>
      </div>
    );
  }

  // Get latest month growth for trend indicator
  const growthValues = Object.values(analytics.monthly_growth);
  const latestGrowth = growthValues[growthValues.length - 1] || 0;

  return (
    <main className="min-h-screen bg-animated-gradient">
      {/* Header */}
      <header className="border-b border-white/10 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 glow-emerald">
                <BarChart3 className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">Sales Analytics</h1>
                <p className="text-gray-500 text-sm">Real-time insights dashboard</p>
              </div>
            </div>
            <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 border border-white/20">
              <TrendingUp className={`w-4 h-4 ${latestGrowth >= 0 ? 'text-emerald-400' : 'text-red-400'}`} />
              <span className={`text-sm font-medium ${latestGrowth >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                {latestGrowth >= 0 ? '+' : ''}{latestGrowth.toFixed(1)}% this month
              </span>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
          <StatCard
            title="Total Revenue"
            value={formatCurrency(analytics.total_revenue)}
            icon="revenue"
            trend={latestGrowth}
          />
          <StatCard
            title="Avg Order Value"
            value={formatCurrency(analytics.average_order_value)}
            icon="aov"
          />
          <StatCard
            title="Customers"
            value={analytics.customer_count}
            icon="customers"
          />
          <StatCard
            title="Total Orders"
            value={analytics.order_count}
            icon="orders"
          />
          <StatCard
            title="Repeat Rate"
            value={`${analytics.repeat_customer_rate}%`}
            icon="repeat"
            subtitle="returning customers"
          />
        </div>

        {/* Charts Row 1 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <RevenueChart 
            data={analytics.monthly_revenue} 
            growth={analytics.monthly_growth} 
          />
          <CategoryChart data={analytics.revenue_by_category} />
        </div>

        {/* Charts Row 2 */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <div className="lg:col-span-2">
            <TopCustomers customers={analytics.top_customers} />
          </div>
          <StatusChart data={analytics.order_status_distribution} />
        </div>

        {/* Products Section */}
        <div className="mb-8">
          <TopProducts products={analytics.top_products} />
        </div>

        {/* Footer */}
        <footer className="text-center py-6 border-t border-white/10">
          <p className="text-gray-500 text-sm">
            Sales Analytics Platform • Data processed by Python backend • 
            Visualization powered by Next.js & Recharts
          </p>
        </footer>
      </div>
    </main>
  );
}
