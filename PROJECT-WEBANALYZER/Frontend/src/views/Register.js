import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Register.css'; // Ensure this path is correct
import axios from 'axios';

const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [username, setUsername] = useState('');
  const [userDetails, setUserDetails] = useState('');
  const [subDetails, setSubDetails] = useState('');
  const [profession, setProfession] = useState('');
  const [image, setImage] = useState(null);
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      alert('Passwords do not match');
      return;
    }
    console.log('Registering with', email, password, username, userDetails, subDetails, profession);

    const formData = new FormData();
    formData.append('email', email);
    formData.append('password', password);
    formData.append('username', username);
    formData.append('user_details', userDetails);
    formData.append('sub_details', subDetails);
    formData.append('profession', profession);
    if (image) {
      formData.append('image', image);
    }

    // Send registration data to the backend using Axios
    try {
      const response = await axios.post('http://localhost:8000/register', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      if (response.status === 200) {
        navigate('/login');
      } else {
        alert('Registration failed');
      }
    } catch (error) {
      console.error('Error during registration:', error);
      alert('An error occurred during registration');
    }
  };

  return (
    <div className="register-body" style={{
      backgroundImage: `url(${process.env.PUBLIC_URL + '/leafs-3898442_1920.jpg'})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
      width: '100%',
      height: '150vh', // Ensure the background covers the entire container
    }}
    >
      <div className="outer-container-register" style={{
      backgroundImage: `url(${process.env.PUBLIC_URL + '/black-1072366_1920.jpg'})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
      width: '550px',
      height: '880px', // Ensure the background covers the entire container
    }}
      >
        <div className="inner-container-register">
          <div className="form-box-register">
            <form className="form-section-register" onSubmit={handleRegister}>
              <h2>Register</h2>
              <div className="input-box-register">
                <label>Username:</label>
                <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
              </div>
              <div className="input-box-register">
                <label>Email:</label>
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
              </div>
              <div className="input-box-register">
                <label>Password:</label>
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
              </div>
              <div className="input-box-register">
                <label>Confirm Password:</label>
                <input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
              </div>
              <div className="input-box-register">
                <label>User Details:</label>
                <textarea value={userDetails} onChange={(e) => setUserDetails(e.target.value)} required></textarea>
              </div>
              <div className="input-box-register">
                <label>Sub Details:</label>
                <textarea value={subDetails} onChange={(e) => setSubDetails(e.target.value)} required></textarea>
              </div>
              <div className="input-box-register">
                <label>Profession:</label>
                <input type="text" value={profession} onChange={(e) => setProfession(e.target.value)} required />
              </div>
              <div className="input-box-register file-upload-register">
                <label htmlFor="profileImage">Choose File</label>
                <input
                  type="file"
                  id="profileImage" // Match with label's htmlFor
                  onChange={(e) => {
                    setImage(e.target.files[0]);
                    const fileNameElement = document.querySelector('.file-name-register');
                    if (fileNameElement) {
                      fileNameElement.textContent = e.target.files[0]?.name || 'No file chosen';
                    }
                  }}
                />
                <span className="file-name-register">No file chosen</span>
              </div>
              <button type="submit" className="btn-register">Register</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;
