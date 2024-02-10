"use client";

import { useRouter } from "next/navigation";
import { Button, ConfigProvider, Typography } from "antd";
import { QuestionCircleOutlined } from "@ant-design/icons";

const { Title } = Typography;

export default function NotFound() {
  const router = useRouter();

  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: "#44ad53",
        },
      }}
    >
      <main className="flex flex-col items-center justify-center gap-2 h-screen">
        <QuestionCircleOutlined
          style={{ fontSize: "2rem", color: "#44ad53" }}
        />
        <Title level={3}>Oops...找不到頁面</Title>
        <Button type="primary" onClick={() => router.back()}>
          回上一頁
        </Button>
      </main>
    </ConfigProvider>
  );
}
