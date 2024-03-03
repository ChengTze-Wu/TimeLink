import { notFound } from "next/navigation";
import { Metadata } from "next";
import { getJson } from "@/app/lib/fetch-api-data";
import { UUID } from "crypto";
import { Group } from "@/app/lib/definitions";

export const metadata: Metadata = {
  title: "Edit | Groups | Dashboard",
};

type GroupResp = Group & {
  status: Number;
};

export default async function Page({ params }: { params: { groupId: UUID } }) {
  const group_id = params.groupId;
  const group: GroupResp = await getJson(`/api/groups/${group_id}`);

  if (group.status === 404) {
    notFound();
  }

  return <main></main>;
}
