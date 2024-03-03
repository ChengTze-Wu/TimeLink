"use client";

import { PlusCircleIcon, UserGroupIcon } from "@heroicons/react/24/solid";
import { createGroup } from "@/app/lib/groups/actions";
import { useFormState } from "react-dom";

export default function CreateForm({ placeholder }: { placeholder: string }) {
  const initialState = { message: "", errors: {} };
  const [state, dispatch] = useFormState(createGroup, initialState);

  return (
    <form
      action={dispatch}
      className="rounded-md flex relative h-10 w-2/3 gap-1"
    >
      <label
        htmlFor="lineGroupId"
        className="text-gray-500 sm:text-sm pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3"
      >
        <UserGroupIcon className="w-5 h-5" />
      </label>
      <input
        type="text"
        name="lineGroupId"
        id="lineGroupId"
        className="w-full rounded-md border border-gray-200 py-1.5 pl-10 pr-20 text-gray-900 placeholder:text-gray-400 sm:text-sm sm:leading-6 outline-primary-green focus:outline-primary-green focus:ring-1 focus:ring-primary-green focus:border-primary-green"
        placeholder={placeholder}
        defaultValue={undefined}
        aria-describedby="error-message"
      />
      <button
        type="submit"
        className=" text-white bg-primary-green hover:bg-green-700 rounded-md w-10 flex items-center justify-center"
      >
        <PlusCircleIcon className="rounded-full w-6 h-6" />
      </button>
      <div
        className="absolute flex items-center pointer-events-none bottom-10 right-10 text-sm text-pink-600"
        id="error-message"
        aria-live="polite"
        aria-atomic="true"
      >
        {state?.errors?.line_group_id &&
          state?.errors?.line_group_id.map((error: string) => (
            <p key={error}>{error}</p>
          ))}
        {!state?.errors && state?.message && <p>{state.message}</p>}
      </div>
    </form>
  );
}
