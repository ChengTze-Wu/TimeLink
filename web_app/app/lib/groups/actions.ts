"use server";

import { z } from "zod";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { postJson, deleteJson, putJson } from "@/app/lib/fetch-api-data";
import { UUID } from "crypto";

const FormSchema = z.object({
  line_group_id: z
    .string({
      required_error: "Line Group id 為必填.",
    })
    .min(1, { message: "Line Group id 為必填." })
    .max(50, { message: "Line Group id 須小於 50 字元." }),
  is_active: z.coerce.boolean().default(true),
});

const CreateGroup = FormSchema.omit({});
const UpdateGroup = FormSchema.omit({
  line_group_id: true,
});

export type State = {
  errors?: {
    line_group_id?: string[];
    is_active?: string[];
  };
  message?: string | null;
};

export async function createGroup(prevState: State, formData: FormData) {
  const validatedFields = CreateGroup.safeParse({
    line_group_id: formData.get("lineGroupId"),
  });

  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
      message: "缺少必填欄位. 群組建立失敗.",
    };
  }

  try {
    const result = await postJson("/api/groups", validatedFields.data);

    if (result.status === 400) {
      return {
        message: "Line Group id 格式錯誤. 群組建立失敗.",
      };
    }

    if (result.status === 401 || result.status === 403) {
      return {
        message: "您沒有權限建立群組.",
      };
    }

    if (result.status === 404) {
      return {
        message: "請確認 ID 是否正確或是您的群組已加進 TimeLink 機器人.",
      };
    }

    if (result.status === 409) {
      return {
        message: "此群組已連結.",
      };
    }
  } catch (error) {
    return {
      message: "群組建立失敗.",
    };
  }

  revalidatePath("/dashboard/groups");
  redirect("/dashboard/groups");
}

export async function updateGroup(
  uuid: UUID,
  prevState: State,
  formData: FormData
) {
  const validatedFields = UpdateGroup.safeParse(formData);

  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
      message: "Missing Fields. Failed to Update Group.",
    };
  }

  try {
    const result = await putJson(`/api/groups/${uuid}`, validatedFields.data);

    if (result.status != 200) {
      return {
        message: result.message,
      };
    }
  } catch (error) {
    return {
      message: "Failed to Create Group.",
    };
  }

  revalidatePath("/dashboard/groups");
  redirect("/dashboard/groups");
}

export async function deleteGroup(uuid: UUID) {
  try {
    const result = await deleteJson(`/api/groups/${uuid}`);

    if (result.status !== 200) {
      return {
        message: result.message,
      };
    }
  } catch (error) {
    return {
      message: "Failed to delete Group.",
    };
  }

  revalidatePath("/dashboard/groups");
}

export async function switchStatus(uuid: UUID, status: boolean) {
  try {
    // set fake pending time
    // await new Promise((resolve) => setTimeout(resolve, 1000));
    const result = await putJson(`/api/groups/${uuid}`, {
      is_active: status,
    });

    if (result.status != 200) {
      return {
        message: result?.message,
      };
    }
  } catch (error) {
    return {
      message: "Failed to Switch Group Status.",
    };
  }
  revalidatePath("/dashboard/groups");
}
