"use client";

import { useEffect } from "react";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Optionally log the error to an error reporting service
    console.error(error);
  }, [error]);

  return (
    <main className="flex h-full flex-col items-center justify-center">
      <h2 className="text-center">伺服器錯誤，請稍候再試一次。</h2>
      <button
        className="mt-4 rounded-md bg-primary-green px-4 py-2 text-sm text-white transition-colors hover:bg-green-400"
        onClick={() => reset()}
      >
        Try again
      </button>
    </main>
  );
}
