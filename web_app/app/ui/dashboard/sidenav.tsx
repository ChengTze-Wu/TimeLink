import Link from "next/link";
import NavLinks from "@/app/ui/dashboard/nav-links";
import {
  ArrowLeftOnRectangleIcon,
  UserCircleIcon,
} from "@heroicons/react/24/solid";

export default function SideNav({ username }: { username: string }) {
  return (
    <div className="flex h-full flex-col px-3 py-4 md:px-2">
      <Link
        className="mb-2 flex h-20 items-center justify-start rounded-md p-4 bg-primary-green"
        href="/"
      >
        <div className="w-32 text-white md:w-40">
          <p className="text-2xl font-bold">TimeLink</p>
        </div>
      </Link>
      <div className="flex grow flex-row justify-between space-x-2 md:flex-col md:space-x-0 md:space-y-2">
        <NavLinks />
        <div className="hidden h-auto w-full grow rounded-md bg-gray-50 md:block"></div>
        <form className="flex gap-2 h-[48px]">
          <button className="flex items-center justify-center gap-2 rounded-md bg-gray-50 p-3 text-sm font-medium hover:bg-green-100 hover:text-primary-green md:flex-none md:justify-start md:p-2 md:px-3">
            <ArrowLeftOnRectangleIcon className="w-6" />
            <div className="hidden md:block">登出</div>
          </button>
          <Link
            href="#"
            className="flex flex-auto items-center justify-center gap-2 rounded-md bg-gray-50 p-3 text-sm font-medium hover:bg-green-100 hover:text-primary-green md:justify-start md:p-2 md:px-3"
          >
            <UserCircleIcon className="w-6" />
            <p className="hidden md:block">王小明</p>
          </Link>
        </form>
      </div>
    </div>
  );
}
