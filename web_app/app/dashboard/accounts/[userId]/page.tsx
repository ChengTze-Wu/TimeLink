import Breadcrumbs from "@/app/ui/common/breadcrumbs";
import { notFound } from "next/navigation";
import { Metadata } from "next";
import { getJson } from "@/app/lib/fetch-api-data";
import { Descriptions, List } from "antd";
import type { DescriptionsProps } from "antd";
import { UUID } from "crypto";

export const metadata: Metadata = {
  title: "Accounts | Dashboard",
};

export default async function Page({ params }: { params: { userId: UUID } }) {
  const user_id = params.userId;
  const user = await getJson(`/api/users/${user_id}`);

  if (user.status === 404) {
    notFound();
  }

  const items: DescriptionsProps["items"] = [
    {
      key: "1",
      label: "名稱",
      children: user.name,
    },
    {
      key: "2",
      label: "帳號",
      children: user.username,
    },
    {
      key: "4",
      label: "電話",
      children:
        user.phone === null ? (
          <span className="text-gray-400">empty</span>
        ) : (
          user.phone
        ),
    },
    {
      key: "3",
      label: "電子郵件",
      children: user.email,
    },
    {
      key: "5",
      label: "角色",
      children: user.role,
    },
    {
      key: "6",
      label: "是否啟用",
      children: user.is_active ? "是" : "否",
    },
    {
      key: "7",
      label: "建立時間",
      children: user.created_at,
    },
    {
      key: "8",
      label: "上次更新時間",
      children: user.updated_at,
    },
  ];

  return (
    <main>
      <Breadcrumbs
        breadcrumbs={[
          { label: "儀表板", href: "/dashboard" },
          {
            label: "使用者資訊",
            href: `/dashboard/accounts/${user_id}`,
            active: true,
          },
        ]}
      />
      <Descriptions title="使用者資訊" layout="vertical" items={items} />
    </main>
  );
}
