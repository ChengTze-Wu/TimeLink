import ReserveForm from "@/app/ui/form";
import { getJson } from "@/app/lib/api-server-fetch";
import { notFound } from "next/navigation";

export default async function Page({
  params,
}: {
  params: { serviceId: string };
}) {
  const serviceId = params?.serviceId;
  const serviceJson = await getJson(`/api/services/${serviceId}`);
  if (serviceJson.status !== 200) return notFound();
  return <ReserveForm service={serviceJson} />;
}
