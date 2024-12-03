import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../components/authContext';
import './Login.css'; // Assuming the CSS file name remains the same

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const { login } = useContext(AuthContext);

  const handleLogin = async (e) => {
    e.preventDefault();
    console.log('Logging in with', email, password);
    try {
      const response = await axios.post('http://localhost:8000/login', {
        email,
        password,
      });
      if (response.status === 200) {
        console.log('Login successful:', response.data);
        localStorage.setItem('user', JSON.stringify(response.data));
        login();
        navigate('/profile');
        window.location.reload();
      } else {
        alert('Login failed');
      }
    } catch (error) {
      console.error('Error during login:', error);
      alert('Invalid email or password');
    }
  };

  return (
    <div className="body-login">
      <div className="container-login" style={{
      backgroundImage: `url(${process.env.PUBLIC_URL + '/leafs-3898442_1920.jpg'})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
      width: '100%',
      height: '100%', // Ensure the background covers the entire container
    }}
      >
        <div className="form-container-login"style={{
      backgroundImage: `url(${process.env.PUBLIC_URL + '/black-1072366_1920.jpg'})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
      width: '600px',
      height: '400px', // Ensure the background covers the entire container
    }}
        >
          <div className="form-box-login">
            <div className="left-panel-login">
              <h2>LOGIN</h2>
              <form onSubmit={handleLogin}>
                <div className="input-box-login">
                  <label>Email:</label>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
                <div className="input-box-login">
                  <label>Password:</label>
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
              </form>
            </div>
            <div
              className="right-panel-login"
              onClick={handleLogin}
            >
              <span className="login-text-login">Login</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
