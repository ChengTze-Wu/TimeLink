import SideNav from "@/app/ui/dashboard/sidenav";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <section className="flex h-screen flex-col md:flex-row md:overflow-hidden text-secondary-gray">
      <nav className="w-full flex-none md:w-64">
        <SideNav username="" />
      </nav>
      <div className="flex-grow p-6 md:overflow-y-auto md:p-10">{children}</div>
    </section>
  );
}
