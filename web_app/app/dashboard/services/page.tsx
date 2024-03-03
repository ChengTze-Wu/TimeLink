import ServicesTable from "@/app/ui/services/table";
import SearchBar from "@/app/ui/common/search";
import { getJson } from "@/app/lib/fetch-api-data";
import { Metadata } from "next";
import { SquaresPlusIcon } from "@heroicons/react/24/solid";
import Link from "next/link";
import { Service } from "@/app/lib/definitions";

export const metadata: Metadata = {
  title: "Services | Dashboard",
};

function formatDate(date: string) {
  return new Date(date).toISOString().slice(0, 19).replace("T", " ");
}

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
  const pageSize = 6;

  const servicesResp = await getJson(
    `/api/services?per_page=${pageSize}&query=${query}&status=${status}`
  );
  const totalItems = servicesResp?.pagination?.total_items || 0;

  const displayDataSet = servicesResp?.data?.map((service: Service) => ({
    name: service.name,
    image: service.image,
    groups: service.groups,
    duration: service.working_period,
    price: service.price,
    isActive: service.is_active,
    updatedAt: formatDate(service.updated_at),
    key: service.id,
  }));

  return (
    <main>
      <div className="flex justify-between gap-4 mb-6">
        <SearchBar placeholder="搜尋服務項目名稱" />
        <Link
          href="/dashboard/services/create"
          className="flex place-items-center p-2 text-sm text-white bg-primary-green rounded-md hover:bg-green-600"
        >
          <SquaresPlusIcon className="w-5 h-5 md:mr-2" />
          <p className="hidden md:block">建立</p>
        </Link>
      </div>
      <ServicesTable
        displayData={displayDataSet}
        currentPage={currentPage}
        pageSize={pageSize}
        totalItems={totalItems}
      />
    </main>
  );
}
