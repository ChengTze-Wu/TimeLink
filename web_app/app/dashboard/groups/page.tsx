import Table from "@/app/ui/groups/table";
import SearchBar from "@/app/ui/common/search";
import Pagination from "@/app/ui/common/pagination";
import Breadcrumbs from "@/app/ui/common/breadcrumbs";
import CreateForm from "@/app/ui/groups/create-form";
import { getJson } from "@/app/lib/fetch-api-data";
import { Metadata } from "next";
import { Suspense } from "react";

export const metadata: Metadata = {
  title: "Groups | Dashboard",
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

  const userDataSet = await getJson(
    `/api/groups?per_page=6&query=${query}&status=${status}`
  );
  const totalPages = userDataSet?.pagination?.total_pages || 1;
  const totalItems = userDataSet?.pagination?.total_items || 0;

  return (
    <main>
      <Breadcrumbs
        breadcrumbs={[
          { label: "儀表板", href: "/dashboard" },
          { label: "群組", href: "/dashboard/groups", active: true },
        ]}
      />
      <div className="flex gap-4 mb-4">
        <SearchBar placeholder="Name" />
        <CreateForm />
      </div>
      <Suspense key={query + currentPage} fallback={<div>Loading...</div>}>
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
    </main>
  );
}
