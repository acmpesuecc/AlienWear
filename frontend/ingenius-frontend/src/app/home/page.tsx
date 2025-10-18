"use client";

import { Button } from "@/components/ui/button";
import Navbar from "@/components/navbar";
import { TypewriterEffectSmooth } from "@/components/typewriterEffect";
import ProductCard from "@/components/productCard";
import Link from "next/link";
import { Search } from "lucide-react";

// Sample product data
const sampleProducts = [
  {
    id: "1",
    description: "park avenue men blue black printed slim fit formal shirt",
    imageUrl: "/1.png",
    price: 1099
  },
  {
    id: "2", 
    description: "blackberrys men brown single breasted formal blazer",
    imageUrl: "/2.png",
    price: 3147
  },
  {
    id: "3",
    description: "manq men coffee brown slim fit pinstriped single breasted formal blazer", 
    imageUrl: "/3.png",
    price: 2499
  },
  {
    id: "4",
    description: "allen solly men single breasted formal blazer",
    imageUrl: "/4.png", 
    price: 4799
  }
];

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
    {
      text: "|",
      className: "animate-pulse",
    },
  ];

  return (
    <div className="min-h-screen">
      <Navbar />
      
      {/* Hero Section */}
      <div className="flex flex-col items-center justify-center py-16">
        <TypewriterEffectSmooth words={words} />
      </div>

      {/* Product Showcase Section */}
      <div className="px-4 py-8">
        <div className="flex overflow-x-auto space-x-4 pb-4">
          {sampleProducts.map((product) => (
            <div key={product.id} className="flex-shrink-0 w-64">
              <ProductCard
                Description={product.description}
                ImageURL={product.imageUrl}
                Price={product.price}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Search Interface */}
      <div className="px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="relative">
            <input
              type="text"
              placeholder="I have a presentation in my college tomorrow show me some good men's formal wear"
              className="w-full h-12 px-6 pr-12 bg-gray-800 text-white rounded-full border-none focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
            <button className="absolute right-2 top-2 h-8 w-8 bg-blue-600 hover:bg-blue-700 rounded-full flex items-center justify-center">
              <Search className="h-4 w-4 text-white" />
            </button>
          </div>
        </div>
      </div>

      {/* AI Assistant Button */}
      <div className="flex justify-center pb-8">
        <Link href="/chat">
          <Button className="bg-gray-800 hover:bg-gray-700 text-white px-8 py-3 rounded-lg text-lg">
            Talk to your personalised Fashion Assistant!
          </Button>
        </Link>
      </div>
    </div>
  );
}
