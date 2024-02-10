"use client";

import { useRouter } from "next/navigation";

export default function NotFound() {
  const router = useRouter();

  return (
    <main className="flex h-full flex-col items-center justify-center gap-2">
      <h2 className="text-xl font-semibold">404</h2>
      <p>QQ...找不到你想要的資源</p>
      <button
        className="mt-4 rounded-md bg-green-600 px-4 py-2 text-sm text-white transition-colors hover:bg-green-500"
        onClick={() => router.back()}
      >
        回上頁
      </button>
    </main>
  );
}
