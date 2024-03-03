"use client";

import { Table, Tag, ConfigProvider, Button, Popconfirm, Switch } from "antd";
import type { TableProps } from "antd";
import { useSearchParams, usePathname, useRouter } from "next/navigation";
import { Group } from "@/app/lib/definitions";
import { QuestionCircleOutlined } from "@ant-design/icons";
import { deleteGroup, switchStatus } from "@/app/lib/groups/actions";
import { UUID } from "crypto";

export default function GroupsTable({
  displayData,
  pageSize,
  currentPage,
  totalItems,
}: {
  displayData: Group[];
  pageSize: number;
  currentPage: number;
  totalItems: number;
}) {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const { replace } = useRouter();

  const handleDelete = async (id: UUID) => {
    const result = await deleteGroup(id);
    return result?.message;
  };

  const handleSwitch = async (id: UUID, status: boolean) => {
    const result = await switchStatus(id, status);
    return result?.message;
  };

  const columns: TableProps<Group>["columns"] = [
    {
      title: "Line 群組名稱",
      dataIndex: "name",
      key: "name",
      width: "15%",
    },
    {
      title: "群組 ID",
      dataIndex: "lineGroupId",
      key: "lineGroupId",
      width: "20%",
    },
    {
      title: "群組管理員",
      dataIndex: "ownerName",
      key: "ownerName",
    },
    {
      title: "群組狀態",
      dataIndex: "",
      key: "isActive",
      render: (row) => (
        <Popconfirm
          title="群組狀態"
          description={`你確定要"${row.isActive ? "停用" : "啟用"}"此群組嗎？`}
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
        <Popconfirm
          title="刪除群組"
          description="確定要刪除嗎？"
          icon={<QuestionCircleOutlined style={{ color: "red" }} />}
          onConfirm={() => handleDelete(row.key)}
          okText="確定"
          cancelText="取消"
        >
          <Button danger>刪除</Button>
        </Popconfirm>
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
