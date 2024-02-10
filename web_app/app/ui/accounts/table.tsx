import { PencilIcon } from "@heroicons/react/24/solid";
import { DeleteAccount } from "@/app/ui/accounts/buttons";
import { getJson } from "@/app/lib/fetch-api-data";
import StatusFilter from "@/app/ui/common/statusFilter";
import clsx from "clsx";
import { User } from "@/app/lib/definitions";
import Link from "next/link";

const roleMap = {
  admin: "管理員",
  group_owner: "群組管理員",
  group_member: "群組成員",
  undefined: "未定義",
};

export default async function AccountsTable({
  query,
  status,
  currentPage,
}: {
  query: string;
  status: string;
  currentPage: number;
}) {
  const userJsonResponse = await getJson(
    `/api/users?per_page=6&query=${query}&status=${status}&page=${currentPage}`
  );

  return (
    <table className="w-full h-full">
      <thead className="border-b-[1px] border-gray-300">
        <tr className="text-left font-light">
          <th>名稱</th>
          <th>帳號</th>
          <th>Email</th>
          <th>電話</th>
          <th>角色</th>
          <th>
            <StatusFilter status={status} />
          </th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {userJsonResponse?.data?.map((user: User) => (
          <tr
            key={user.id}
            className="border-b-[1px] border-gray-300 last:border-b-0"
          >
            <td className="h-[4.5rem]">
              <Link
                className="hover:text-primary-green"
                href={`/dashboard/accounts/${user.id}`}
              >
                {user.name}
              </Link>
            </td>
            <td>{user.username}</td>
            <td>{user.email}</td>
            <td>
              {user.phone ? (
                user.phone
              ) : (
                <span className="text-gray-400">None</span>
              )}
            </td>
            <td>
              {roleMap[user.role as keyof typeof roleMap] ||
                roleMap["undefined"]}
            </td>
            <td
              className={clsx(
                user.is_active ? "text-primary-green" : "text-pink-600"
              )}
            >
              {user.is_active ? "● 啟用" : "● 停用"}
            </td>
            <td className="md:flex gap-4 items-center h-full">
              <Link
                href={`/dashboard/accounts/${user.id}/edit`}
                className="rounded-md border p-2 hover:bg-gray-100"
              >
                <PencilIcon className="w-5  text-gray-500" />
              </Link>
              <DeleteAccount user={user} />
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
