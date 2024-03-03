import GroupsTable from "@/app/ui/groups/table";
import SearchBar from "@/app/ui/common/search";
import CreateForm from "@/app/ui/groups/create-form";
import { getJson } from "@/app/lib/fetch-api-data";
import { Metadata } from "next";
import { Group } from "@/app/lib/definitions";

export const metadata: Metadata = {
  title: "Groups | Dashboard",
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
  const perPage = 7;

  const groupResp = await getJson(
    `/api/groups?per_page=${perPage}&query=${query}&status=${status}`
  );

  const totalItems = groupResp?.pagination?.total_items || 0;

  const displayDataSet = groupResp?.data?.map((group: Group) => ({
    name: group.name,
    lineGroupId: group.line_group_id,
    ownerName: group.owner.username,
    isActive: group.is_active,
    updatedAt: formatDate(group.updated_at),
    key: group.id,
  }));

  return (
    <main>
      <div className="flex gap-4 mb-6">
        <SearchBar placeholder="查詢 Line 群組名稱" />
        <CreateForm placeholder="連結 Line 群組，請輸入 Line 群組 ID" />
      </div>
      <GroupsTable
        displayData={displayDataSet}
        pageSize={perPage}
        currentPage={currentPage}
        totalItems={totalItems}
      />
    </main>
  );
}
