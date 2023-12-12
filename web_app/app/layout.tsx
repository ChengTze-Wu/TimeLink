import type { Metadata } from "next";
import { inter } from "@/app/ui/fonts";
import "@/app/ui/globals.css";

export const metadata: Metadata = {
  title: {
    template: "%s | TimeLink",
    default: "TimeLink",
  },
  description: "TimeLink is a booking system for your business.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
