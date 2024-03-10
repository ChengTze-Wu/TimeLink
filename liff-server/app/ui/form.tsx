"use client";
import Image from "next/image";
import { Service } from "@/app/lib/definitions";
import { createReserve } from "@/app/lib/actions";
import { useContext } from "react";
import ContextAlert from "@/app/ui/alert";
import { LiffContext } from "@/app/liff-provider";
import { useFormState } from "react-dom";

export default function ReserveForm({ service }: { service: Service }) {
  const { liff, error } = useContext(LiffContext);

  const initialState = { message: "", errors: {} };
  const [state, dispatch] = useFormState(createReserve, initialState);

  if (!liff?.isInClient()) return <ContextAlert />;

  const context = liff?.getContext();
  const lineUserId = context?.userId;

  const dayOfWeekMap = {
    Monday: "星期一",
    Tuesday: "星期二",
    Wednesday: "星期三",
    Thursday: "星期四",
    Friday: "星期五",
    Saturday: "星期六",
    Sunday: "星期日",
  };

  const imageUrl = service.image
    ? service.image
    : "https://via.placeholder.com/1024x1024.png?text=No+Image";

  const description = service.description || "尚未有說明";
  const status = service.is_active ? (
    <span className=" text-green-500">開放預約</span>
  ) : (
    <span className=" text-red-500">暫停預約</span>
  );

  return (
    <div className="space-y-3">
      <h1 className="text-2xl">{service.name}</h1>
      <div className="flex flex-row">
        <div className="w-1/2">
          <p>價格：NT$ {service.price}</p>
          <p>狀態：{status}</p>
          <p>服務時長：{service.working_period} 分鐘</p>
          <p>說明：{description}</p>
        </div>
        <Image
          className="w-1/2"
          src={imageUrl}
          width={100}
          height={100}
          alt="service image"
        />
      </div>
      <h2 className="text-xl">營業時間</h2>
      {service.working_hours.map((working_hour) => (
        <p key={working_hour.id}>
          {dayOfWeekMap[working_hour.day_of_week as keyof typeof dayOfWeekMap]}{" "}
          {working_hour.start_time} ~ {working_hour.end_time}
        </p>
      ))}
      <hr />
      {state.message !== "" && (
        <p className="text-red-600">
          {state.message.includes("not active")
            ? "*該服務目前暫停預約"
            : "*請填合理時間"}
        </p>
      )}
      <form action={dispatch}>
        <p className="text">請選擇預約時間: </p>
        <em>* 請填未來時間以及營業時間範圍內（不超過預約時間+服務時長）</em>
        <div className="flex flex-row gap-1">
          <input
            type="text"
            name="lineUserId"
            value={lineUserId}
            required
            hidden
            readOnly
          />
          <input
            type="text"
            name="serviceId"
            value={service.id}
            required
            hidden
            readOnly
          />
          <label htmlFor="date">日期</label>
          <input type="date" name="date" id="date" />
          <label htmlFor="time">時間</label>
          <input type="time" name="time" id="time" />
          <button
            className="w-12 h-12 bg-green-500 rounded-lg text-white"
            type="submit"
          >
            預約
          </button>
        </div>
        <div className="w-full mt-4 border-2 border-gray-200 rounded-lg p-1">
          <textarea
            id="notes"
            name="notes"
            rows={3}
            cols={40}
            placeholder="請填寫備註"
            className="w-full"
          />
        </div>
      </form>
    </div>
  );
}
