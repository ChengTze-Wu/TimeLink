import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import LiffProvider from "./liff-provider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "LIFF App Starter",
  description: "A starter template for LIFF apps.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <LiffProvider>{children}</LiffProvider>
      </body>
    </html>
  );
}
