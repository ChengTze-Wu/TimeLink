"use client";

import {
  UserIcon,
  UserGroupIcon,
  RectangleGroupIcon,
  ShieldCheckIcon,
  SquaresPlusIcon,
  TableCellsIcon,
  CalendarDaysIcon,
} from "@heroicons/react/24/solid";
import Link from "next/link";
import { usePathname } from "next/navigation";
import clsx from "clsx";

const links = [
  { name: "儀表板", href: "/dashboard", icon: RectangleGroupIcon },
  { name: "群組", href: "/dashboard/groups", icon: UserGroupIcon },
  {
    name: "服務",
    href: "/dashboard/services",
    icon: SquaresPlusIcon,
  },
  { name: "預約", href: "/dashboard/bookings", icon: CalendarDaysIcon },
  { name: "帳號", href: "/dashboard/accounts", icon: UserIcon },
  // { name: "系統紀錄", href: "/dashboard/records", icon: TableCellsIcon },
];

export default function NavLinks() {
  const pathname = usePathname();

  return (
    <>
      {links.map((link) => {
        const LinkIcon = link.icon;
        return (
          <Link
            key={link.name}
            href={link.href}
            className={clsx(
              "flex h-[48px] grow items-center justify-center gap-2 rounded-md bg-gray-50 p-3 text-sm font-medium hover:bg-green-100 hover:text-primary-green md:flex-none md:justify-start md:p-2 md:px-3",
              {
                "bg-green-100": pathname === link.href,
              }
            )}
          >
            <LinkIcon className="w-6" />
            <p className="hidden md:block">{link.name}</p>
          </Link>
        );
      })}
    </>
  );
}
