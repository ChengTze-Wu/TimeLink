"use client";

import { TrashIcon } from "@heroicons/react/24/solid";
import { deleteService } from "@/app/lib/services/actions";
import { DeletePopup } from "@/app/ui/common/popup";
import { useState } from "react";
import { Service } from "@/app/lib/definitions";

export function DeleteService({ service }: { service: Service }) {
  const deleteServiceWithUuid = deleteService.bind(null, service.id);
  const [popup, showPopup] = useState(false);

  return (
    <>
      <button
        className="rounded-md border p-2 hover:bg-gray-100 hover:text-pink-600"
        onClick={() => showPopup(true)}
      >
        <span className="sr-only">Delete</span>
        <TrashIcon className="w-5 text-gray-500" />
      </button>
      {popup && (
        <DeletePopup
          showPopup={showPopup}
          action={deleteServiceWithUuid}
          title={service.name}
        />
      )}
    </>
  );
}
