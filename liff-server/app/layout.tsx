import type { Metadata } from "next";
import "./globals.css";
import { AntdRegistry } from "@ant-design/nextjs-registry";
import LiffProvider from "@/app/liff-provider";

export const metadata: Metadata = {
  title: "TimeLink 預約系統",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <AntdRegistry>
        <body className="px-5">
          <LiffProvider>{children}</LiffProvider>
        </body>
      </AntdRegistry>
    </html>
  );
}
