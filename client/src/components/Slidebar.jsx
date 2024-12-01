import React, { useState, useEffect } from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import Image from '../assets/logo.png';
import { NavLink, useLocation } from 'react-router-dom';

// const settings = ['Profile', 'Account', 'Dashboard', 'Logout'];
const settings = ['Logout'];

function Slidebar(props) {
  const [anchorElUser, setAnchorElUser] = useState(null);
  const [activeButton, setActiveButton] = useState('');
  const [userName, setUsername] = useState('');

  const location = useLocation();
  const path = location.pathname;
  // Determine the current path for setting active button state
  useEffect(() => {
    if (path === '/team') {
      setActiveButton('General Dashboard');
    } else if (path === '/individual') {
      setActiveButton('My Dashboard');
    } else {
      setActiveButton('');
    }
  }, [path]);

  const logOut = async () => {
    props.logOut();
    setUsername('');
  };

  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  const handleButtonClick = (button) => {
    setActiveButton(button);
  };

  return (
    <AppBar position="fixed" sx={{ backgroundColor: '#fff', boxShadow: 'none', borderBottom: '1px solid #e0e0e0' }}>
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          <Typography
            variant="h6"
            noWrap
            component="a"
            href="/"
            sx={{
              display: { xs: 'none', md: 'flex' },
              fontFamily: 'monospace',
              fontWeight: 700,
              letterSpacing: '.3rem',
              color: 'inherit',
              textDecoration: 'none',
            }}
          >
            <img src={Image} alt="Logo" style={{ height: '40px', marginRight: '10px' }} />
          </Typography>
          { props.status !== 'login' ? '' :
          <>
          <Box sx={{ flexGrow: 1, display: 'flex', justifyContent: 'center' }}>
            <NavLink to='/individual'>
              <Button
                variant={activeButton === 'My Dashboard' ? 'contained' : 'outlined'}
                sx={{
                  marginRight: 2,
                  backgroundColor: activeButton === 'My Dashboard' ? '#001f3f' : 'transparent',
                  color: activeButton === 'My Dashboard' ? '#fff' : '#001f3f',
                  textTransform: 'none',
                  border: 'none',
                  '&:hover': {
                    backgroundColor: activeButton === 'My Dashboard' ? '#001830' : 'rgba(0, 31, 63, 0.04)',
                  },
                  minWidth: '150px',
                }}
                onClick={() => handleButtonClick('My Dashboard')}
              >
                My Dashboard
              </Button>
            </NavLink>
            <NavLink to='/team'>
              <Button
                variant={activeButton === 'General Dashboard' ? 'contained' : 'outlined'}
                sx={{
                  marginLeft: 2,
                  backgroundColor: activeButton === 'General Dashboard' ? '#001f3f' : 'transparent',
                  color: activeButton === 'General Dashboard' ? '#fff' : '#001f3f',
                  textTransform: 'none',
                  border: 'none',
                  '&:hover': {
                    backgroundColor: activeButton === 'General Dashboard' ? '#001830' : 'rgba(0, 31, 63, 0.04)',
                  },
                  minWidth: '150px',
                }}
                onClick={() => handleButtonClick('General Dashboard')}
              >
                General Dashboard
              </Button>
            </NavLink>
          </Box>
          <Box sx={{ flexGrow: 0 }}>
            <Tooltip title="Open settings">
              <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }} className='setting-button'>
                <Typography variant="body1" sx={{ cursor: 'pointer', display: 'flex', alignItems: 'center' }} className='setting'>
                  {props.name}
                  <span style={{ marginLeft: '5px', fontSize: '12px' }}>▼</span>
                </Typography>
              </IconButton>
            </Tooltip>
            <Menu
              sx={{ mt: '45px' }}
              id="menu-appbar"
              anchorEl={anchorElUser}
              anchorOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={Boolean(anchorElUser)}
              onClose={handleCloseUserMenu}
              PaperProps={{
                style: {
                  boxShadow: '0px 0px 0px 0px',
                },
              }}
            >
              {settings.map((setting) => (
                <MenuItem key={setting} onClick={handleCloseUserMenu}>
                  <Typography textAlign="center" onClick={logOut}>{setting}</Typography>
                </MenuItem>
              ))}
            </Menu>
          </Box>
          </>
        }
        </Toolbar>
      </Container>
    </AppBar>
  );
}

export default Slidebar;
