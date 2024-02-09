"use server";

import { z } from "zod";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { postJson, deleteJson, putJson } from "@/app/lib/fetch-api-data";
import { UUID } from "crypto";
import { Service } from "@/app/lib/definitions";

const FormSchema = z.object({
  name: z
    .string({
      required_error: "name is required.",
    })
    .min(1, { message: "name is required" })
    .max(50, { message: "name must be less than 50 characters" }),
  price: z.coerce
    .number()
    .min(0, { message: "price must be greater than 0" })
    .nullable()
    .optional(),
  description: z
    .string()
    .max(100, { message: "description must be less than 100 characters" })
    .transform((value) => (value === "undefined" ? null : value))
    .nullable()
    .optional(),
  working_period: z.coerce
    .number()
    .min(0, { message: "working period must be greater than 0" })
    .nullable()
    .optional(),
  working_hours: z
    .array(
      z.object({
        day_of_week: z.string(),
        start_time: z.string(),
        end_time: z.string(),
      })
    )
    .nullable()
    .optional(),
  unavailable_periods: z.array(z.string()).nullable().optional(),
  is_active: z.coerce.boolean().nullable().optional(),
  groups: z.array(z.string()).nullable().optional(),
});

const CreateService = FormSchema.omit({});
const UpdateService = FormSchema.omit({});

export type State = {
  errors?: {
    name?: string[];
    price?: string[];
    image?: string[];
    description?: string[];
    working_period?: string[];
    working_hours?: string[];
    unavailable_periods?: string[];
    isActive?: string[];
    groups?: string[];
  };
  message?: string | null;
};

export async function createService(prevState: State, serviceData: any) {
  const validatedFields = CreateService.safeParse(serviceData);

  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
      message: "Missing Fields. Failed to Create Service.",
    };
  }

  try {
    const result = await postJson("/api/services", validatedFields.data);

    if (result.status !== 201) {
      return {
        message: result.message,
      };
    }
  } catch (error) {
    return {
      message: "Failed to Create Service.",
    };
  }

  revalidatePath("/dashboard/services");
  redirect("/dashboard/services");
}

export async function updateService(
  service_id: UUID,
  prevState: State,
  serviceData: any
) {
  const validatedFields = UpdateService.safeParse(serviceData);

  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
      message: "Missing Fields. Failed to Update Service.",
    };
  }

  try {
    const result = await putJson(
      `/api/services/${service_id}`,
      validatedFields.data
    );

    if (result.status != 200) {
      return {
        message: result.message,
      };
    }
  } catch (error) {
    return {
      message: "Failed to Update Service.",
    };
  }

  revalidatePath("/dashboard/services");
  redirect("/dashboard/services");
}

export async function deleteService(service_id: UUID) {
  try {
    const result = await deleteJson(`/api/services/${service_id}`);

    if (result.status !== 200) {
      return {
        message: result.message,
      };
    }
  } catch (error) {
    return {
      message: "Failed to Delete Service.",
    };
  }

  revalidatePath("/dashboard/services");
}
