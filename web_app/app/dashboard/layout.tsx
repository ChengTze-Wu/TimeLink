import SideNav from "@/app/ui/common/sidenav";
import { cookies } from "next/headers";

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const userInfo = cookies().get("user_info")?.value || "{}";

  return (
    <section className="flex h-screen flex-col md:flex-row md:overflow-hidden text-secondary-gray">
      <nav className="w-full flex-none md:w-64">
        <SideNav userInfo={JSON.parse(userInfo)} />
      </nav>
      <div className="flex-grow p-6 md:overflow-y-auto md:p-10">{children}</div>
    </section>
  );
}
