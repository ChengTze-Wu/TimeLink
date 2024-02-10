"use client";

import { Table, Tag } from "antd";
import { useSearchParams, usePathname, useRouter } from "next/navigation";

export default function BookingsTable({
  displayAppointments,
  currentPage,
  totalItems,
}: {
  displayAppointments: any[];
  currentPage: number;
  totalItems: number;
}) {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const { replace } = useRouter();

  const handlePageChange = (page: number) => {
    const params = new URLSearchParams(searchParams);
    params.set("page", page.toString());
    replace(`${pathname}?${params.toString()}`);
  };

  const columns = [
    {
      title: "服務名稱",
      dataIndex: "serviceName",
      key: "serviceName",
    },
    {
      title: "預約人",
      dataIndex: "username",
      key: "username",
    },
    {
      title: "聯絡電話",
      dataIndex: "userPhone",
      key: "userPhone",
    },
    {
      title: "電子郵件",
      dataIndex: "userEmail",
      key: "userEmail",
    },
    {
      title: "預約日期",
      dataIndex: "reservedAt",
      key: "reservedAt",
    },
    {
      title: "狀態",
      dataIndex: "isActive",
      key: "isActive",
      render: (status: string) => {
        return <Tag color={status === "確認" ? "green" : "red"}>{status}</Tag>;
      },
    },
  ];

  return (
    <Table
      columns={columns}
      dataSource={displayAppointments}
      pagination={{
        pageSize: 9,
        position: ["bottomCenter"],
        current: currentPage,
        total: totalItems,
        onChange: handlePageChange,
      }}
    />
  );
}