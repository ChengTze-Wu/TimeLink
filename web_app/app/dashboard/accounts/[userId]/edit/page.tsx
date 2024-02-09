import Form from "@/app/ui/accounts/edit-form";
import Breadcrumbs from "@/app/ui/common/breadcrumbs";
import { notFound } from "next/navigation";
import { Metadata } from "next";
import { getJson } from "@/app/lib/fetch-api-data";
import { UUID } from "crypto";

export const metadata: Metadata = {
  title: "Edit | Accounts | Dashboard",
};

export default async function Page({ params }: { params: { userId: UUID } }) {
  const user_id = params.userId;
  const user = await getJson(`/api/users/${user_id}`);

  if (user.status === 404) {
    notFound();
  }

  return (
    <main>
      <Breadcrumbs
        breadcrumbs={[
          { label: "儀表板", href: "/dashboard" },
          { label: "系統帳號", href: "/dashboard/accounts" },
          {
            label: `修改 ${user.name}`,
            href: `/dashboard/accounts/${user_id}/edit`,
            active: true,
          },
        ]}
      />
      <Form user={user} />
    </main>
  );
}
