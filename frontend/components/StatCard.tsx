'use client';

import { TrendingUp, TrendingDown, DollarSign, Users, ShoppingCart, Repeat } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: 'revenue' | 'aov' | 'customers' | 'orders' | 'repeat';
  trend?: number;
}

const iconMap = {
  revenue: DollarSign,
  aov: TrendingUp,
  customers: Users,
  orders: ShoppingCart,
  repeat: Repeat,
};

const colorMap = {
  revenue: 'from-emerald-500 to-teal-600',
  aov: 'from-blue-500 to-indigo-600',
  customers: 'from-purple-500 to-pink-600',
  orders: 'from-orange-500 to-red-600',
  repeat: 'from-cyan-500 to-blue-600',
};

export default function StatCard({ title, value, subtitle, icon, trend }: StatCardProps) {
  const Icon = iconMap[icon];
  const gradient = colorMap[icon];

  return (
    <div className="relative overflow-hidden rounded-2xl bg-white/10 backdrop-blur-xl border border-white/20 p-6 transition-all duration-300 hover:scale-105 hover:bg-white/15 group">
      {/* Gradient glow effect */}
      <div className={`absolute -top-4 -right-4 w-24 h-24 bg-gradient-to-br ${gradient} rounded-full opacity-20 blur-2xl group-hover:opacity-30 transition-opacity`} />
      
      <div className="relative z-10">
        <div className="flex items-center justify-between mb-4">
          <div className={`p-3 rounded-xl bg-gradient-to-br ${gradient}`}>
            <Icon className="w-6 h-6 text-white" />
          </div>
          {trend !== undefined && (
            <div className={`flex items-center gap-1 text-sm ${trend >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
              {trend >= 0 ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
              <span>{Math.abs(trend).toFixed(1)}%</span>
            </div>
          )}
        </div>

        <h3 className="text-gray-400 text-sm font-medium uppercase tracking-wide">{title}</h3>
        <p className="text-3xl font-bold text-white mt-1">{value}</p>
        {subtitle && <p className="text-gray-500 text-sm mt-1">{subtitle}</p>}
      </div>
    </div>
  );
}
