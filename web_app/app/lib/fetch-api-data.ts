"use server";

import { unstable_noStore as noStore } from "next/cache";

export async function get(apiEndpoint: string) {
  noStore();
  try {
    const res = await fetch(apiEndpoint, {
      method: "GET",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    });
    return res.json();
  } catch (error) {
    console.error(`Error fetching ${apiEndpoint}: ${error}`);
    throw new Error("Failed to fetch API data");
  }
}
