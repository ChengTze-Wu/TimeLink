"use client";
import { ConfigProvider, Avatar, List } from "antd";
import { Service } from "@/app/lib/definitions";
import Link from "next/link";
import { useContext } from "react";
import ContextAlert from "@/app/ui/alert";
import { LiffContext } from "@/app/liff-provider";

export default function ServiceMenu({ services }: { services: Service[] }) {
  const { liff, error } = useContext(LiffContext);
  if (!liff?.isInClient()) return <ContextAlert />;

  const data = services?.map((service) => ({
    id: service.id,
    title: service.name,
    image: service.image,
    description: service.description || "尚未有說明",
    isActive: service.is_active ? (
      <Link href={`/services/${service.id}`}>點此預約</Link>
    ) : (
      "暫停預約"
    ),
  }));

  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: "#44ad53",
        },
      }}
    >
      <List
        itemLayout="horizontal"
        dataSource={data}
        renderItem={(item, index) => (
          <List.Item key={index} extra={item.isActive}>
            <List.Item.Meta
              avatar={<Avatar src={item.image} />}
              title={item.title}
              description={item.description}
            />
          </List.Item>
        )}
      />
    </ConfigProvider>
  );
}
