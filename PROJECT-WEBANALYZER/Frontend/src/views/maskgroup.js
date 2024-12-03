import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { Helmet } from 'react-helmet';
import axios from 'axios';
import DashboardCard from './DashboardCard';
import './newMaskgroup.css'; // Updated CSS file
import PieChart from './PieChart';

const Maskgroup = () => {
  const location = useLocation();
  const { data: initialData, feature, sub_feature, url } = location.state || {};
  const [data, setData] = useState(initialData || {}); // State for current report details
  const [reportsData, setReportsData] = useState([]); // State for recent reports
  const [popupDetail, setPopupDetail] = useState(''); // Popup content state

  useEffect(() => {
    // Fetching the recent reports
    const fetchReports = async () => {
      const user = JSON.parse(localStorage.getItem("user"));
      if (user) {
        try {
          const response = await axios.get(`http://localhost:8000/reports/${user.user_id}`);
          setReportsData(response.data);
        } catch (error) {
          console.error('Error fetching reports:', error);
        }
      }
    };
    fetchReports();
  }, []);

  // Handle report update when "View Report" is clicked
  const handleViewReport = async (reportId) => {
    try {
      const response = await axios.get(`http://localhost:8000/report/${reportId}`);
      console.log(response);
  
      // Update the state with the main report details
      setData({
        ...response.data,          // Include all report-level data
        ...response.data.data,     // Include the `data` field's contents
      });
    } catch (error) {
      console.error('Error fetching report details:', error);
      alert('Failed to load report details. Please try again.');
    }
  };
  

  // Handle popup for one-liner details
  const handleInfoClick = (details) => {
    setPopupDetail(details); // Show details in the popup
  };

  const handleClosePopup = () => {
    setPopupDetail(''); // Close popup
  };

  const pieChartData = data.results?.total_score 
    ? [data.results.total_score, 100 - data.results.total_score] 
    : [0, 100];
  
  const numericalData = data.results?.numerical_data || {};

  const cardsData = Object.keys(numericalData).map((key) => {
    const card = numericalData[key];
    return {
      title: card.title,
      value: card.value || 0,
      percentage: card.percentage || '', // If percentage data exists
      details: card.details || 'No additional details available', // Pass details here
      className: `maskgroup-dashboardcard`,
      arrowClass: card.percentage > 0 ? 'arrow-up' : 'arrow-down',
    };
  });

  const oneLinerData = data.results?.one_liner_data || [];

  const recentReports = reportsData
    .sort((a, b) => b.report_id - a.report_id)
    .slice(0, 5);

  return (
    <div className="container-group">
      <Helmet>
        <title>Web Analyzer Report</title>
      </Helmet>
      <h1>{data.feature || feature} - {data.sub_feature || sub_feature}</h1>
      <h2>Report for the {data.url || url}</h2>

      {/* Cards Section */}
      <div className="maskgroup-dashboard">
        {cardsData.slice(0, 8).map((card, index) => (
          <DashboardCard
            key={index}
            title={card.title}
            value={card.value}
            percentage={card.percentage}
            details={card.details}
            className={`maskgroup-card`}
          />
        ))}
      </div>

      {/* Lower Section with Chart and One-Liner Data */}
      <div className="maskgroup-lower-section">
        <div className="maskgroup-chart-container">
          <div className="chart-and-details">
            <div className="chart">
              <PieChart data={pieChartData} />
            </div>
            <div className="chart-details">
              <p>Here you can add some details about the chart...</p>
              <p>Additional information can go here.</p>
            </div>
          </div>
        </div>
        <div className="maskgroup-one-liner">
          {oneLinerData.map((line, index) => (
            <div className="one-liner-item" key={index}>
              <span className="one-liner-title">{line.title}</span>
              <img
                src="icons8-info-50.png"
                alt="Info"
                className="info-icon"
                onClick={() => handleInfoClick(line.details)} // Show popup on click
              />
            </div>
          ))}
        </div>
      </div>

      {/* Popup for One-Liner Details */}
      {popupDetail && (
        <div className="popup-container">
          <div className="popup-content">
            <button className="popup-close-button" onClick={handleClosePopup}>
              &times;
            </button>
            <p>{popupDetail}</p>
          </div>
        </div>
      )}

      {/* Recent Reports Section */}
      <div className="maskgroup-reports">
        {recentReports.map((report) => (
          <div className="report-item" key={report.report_id}>
            <div className="report-row">
              <span className="report-title">{`Report: ${report.report_id}`}</span>
              <span className="report-url">{`Report for the ${report.url}`}</span>
              <span className="report-date">
                {`Date: ${new Date(report.date).toLocaleDateString('en-GB', {
                  day: 'numeric',
                  month: 'long',
                  year: 'numeric',
                })}`}
              </span>
            </div>
            <div className="report-row">
              <span className="report-feature">{`Feature: ${report.feature}`}</span>
              <span className="report-subfeature">{`Sub-Feature: ${report.sub_feature}`}</span>
              <button
                className="view-report-button"
                onClick={() => handleViewReport(report.report_id)} // Fetch and update report details
              >
                View Report
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Maskgroup;
