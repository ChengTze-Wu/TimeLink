"use server";

import { unstable_noStore as noStore } from "next/cache";
const { API_GATEWAY } = process.env;

export async function getJson(apiEndpoint: string) {
  noStore();
  try {
    const res = await fetch(API_GATEWAY + apiEndpoint, {
      method: "GET",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
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
  noStore();
  try {
    const res = await fetch(API_GATEWAY + apiEndpoint, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
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

export async function putJson(apiEndpoint: string, data: any) {
  noStore();
  try {
    const res = await fetch(API_GATEWAY + apiEndpoint, {
      method: "PUT",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
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
  noStore();
  try {
    const res = await fetch(API_GATEWAY + apiEndpoint, {
      method: "DELETE",
    });
    const jsonResonseBody = await res.json();
    jsonResonseBody.status = res.status;
    return jsonResonseBody;
  } catch (error) {
    console.error(`Error fetching ${apiEndpoint}: ${error}`);
    throw new Error("Failed to fetch API data");
  }
}
