import { Metadata } from "next";
import { ServicesStatistic, GroupsStatistic } from "../ui/dashboard/statistics";
import { getJson } from "../lib/fetch-api-data";

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
  const servicesResp: ServiceResp = await getJson("/api/services?per_page=999");

  const servicesStatlabels = servicesResp.data.map((service) => service.name);
  const servicesStatdata = servicesResp.data.map(
    (service) => service.appointments.length
  );

  const groupsResp: GroupResp = await getJson("/api/groups?per_page=999");
  const groupsStatlabels = groupsResp.data.map((group) => group.name);
  const groupsStatdata = groupsResp.data.map((group) => group.users.length);

  return (
    <div className="flex flex-col items-center gap-4">
      <ServicesStatistic labels={servicesStatlabels} data={servicesStatdata} />
      <GroupsStatistic labels={groupsStatlabels} data={groupsStatdata} />
    </div>
  );
}
