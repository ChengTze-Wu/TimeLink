"use client";

import { updateService, uploadImageToGCS } from "@/app/lib/services/actions";
import { useFormState } from "react-dom";
import { Service, Group } from "@/app/lib/definitions";
import { useState, useEffect } from "react";
import { getJson } from "@/app/lib/fetch-api-data";
import dayjs from "dayjs";

import {
  TimePicker,
  ConfigProvider,
  Checkbox,
  Form,
  Button,
  Input,
  Switch,
  Typography,
  InputNumber,
  Select,
  Flex,
  Upload,
  message,
} from "antd";

import { UploadOutlined } from "@ant-design/icons";
import { UploadRequestOption } from "rc-upload/lib/interface";

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

export default function EditForm({ service }: { service: Service }) {
  const initialState = { message: "", errors: {} };

  const updateServiceWithUuid = updateService.bind(null, service.id);
  const [state, dispatch] = useFormState(updateServiceWithUuid, initialState);
  const [imageName, setImageName] = useState<string | null>(service.image);

  const [checkboxStatus, setCheckboxStatus] = useState(() => {
    const checkboxStatus: { [key: string]: boolean } = {};
    weekdays.forEach((weekday) => {
      if (
        service.working_hours?.some(
          (workingHour) => workingHour.day_of_week === weekday.value
        )
      ) {
        checkboxStatus[weekday.value] = true;
      } else {
        checkboxStatus[weekday.value] = false;
      }
    });

    return checkboxStatus;
  });
  const [timeRange, setTimeRange] = useState(() => {
    const timeRange: { [key: string]: string[] | null[] } = {};
    weekdays.forEach((weekday) => {
      const workingHour = service.working_hours?.find(
        (item) => item.day_of_week === weekday.value
      );
      if (workingHour) {
        timeRange[weekday.value] = [
          workingHour.start_time,
          workingHour.end_time,
        ];
      } else {
        timeRange[weekday.value] = [];
      }
    });

    return timeRange;
  });

  const [groupOptions, setGroupOptions] = useState([]);
  useEffect(() => {
    const fetchData = async () => {
      const groupJsonResponse = await getJson("/api/groups?per_page=999");
      const groupOptions = groupJsonResponse?.data.map((group: Group) => ({
        label: group.name,
        value: group.id,
      }));
      setGroupOptions(groupOptions);
    };
    fetchData();
  }, []);

  const onFinish = (values: Service) => {
    const groupIds = values.groups?.map((group: any) => {
      return group?.value ? group.value : group;
    });

    const workingHoursArray: {
      day_of_week: string;
      start_time: string;
      end_time: string;
    }[] = [];

    for (const [key, value] of Object.entries(timeRange)) {
      if (value.length === 2 && checkboxStatus[key]) {
        if (value[0] === "" || value[1] === "") {
          continue;
        }
        workingHoursArray.push({
          day_of_week: key,
          start_time: value[0] || "",
          end_time: value[1] || "",
        });
      }
    }

    const formData = {
      ...values,
      image: imageName,
      working_hours: workingHoursArray,
      groups: groupIds,
    };

    dispatch(formData);
  };

  const handleUpload = async (options: UploadRequestOption) => {
    const { file, onSuccess, onError } = options;
    const { name } = file as File;
    const arrayBuffer = await (file as File).arrayBuffer();
    const buffer = new Uint8Array(arrayBuffer);
    try {
      const uploadedFileName = await uploadImageToGCS(buffer, name);
      if (onSuccess) {
        setImageName(uploadedFileName);
        onSuccess("ok");
      }
    } catch (error) {
      if (onError) {
        onError(new Error("Upload failed"));
      }
    }
  };

  const beforeUpload = (file: any) => {
    const asscptedTypes = [
      "image/png",
      "image/jpeg",
      "image/jpg",
      "image/webp",
    ];
    const isImage = asscptedTypes.includes(file.type);
    if (!isImage) {
      message.error("You can only upload image file!");
    }
    const isLt2M = file.size / 1024 / 1024 < 2.005;
    if (!isLt2M) {
      message.error("Image must smaller than 2MB!");
    }
    return isImage && isLt2M;
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
        <div className="xl:flex gap-8">
          <div className="xl:min-w-[600px]">
            <Title level={4}>基本資訊</Title>
            <Form.Item
              name="name"
              label="名稱"
              rules={[{ required: true, message: "請輸入服務名稱" }]}
              initialValue={service.name}
            >
              <Input size="large" />
            </Form.Item>
            <Form.Item label="上傳圖片" valuePropName="fileList">
              <Upload
                listType="picture"
                maxCount={1}
                accept="image/*"
                customRequest={handleUpload}
                onRemove={() => setImageName(null)}
                beforeUpload={beforeUpload}
                defaultFileList={
                  service?.image
                    ? [
                        {
                          uid: "1",
                          name: service.image.split("/").pop() || "",
                          status: "done",
                          url: service.image,
                        },
                      ]
                    : []
                }
              >
                <Button icon={<UploadOutlined />}>Upload</Button>
              </Upload>
            </Form.Item>
            <Form.Item label="價格" name="price" initialValue={service.price}>
              <InputNumber
                size="large"
                prefix="NT$"
                suffix="TWD"
                style={{ width: "100%" }}
                placeholder="499"
              />
            </Form.Item>
            <Form.Item
              label="服務單位時間"
              name="working_period"
              initialValue={service.working_period}
            >
              <InputNumber
                placeholder="15"
                size="large"
                suffix="分鐘"
                style={{ width: "100%" }}
              />
            </Form.Item>
            <Form.Item
              label="描述"
              name="description"
              initialValue={service.description}
            >
              <TextArea
                placeholder=""
                size="large"
                showCount
                maxLength={100}
                className="h-[200px]"
                style={{ resize: "none" }}
              />
            </Form.Item>
            <Form.Item
              valuePropName="checked"
              name="is_active"
              initialValue={service.is_active}
            >
              <Switch checkedChildren="啟用" unCheckedChildren="停用" />
            </Form.Item>
          </div>
          <div className="w-full">
            <Title level={4}>群組歸屬</Title>
            <Form.Item
              name="groups"
              initialValue={service?.groups?.map((group) => ({
                label: group.name,
                value: group.id,
              }))}
            >
              <Select
                mode="multiple"
                allowClear
                style={{ width: "100%" }}
                options={groupOptions}
                placeholder="---請選擇（可多選）---"
              />
            </Form.Item>
            <Title level={4}>開放時間</Title>
            <Flex vertical gap={12}>
              {weekdays?.map((day) => (
                <div key={day.value}>
                  <Checkbox
                    defaultChecked={checkboxStatus[day.value]}
                    onChange={(e) => {
                      setCheckboxStatus({
                        ...checkboxStatus,
                        [day.value]: e.target.checked,
                      });
                    }}
                  >
                    {day.label}
                  </Checkbox>
                  <TimePicker.RangePicker
                    defaultValue={
                      checkboxStatus[day.value]
                        ? [
                            dayjs(timeRange[day.value][0], "HH:mm"),
                            dayjs(timeRange[day.value][1], "HH:mm"),
                          ]
                        : [null, null]
                    }
                    format="HH:mm"
                    disabled={!checkboxStatus[day.value]}
                    changeOnBlur={true}
                    minuteStep={15}
                    use12Hours
                    onChange={(time, timeString) => {
                      setTimeRange({
                        ...timeRange,
                        [day.value]: timeString,
                      });
                    }}
                  />
                </div>
              ))}
            </Flex>
          </div>
        </div>
        <Form.Item>
          <Button htmlType="submit">儲存</Button>
        </Form.Item>
      </Form>
    </ConfigProvider>
  );
}
