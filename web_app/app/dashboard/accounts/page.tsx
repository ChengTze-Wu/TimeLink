import Table from "@/app/ui/accounts/table";
import SearchBar from "@/app/ui/accounts/search";
import Pagination from "@/app/ui/accounts/pagination";
import { get } from "@/app/lib/fetch-api-data";
import { Metadata } from "next";
import { Suspense } from "react";
import { UserPlusIcon } from "@heroicons/react/24/solid";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Accounts | Dashboard",
};

export default async function Page({
  searchParams,
}: {
  searchParams?: {
    query?: string;
    page?: string;
    status?: string;
  };
}) {
  const query = searchParams?.query || "";
  const currentPage = Number(searchParams?.page) || 1;
  const status = searchParams?.status || "";

  const userDataSet = await get(
    `http://127.0.0.1:8000/api/users?per_page=6&$page=${currentPage}&query=${query}&status=${status}`
  );
  const totalPages = userDataSet?.pagination?.total_pages || 1;
  const totalItems = userDataSet?.pagination?.total_items || 0;

  return (
    <div className="flex flex-col">
      <h1 className="text-3xl mb-4">系統帳號管理</h1>
      <div className="flex justify-between gap-4 mb-4">
        <SearchBar placeholder="Username, Name, Email, Phone..." />
        <Link
          href="/dashboard/accounts/create"
          className="flex place-items-center p-3 text-sm text-white bg-primary-green rounded-md hover:bg-green-600"
        >
          <UserPlusIcon className="w-5 h-5 md:mr-2" />
          <p className="hidden md:block">新增</p>
        </Link>
      </div>
      <Suspense key={query + status} fallback={<div>Loading...</div>}>
        <Table query={query} status={status} currentPage={currentPage} />
      </Suspense>
      <div className="w-full flex mt-7">
        <div className="basis-1/3"></div>
        <div className="flex justify-center basis-1/3">
          <Pagination totalPages={totalPages} />
        </div>
        <p className="text-sm text-gray-400 flex basis-1/3 justify-end items-start">
          共 {totalItems} 筆資料
        </p>
      </div>
    </div>
  );
}
