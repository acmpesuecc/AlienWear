import React from 'react';

interface ProductCardProps {
  Description: string;
  ImageURL: string;
  Price: number;
}

const ProductCard: React.FC<ProductCardProps> = ({ Description, ImageURL, Price }) => {
  return (
    <div className="w-64 bg-gray-800 border border-gray-700 rounded-lg shadow-lg hover:shadow-xl transition-shadow">
      <div className="h-64 w-full">
        <img 
          src={ImageURL} 
          alt={Description}
          className="w-full h-full object-cover rounded-t-lg"
        />
      </div>
      <div className="p-4">
        <h5 className="text-sm text-white mb-3 line-clamp-2">{Description}</h5>
        <div className="flex items-center justify-between">
          <span className="text-xl font-bold text-blue-400">₹{Price}</span>
          <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg text-sm px-4 py-2 transition-colors">
            Add to cart
          </button>
        </div>
      </div>
    </div>
  );
}

export default ProductCard;