import Table from "@/app/ui/accounts/table";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Accounts | Dashboard",
};

export default function Page() {
  return (
    <div className="flex flex-col">
      <h1 className="text-3xl font-semibold">帳號管理</h1>
      <div className="mt-6">
        <Table />
      </div>
    </div>
  );
}
