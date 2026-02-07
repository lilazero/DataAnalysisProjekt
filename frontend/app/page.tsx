'use client';

import { useEffect, useState } from 'react';

interface Analytics {
  total_revenue: number;
  average_order_value: number;
  customer_count: number;
  order_count: number;
  repeat_customer_rate: number;
  most_profitable_category: { name: string; revenue: number };
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
          <div className="w-12 h-12 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          <p className="text-gray-400 text-base">Loading analytics...</p>
        </div>
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="min-h-screen bg-animated-gradient flex items-center justify-center">
        <div className="text-center max-w-md">
          <p className="text-red-400 text-lg">Failed to load analytics data</p>
          <p className="text-gray-500 mt-2 text-sm">
            Run the Python pipeline to generate frontend/public/analytics.json.
          </p>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-animated-gradient">
      <div className="max-w-4xl mx-auto px-6 py-10">
        <header className="mb-8">
          <h1 className="text-2xl font-bold text-white">Sales Analytics</h1>
          <p className="text-gray-500 text-sm">
            Minimal UI to prove Python analytics load in Next.js.
          </p>
        </header>

        <section className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="rounded-xl border border-white/10 bg-white/5 p-4">
            <p className="text-gray-400 text-xs uppercase tracking-wide">Total Revenue</p>
            <p className="text-white text-2xl font-semibold mt-2">
              {formatCurrency(analytics.total_revenue)}
            </p>
          </div>
          <div className="rounded-xl border border-white/10 bg-white/5 p-4">
            <p className="text-gray-400 text-xs uppercase tracking-wide">Orders</p>
            <p className="text-white text-2xl font-semibold mt-2">
              {analytics.order_count}
            </p>
          </div>
          <div className="rounded-xl border border-white/10 bg-white/5 p-4">
            <p className="text-gray-400 text-xs uppercase tracking-wide">Customers</p>
            <p className="text-white text-2xl font-semibold mt-2">
              {analytics.customer_count}
            </p>
          </div>
        </section>

        <section className="rounded-xl border border-white/10 bg-white/5 p-5">
          <h2 className="text-white font-semibold">Top Category</h2>
          <p className="text-gray-400 text-sm mt-1">
            {analytics.most_profitable_category.name}
          </p>
          <p className="text-white text-lg mt-3">
            {formatCurrency(analytics.most_profitable_category.revenue)}
          </p>
          <p className="text-gray-500 text-xs mt-4">
            Data source: frontend/public/analytics.json
          </p>
        </section>
      </div>
    </main>
  );
}
