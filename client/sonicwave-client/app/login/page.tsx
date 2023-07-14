"use client"
import React,{useState,useEffect} from "react";
import qs from 'qs';
import axios from "axios";
import{useRouter} from "next/navigation"
import ErrorComponent from "./error";




function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const router = useRouter();


    useEffect(() => {
      if (isLoggedIn) {
        // Redirect to the dashboard page
        router.push('/');
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
  
      try {
        const response = await axios(config);
        localStorage.setItem('token', response.data.access_token);
        router.push('/dashboard');
    } catch (err) {
        setError("Your credentials might be wrong!");  //Setting error state
    }
  }

  return (
    <>
    
    <div className='h-screen flex bg-gray-bg1'>
            <div className='w-full max-w-md m-auto bg-white rounded-lg border border-primaryBorder shadow-default py-10 px-16'>
                <h1 className='text-2xl font-medium text-slate-950 mt-4 mb-12 text-center'>
                    Log in to your account 🔐
                </h1>

                <form onSubmit={handleSubmit}>
                {error && <ErrorComponent errorMsg={error} />}
                    <div>
                        <label htmlFor='username'>Username</label>
                        <input
                           type="text" value={username} onChange={e => setUsername(e.target.value)}
                            className={`w-full p-2  text-slate-950  border rounded-md outline-none text-sm transition duration-150 ease-in-out mb-4`}
                            id='username'
                            placeholder='Your Username'
                            
                        />
                    </div>
                    <div >
                        <label htmlFor='password'>Password</label>
                        <input
                            type='password'
                            className={`w-full p-2  text-slate-950  border rounded-md outline-none text-sm transition duration-150 ease-in-out mb-4`}
                            id='password'
                            placeholder='Your Password'
                            value={password} onChange={e => setPassword(e.target.value)}
                        />
                    </div>

                    <div className='flex justify-center items-center mt-6'>
                        <button
                            className={`bg-green-600 py-2 px-4 text-sm text-white rounded border border-green focus:outline-none focus:border-green-dark`}
                        >
                            Login
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </>
  );
}

export default Login;
