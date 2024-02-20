import { PencilIcon } from "@heroicons/react/24/solid";
import { DeleteService } from "@/app/ui/services/buttons";
import { getJson } from "@/app/lib/fetch-api-data";
import StatusFilter from "@/app/ui/common/statusFilter";
import clsx from "clsx";
import { Service } from "@/app/lib/definitions";
import Link from "next/link";
import Image from "next/image";

export default async function ServicesTable({
  query,
  status,
  currentPage,
}: {
  query: string;
  status: string;
  currentPage: number;
}) {
  const serviceJsonResponse = await getJson(
    `/api/services?per_page=6&query=${query}&status=${status}&page=${currentPage}`
  );

  return (
    <table className="w-full h-full table-fixed">
      <thead className="border-b-[1px] border-gray-300">
        <tr className="text-left font-light">
          <th>項目</th>
          <th>隸屬群組</th>
          <th>服務單位時間</th>
          <th>價格</th>
          <th>
            <StatusFilter status={status} />
          </th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {serviceJsonResponse?.data?.map((service: Service) => (
          <tr
            key={service.id}
            className="border-b-[1px] border-gray-300 last:border-b-0 h-[4.5rem]"
          >
            <td className="flex items-center gap-2 h-full">
              <Image
                src={
                  service.image ||
                  "https://via.placeholder.com/1024x1024.png?text=No+Image"
                }
                className="rounded-full w-12 h-12"
                width={48}
                height={48}
                alt="服務的示意圖"
              />
              <p>{service.name}</p>
            </td>
            <td>
              {service.groups.length === 0 ? (
                <p className="text-gray-500 font-light">尚未隸屬於任何群組</p>
              ) : (
                service.groups.map((group) => (
                  <p key={group.id}>{group.name}</p>
                ))
              )}
            </td>
            <td className={clsx(service.working_period || "text-gray-400")}>
              {service.working_period || "待定"}
            </td>
            <td>{service.price}</td>
            <td
              className={clsx(
                service.is_active ? "text-primary-green" : "text-pink-600"
              )}
            >
              {service.is_active ? "● 啟用" : "● 停用"}
            </td>
            <td className="md:flex gap-4 items-center h-full">
              <Link
                href={`/dashboard/services/${service.id}/edit`}
                className="rounded-md border hover:bg-gray-100 p-2"
              >
                <PencilIcon className="w-5 text-gray-500" />
              </Link>
              <DeleteService service={service} />
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
