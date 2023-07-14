"use client";
import { PhotoIcon, UserCircleIcon } from '@heroicons/react/24/solid'
import { useRouter } from 'next/navigation';
import { FormEvent, useEffect, useState } from 'react';

export default function Settings() {
    const router = useRouter();
    const [openAIToken, setOpenAIToken] = useState('');
    const [elevenLabsToken, setElevenLabsToken] = useState('');
  
    useEffect(() => {
      let token; 
  
      if (typeof window !== 'undefined') { // Check if window is defined
        token = localStorage.getItem('token');
      }
  
      // If there's no token, redirect to login
      if (!token) {
        router.push('/login');
      }
    }, []);
  
    const handleSubmit = (e: FormEvent) => {
      e.preventDefault();
  
      // Save the tokens in local storage
      localStorage.setItem('openAIToken', openAIToken);
      localStorage.setItem('elevenLabsToken', elevenLabsToken);
  
      console.log('Tokens saved!');
    };
  return (
    <div className='w-full p-4 bg-white border border-gray-200 rounded-lg shadow sm:p-8 '>
      <form onSubmit={handleSubmit}>
        <label htmlFor="openai-token">
          OpenAI Token:
          <input
            id="openai-token"
            type="text"
            value={openAIToken}
            onChange={(e) => setOpenAIToken(e.target.value)}
          />
        </label>
        <label htmlFor="11labs-token">
          11 Labs Token:
          <input
            id="11labs-token"
            type="text"
            value={elevenLabsToken}
            onChange={(e) => setElevenLabsToken(e.target.value)}
          />
        </label>
        <button type="submit">Save Tokens</button>
      </form>
    </div>
  );
};
