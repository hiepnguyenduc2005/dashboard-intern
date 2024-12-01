import React, { useState, useEffect } from 'react';
import { useRoutes, useNavigate } from 'react-router-dom';
import './App.css';
import Landing from './components/Landing';
import Individual from './components/Individual';
import Team from './components/Team';
import Slidebar from './components/Slidebar';
import NotFound from './components/NotFound';
import httpClient from './components/Authentication/httpClient';

const App = () => {
  const [id, setId] = useState(localStorage.getItem('userId') || null);
  const [user, setUser] = useState({'name': '', 'username': '', 'team': ''});
  const [status, setStatus] = useState(localStorage.getItem('status') || 'logout');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      if (status === 'login') {
        try {
          const response = await httpClient.get('/api/@me');
          setId(response.data.id);
          setUser({'name': response.data.name, 'username': response.data.username, 'team': response.data.team});
          localStorage.setItem('userId', response.data.id);
          console.log('User data fetched:', response.data);
        } catch (error) {
          localStorage.removeItem('status');
          localStorage.removeItem('userId');
          console.error('Error fetching user data:', error);
          window.location.reload();
        }
      }
    };
    fetchData();
  }, [status]);

  useEffect(() => {
    if (status !== 'login') {
      navigate('/');
    }
  }, [status, navigate]);

  const logIn = async (info) => {
    try {
      const response = await httpClient.post('/api/login', info);
      console.log('Login response:', response.data);
      setStatus('login');
      localStorage.setItem('status', 'login');
      navigate('/individual');
      console.log('Logged in');
    } catch (error) {
      if (error.response.status === 401) {
        alert("Invalid credentials");
      } else {
        console.error('Login error:', error);
      }
    }
  };

  const register = async (info) => {
    try {
      const response = await httpClient.post('/api/register', info);
      console.log('Register response:', response.data);
      setStatus('login');
      localStorage.setItem('status', 'login');
      navigate('/individual');
      console.log('Registered');
    } catch (error) {
      if (error.response.status === 409) {
        alert("Invalid credentials");
      } else {
        console.error('Register error:', error);
      }
    }
  };

  const logOut = async () => {
    try {
      await httpClient.post('/api/logout');
      setStatus('logout');
      setId(null);
      localStorage.removeItem('status');
      localStorage.removeItem('userId');
      navigate('/');
      console.log('Logged out');
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  // assumed month test
  const month = '07-2023';

  // routing
  let element = useRoutes([
    {
      path: '/',
      element: <Landing logIn={logIn} register={register} status={status} user={user}/>,
    },
    {
      path: '/individual',
      element: status === 'login' ? <Individual id={id} status={status} /> : <Landing logIn={logIn} status={status} />,
    },
    {
      path: '/team',
      element: status === 'login' ? <Team id={id} month={month} status={status} /> : <Landing logIn={logIn} status={status} />,
    },
    {
      path: '*',
      element: <NotFound status={status} />,
    }
  ]);

  return (
    <>
      <div>
        <Slidebar name={user.name} status={status} logOut={logOut} />
      </div>
      <div>
        {element}
      </div>
    </>
  );
};

export default App;
