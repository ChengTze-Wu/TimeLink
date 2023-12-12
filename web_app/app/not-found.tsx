'use client';

import { useRouter } from 'next/navigation';
import { FaceFrownIcon } from '@heroicons/react/24/solid';

export default function NotFound() {
  const router = useRouter();
  
  return (
    <main className="flex flex-col items-center justify-center gap-2 text-secondary-blue h-screen">
      <FaceFrownIcon className="w-10" />
      <h2 className="text-xl font-semibold">404 Not Found</h2>
      <button
        type="button"
        onClick={() => router.back()}
        className="mt-4 rounded-md bg-primary-green px-4 py-2 text-sm text-primary-white transition-colors hover:bg-green-400"
      >
        Go Back
      </button>
    </main>
  );
}
