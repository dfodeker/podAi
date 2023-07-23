"use client"
import React, { useEffect, useState } from 'react';
import axios, { AxiosResponse } from 'axios';
import { useRouter } from 'next/navigation';

interface User {
  username: string;
  email: string;
  // Add more fields as necessary, based on the response data
}

const Dashboard: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const router = useRouter();

  useEffect(() => {
    fetchUser();
  }, []);

  const fetchUser = async () => {
    const token = localStorage.getItem('token');
    const openAIToken = localStorage.getItem('openAIToken');
    const elevenLabsToken = localStorage.getItem('elevenLabsToken');
    
    console.log('OpenAI Token: ', openAIToken);
    console.log('11 Labs Token: ', elevenLabsToken);
    // If there's no token, redirect to login
    if (!token) {
      router.push('/login');
      return;
    }
    // If there is a token, try to fetch the user
    try {
      const config = {
        headers: { Authorization: `Bearer ${token}` },
      };

      const response: AxiosResponse<User> = await axios.get('http://127.0.0.1:8000/users/me/', config);

      setUser(response.data);
    } catch (error) {
      console.error("Error fetching user", error);
      // If error occurs, it might be due to invalid/expired token, redirect to login
      router.push('/login');
    }
  };

  if (!user) {
    return <p>Loading...</p>; // Or your preferred loading state
  }

  return (
    <div>
      <h1>Welcome, {user.username}!</h1>
      {/* Display other user info as needed */}
      
    </div>
  );
};

export default Dashboard;
