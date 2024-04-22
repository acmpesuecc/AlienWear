"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import Navbar from "@/components/navbar";
import ProductCard from "@/components/ProductCard";
import { TypewriterEffectSmooth } from "@/components/typewriterEffect";

interface Message {
  sender: "user" | "bot";
  text: string;
}

interface Product {
  Description: string;
  ImageURL: string;
  Price: number;
  Product_id: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [products, setProducts] = useState<Product[]>([]);
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

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInput(event.target.value);
  };

  const handleSendClick = async () => {
    setMessages([...messages, { sender: "user", text: input }]);
    setInput("");

    try {
      const response = await fetch("backend/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: input }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: "bot", text: data.message },
      ]);
    } catch (error) {
      console.error("Error:", error);
    }
  };
  const handleSuggestionClick = async () => {
    try {
      const response = await fetch("backend/chat", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: "bot", text: data.message },
      ]);
      setProducts(data.response); // Update the products state variable with the products from the response
    } catch (error) {
      console.error("Error:", error);
    }
  };
  return (
    <>
      <Navbar />
      <TypewriterEffectSmooth words={words} />
      <div className="flex flex-col h-[calc(100vh-75px)] justify-center items-center">
        <div className="overflow-auto w-full max-w-3xl">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${
                message.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`rounded px-2 py-1 m-1 ${
                  message.sender === "user"
                    ? "bg-blue-500 text-white"
                    : "bg-gray-300 text-black"
                }`}
              >
                {message.text}
              </div>
            </div>
          ))}
        </div>
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
            type="text"
            value={input}
            onChange={handleInputChange}
            className="flex-grow rounded px-2 py-1 m-1 border"
          />
          <Button onClick={handleSendClick} className="text-lg">
            Send
          </Button>
        </div>
        <div className="mt-4 flex w-full max-w-3xl">
          <Button onClick={handleSuggestionClick} className="text-lg w-full">
            Yes generate the suggestions
          </Button>
        </div>
      </div>
    </>
  );
}
