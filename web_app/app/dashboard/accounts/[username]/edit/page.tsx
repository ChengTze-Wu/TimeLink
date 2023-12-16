import Form from "@/app/ui/accounts/edit-form";
import Breadcrumbs from "@/app/ui/dashboard/breadcrumbs";
import { notFound } from "next/navigation";
import { Metadata } from "next";
import { getJson } from "@/app/lib/fetch-api-data";

export const metadata: Metadata = {
  title: "Edit | Accounts | Dashboard",
};

export default async function Page({
  params,
}: {
  params: { username: string };
}) {
  const username = params.username;
  const user = await getJson(`/api/users/${username}`);

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
            label: `${username} 修改`,
            href: `/dashboard/accounts/${username}/edit`,
            active: true,
          },
        ]}
      />
      <Form user={user} />
    </main>
  );
}
