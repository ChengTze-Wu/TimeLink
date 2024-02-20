import { Metadata } from "next";
import BookingsTable from "@/app/ui/bookings/table";
import { getJson } from "@/app/lib/fetch-api-data";
import { notFound } from "next/navigation";

export const metadata: Metadata = {
  title: "Bookings | Dashboard",
};

type AppointmentsResp = {
  data: {
    id: number;
    key: number;
    user: { name: string; phone: string; email: string };
    service: { name: string };
    reserved_at: string;
    is_active: boolean;
  }[];
  pagination: {
    current_page: number;
    next_page: number;
    current_page_items: number;
    total_pages: number;
    total_items: number;
  };
  status: number;
};

function formatDate(date: string) {
  return new Date(date).toISOString().slice(0, 19).replace("T", " ");
}

export default async function Page({
  searchParams,
}: {
  searchParams?: {
    page?: string;
  };
}) {
  const currentPage = Number(searchParams?.page) || 1;

  const appointmentsResp: AppointmentsResp = await getJson(
    `/api/appointments?per_page=9&page=${currentPage}`
  );

  if (appointmentsResp.status !== 200) {
    notFound();
  }

  const displayAppointments = appointmentsResp.data.map((Appointment) => {
    return {
      key: Appointment.id,
      serviceName: Appointment.service.name,
      username: Appointment.user.name,
      userPhone: Appointment.user.phone,
      userEmail: Appointment.user.email,
      reservedAt: formatDate(Appointment.reserved_at),
      isActive: Appointment.is_active ? "確認" : "取消",
    };
  });

  return (
    <BookingsTable
      displayAppointments={displayAppointments}
      pageSize={9}
      currentPage={currentPage}
      totalItems={appointmentsResp.pagination.total_items}
    />
  );
}
