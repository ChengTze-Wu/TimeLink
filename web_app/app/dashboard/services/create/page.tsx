import { Metadata } from "next";
import CreateForm from "@/app/ui/services/create-form";
import Breadcrumbs from "@/app/ui/common/breadcrumbs";

export const metadata: Metadata = {
  title: "Create | Services | Dashboard",
};

export default function Page() {
  return (
    <main>
      <Breadcrumbs
        breadcrumbs={[
          { label: "儀表板", href: "/dashboard" },
          { label: "服務", href: "/dashboard/services" },
          {
            label: "建立",
            href: "/dashboard/services/create",
            active: true,
          },
        ]}
      />
      <CreateForm />
    </main>
  );
}
