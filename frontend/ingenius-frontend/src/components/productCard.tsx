import React from 'react';

interface ProductCardProps {
  Description: string;
  ImageURL: string;
  Price: number;
}

const ProductCard: React.FC<ProductCardProps> = ({ Description, ImageURL, Price }) => {
  return (
    <div className="min-w-64 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700 mr-2">
      <a href="#">
        <img className="h-64 w-full p-8 rounded-t-lg" src={ImageURL} alt="product image" />
      </a>
      <div className="px-5 pb-5">
        <a href="#">
          <h5 className="text-sm tracking-tight text-gray-900 dark:text-white">{Description}</h5>
        </a>
        <div className="flex items-center mt-2.5 mb-5">
          <div className="flex items-center space-x-1 rtl:space-x-reverse">
            {/* Star SVGs here */}
          </div>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-2xl font-bold text-gray-900 dark:text-white">₹{Price}</span>
          <a href="#" className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Add to cart</a>
        </div>
      </div>
    </div>
  );
}

export default ProductCard;