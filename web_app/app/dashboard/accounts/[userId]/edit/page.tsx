import Form from "@/app/ui/accounts/edit-form";
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
      <Form user={user} />
    </main>
  );
}
