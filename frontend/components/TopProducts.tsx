'use client';

import { Package } from 'lucide-react';

interface Product {
  product_category: string;
  product_name: string;
  revenue: number;
  quantity: number;
  order_count: number;
}

interface TopProductsProps {
  products: Product[];
}

const categoryColors: Record<string, string> = {
  'Electronics': 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  'Clothing': 'bg-purple-500/20 text-purple-400 border-purple-500/30',
  'Home & Garden': 'bg-green-500/20 text-green-400 border-green-500/30',
  'Sports': 'bg-orange-500/20 text-orange-400 border-orange-500/30',
  'Books': 'bg-pink-500/20 text-pink-400 border-pink-500/30',
};

export default function TopProducts({ products }: TopProductsProps) {
  const formatCurrency = (value: number) => {
    return value.toLocaleString('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    });
  };

  return (
    <div className="relative overflow-hidden rounded-2xl bg-white/10 backdrop-blur-xl border border-white/20 p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600">
          <Package className="w-5 h-5 text-white" />
        </div>
        <h3 className="text-xl font-bold text-white">Top Products</h3>
      </div>

      <div className="space-y-3">
        {products.slice(0, 8).map((product, index) => {
          const maxRevenue = products[0]?.revenue || 1;
          const barWidth = (product.revenue / maxRevenue) * 100;
          const colorClass = categoryColors[product.product_category] || 'bg-gray-500/20 text-gray-400 border-gray-500/30';

          return (
            <div key={`${product.product_category}-${product.product_name}`} className="relative">
              {/* Progress bar background */}
              <div 
                className="absolute inset-0 rounded-lg bg-gradient-to-r from-emerald-500/20 to-transparent"
                style={{ width: `${barWidth}%` }}
              />
              
              <div className="relative flex items-center justify-between p-3 rounded-lg border border-white/5 hover:border-white/10 transition-colors">
                <div className="flex items-center gap-3">
                  <span className="text-gray-500 text-sm w-6">{index + 1}.</span>
                  <div>
                    <p className="text-white font-medium">{product.product_name}</p>
                    <span className={`text-xs px-2 py-0.5 rounded-full border ${colorClass}`}>
                      {product.product_category}
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-emerald-400 font-bold">{formatCurrency(product.revenue)}</p>
                  <p className="text-gray-500 text-sm">{product.quantity} units</p>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
