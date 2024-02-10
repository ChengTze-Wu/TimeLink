"use client";

import { FaceFrownIcon } from "@heroicons/react/24/outline";

export default function NotFound() {
  return (
    <main className="flex h-full flex-col items-center justify-center gap-2">
      <FaceFrownIcon className="w-10 text-gray-400" />
      <h2 className="text-xl font-semibold">404</h2>
      <p>QQ...找不到你想要的資源</p>
      <button
        className="mt-4 rounded-md bg-primary-green px-4 py-2 text-sm text-white transition-colors hover:bg-green-600"
        onClick={() => history.back()}
      >
        回上頁
      </button>
    </main>
  );
}
