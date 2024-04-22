"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import Navbar from "@/components/navbar";
import ProductCard from "@/components/ProductCard";
import { TypewriterEffectSmooth } from "@/components/typewriterEffect";

interface Product {
  Description: string;
  ImageURL: string;
  Price: number;
  Product_id: string;
}

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
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [input, setInput] = useState("");

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onloadend = () => {
        setSelectedFile(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInput(event.target.value);
  };

  const handleSendClick = async () => {
    console.log(selectedFile);
    try {
      const response = await fetch("backend/imagecapture", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ imgURI: selectedFile, text: input }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      console.log(data);
      setProducts(data.response);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <>
      <Navbar />
      <TypewriterEffectSmooth words={words} />
      <div className="flex flex-col h-[calc(100vh-75px)] justify-center items-center">
        <div className="relative flex items-center w-full max-w-3xl mt-4">
          <div className="flex overflow-x-auto">
            {products.map((product, index) => (
              <ProductCard
                key={index}
                ImageURL={product.ImageURL}
                Description={product.Description}
                Price={product.Price}
              />
            ))}
          </div>
        </div>

        <div className="flex justify-between mt-4 w-full max-w-3xl">
          <input
            type="file"
            onChange={handleFileChange}
            className="flex-grow rounded px-2 py-1 m-1 border"
          />
          <button onClick={handleSendClick} className="text-lg">
            Upload
          </button>
        </div>

        <div className="flex justify-between mt-4 w-full max-w-3xl">
          <input
            type="text"
            value={input}
            onChange={handleInputChange}
            className="flex-grow rounded px-2 py-1 m-1 border"
          />
          <Button onClick={handleSendClick} className="text-lg">
            Send
          </Button>
        </div>
      </div>
    </>
  );
}
