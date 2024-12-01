import React, {useState} from 'react';
import { useNavigate } from 'react-router-dom';
import httpClient from './httpClient';

const ChangePass = (props) => {
    const [info, setInfo] = useState({ old_password: '', new_password: '', cf_password: ''});

    const handleChange = (event) => {
        const { name, value } = event.target;
        setInfo(prev => {
            return {
                ...prev,
                [name]:  value,
            };
        });
    }
    const navigate = useNavigate();
    const changePassword = async (event) => {
        event.preventDefault();
        try {
          const response = await httpClient.post('/api/change-password', info);
          console.log('Change password response:', response.data);
          navigate('/individual');
        } catch (error) {
          if (error.response.status === 401) {
            alert("Invalid credentials");
          } else {
            console.error('Change password error:', error);
          }
        }
      };

    return(
        <div className='component'>
            <h2>Change Password</h2>
            <form onSubmit={changePassword}>
                <input type='password' name='old_password' placeholder='Old Password' value={info.old_password} onChange={handleChange} />
                <br />
                <input type='password' name='new_password' placeholder='New Password' value={info.new_password} onChange={handleChange} />
                <br />
                <input type='password' name='cf_password' placeholder='Confirm Password' value={info.cf_password} onChange={handleChange} />
                <br />
                <input type="submit" value="Change Password" onClick={changePassword}  />
            </form>
        </div>
    )
}

export default ChangePass;