"use server";

import { unstable_noStore as noStore } from "next/cache";

const { API_SERVER_URL } = process.env;
const { API_SERVER_ACCESS_TOKEN } = process.env;

if (!API_SERVER_URL || !API_SERVER_ACCESS_TOKEN) {
  throw new Error("API_SERVER_URL or API_SERVER_ACCESS_TOKEN not set");
}

export async function getJson(apiEndpoint: string) {
  try {
    noStore();
    const res = await fetch(API_SERVER_URL + apiEndpoint, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${API_SERVER_ACCESS_TOKEN}`,
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
  try {
    noStore();
    const res = await fetch(API_SERVER_URL + apiEndpoint, {
      method: "POST",
      headers: new Headers({
        "Content-Type": "application/json",
        Accept: "application/json",
        Authorization: `Bearer ${API_SERVER_ACCESS_TOKEN}`,
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
  try {
    noStore();
    const res = await fetch(API_SERVER_URL + apiEndpoint, {
      method: "PUT",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: `Bearer ${API_SERVER_ACCESS_TOKEN}`,
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
  try {
    noStore();
    const res = await fetch(API_SERVER_URL + apiEndpoint, {
      method: "DELETE",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: `Bearer ${API_SERVER_ACCESS_TOKEN}`,
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
