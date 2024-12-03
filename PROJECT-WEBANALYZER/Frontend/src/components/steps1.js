import React from 'react';
import PropTypes from 'prop-types';
import './steps1.css';

const Steps1 = (props) => {
  return (
    <div
      className="steps1-container1 thq-section-padding"
      style={{
        backgroundImage: `url(${process.env.PUBLIC_URL + '/background.png'})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        width: '100%',
        height: '100%', // Ensure the background covers the entire container
      }}
    >
      <h1 className="steps1-main-heading thq-heading-1">
            Transform Your Website in Just a Few Steps!
          </h1>
      <div className="steps1-max-width thq-section-max-width">
        <div className="steps1-container2">
          <div className="steps1-container3 thq-card">
            <h2 className="thq-heading-2">{props.step1Title}</h2>
            <span className="steps1-text2 thq-body-small">
              {props.step1Description}
            </span>
          </div>
          <div className="steps1-container4 thq-card">
            <h2 className="steps1-text3 thq-heading-2">{props.step2Title}</h2>
            <span className="steps1-text4 thq-body-small">
              {props.step2Description}
            </span>
          </div>
        </div>
        <div className="steps1-container5">
          <div className="steps1-container6 thq-card">
            <h2 className="thq-heading-2">{props.step3Title}</h2>
            <span className="steps1-text6 thq-body-small">
              {props.step3Description}
            </span>
          </div>
          <div className="steps1-container7 thq-card">
            <h2 className="thq-heading-2">{props.step4Title}</h2>
            <span className="steps1-text8 thq-body-small">
              {props.step4Description}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

Steps1.defaultProps = {
  step1Description:
    'Start by creating an account or logging in to access the full set of features. Customize your profile and get ready to analyze your website seamlessly.',
  step4Title: 'Stay Updated with Insights',
  step1Title: 'Get Started with Registration',
  step3Title: 'Review and Implement Results',
  step3Description:
    'Explore a comprehensive report that highlights your website’s strengths and areas for improvement. Use actionable insights to enhance performance.',
  text: '04',
  step2Title: 'Submit and Analyze Your Website',
  step4Description:
    'Keep track of new tools, features, and strategies by subscribing to our updates. Stay ahead in optimizing your website regularly.',
  step2Description:
    'Enter your website’s URL and let our platform analyze its performance. Get detailed insights on SEO, security, design, and user engagement metrics.',
};

Steps1.propTypes = {
  step1Description: PropTypes.string,
  step4Title: PropTypes.string,
  step1Title: PropTypes.string,
  step3Title: PropTypes.string,
  step3Description: PropTypes.string,
  text: PropTypes.string,
  step2Title: PropTypes.string,
  step4Description: PropTypes.string,
  step2Description: PropTypes.string,
};

export default Steps1;
