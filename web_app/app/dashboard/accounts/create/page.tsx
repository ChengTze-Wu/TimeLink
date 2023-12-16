import { Metadata } from "next";
import CreateForm from "@/app/ui/accounts/create-form";
import Breadcrumbs from "@/app/ui/dashboard/breadcrumbs";

export const metadata: Metadata = {
  title: "Create | Accounts | Dashboard",
};

export default function Page() {
  return (
    <main>
      <Breadcrumbs
        breadcrumbs={[
          { label: "儀表板", href: "/dashboard" },
          { label: "系統帳號", href: "/dashboard/accounts" },
          {
            label: "建立",
            href: "/dashboard/accounts/create",
            active: true,
          },
        ]}
      />
      <CreateForm />
    </main>
  );
}
