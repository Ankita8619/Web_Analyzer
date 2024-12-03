import React, { useState, useEffect } from "react";
import { Helmet } from "react-helmet";

import Stats8 from "../components/stats8";
import FAQ11 from "../components/faq11";
import Footer from "../components/footer";
import "./learn.css";

const Learn = () => {
  const [features, setFeatures] = useState([]);
  const [selectedFeature, setSelectedFeature] = useState(null);

  useEffect(() => {
    // Fetch the features.json file
    fetch(`${process.env.PUBLIC_URL}/features.json`)
      .then((response) => response.json())
      .then((jsonData) => {
        setFeatures(jsonData);
        if (jsonData.length > 0) {
          setSelectedFeature(jsonData[0]); // Default to the first feature
        }
      })
      .catch((error) => console.error("Error fetching features.json:", error));
  }, []);

  const handleFeatureClick = (feature) => {
    setSelectedFeature(feature);

    // Scroll to the top of the page
    window.scrollTo({
      top: 0, // Position to scroll to (top of the page)
      behavior: "smooth", // Smooth scrolling effect
    });
  };

  return (
    <div className="learn-container">
      <Helmet>
        <title>Learn - WebAnalyzer</title>
        <meta property="og:title" content="Learn - WebAnalyzer" />
      </Helmet>

      {/* Display the selected feature's stats */}
      {selectedFeature && <Stats8 data={selectedFeature}></Stats8>}

      {/* Feature Selection Buttons */}
      <div className="learn-feature-buttons">
        {features.map((feature, index) => (
          <button
            key={index}
            className="learn-feature-button"
            onClick={() => handleFeatureClick(feature)}
          >
            {feature.featureName}
          </button>
        ))}
      </div>

      <FAQ11></FAQ11>
      <Footer></Footer>
    </div>
  );
};

export default Learn;
