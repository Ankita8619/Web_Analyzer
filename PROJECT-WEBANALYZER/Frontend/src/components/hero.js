import React, { useContext } from 'react';
import Script from 'dangerous-html/react';
import PropTypes from 'prop-types';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from './authContext'; // Import AuthContext for authentication checks

import './hero.css';

const Hero = (props) => {
  const { isLoggedIn } = useContext(AuthContext); // Get the authentication status
  const navigate = useNavigate();

  const handleNavigation = (path) => {
    if (isLoggedIn) {
      navigate(path); // Navigate to the path if logged in
    } else {
      alert('Please log in to access this feature.');
      navigate('/login'); // Redirect to login if not authenticated
    }
  };

  return (
    <div
      className={`hero-header78 ${props.rootClassName}`}
      style={{
        backgroundImage: `url(${process.env.PUBLIC_URL + '/background.png'})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        width: '100%',
        height: '100vh', // Full viewport height
      }}
    >
      <div className="hero-column thq-section-max-width thq-section-padding">
        <div className="hero-content1">
          <h1 className="hero-text1 thq-heading-1">
            {props.heading1 || 'Optimize Your Website Seamlessly'}
          </h1>
          <p className="hero-text2 thq-body-large">
            {props.content1 ||
              'Unlock your website’s potential with advanced optimization tools. Analyze performance, improve user experience, ensure security, and enhance SEO rankings all in one platform.'}
          </p>
        </div>
        <div className="hero-actions">
          <button
            className="thq-button-filled hero-button1"
            onClick={() => handleNavigation('/analyzer')} // Use handleNavigation for Analyze
          >
            <span className="thq-body-small">{props.action1 || 'Analyze'}</span>
          </button>
          <button
            className="thq-button-outline hero-button2"
            onClick={() => handleNavigation('/profile')} // Use handleNavigation for Profile
          >
            <span className="thq-body-small">{props.action2 || 'Profile'}</span>
          </button>
        </div>
      </div>
    </div>
  );
};

Hero.defaultProps = {
  heading1: 'Optimize Your Website Seamlessly',
  content1:
    'Unlock your website’s potential with advanced optimization tools. Analyze performance, improve user experience, ensure security, and enhance SEO rankings all in one platform.',
  action1: 'Analyze',
  action2: 'Profile',
  rootClassName: '',
};

Hero.propTypes = {
  heading1: PropTypes.string,
  content1: PropTypes.string,
  action1: PropTypes.string,
  rootClassName: PropTypes.string,
  action2: PropTypes.string,
};

export default Hero;
