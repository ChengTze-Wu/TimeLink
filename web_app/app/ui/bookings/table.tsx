"use client";

import { Table, Tag } from "antd";
import { useSearchParams, usePathname, useRouter } from "next/navigation";

export default function BookingsTable({
  displayAppointments,
  pageSize,
  currentPage,
  totalItems,
}: {
  displayAppointments: any[];
  pageSize: number;
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
        pageSize: pageSize,
        position: ["bottomCenter"],
        current: currentPage,
        total: totalItems,
        onChange: handlePageChange,
      }}
    />
  );
}
