import { Metadata } from "next";
import {
  ServicesStatistic,
  GroupsStatistic,
} from "@/app/ui/dashboard/statistics";
import { BillboardCard } from "@/app/ui/dashboard/billboard";
import { getJson } from "@/app/lib/fetch-api-data";
import Breadcrumbs from "@/app/ui/common/breadcrumbs";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

export const metadata: Metadata = {
  title: "Dashboard",
};

type ServiceResp = {
  data: {
    id: number;
    name: string;
    appointments: {}[];
  }[];
};

type GroupResp = {
  data: {
    id: number;
    name: string;
    users: {}[];
  }[];
};

export default async function Page() {
  const userInfo = cookies().get("user_info")?.value;
  const user = JSON.parse(userInfo || "{}");

  if (user?.role == "group_member") {
    redirect("/dashboard/bookings");
  }

  const servicesResp: ServiceResp = await getJson("/api/services?per_page=999");
  const servicesStatlabels = servicesResp.data?.map((service) => service.name);
  const servicesStatdata = servicesResp.data?.map(
    (service) => service.appointments.length
  );

  const groupsResp: GroupResp = await getJson("/api/groups?per_page=999");
  const groupsStatlabels = groupsResp.data?.map((group) => group.name);
  const groupsStatdata = groupsResp.data?.map((group) => group.users.length);

  const totalMembers = groupsResp.data?.reduce(
    (acc, group) => acc + group.users.length,
    0
  );

  const totalAppointments = servicesResp.data?.reduce(
    (acc, service) => acc + service.appointments.length,
    0
  );

  return (
    <main>
      <Breadcrumbs breadcrumbs={[{ label: "儀表板", href: "/dashboard" }]} />
      <div className="flex flex-col h-full gap-10">
        <div className="flex h-1/4 gap-12">
          <BillboardCard title="總預約數" value={totalAppointments} />
          <BillboardCard title="總成員數" value={totalMembers} />
        </div>
        <div className="flex h-3/4">
          <ServicesStatistic
            labels={servicesStatlabels}
            data={servicesStatdata}
          />
          <GroupsStatistic labels={groupsStatlabels} data={groupsStatdata} />
        </div>
      </div>
    </main>
  );
}
