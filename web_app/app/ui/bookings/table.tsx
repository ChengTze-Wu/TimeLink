"use client";

import { Table, Tag, ConfigProvider, Input, Space } from "antd";
import type { TableProps } from "antd";
import { useSearchParams, usePathname, useRouter } from "next/navigation";
import { AppointmentsResp } from "@/app/dashboard/bookings/page";
import zh_TW from "antd/locale/zh_TW";

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

  const { Search } = Input;

  const columns: TableProps<AppointmentsResp>["columns"] = [
    {
      title: "預約人",
      dataIndex: "username",
      key: "username",
    },
    {
      title: "服務名稱",
      dataIndex: "serviceName",
      key: "serviceName",
    },
    {
      title: "預約日期",
      dataIndex: "reservedAt",
      key: "reservedAt",
      sorter: true,
    },
    {
      title: "服務擁有者",
      dataIndex: "serviceOwnerName",
      key: "serviceOwnerName",
    },
    {
      title: "歸屬群組",
      dataIndex: "serviceGroupNames",
      key: "serviceGroupNames",
    },
    {
      title: "更新日期",
      dataIndex: "updatedAt",
      key: "updatedAt",
      sorter: true,
    },
  ];

  const handleSearch = (value: string) => {
    const params = new URLSearchParams(searchParams);
    params.set("query", value);
    params.set("page", "1");
    replace(`${pathname}?${params.toString()}`);
  };

  return (
    <ConfigProvider
      locale={zh_TW}
      theme={{
        token: {
          colorPrimary: "#44ad53",
        },
      }}
    >
      <Space direction="vertical" style={{ width: "100%" }} size={24}>
        <Search
          placeholder="搜尋"
          enterButton="Search"
          size="large"
          onSearch={handleSearch}
        />
        <Table
          columns={columns}
          dataSource={displayAppointments}
          expandable={{
            expandedRowRender: (record) => (
              <p>
                <span className="font-semibold">備註：</span>
                {record.notes}
              </p>
            ),
            rowExpandable: (record) => record.notes,
          }}
          pagination={{
            pageSize: pageSize,
            position: ["bottomCenter"],
            current: currentPage,
            total: totalItems,
            showSizeChanger: false,
            showQuickJumper: true,
          }}
          onChange={(pagination, filters, sorter: any) => {
            const params = new URLSearchParams(searchParams);
            params.delete("sortField");
            params.delete("sortOrder");
            if (pagination.current) {
              params.set("page", pagination.current.toString());
            }
            if (sorter.field && sorter.order) {
              params.set("sortField", sorter.field);
              params.set("sortOrder", sorter.order);
            }
            if (Object.keys(filters).length > 0) {
              params.set("filters", JSON.stringify(filters));
            }
            replace(`${pathname}?${params.toString()}`);
          }}
          footer={() => <p className="text-right">共 {totalItems} 筆資料</p>}
        />
      </Space>
    </ConfigProvider>
  );
}
