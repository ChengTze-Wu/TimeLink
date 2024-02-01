"use client";
import { useContext } from "react";
import { LiffContext } from "@/app/liff-provider";

export default function Page() {
  const { liff, error } = useContext(LiffContext);

  setTimeout(() => {
    liff?.closeWindow();
  }, 1000);

  return (
    <div className="flex flex-col justify-center items-center h-screen">
      <h1 className="text-2xl">預約成功</h1>
    </div>
  );
}
