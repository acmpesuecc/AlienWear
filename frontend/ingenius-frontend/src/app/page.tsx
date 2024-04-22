"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { BackgroundGradientAnimation } from "@/components/bgGradientAnimation";
import { Skeleton } from "@/components/ui/skeleton";

export default function Home() {
  const [hasRendered, setHasRendered] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const timer = setTimeout(() => {
      setHasRendered(true);
      router.push("/home");
    }, 5000);

    return () => clearTimeout(timer);
  }, [router]);

  if (!hasRendered) {
    return (
      <BackgroundGradientAnimation>
        <div className="absolute flex flex-col items-center justify-center h-screen z-50 inset-0 text-white font-bold px-4 pointer-events-none text-center">
          <p className="bg-clip-text text-transparent drop-shadow-2xl text-4xl md:text-4xl lg:text-7xl bg-gradient-to-b from-white/80 to-white/20 mb-4">
            AlienWear
          </p>
          <p className="bg-clip-text text-transparent drop-shadow-2xl text-xl md:text-2xl lg:text-4xl bg-gradient-to-b from-white/80 to-white/20">
            Step into a revolutionary way to find clothes
          </p>
        </div>
      </BackgroundGradientAnimation>
    );
  }

  return (
    <div className="flex items-center space-x-4">
      <Skeleton className="h-12 w-12 rounded-full" />
      <div className="space-y-2">
        <Skeleton className="h-4 w-[250px]" />
        <Skeleton className="h-4 w-[200px]" />
      </div>
    </div>
  );
}
