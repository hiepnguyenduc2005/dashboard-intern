import React, {useState} from 'react';

const Register = (props) => {
    const [info, setInfo] = useState({ username: '', password: '', cf_password: '', first_name: '', last_name: '', team: '' });

    const handleChange = (event) => {
        const { name, value } = event.target;
        setInfo(prev => {
            return {
                ...prev,
                [name]:  value,
            };
        });
    }

    const register = async (event) => {
        event.preventDefault();
        if (info.username === '' || info.password === '' || info.cf_password === '' || 
            info.first_name === '' || info.last_name === '') {
            alert('Please fill out all fields.');
            return;
        }
        else if (info.team === '' ) {
            alert('Please select a valid team.');
            return;
        }
        props.register(info);
        console.log(props.status);
    }

    return(
        <div className='component'>
            <h2>Register</h2>
            <form onSubmit={register}>
                <input type='text' name='username' placeholder='Username' value={info.username} onChange={handleChange} />
                <br />
                <input type='password' name='password' placeholder='Password' value={info.password} onChange={handleChange} />
                <br />
                <input type='password' name='cf_password' placeholder='Confirm Password' value={info.cf_password} onChange={handleChange} />
                <br />
                <input type='text' name='first_name' placeholder='First Name' value={info.first_name} onChange={handleChange} />
                <br />
                <input type='text' name='last_name' placeholder='Last Name' value={info.last_name} onChange={handleChange} />
                <br />
                <select name='team' value={info.team} onChange={handleChange}>
                    <option value='' disabled selected>Select Team</option>
                    <option value='Admin Portal'>Admin Portal</option>
                    <option value='Compute'>Compute</option>
                    <option value='Data Fusion'>Data Fusion</option>
                    <option value='Not Applicable'>N/A (Not Applicable)</option>
                </select>
                <br />
                <input type="submit" value="Register" onClick={register}  />
            </form>
        </div>
    )
}

export default Register;