"use client";

import clsx from "clsx";
import { useSearchParams, usePathname, useRouter } from "next/navigation";
import {
  CheckCircleIcon,
  XCircleIcon,
  FunnelIcon,
} from "@heroicons/react/24/solid";

export default function StatusFilter({ status }: { status: string }) {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const { replace } = useRouter();

  function handleStatus() {
    const params = new URLSearchParams(searchParams);
    params.set("page", "1");
    if (status === "1") {
      params.set("status", String(0));
    } else if (status === "0") {
      params.delete("status");
    } else {
      params.set("status", String(1));
    }
    replace(`${pathname}?${params.toString()}`);
  }

  return (
    <button
      className={clsx(
        "flex items-center gap-1",
        status === "0"
          ? "text-pink-500 hover:text-pink-400"
          : status === "1"
          ? "text-primary-green hover:text-green-400"
          : "text-secondary-gray hover:text-gray-500"
      )}
      onClick={handleStatus}
    >
      <p>狀態</p>
      {status === "0" ? (
        <XCircleIcon className="w-4 h-4" />
      ) : status === "1" ? (
        <CheckCircleIcon className="w-4 h-4" />
      ) : (
        <FunnelIcon className="w-4 h-4" />
      )}
    </button>
  );
}
