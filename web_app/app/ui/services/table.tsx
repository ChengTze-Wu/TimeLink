"use client";

import {
  Table,
  Tag,
  ConfigProvider,
  Button,
  Popconfirm,
  Switch,
  Avatar,
} from "antd";
import type { TableProps } from "antd";
import { useSearchParams, usePathname, useRouter } from "next/navigation";
import { Group, Service } from "@/app/lib/definitions";
import {
  QuestionCircleOutlined,
  DeleteOutlined,
  EditOutlined,
} from "@ant-design/icons";
import { deleteService, switchStatus } from "@/app/lib/services/actions";
import { UUID } from "crypto";
import { PhotoIcon } from "@heroicons/react/24/solid";
import Link from "next/link";

export default function ServicesTable({
  displayData,
  pageSize,
  currentPage,
  totalItems,
}: {
  displayData: Service[];
  pageSize: number;
  currentPage: number;
  totalItems: number;
}) {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const { replace } = useRouter();

  const handleDelete = async (id: UUID) => {
    const result = await deleteService(id);
    return result?.message;
  };

  const handleSwitch = async (id: UUID, status: boolean) => {
    const result = await switchStatus(id, status);
    return result?.message;
  };

  const columns: TableProps<Service>["columns"] = [
    {
      title: "服務項目名稱",
      dataIndex: "name",
      key: "name",
      width: "15%",
      render: (name: string, row: Service) => (
        <span className="flex gap-2 items-center">
          <Avatar
            size="large"
            src={row.image}
            alt={name}
            icon={<PhotoIcon />}
          />
          <span>{name}</span>
        </span>
      ),
    },
    {
      title: "隸屬群組",
      dataIndex: "groups",
      key: "groups",
      width: "20%",
      render: (groups: Group[]) => (
        <span>
          {groups.map((group) => {
            return <Tag key={group.id}>{group.name}</Tag>;
          })}
        </span>
      ),
    },
    {
      title: "單位時間",
      dataIndex: "duration",
      key: "duration",
      render: (duration) => <span>{duration} 分鐘</span>,
    },
    {
      title: "價格",
      dataIndex: "price",
      key: "price",
      render: (price) => <span>NT$ {price} 元</span>,
    },
    {
      title: "狀態",
      dataIndex: "",
      key: "isActive",
      render: (row) => (
        <Popconfirm
          title="狀態"
          description={`你確定要"${row.isActive ? "停用" : "啟用"}"此服務嗎？`}
          icon={<QuestionCircleOutlined style={{ color: "red" }} />}
          okText="確定"
          cancelText="取消"
          onConfirm={() => handleSwitch(row.key, !row.isActive)}
        >
          <Switch
            checkedChildren="啟用中"
            unCheckedChildren="停用中"
            defaultChecked={row.isActive}
            checked={row.isActive}
          />
        </Popconfirm>
      ),
    },
    {
      title: "上次修改時間",
      dataIndex: "updatedAt",
      key: "updatedAt",
    },
    {
      title: "",
      dataIndex: "",
      key: "x",
      render: (row) => (
        <div className=" flex gap-2">
          <Link href={`/dashboard/services/${row.key}/edit`}>
            <Button icon={<EditOutlined />} />
          </Link>
          <Popconfirm
            title="刪除服務項目"
            description="確定要刪除嗎？"
            icon={<QuestionCircleOutlined style={{ color: "red" }} />}
            onConfirm={() => handleDelete(row.key)}
            okText="確定"
            cancelText="取消"
          >
            <Button icon={<DeleteOutlined />} danger />
          </Popconfirm>
        </div>
      ),
    },
  ];

  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: "#44ad53",
        },
      }}
    >
      <Table
        columns={columns}
        dataSource={displayData}
        pagination={{
          pageSize: pageSize,
          position: ["bottomCenter"],
          current: currentPage,
          total: totalItems,
          showSizeChanger: false,
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
    </ConfigProvider>
  );
}
