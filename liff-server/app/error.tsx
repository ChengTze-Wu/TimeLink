"use client";

export default function Error({ reset }: { reset: () => void }) {
  return (
    <main className="flex h-screen flex-col items-center justify-center">
      <h2 className="text-center">伺服器發生錯誤</h2>
      <button
        className="mt-4 rounded-md bg-green-500 px-4 py-2 text-sm text-white transition-colors hover:bg-green-400"
        onClick={() => reset()}
      >
        重試
      </button>
    </main>
  );
}
