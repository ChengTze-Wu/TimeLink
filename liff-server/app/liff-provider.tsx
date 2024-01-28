"use client";

import React, { useState, useEffect, createContext } from "react";
import liff, { Liff } from "@line/liff";

type LiffContextType = {
  liff: Liff | null;
  error: string | null;
};

export const LiffContext = createContext<LiffContextType>({
  liff: null,
  error: null,
});

export default function LiffProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [liffObject, setLiffObject] = useState<Liff | null>(null);
  const [liffError, setLiffError] = useState<string | null>(null);

  useEffect(() => {
    console.log("start liff.init()...");
    const liffId = process.env.LIFF_ID || "";
    liff
      .init({ liffId: liffId })
      .then(() => {
        console.log("liff.init() done");
        setLiffObject(liff);
      })
      .catch((error) => {
        console.log(`liff.init() failed: ${error}`);
        if (!process.env.liffId) {
          console.info(
            "LIFF Starter: Please make sure that you provided `LIFF_ID` as an environmental variable."
          );
        }
        setLiffError(error.toString());
      });
  }, []);

  return (
    <LiffContext.Provider value={{ liff: liffObject, error: liffError }}>
      {children}
    </LiffContext.Provider>
  );
}
