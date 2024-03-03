import { Metadata } from "next";
import BookingsTable from "@/app/ui/bookings/table";
import { getJson } from "@/app/lib/fetch-api-data";
import { notFound } from "next/navigation";

export const metadata: Metadata = {
  title: "Bookings | Dashboard",
};

export type AppointmentsResp = {
  data: {
    id: number;
    key: number;
    user: { name: string; phone: string; email: string };
    notes: string;
    service: {
      name: string;
      owner: { name: string };
      groups: { name: string }[];
    };
    reserved_at: string;
    is_active: boolean;
    created_at: string;
    updated_at: string;
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
    sortField?: string;
    sortOrder?: string;
    filters?: string;
    query?: string;
  };
}) {
  const currentPage = Number(searchParams?.page) || 1;
  const sortField = searchParams?.sortField;
  const sortOrder = searchParams?.sortOrder;
  const filters = searchParams?.filters;
  const query = searchParams?.query;
  const perPage = 7;

  let url = `/api/appointments?per_page=${perPage}&page=${currentPage}`;

  if (sortField) {
    url += `&sortField=${sortField}`;
  }

  if (sortOrder) {
    url += `&sortOrder=${sortOrder}`;
  }

  if (filters) {
    url += `&filters=${filters}`;
  }

  if (query) {
    url += `&query=${query}`;
  }

  const appointmentsResp: AppointmentsResp = await getJson(url);

  if (appointmentsResp.status === 404) {
    notFound();
  }

  const displayAppointments = appointmentsResp.data.map((Appointment) => {
    return {
      key: Appointment.id,
      serviceName: Appointment.service.name,
      serviceOwnerName: Appointment.service.owner.name,
      serviceGroupNames: Appointment.service?.groups
        .map((group) => group.name)
        .join(", "),
      username: Appointment.user.name,
      userPhone: Appointment.user.phone,
      userEmail: Appointment.user.email,
      notes: Appointment.notes,
      reservedAt: formatDate(Appointment.reserved_at),
      updatedAt: formatDate(Appointment.updated_at),
      isActive: Appointment.is_active ? "確認" : "取消",
    };
  });

  return (
    <BookingsTable
      displayAppointments={displayAppointments}
      pageSize={perPage}
      currentPage={currentPage}
      totalItems={appointmentsResp.pagination.total_items}
    />
  );
}
