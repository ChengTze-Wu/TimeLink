"use client";

import {
  UserCircleIcon,
  EnvelopeIcon,
  KeyIcon,
  FaceSmileIcon,
  DevicePhoneMobileIcon,
  ShieldCheckIcon,
} from "@heroicons/react/24/solid";
import { createAccount } from "@/app/ui/accounts/actions";
import { useFormState } from "react-dom";

const createInputFields = [
  {
    type: "text",
    name: "username",
    placeholder: "Username",
    icon: UserCircleIcon,
  },
  {
    type: "text",
    name: "name",
    placeholder: "Name",
    icon: FaceSmileIcon,
  },
  {
    type: "text",
    name: "email",
    placeholder: "Email",
    icon: EnvelopeIcon,
  },
  {
    type: "password",
    name: "password",
    placeholder: "Password",
    icon: KeyIcon,
  },
  {
    type: "password",
    name: "confirmPassword",
    placeholder: "Confirm Password",
    icon: ShieldCheckIcon,
  },
  {
    type: "text",
    name: "phone",
    placeholder: "Phone Number",
    icon: DevicePhoneMobileIcon,
  },
];

export default function CerateForm() {
  const initialState = { message: null, errors: {} };
  const [state, dispatch] = useFormState(createAccount, initialState);

  return (
    <form
      action={dispatch}
      className="w-full h-full p-10 bg-gray-50 rounded-md flex flex-col"
    >
      {createInputFields.map((inputField) => {
        const InputIcon = inputField.icon;
        return (
          <div
            key={inputField.name}
            className="relative mt-6 rounded-md shadow-sm"
          >
            <label
              htmlFor={inputField.name}
              className="text-gray-500 sm:text-sm pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3"
            >
              <InputIcon className="w-5 h-5" />
            </label>
            <input
              type={inputField.type}
              name={inputField.name}
              id={inputField.name}
              className="w-full rounded-md border-0 py-1.5 pl-10 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-green sm:text-sm sm:leading-6 outline-none"
              placeholder={inputField.placeholder}
              defaultValue={undefined}
            />
          </div>
        );
      })}
      <div className="mt-2 rounded-md flex gap-2 items-center">
        <label htmlFor="isActive" className="">
          啟用
        </label>
        <input
          type="checkbox"
          name="isActive"
          id="isActive"
          defaultChecked={true}
          className="rounded-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-green sm:text-sm sm:leading-6 outline-none"
        />
      </div>
      <div className="mt-4 grow flex items-end justify-center">
        <button
          type="submit"
          className="w-20 rounded-md bg-primary-green py-2 text-white font-medium hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 self-end"
        >
          建立
        </button>
      </div>
    </form>
  );
}
