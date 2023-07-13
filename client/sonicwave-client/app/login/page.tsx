"use client"
import React,{useState,useEffect} from "react";
import qs from 'qs';
import axios from "axios";
import Router from 'next/router';


function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [isLoggedIn, setIsLoggedIn] = useState(false);
   

    useEffect(() => {
      if (isLoggedIn) {
        // Redirect to the dashboard page
        Router.push('/dashboard');
      }
    }, [isLoggedIn]);
  
    const handleSubmit = async (event: any) => {
      event.preventDefault();
  
      const data = qs.stringify({
        grant_type: '',
        username: username,
        password: password,
        scope: '',
        client_id: '',
        client_secret: '',
      });
          
      const config = {
        method: 'post',
        url: 'http://127.0.0.1:8000/token',
        headers: { 
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        data: data
      };
  
      axios(config)
        .then((response) => {
          console.log(response.data);
          localStorage.setItem('token', response.data.access_token);
          console.log(localStorage.getItem('token'));
  
          // Redirect to the dashboard page
          Router.push('/dashboard');
        })
        .catch((error) => {
          console.log(error);
        });
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Username:
        <input type="text" value={username} onChange={e => setUsername(e.target.value)} />
      </label>
      <label>
        Password:
        <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
      </label>
      <input type="submit" value="Submit" />
    </form>
  );
}

export default Login;
