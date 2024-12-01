import React from 'react';
import Login from './Authentication/Login';
import Register from './Authentication/Register';
import ChangePass from './Authentication/ChangePass';
import Welcome from './Authentication/Welcome';

const Landing = (props) => {
    
    return (
        <>
        <div className='heading'>
                <h1>Welcome to FCI Peformance Dashboard</h1>
        </div>
        { 
            props.status === 'login' 
            ? ( 
                <div className='subhead grid2'>
                    <Welcome user={props.user}/>
                    <ChangePass />
                </div>
            )
            : (
                <div className='subhead grid2'>
                    <Login status={props.status} logIn={props.logIn}/>
                    <Register status={props.status} register={props.register}/>
                </div>
            )
        }
        </>
    )
};

export default Landing;