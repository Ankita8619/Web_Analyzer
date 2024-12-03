import React from "react";
import PropTypes from "prop-types";
import "./stats8.css";

const Stats8 = ({ data }) => {
  if (!data) {
    return <div>Loading...</div>;
  }

  // Ensure there are always 4 importance details
  const paddedImportanceDetails = [...data.importanceDetails];
  while (paddedImportanceDetails.length < 4) {
    paddedImportanceDetails.push("Additional importance detail to fill space.");
  }

  return (
    <div id="slider" className="slider thq-section-padding">
      {/* Main Feature Heading */}
      <div className="stats8-max-width1 thq-section-max-width">
        <div className="stats8-container2">
          <h2 className="thq-heading-1 stats8-title">{data.featureName}</h2>
        </div>

        {/* Importance Details in 4 Boxes */}
        <div className="stats8-container3 thq-grid-4">
          {paddedImportanceDetails.slice(0, 4).map((detail, index) => (
            <div
              key={index}
              className={`stats8-container${index + 4} thq-card thq-box-shadow`}
            >
              <h2 className="thq-heading-2">Key Detail {index + 1}</h2>
              <p className="stats8-text12 thq-body-large">{detail}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Learn the Parameters Section */}
      <div className="stats8-max-width2 thq-section-max-width">
        <div className="thq-card thq-flex-column">
          <h1 className="thq-heading-1 stats8-text22">
            Learn the parameters used by us.
          </h1>
          <div className="thq-divider-horizontal"></div>
          <span className="stats8-text23 thq-body-small">
            Discover how our services can boost your website performance and
            drive results.
          </span>
        </div>
      </div>

      {/* Parameters Section */}
      <div className="stats8-max-width3 thq-section-max-width">
        <h2 className="thq-heading-2 stats8-title">Parameters</h2>
        <div className="stats8-container-parameters">
          {data.parameters.map((param, index) => (
            <div
              key={index}
              className="stats8-parameter-card thq-card thq-box-shadow"
            >
              <h3 className="thq-heading-3">{param.name}</h3>
              <p className="thq-body-small">
                <strong>Importance:</strong> {param.importance}
              </p>
              <p className="thq-body-small">
                <strong>Effectiveness:</strong> {param.effectiveness}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

Stats8.propTypes = {
  data: PropTypes.shape({
    featureName: PropTypes.string,
    importanceDetails: PropTypes.arrayOf(PropTypes.string),
    parameters: PropTypes.arrayOf(
      PropTypes.shape({
        name: PropTypes.string,
        importance: PropTypes.string,
        effectiveness: PropTypes.string,
      })
    ),
  }),
};

export default Stats8;
