import { Metadata } from "next";
import CreateForm from "@/app/ui/accounts/create-form";

export const metadata: Metadata = {
  title: "Create | Accounts | Dashboard",
};

export default function Page() {
  return (
    <main>
      <CreateForm />
    </main>
  );
}
