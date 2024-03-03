import { Metadata } from "next";
import CreateForm from "@/app/ui/services/create-form";

export const metadata: Metadata = {
  title: "Create | Services | Dashboard",
};

export default function Page() {
  return (
    <main>
      <CreateForm />
    </main>
  );
}
