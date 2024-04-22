"use client";

import { Button } from "@/components/ui/button";
import Navbar from "@/components/navbar";
import { TypewriterEffectSmooth } from "@/components/typewriterEffect";
import SearchBar from "@/components/searchBar";
import Link from "next/link";
import Image from "next/image";

export default function Home() {
  const words = [
    {
      text: "Welcome",
    },
    {
      text: "to",
    },
    {
      text: "the",
    },
    {
      text: "AlienWear",
      className: "text-blue-500 dark:text-blue-500",
    },
    {
      text: "Experience",
    },
  ];

  return (
    <>
      <Navbar />
      <div className="flex flex-col h-[calc(100vh-75px)] justify-center">
        <TypewriterEffectSmooth words={words} />
        <SearchBar />
        <div className="flex justify-center mt-4">
          <Link href="/chat">
            <Button className="text-lg">
              Talk to your personalised Fashion Assistant!
            </Button>
          </Link>
        </div>
      </div>
    </>
  );
}
