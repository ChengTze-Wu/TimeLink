"use server";

import { z } from "zod";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { postJson, deleteJson, putJson } from "@/app/lib/fetch-api-data";
import { UUID } from "crypto";

const FormSchema = z.object({
  username: z
    .string({
      required_error: "Username is required.",
    })
    .min(1, { message: "Username is required" })
    .max(50, { message: "Username must be less than 50 characters" }),
  email: z
    .string({
      required_error: "Email is required.",
    })
    .email({ message: "Email is invalid" })
    .min(1, { message: "Email is required" })
    .max(100, { message: "Email must be less than 100 characters" }),
  password: z
    .string({
      required_error: "Password is required.",
    })
    .min(8, { message: "Password must be at least 8 characters" })
    .max(100, { message: "Password must be less than 100 characters" })
    .regex(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@$!%*?&.]).{8,100}$/,
      "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character: `@$!%*?&.`"
    ),
  confirmPassword: z.string({
    required_error: "Password Check is required.",
  }),
  name: z
    .string({
      required_error: "Name is required.",
    })
    .min(1, { message: "Name is required" })
    .max(50, { message: "Name must be less than 50 characters" }),
  phone: z
    .string()
    .max(50, { message: "Phone must be less than 50 characters" }),
  is_active: z.coerce.boolean(),
});

const CreateAccount = FormSchema.omit({});
const CreateAccountWithPassword = CreateAccount.refine(
  (data) => data.confirmPassword === data.password,
  {
    message: "Password does not match.",
    path: ["confirmPassword"],
  }
);

const UpdateAccount = FormSchema.omit({
  password: true,
  confirmPassword: true,
});

export type State = {
  errors?: {
    name?: string[];
    username?: string[];
    email?: string[];
    password?: string[];
    confirmPassword?: string[];
    phone?: string[];
    isActive?: string[];
  };
  message?: string | null;
};

export async function createAccount(
  prevState: State,
  formData: FormData
): Promise<State> {
  const validatedFields = CreateAccountWithPassword.safeParse({
    username: formData.get("username"),
    email: formData.get("email"),
    password: formData.get("password"),
    confirmPassword: formData.get("confirmPassword"),
    name: formData.get("name"),
    phone: formData.get("phone"),
    is_active: formData.get("isActive"),
  });

  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
      message: "Missing Fields. Failed to Create Invoice.",
    };
  }

  try {
    const result = await postJson("/api/users", validatedFields.data);

    if (result.status === 400) {
      return {
        message: result.message,
      };
    }
  } catch (error) {
    return {
      message: "Failed to Create Account.",
    };
  }

  revalidatePath("/dashboard/accounts");
  redirect("/dashboard/accounts");
}

export async function updateAccount(
  uuid: UUID,
  prevState: State,
  formData: FormData
): Promise<State> {
  const validatedFields = UpdateAccount.safeParse({
    username: formData.get("username"),
    email: formData.get("email"),
    name: formData.get("name"),
    phone: formData.get("phone"),
    is_active: formData.get("isActive"),
  });

  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
      message: "Missing Fields. Failed to Create Invoice.",
    };
  }

  try {
    const result = await putJson(`/api/users/${uuid}`, validatedFields.data);

    if (result.status != 200) {
      return {
        message: result.message,
      };
    }
  } catch (error) {
    return {
      message: "Failed to Create Account.",
    };
  }

  revalidatePath("/dashboard/accounts");
  redirect("/dashboard/accounts");
}

export async function deleteAccount(uuid: UUID) {
  try {
    const result = await deleteJson(`/api/users/${uuid}`);

    if (result.status !== 200) {
      return {
        message: result.message,
      };
    }
  } catch (error) {
    return {
      message: "Failed to Create Account.",
    };
  }

  revalidatePath("/dashboard/accounts");
}
