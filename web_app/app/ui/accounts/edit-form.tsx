"use client";

import {
  UserCircleIcon,
  EnvelopeIcon,
  KeyIcon,
  FaceSmileIcon,
  DevicePhoneMobileIcon,
  ShieldCheckIcon,
} from "@heroicons/react/24/solid";
import { updateAccount } from "@/app/lib/accounts/actions";
import { useFormState } from "react-dom";
import { User } from "@/app/lib/definitions";

export default function EditForm({ user }: { user: User }) {
  const initialState = { message: null, errors: {} };

  const updateAccountWithUuid = updateAccount.bind(null, user.id);
  const [state, dispatch] = useFormState(updateAccountWithUuid, initialState);

  return (
    <form
      action={dispatch}
      className="w-full h-full p-10 bg-gray-50 rounded-md flex flex-col"
    >
      <div className="relative mt-6 rounded-md shadow-sm">
        <label
          htmlFor="username"
          className="text-gray-500 sm:text-sm pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3"
        >
          <UserCircleIcon className="w-5 h-5" />
        </label>
        <input
          type="text"
          name="username"
          id="username"
          className="w-full rounded-md border-0 py-1.5 pl-10 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-green sm:text-sm sm:leading-6 outline-none"
          defaultValue={user.username}
          placeholder="Username"
        />
      </div>
      <div className="relative mt-6 rounded-md shadow-sm">
        <label
          htmlFor="name"
          className="text-gray-500 sm:text-sm pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3"
        >
          <FaceSmileIcon className="w-5 h-5" />
        </label>
        <input
          type="text"
          name="name"
          id="name"
          className="w-full rounded-md border-0 py-1.5 pl-10 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-green sm:text-sm sm:leading-6 outline-none"
          defaultValue={user.name}
          placeholder="Name"
        />
      </div>
      <div className="relative mt-6 rounded-md shadow-sm">
        <label
          htmlFor="email"
          className="text-gray-500 sm:text-sm pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3"
        >
          <EnvelopeIcon className="w-5 h-5" />
        </label>
        <input
          type="text"
          name="email"
          id="email"
          className="w-full rounded-md border-0 py-1.5 pl-10 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-green sm:text-sm sm:leading-6 outline-none"
          defaultValue={user.email}
          placeholder="Email"
        />
      </div>
      <div className="relative mt-6 rounded-md shadow-sm">
        <label
          htmlFor="phone"
          className="text-gray-500 sm:text-sm pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3"
        >
          <DevicePhoneMobileIcon className="w-5 h-5" />
        </label>
        <input
          type="text"
          name="phone"
          id="phone"
          className="w-full rounded-md border-0 py-1.5 pl-10 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-green sm:text-sm sm:leading-6 outline-none"
          defaultValue={user.phone}
          placeholder="Phone"
        />
      </div>
      <div className="relative mt-6 rounded-md shadow-sm">
        <select
          name="role"
          defaultValue={user.role}
          className="w-full rounded-md border-0 py-2 pl-3 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-green sm:text-sm sm:leading-6 outline-none"
        >
          <option>----請下拉選擇----</option>
          <option value="admin">管理員</option>
          <option value="group_owner">群組管理員</option>
          <option value="group_member">群組成員</option>
        </select>
      </div>
      <div className="mt-6 rounded-md flex gap-2 items-center">
        <label htmlFor="isActive" className="">
          啟用
        </label>
        <input
          type="checkbox"
          name="isActive"
          id="isActive"
          defaultChecked={user.is_active}
          className="rounded-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-green sm:text-sm sm:leading-6 outline-none"
        />
      </div>
      <div className="mt-4 grow flex items-end justify-center">
        <button
          type="submit"
          className="w-20 rounded-md bg-primary-green py-2 text-white font-medium hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 self-end"
        >
          修改
        </button>
      </div>
    </form>
  );
}
