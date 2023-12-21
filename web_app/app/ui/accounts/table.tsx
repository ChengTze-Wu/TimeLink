import { PencilIcon } from "@heroicons/react/24/solid";
import { DeleteAccount } from "./buttons";
import { getJson } from "@/app/lib/fetch-api-data";
import StatusFilter from "./statusFilter";
import clsx from "clsx";
import { User } from "@/app/lib/definitions";
import Link from "next/link";

export default async function AccountsTable({
  query,
  status,
  currentPage,
}: {
  query: string;
  status: string;
  currentPage: number;
}) {
  const userDataSet = await getJson(
    `/api/users?per_page=6&query=${query}&status=${status}&page=${currentPage}`
  );

  return (
    <table className="w-full h-full">
      <thead className="border-b-[1px] border-gray-300">
        <tr className="text-left font-light">
          <th>Name</th>
          <th>Username</th>
          <th>Email</th>
          <th>Phone</th>
          <th>
            <StatusFilter status={status} />
          </th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {userDataSet?.data.map((user: User) => (
          <tr
            key={user.id}
            className="border-b-[1px] border-gray-300 last:border-b-0"
          >
            <td className="h-[4.5rem]">{user.name}</td>
            <td>{user.username}</td>
            <td>{user.email}</td>
            <td>
              {user.phone ? (
                user.phone
              ) : (
                <span className="text-gray-400">None</span>
              )}
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
