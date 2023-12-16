"use client";

import { TrashIcon } from "@heroicons/react/24/solid";
import { deleteAccount } from "./actions";
import { DeletePopup } from "./popup";
import { useState } from "react";
import { User } from "@/app/lib/definitions";

export function EditAccount({ user }: { user: User }) {}

export function DeleteAccount({ user }: { user: User }) {
  const deleteAccountWithUuid = deleteAccount.bind(null, user.id);
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
          action={deleteAccountWithUuid}
          username={user.username}
        />
      )}
    </>
  );
}
