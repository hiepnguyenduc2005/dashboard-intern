import React, {useState} from 'react';

const Login = (props) => {
    const [info, setInfo] = useState({ username: '', password: '' });

    const handleChange = (event) => {
        const { name, value } = event.target;
        setInfo(prev => {
            return {
                ...prev,
                [name]:  value,
            };
        });
    }

    const logIn = async (event) => {
        event.preventDefault();
        props.logIn(info);
        console.log(props.status);
    }

    return(
        <div className='component'>
            <h2>Login</h2>
            <form onSubmit={logIn}>
                <input type='text' name='username' placeholder='Username' value={info.username} onChange={handleChange} />
                <br />
                <input type='password' name='password' placeholder='Password' value={info.password} onChange={handleChange} />
                <br />
                <input type="submit" value="Login" onClick={logIn}  />
            </form>
        </div>
    )
}

export default Login;