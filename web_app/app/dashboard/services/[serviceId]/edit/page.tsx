import Form from "@/app/ui/services/edit-form";
import Breadcrumbs from "@/app/ui/common/breadcrumbs";
import { notFound } from "next/navigation";
import { Metadata } from "next";
import { getJson } from "@/app/lib/fetch-api-data";
import { UUID } from "crypto";

export const metadata: Metadata = {
  title: "Edit | Services | Dashboard",
};

export default async function Page({
  params,
}: {
  params: { serviceId: UUID };
}) {
  const serviceId = params.serviceId;
  const service = await getJson(`/api/services/${serviceId}`);

  if (service.status === 404) {
    notFound();
  }

  return (
    <main>
      <Breadcrumbs
        breadcrumbs={[
          { label: "儀表板", href: "/dashboard" },
          { label: "服務", href: "/dashboard/services" },
          {
            label: `修改 ${service.name}`,
            href: `/dashboard/services/${serviceId}/edit`,
            active: true,
          },
        ]}
      />
      <Form service={service} />
    </main>
  );
}
