"use client";
import { Button, Form, Input, ConfigProvider, Typography } from "antd";
import { useFormState, useFormStatus } from "react-dom";
import { authenticate } from "@/app/lib/auth/actions";
import { ExclamationCircleOutlined } from "@ant-design/icons";

const onFinishFailed = (errorInfo: any) => {
  console.log("Failed:", errorInfo);
};

type FieldType = {
  username?: string;
  password?: string;
};

const { Title } = Typography;

export default function LoginForm() {
  const [errorMessage, dispatch] = useFormState(authenticate, undefined);
  const { pending } = useFormStatus();

  return (
    <ConfigProvider
      theme={{
        token: {
          colorTextLightSolid: "#fff",
          colorPrimary: "#44ad53",
        },
      }}
    >
      <Title level={1} className="mb-4">
        Time<span className="text-primary-green">Link</span>
      </Title>
      <Form
        name="basic"
        labelCol={{ span: 8 }}
        wrapperCol={{ span: 16 }}
        style={{ maxWidth: 600 }}
        initialValues={{ remember: true }}
        onFinish={dispatch}
        onFinishFailed={onFinishFailed}
        autoComplete="off"
      >
        <Form.Item<FieldType>
          label="帳號"
          name="username"
          rules={[{ required: true, message: "請輸入您的帳號!" }]}
        >
          <Input />
        </Form.Item>

        <Form.Item<FieldType>
          label="密碼"
          name="password"
          rules={[{ required: true, message: "請輸入您的密碼!" }]}
        >
          <Input.Password />
        </Form.Item>
        <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
          <Button type="primary" htmlType="submit" aria-disabled={pending}>
            登入
          </Button>
        </Form.Item>
      </Form>
      <div
        className="flex items-center space-x-1"
        aria-live="polite"
        aria-atomic="true"
      >
        {errorMessage && (
          <>
            <ExclamationCircleOutlined style={{ fontSize: "20px" }} />
            <p className="text-sm text-red-500">{errorMessage}</p>
          </>
        )}
      </div>
    </ConfigProvider>
  );
}
