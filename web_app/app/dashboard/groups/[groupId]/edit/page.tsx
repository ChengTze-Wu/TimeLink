import Form from "@/app/ui/groups/edit-form";
import { notFound } from "next/navigation";
import { Metadata } from "next";
import { getJson } from "@/app/lib/fetch-api-data";
import { UUID } from "crypto";

export const metadata: Metadata = {
  title: "Edit | Groups | Dashboard",
};

export default async function Page({ params }: { params: { groupId: UUID } }) {
  const group_id = params.groupId;
  const group = await getJson(`/api/groups/${group_id}`);

  if (group.status === 404) {
    notFound();
  }

  return (
    <main>
      <Form group={group} />
    </main>
  );
}
