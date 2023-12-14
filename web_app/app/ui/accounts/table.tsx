import Image from "next/image";
import { PencilIcon, TrashIcon } from "@heroicons/react/24/solid";
import { get } from "@/app/lib/fetch-api-data";
import StatusFilter from "./statusFilter";
import clsx from "clsx";

export type User = {
  id: number;
  name: string;
  username: string;
  email: string;
  phone: string;
  is_active: boolean;
  updated_at: string;
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
  const userDataSet = await get(
    `http://127.0.0.1:8000/api/users?per_page=6&query=${query}&status=${status}&page=${currentPage}`
  );

  return (
    <table className="w-full h-full">
      <thead className="border-b-[1px] border-gray-300">
        <tr className="text-left font-light">
          <th></th>
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
            <td className="py-1 flex justify-start">
              <div className="flex flex-col items-center">
                <Image
                  className="rounded-full"
                  src="/avatar-placeholder.webp"
                  width={40}
                  height={40}
                  alt="avatar"
                />
                <p>{user.name}</p>
              </div>
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
            <td
              className={clsx(
                user.is_active ? "text-primary-green" : "text-pink-600"
              )}
            >
              {user.is_active ? "● 啟用" : "● 停用"}
            </td>
            <td className="flex gap-4">
              <PencilIcon className="w-5 h-5 text-gray-500" />
              <TrashIcon className="w-5 h-5 text-gray-500" />
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
