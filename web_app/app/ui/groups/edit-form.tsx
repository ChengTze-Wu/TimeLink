"use client";

import { updateGroup } from "@/app/lib/groups/actions";
import { useFormState } from "react-dom";
import { Group } from "@/app/lib/definitions";
import { Switch, Form, Button, ConfigProvider } from "antd";

export default function EditForm({ group }: { group: Group }) {
  const initialState = { message: "", errors: {} };

  const updateGroupWithUuid = updateGroup.bind(null, group.id);
  const [state, dispatch] = useFormState(updateGroupWithUuid, initialState);

  return (
    <ConfigProvider
      theme={{
        token: {
          colorTextLightSolid: "#fff",
          colorPrimary: "#44ad53",
        },
      }}
    >
      <div className="w-full h-full p-10 bg-gray-50 rounded-md flex flex-col">
        <Form onFinish={dispatch}>
          <div className="mt-2 rounded-md flex gap-2 items-center">
            <Form.Item name="is_active" initialValue={group.is_active}>
              <Switch checkedChildren="啟用" unCheckedChildren="關閉" />
            </Form.Item>
          </div>
          <div className="mt-4 grow flex items-end justify-center">
            <Button htmlType="submit">更新</Button>
          </div>
        </Form>
      </div>
    </ConfigProvider>
  );
}
