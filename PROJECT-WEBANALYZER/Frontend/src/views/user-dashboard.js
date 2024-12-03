import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Helmet } from "react-helmet";
import axios from "axios";
import "./user-dashboard.css";

const UserDashboard = () => {
  const [userData, setUserData] = useState(null);
  const [userReports, setUserReports] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const user = JSON.parse(localStorage.getItem("user"));
        if (!user) {
          navigate("/login");
          return;
        }

        // Fetch user data
        const userResponse = await axios.get(`http://localhost:8000/users/${user.user_id}`);
        setUserData(userResponse.data);

        // Fetch user reports
        try {
          const reportsResponse = await axios.get(`http://localhost:8000/reports/${user.user_id}`);
          setUserReports(reportsResponse.data);
        } catch (reportError) {
          if (reportError.response && reportError.response.status === 404) {
            console.warn("No reports found for this user.");
            setUserReports([]); // Ensure the state is empty if no reports are found
          } else {
            throw reportError; // Re-throw error for other cases
          }
        }
      } catch (error) {
        console.error("Error fetching data:", error);
        navigate("/login");
      }
    };

    fetchUserData();
  }, [navigate]);

  if (!userData) {
    return <div>Loading...</div>;
  }

  const userImageSrc = userData.image ? `http://localhost:8000${userData.image}` : null;

  return (
    <div className="dashboard-container">
      <Helmet>
        <title>User Dashboard</title>
      </Helmet>
      <div className="overview-title">
        <h2>Overview</h2>
        <div className="underline"></div>
      </div>
      <div className="dashboard-content">
        {/* Left Section */}
        <div className="left-section">
          <h3>Details</h3>
          <div className="tabs">
            <span>Analytics</span>
            <span>Insights</span>
            <span>Upgrade Plan</span>
            <span>Update Profile</span>
          </div>
          <div className="description">
            <p>{userData.sub_details}</p>
            <p>{userData.user_details}</p>
          </div>
          <div className="stats">
            <div className="stat-box purple-box">
              <h3>{userReports.length}</h3>
              <p>Reports Generated</p>
            </div>
            <div className="stat-box">
              <h3>10</h3>
              <p>Features Explored</p>
            </div>
            <div className="stat-box">
              <h3>{userData.days_left}</h3>
              <p>Days Left</p>
            </div>
          </div>
        </div>
        {/* Right Section */}
        <div className="right-section">
          <div className="user-info">
            {userImageSrc ? (
              <img
                src={userImageSrc}
                alt="User Profile"
                className="avatar"
              />
            ) : (
              <div className="avatar-placeholder"></div>
            )}
            <h3>{userData.username}</h3>
            <p>{userData.profession}</p>
          </div>
          {userReports.length > 0 && (
            <div className="activities">
              <h4>Last Activities</h4>
              {userReports
                .slice(-3) // Get the last three reports
                .reverse() // Reverse to show the most recent first
                .map((report, index) => (
                  <div key={index} className="activity-box">
                    <p>Generated report of: {report.feature}</p>
                    <p>Date: {new Date(report.date).toLocaleString()}</p>
                  </div>
                ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UserDashboard;
