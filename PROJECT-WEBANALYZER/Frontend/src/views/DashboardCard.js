import React, { useState } from 'react';
import './Dashboardcard.css';

const DashboardCard = ({ title, value, percentage, details, className, arrowClass }) => {
  const [isFlipped, setIsFlipped] = useState(false);

  return (
    <div
      className={`flip-card ${className}`} // This is now the outermost container
      onMouseEnter={() => setIsFlipped(true)}
      onMouseLeave={() => setIsFlipped(false)}
    >
      <div className={`flip-card-inner ${isFlipped ? 'flipped' : ''}`}>
        {/* Front Side */}
        <div className="flip-card-front">
          <div className="dashboard-card-content">
            <div className="card-title">
              <span className="maskgroup-text145 BodyTextInter16Medium">
                <span>{title}</span>
              </span>
            </div>
            <div className="card-value">
              <span className="maskgroup-text147">
                <span>{value}</span>
              </span>
              <div className="maskgroup-badge-tag10">
                <span className="maskgroup-text149">
                  <span>{percentage}</span>
                </span>
                <span className={arrowClass}></span>
              </div>
            </div>
          </div>
        </div>

        {/* Back Side */}
        <div className="flip-card-back">
          <p>{details}</p>
        </div>
      </div>
    </div>
  );
};

export default DashboardCard;
