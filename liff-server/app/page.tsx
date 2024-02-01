import ServiceMenu from "@/app/ui/menu";
import { getJson } from "@/app/lib/api-server-fetch";
import { Group } from "@/app/lib/definitions";

export default async function Page({
  searchParams,
}: {
  searchParams?: {
    lineGroupId?: string;
  };
}) {
  const lineGroupId = searchParams?.lineGroupId;
  const group: Group = await getJson(`/api/groups/${lineGroupId}`);
  const services = group?.services;
  return <ServiceMenu services={services} />;
}
