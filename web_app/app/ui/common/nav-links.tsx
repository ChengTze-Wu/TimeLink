"use client";

import {
  UserIcon,
  UserGroupIcon,
  RectangleGroupIcon,
  SquaresPlusIcon,
  CalendarDaysIcon,
} from "@heroicons/react/24/solid";
import Link from "next/link";
import { usePathname } from "next/navigation";
import clsx from "clsx";

const links = [
  {
    name: "儀表板",
    href: "/dashboard",
    icon: RectangleGroupIcon,
    roles: ["admin", "group_owner"],
  },
  {
    name: "群組",
    href: "/dashboard/groups",
    icon: UserGroupIcon,
    roles: ["admin", "group_owner"],
  },
  {
    name: "服務",
    href: "/dashboard/services",
    icon: SquaresPlusIcon,
    roles: ["admin", "group_owner"],
  },
  {
    name: "預約",
    href: "/dashboard/bookings",
    icon: CalendarDaysIcon,
    roles: ["admin", "group_owner", "group_member"],
  },
  {
    name: "系統帳號",
    href: "/dashboard/accounts",
    icon: UserIcon,
    roles: ["admin"],
  },
];

export default function NavLinks({ role }: { role: string }) {
  const pathname = usePathname();

  return (
    <>
      {links.map((link) => {
        const LinkIcon = link.icon;
        if (!link.roles.includes(role)) return null;
        return (
          <Link
            key={link.name}
            href={link.href}
            className={clsx(
              "flex h-[48px] grow items-center justify-center gap-2 rounded-md bg-gray-50 p-3 text-sm font-medium hover:bg-green-100 hover:text-primary-green md:flex-none md:justify-start md:p-2 md:px-3",
              {
                "bg-green-100":
                  (pathname.startsWith(link.href) &&
                    link.href !== "/dashboard") ||
                  pathname === link.href,
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
