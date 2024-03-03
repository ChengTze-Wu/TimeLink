import ServiceMenu from "@/app/ui/menu";
import { getJson } from "@/app/lib/api-server-fetch";
import { Service } from "@/app/lib/definitions";

export default async function Page({
  searchParams,
}: {
  searchParams?: {
    lineGroupId?: string;
  };
}) {
  const lineGroupId = searchParams?.lineGroupId;
  const groupServicesResp = await getJson(
    `/api/groups/${lineGroupId}/services`
  );
  const services: Service[] = groupServicesResp?.data;
  return <ServiceMenu services={services} />;
}
