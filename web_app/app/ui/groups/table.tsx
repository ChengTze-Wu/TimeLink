import { PencilIcon } from "@heroicons/react/24/solid";
import { DeleteGroup } from "@/app/ui/groups/buttons";
import { getJson } from "@/app/lib/fetch-api-data";
import { Group } from "@/app/lib/definitions";
import StatusFilter from "@/app/ui/common/statusFilter";
import clsx from "clsx";
import Link from "next/link";

export default async function GroupsTable({
  query,
  status,
  currentPage,
}: {
  query: string;
  status: string;
  currentPage: number;
}) {
  const groupJsonResponse = await getJson(
    `/api/groups?per_page=6&query=${query}&status=${status}&page=${currentPage}`
  );

  return (
    <table className="w-full h-full">
      <thead className="border-b-[1px] border-gray-300">
        <tr className="text-left font-light">
          <th>Name</th>
          <th>Line Group ID</th>
          <th>群組管理員</th>
          <th>擁有服務數</th>
          <th>
            <StatusFilter status={status} />
          </th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {groupJsonResponse?.data?.map((group: Group) => (
          <tr
            key={group.id}
            className="border-b-[1px] border-gray-300 last:border-b-0"
          >
            <td className="h-[4.5rem]">{group.name}</td>
            <td className="h-[4.5rem]">{group.line_group_id}</td>
            <td className="h-[4.5rem]">{group.owner.username}</td>
            <td className="h-[4.5rem]">{group.services.length}</td>
            <td
              className={clsx(
                group.is_active ? "text-primary-green" : "text-pink-600"
              )}
            >
              {group.is_active ? "● 啟用" : "● 停用"}
            </td>
            <td className="md:flex gap-4 items-center h-full">
              <Link
                href={`/dashboard/groups/${group.id}/edit`}
                className="rounded-md border p-2 hover:bg-gray-100"
              >
                <PencilIcon className="w-5 text-gray-500" />
              </Link>
              <DeleteGroup group={group} />
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
