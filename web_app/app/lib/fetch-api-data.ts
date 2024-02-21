"use server";

import { unstable_noStore as noStore } from "next/cache";
import { cookies } from "next/headers";

export async function getJson(apiEndpoint: string) {
  const { API_GATEWAY } = process.env;
  try {
    noStore();
    const access_token = cookies().get("access_token")?.value;
    const res = await fetch(API_GATEWAY + apiEndpoint, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${access_token}`,
      },
    });
    const jsonResonseBody = await res.json();
    jsonResonseBody.status = res.status;
    return jsonResonseBody;
  } catch (error) {
    console.error(`Error fetching ${apiEndpoint}: ${error}`);
    throw new Error("Failed to fetch API data");
  }
}

export async function postJson(apiEndpoint: string, data: any) {
  const { API_GATEWAY } = process.env;
  try {
    noStore();
    const access_token = cookies().get("access_token")?.value;
    const res = await fetch(API_GATEWAY + apiEndpoint, {
      method: "POST",
      headers: new Headers({
        "Content-Type": "application/json",
        Accept: "application/json",
        Authorization: `Bearer ${access_token}`,
      }),
      body: JSON.stringify(data),
    });
    const jsonResonseBody = await res.json();
    jsonResonseBody.status = res.status;
    return jsonResonseBody;
  } catch (error) {
    console.error(`Error fetching ${apiEndpoint}: ${error}`);
    throw new Error("Failed to fetch API data");
  }
}

export async function putJson(apiEndpoint: string, data: any) {
  const { API_GATEWAY } = process.env;
  try {
    noStore();
    const access_token = cookies().get("access_token")?.value;
    const res = await fetch(API_GATEWAY + apiEndpoint, {
      method: "PUT",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: `Bearer ${access_token}`,
      },
      body: JSON.stringify(data),
    });
    const jsonResonseBody = await res.json();
    jsonResonseBody.status = res.status;
    return jsonResonseBody;
  } catch (error) {
    console.error(`Error fetching ${apiEndpoint}: ${error}`);
    throw new Error("Failed to fetch API data");
  }
}

export async function deleteJson(apiEndpoint: string) {
  const { API_GATEWAY } = process.env;
  try {
    noStore();
    const access_token = cookies().get("access_token")?.value;
    const res = await fetch(API_GATEWAY + apiEndpoint, {
      method: "DELETE",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: `Bearer ${access_token}`,
      },
    });
    const jsonResonseBody = await res.json();
    jsonResonseBody.status = res.status;
    return jsonResonseBody;
  } catch (error) {
    console.error(`Error fetching ${apiEndpoint}: ${error}`);
    throw new Error("Failed to fetch API data");
  }
}
