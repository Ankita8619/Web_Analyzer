import React from "react";
import PropTypes from "prop-types";
import "./features21.css";

const Features21 = (props) => {
  return (
    <div className="features21-layout302 thq-section-padding">
      <div className="features21-max-width thq-section-max-width">
        <div className="features21-section-title thq-flex-column">
          <h2 className="thq-heading-2">{props.sectionTitle}</h2>
          <p className="thq-body-large">{props.sectionDescription}</p>
        </div>
        <div className="features21-content1">
          <div className="thq-grid-5">
            {/* Feature 1: User Interface */}
            <div className="features21-feature1 thq-flex-column">
              <img
                alt={props.feature1ImageAlt}
                src="/ui.jpg"
                className="thq-team-image-round"
              />
              <div className="thq-flex-column">
                <h3 className="thq-heading-3">{props.feature1Title}</h3>
                <span className="thq-body-small">
                  {props.feature1Description}
                </span>
              </div>
            </div>
            {/* Feature 2: User Experience */}
            <div className="features21-feature2 thq-flex-column">
              <img
                alt={props.feature2ImageAlt}
                src="/ux.jpg"
                className="thq-team-image-round"
              />
              <div className="thq-flex-column">
                <h3 className="thq-heading-3">{props.feature2Title}</h3>
                <span className="thq-body-small">
                  {props.feature2Description}
                </span>
              </div>
            </div>
            {/* Feature 3: SEO */}
            <div className="features21-feature3 thq-flex-column">
              <img
                alt={props.feature3ImageAlt}
                src="/seo.png"
                className="thq-team-image-round"
              />
              <div className="thq-flex-column">
                <h3 className="thq-heading-3">{props.feature3Title}</h3>
                <span className="thq-body-small">
                  {props.feature3Description}
                </span>
              </div>
            </div>
            {/* Feature 4: Security */}
            <div className="features21-feature4 thq-flex-column">
              <img
                alt={props.feature4ImageAlt}
                src="/secure.jpg"
                className="thq-team-image-round"
              />
              <div className="thq-flex-column">
                <h3 className="thq-heading-3">{props.feature4Title}</h3>
                <span className="thq-body-small">
                  {props.feature4Description}
                </span>
              </div>
            </div>
            {/* Feature 5: Website Marketing */}
            <div className="features21-feature5 thq-flex-column">
              <img
                alt={props.feature5ImageAlt}
                src="/market.jpg"
                className="thq-team-image-round"
              />
              <div className="thq-flex-column">
                <h3 className="thq-heading-3">{props.feature5Title}</h3>
                <span className="thq-body-small">
                  {props.feature5Description}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

Features21.defaultProps = {
  sectionTitle: "Key Features",
  sectionDescription:
    "Explore the features that set us apart and help elevate your website's performance.",
  feature1Title: "User Interface (UI)",
  feature1Description:
    "Enhance your website's visual appeal and usability with intuitive designs, harmonious layouts, and responsive interfaces.",
  feature1ImageAlt: "User Interface Design",
  feature2Title: "User Experience (UX)",
  feature2Description:
    "Optimize the user journey with faster page load times, mobile responsiveness, and seamless interactions.",
  feature2ImageAlt: "User Experience Enhancement",
  feature3Title: "Search Engine Optimization (SEO)",
  feature3Description:
    "Boost visibility and organic traffic with keyword research, meta tag optimization, and trend analysis.",
  feature3ImageAlt: "SEO Strategies",
  feature4Title: "Website Security",
  feature4Description:
    "Ensure robust security with HTTPS, SSL certifications, and threat protection to safeguard user data.",
  feature4ImageAlt: "Website Security Measures",
  feature5Title: "Website Marketing",
  feature5Description:
    "Increase your reach with strategic ad placements, social media integration, and actionable marketing insights.",
  feature5ImageAlt: "Website Marketing Strategies",
};

Features21.propTypes = {
  sectionTitle: PropTypes.string,
  sectionDescription: PropTypes.string,
  feature1Title: PropTypes.string,
  feature1Description: PropTypes.string,
  feature1ImageAlt: PropTypes.string,
  feature2Title: PropTypes.string,
  feature2Description: PropTypes.string,
  feature2ImageAlt: PropTypes.string,
  feature3Title: PropTypes.string,
  feature3Description: PropTypes.string,
  feature3ImageAlt: PropTypes.string,
  feature4Title: PropTypes.string,
  feature4Description: PropTypes.string,
  feature4ImageAlt: PropTypes.string,
  feature5Title: PropTypes.string,
  feature5Description: PropTypes.string,
  feature5ImageAlt: PropTypes.string,
};

export default Features21;
