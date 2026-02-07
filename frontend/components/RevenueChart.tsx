'use client';

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Area,
  AreaChart,
} from 'recharts';

interface RevenueChartProps {
  data: Record<string, number>;
  growth: Record<string, number>;
}

export default function RevenueChart({ data, growth }: RevenueChartProps) {
  const chartData = Object.entries(data).map(([month, revenue]) => {
    const monthName = new Date(month + '-01').toLocaleDateString('en-US', { month: 'short' });
    return {
      month: monthName,
      fullMonth: month,
      revenue,
      growth: growth[month] || 0,
    };
  });

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-gray-900/95 backdrop-blur-sm border border-white/20 rounded-lg p-4 shadow-xl">
          <p className="text-gray-400 text-sm">{payload[0].payload.fullMonth}</p>
          <p className="text-white font-bold text-lg">
            ${payload[0].value.toLocaleString('en-US', { minimumFractionDigits: 2 })}
          </p>
          {payload[0].payload.growth !== 0 && (
            <p className={`text-sm ${payload[0].payload.growth >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
              {payload[0].payload.growth >= 0 ? '+' : ''}{payload[0].payload.growth.toFixed(1)}% MoM
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="relative overflow-hidden rounded-2xl bg-white/10 backdrop-blur-xl border border-white/20 p-6">
      <h3 className="text-xl font-bold text-white mb-6">Monthly Revenue Trend</h3>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="revenueGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis 
              dataKey="month" 
              stroke="#9ca3af"
              axisLine={false}
              tickLine={false}
            />
            <YAxis 
              stroke="#9ca3af"
              axisLine={false}
              tickLine={false}
              tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Area
              type="monotone"
              dataKey="revenue"
              stroke="#3b82f6"
              strokeWidth={3}
              fill="url(#revenueGradient)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
