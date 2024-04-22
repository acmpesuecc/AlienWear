import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { SearchIcon } from "lucide-react";
import { useState, ChangeEvent, FormEvent } from "react";
import ProductCard from "./ProductCard";

interface Product {
  Description: string;
  ImageURL: string;
  Price: number;
  Product_id: string;
}

export default function SearchBar() {
  const [searchText, setSearchText] = useState("");
  const [products, setProducts] = useState<Product[]>([]);

  const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
    setSearchText(event.target.value);
  };

  const handleClick = async (event: FormEvent) => {
    event.preventDefault();
    try {
      const response = await fetch(`backend/occasion?query=${searchText}`);
      const data = await response.json();
      setProducts(data.response);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <header className="w-full my-4">
      <div className="container mx-auto flex items-center justify-center">
        <form className="w-full max-w-4xl" onSubmit={handleClick}>
          <div className="relative flex items-center">
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
          <div className="relative flex items-center p-2">
            <Input
              className="h-12 w-full rounded-full border-none px-6 focus:ring-2 bg-gray-800 text-gray-100 focus:ring-gray-600"
              placeholder="Search for products, brands, and more..."
              type="search"
              value={searchText}
              onChange={handleInputChange}
            />
            <Button
              className="absolute right-2 h-10 w-10 rounded-full text-white hover:bg-gray-700 focus:ring-2 bg-gray-500 hover:bg-gray-500= focus:ring-gray-700"
              type="submit"
            >
              <SearchIcon className="h-8 w-8 text-white" />
            </Button>
          </div>
        </form>
      </div>
    </header>
  );
}