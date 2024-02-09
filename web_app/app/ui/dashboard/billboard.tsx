"use client";

import { Card, Statistic } from "antd";

export function BillboardCard({
  title,
  value,
}: {
  title: string;
  value: number;
}) {
  return (
    <Card bordered={false} className="w-1/4">
      <Statistic
        title={title}
        value={value}
        valueStyle={{
          color: "#3f8600",
          fontSize: "3rem",
        }}
      />
    </Card>
  );
}
