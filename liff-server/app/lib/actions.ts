"use server";
import { z } from "zod";
import { redirect } from "next/navigation";
import { postJson } from "@/app/lib/api-server-fetch";
import moment from "moment";

const reserveSchema = z.object({
  date: z.coerce.date({
    required_error: "Please select a date and time",
    invalid_type_error: "That's not a date!",
  }),
  lineUserId: z.string(),
  serviceId: z.string(),
});

export type ReserveState = {
  errors?: {
    date?: string[];
    lineUserId?: string[];
    serviceId?: string[];
  };
  message?: string | null;
};

export async function createReserve(
  prevState: ReserveState,
  formData: FormData
) {
  const validatedFields = reserveSchema.safeParse({
    date: formData.get("date"),
    lineUserId: formData.get("lineUserId"),
    serviceId: formData.get("serviceId"),
  });

  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
      message: "Missing Fields. Failed to Create Reserve.",
    };
  }

  const date = validatedFields.data.date.toDateString();
  const time = formData.get("time");
  const datetime = new Date(`${date} ${time}`);
  const reservedAt = moment(datetime, false).format("YYYY-MM-DD HH:mm:ss");

  try {
    const result = await postJson("/api/appointments", {
      line_user_id: validatedFields.data.lineUserId,
      service_id: validatedFields.data.serviceId,
      reserved_at: reservedAt,
    });

    const message = result.message ? result.message.join(", ") : "";

    if (result.status !== 201) {
      console.error("Failed to Create Reserve", message);
      return {
        message: message,
      };
    }
  } catch (error) {
    console.error("Error creating reserve", error);
    return {
      message: "Failed to Create Reserve.",
    };
  }

  redirect("/success");
}
