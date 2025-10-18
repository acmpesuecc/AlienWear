"use client";

import * as React from "react";
import Link from "next/link";
import { Menu, Search, ShoppingCart } from "lucide-react";
import { ModeToggle } from "./themeToggle";
import { Button } from "./ui/button";
// import { UserAvatar } from "./userAvatar";
// import { useSession } from "next-auth/react";

export default function Navbar() {
  const [state, setState] = React.useState(false);
  //   const { status } = useSession();

  const menus = [
    { title: "Home", path: "/" },
    { title: "About", path: "/" },
    { title: "Products", path: "/products" },
    { title: "Contact Us", path: "/" },
  ];

  return (
    <nav className="w-full bg-gray-900 border-b border-gray-800">
      <div className="items-center px-4 max-w-screen-xl mx-auto md:flex md:px-8">
        <div className="flex items-center justify-between py-3 md:py-5 md:block">
          <Link href="/">
            <h1 className="text-3xl font-bold text-white">AlienWear</h1>
          </Link>
          <div className="md:hidden">
            <button
              className="text-white outline-none p-2 rounded-md focus:border-gray-400 focus:border"
              onClick={() => setState(!state)}
            >
              <Menu />
            </button>
          </div>
        </div>
        <div
          className={`flex-1 justify-self-center pb-3 mt-8 md:block md:pb-0 md:mt-0 ${
            state ? "block" : "hidden"
          }`}
        >
          <ul className="justify-end items-center space-y-8 md:flex md:space-x-6 md:space-y-0">
            {menus.map((item, idx) => (
              <li key={idx} className="text-white hover:text-blue-400 transition-colors">
                <Link href={item.path}>{item.title}</Link>
              </li>
            ))}
            <li>
              <Link href="/login">
                <Button className="bg-white text-gray-900 hover:bg-gray-100">Log In</Button>
              </Link>
            </li>
            <Link href="/cart">
              <Button variant="ghost" size="icon" className="text-white hover:bg-gray-800">
                <ShoppingCart />
              </Button>
            </Link>
            <ModeToggle />
          </ul>
        </div>
      </div>
    </nav>
  );
}
