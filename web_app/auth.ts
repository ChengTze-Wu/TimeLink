import NextAuth from "next-auth";
import { authConfig } from "./auth.config";
import Credentials from "next-auth/providers/credentials";
import { z } from "zod";
import type { Auth } from "@/app/lib/definitions";
import { postJson } from "./app/lib/fetch-api-data";
import { cookies } from "next/headers";

async function authUser(
  username: string,
  password: string
): Promise<Auth | undefined> {
  try {
    const authResp = await postJson("/api/auth", {
      username,
      password,
    });
    return authResp;
  } catch (error) {
    console.error("Failed to fetch user:", error);
    throw new Error("Failed to fetch user.");
  }
}

export const { auth, signIn, signOut } = NextAuth({
  ...authConfig,
  providers: [
    Credentials({
      async authorize(credentials) {
        const parsedCredentials = z
          .object({ username: z.string(), password: z.string() })
          .safeParse(credentials);

        if (parsedCredentials.success) {
          const { username, password } = parsedCredentials.data;
          const authResp = await authUser(username, password);
          if (!authResp) return null;
          if (authResp.status !== 200) return null;
          cookies().set("access_token", authResp.token.access_token, {
            httpOnly: true,
            sameSite: "lax",
          });
          cookies().set(
            "user_info",
            JSON.stringify({
              userId: authResp.id,
              name: authResp.name,
              role: authResp.role,
            }),
            {
              httpOnly: true,
              sameSite: "lax",
            }
          );
          return authResp;
        }

        return null;
      },
    }),
  ],
});
