// verify-tailwind.tsx
import React from 'react';

const VerifyTailwindPage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-xl shadow-lg p-8 space-y-4">
        <h1 className="text-3xl font-bold text-center text-indigo-600">Tailwind CSS Verification</h1>
        <p className="text-gray-600 text-center">
          If you see colors and proper styling, Tailwind CSS is working!
        </p>
        
        <div className="flex space-x-4 justify-center">
          <div className="w-16 h-16 bg-red-500 rounded-lg"></div>
          <div className="w-16 h-16 bg-green-500 rounded-lg"></div>
          <div className="w-16 h-16 bg-blue-500 rounded-lg"></div>
        </div>
        
        <button className="w-full py-3 bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-semibold rounded-lg hover:from-indigo-600 hover:to-purple-700 transition-all shadow-md">
          Styled Button
        </button>
        
        <div className="pt-4 text-center text-sm text-gray-500">
          <p>This page verifies Tailwind CSS is properly configured.</p>
        </div>
      </div>
    </div>
  );
};

export default VerifyTailwindPage;