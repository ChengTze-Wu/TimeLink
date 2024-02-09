"use client";

import { createService } from "@/app/lib/services/actions";
import { useFormState } from "react-dom";
import { useState, useEffect } from "react";
import { getJson } from "@/app/lib/fetch-api-data";

import {
  TimePicker,
  ConfigProvider,
  Checkbox,
  Row,
  Form,
  Button,
  Input,
  Switch,
  Typography,
  InputNumber,
  Select,
} from "antd";

const { TextArea } = Input;
const { Title } = Typography;

const weekdays = [
  { label: "星期一", value: "Monday" },
  { label: "星期二", value: "Tuesday" },
  { label: "星期三", value: "Wednesday" },
  { label: "星期四", value: "Thursday" },
  { label: "星期五", value: "Friday" },
  { label: "星期六", value: "Saturday" },
  { label: "星期日", value: "Sunday" },
];

export default function CerateForm() {
  const initialState = { message: "", errors: {} };
  const [state, dispatch] = useFormState(createService, initialState);
  const [checkboxStatus, setCheckboxStatus] = useState<{
    [key: string]: boolean;
  }>({});
  const [timeRange, setTimeRange] = useState<{
    [key: string]: [string, string];
  }>({});

  const [groupOptions, setGroupOptions] = useState([]);
  useEffect(() => {
    const fetchData = async () => {
      const groupJsonResponse = await getJson("/api/groups?per_page=999");
      const groupOptions = groupJsonResponse?.data.map((group: any) => ({
        label: group.name,
        value: group.id,
      }));
      setGroupOptions(groupOptions);
    };
    fetchData();
  }, []);

  const onFinish = (values: any) => {
    const groupIds = values.groups?.map((group: any) => {
      return group?.value ? group.value : group;
    });

    const workingHoursArray: {
      day_of_week: string;
      start_time: string;
      end_time: string;
    }[] = [];

    Object.keys(timeRange).forEach((weekday) => {
      if (!checkboxStatus[weekday]) return;
      workingHoursArray.push({
        day_of_week: weekday,
        start_time: timeRange[weekday][0],
        end_time: timeRange[weekday][1],
      });
    });

    const formData = {
      ...values,
      working_hours: workingHoursArray,
      groups: groupIds,
    };

    dispatch(formData);
  };

  return (
    <ConfigProvider
      theme={{
        token: {
          colorTextLightSolid: "#fff",
          colorPrimary: "#44ad53",
        },
      }}
    >
      <Form onFinish={onFinish} layout="vertical">
        <div className="xl:flex gap-10">
          <div className="xl:min-w-[600px]">
            <Title level={4}>基本資訊</Title>
            <Form.Item
              name="name"
              label="名稱"
              rules={[{ required: true, message: "請輸入服務名稱" }]}
            >
              <Input placeholder="剪頭髮" size="large" />
            </Form.Item>
            <Form.Item label="價格" name="price">
              <InputNumber
                placeholder="399"
                size="large"
                prefix="NT$"
                suffix="TWD"
                style={{ width: "100%" }}
              />
            </Form.Item>
            <Form.Item label="服務單位時間" name="working_period">
              <InputNumber
                placeholder="15"
                size="large"
                suffix="分鐘"
                style={{ width: "100%" }}
              />
            </Form.Item>
            <Form.Item label="描述" name="description">
              <TextArea
                placeholder=""
                size="large"
                showCount
                maxLength={100}
                className="h-[200px]"
                style={{ resize: "none" }}
              />
            </Form.Item>
            <Form.Item valuePropName="checked" name="is_active">
              <Switch
                checkedChildren="啟用"
                unCheckedChildren="停用"
                defaultChecked
              />
            </Form.Item>
          </div>
          <div className="w-full">
            <Title level={4}>群組歸屬</Title>
            <Form.Item name="groups">
              <Select
                mode="multiple"
                allowClear
                style={{ width: "100%" }}
                placeholder="---請選擇（可多選）---"
                options={groupOptions}
              />
            </Form.Item>
            <Title level={4}>開放時間</Title>
            {weekdays?.map((day) => (
              <Row key={day.value}>
                <Form.Item valuePropName="checked">
                  <Checkbox
                    onChange={(e) => {
                      setCheckboxStatus({
                        ...checkboxStatus,
                        [day.value]: e.target.checked,
                      });
                    }}
                  >
                    {day.label}
                  </Checkbox>
                </Form.Item>
                <Form.Item>
                  <TimePicker.RangePicker
                    format="H:mm"
                    disabled={
                      !checkboxStatus[day.value as keyof typeof checkboxStatus]
                    }
                    onChange={(time, timeString) => {
                      setTimeRange({
                        ...timeRange,
                        [day.value]: timeString,
                      });
                    }}
                    changeOnBlur={true}
                    minuteStep={15}
                    use12Hours
                  />
                </Form.Item>
              </Row>
            ))}
          </div>
        </div>
        <Form.Item>
          <Button htmlType="submit">建立</Button>
        </Form.Item>
      </Form>
    </ConfigProvider>
  );
}
