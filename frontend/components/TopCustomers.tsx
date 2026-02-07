'use client';

import { Trophy } from 'lucide-react';

interface Customer {
  customer_id: string;
  lifetime_value: number;
  order_count: number;
  avg_order_value: number;
}

interface TopCustomersProps {
  customers: Customer[];
}

export default function TopCustomers({ customers }: TopCustomersProps) {
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
        <div className="p-2 rounded-lg bg-gradient-to-br from-yellow-500 to-orange-600">
          <Trophy className="w-5 h-5 text-white" />
        </div>
        <h3 className="text-xl font-bold text-white">Top Customers</h3>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="text-left text-gray-400 text-sm border-b border-white/10">
              <th className="pb-3 font-medium">#</th>
              <th className="pb-3 font-medium">Customer</th>
              <th className="pb-3 font-medium text-right">Lifetime Value</th>
              <th className="pb-3 font-medium text-right">Orders</th>
              <th className="pb-3 font-medium text-right">Avg Order</th>
            </tr>
          </thead>
          <tbody>
            {customers.slice(0, 10).map((customer, index) => (
              <tr
                key={customer.customer_id}
                className="border-b border-white/5 hover:bg-white/5 transition-colors"
              >
                <td className="py-3">
                  {index < 3 ? (
                    <span
                      className={`inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-bold ${
                        index === 0
                          ? 'bg-yellow-500 text-yellow-900'
                          : index === 1
                          ? 'bg-gray-300 text-gray-700'
                          : 'bg-orange-600 text-orange-100'
                      }`}
                    >
                      {index + 1}
                    </span>
                  ) : (
                    <span className="text-gray-500 pl-2">{index + 1}</span>
                  )}
                </td>
                <td className="py-3">
                  <span className="text-white font-medium">{customer.customer_id}</span>
                </td>
                <td className="py-3 text-right">
                  <span className="text-emerald-400 font-bold">
                    {formatCurrency(customer.lifetime_value)}
                  </span>
                </td>
                <td className="py-3 text-right text-gray-300">{customer.order_count}</td>
                <td className="py-3 text-right text-gray-400">
                  {formatCurrency(customer.avg_order_value)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
