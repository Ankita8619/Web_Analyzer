import React, { useState, useEffect, useContext } from 'react';
import './Webanalyzer.css';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../components/authContext'; // Import AuthContext

const DynamicForm = () => {
  const [url, setUrl] = useState('');
  const [firstOption, setFirstOption] = useState('');
  const [secondOptions, setSecondOptions] = useState([]);
  const [secondOption, setSecondOption] = useState('');
  const { isLoggedIn } = useContext(AuthContext); // Use context for authentication
  const navigate = useNavigate();

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!isLoggedIn) {
      navigate('/login');
    }
  }, [isLoggedIn, navigate]);

  // Update sub-options based on the selected feature
  const handleFirstOptionChange = (e) => {
    const selectedOption = e.target.value;
    setFirstOption(selectedOption);
    switch (selectedOption) {
      case 'User Interface':
        setSecondOptions(['Color Grading', 'Content Style', 'Element Layout']);
        break;
      case 'User Experience':
        setSecondOptions(['WebPage Performance', 'WebPage Quality']);
        break;
      case 'Website Security':
        setSecondOptions(['Security and Policy', 'Threats Mitigation']);
        break;
      case 'SEO':
        setSecondOptions(['Website Ranking', 'SEO Grading', 'Competitor Analysis', 'Keyword Tracking', 'Trend Analysis']);
        break;
      case 'Website Advertisement':
        setSecondOptions(['Ads Recommendation', 'Ads Positioning']);
        break;
      default:
        setSecondOptions([]);
    }
  };

  // Analyze website styles for the "Content Style" sub-feature
  const analyzeWebsiteStyles = () => {
    return new Promise((resolve, reject) => {
      try {
        const consistencyReport = (() => {
          function checkAlignmentCounts(selector) {
            const elements = document.querySelectorAll(selector);
            const alignmentCounts = { total: elements.length, left: 0, center: 0, right: 0 };
  
            elements.forEach(element => {
              const styles = window.getComputedStyle(element);
              const textAlign = styles.textAlign;
  
              if (textAlign === 'left' || textAlign === 'start') {
                alignmentCounts.left += 1;
              } else if (textAlign === 'center') {
                alignmentCounts.center += 1;
              } else if (textAlign === 'right' || textAlign === 'end') {
                alignmentCounts.right += 1;
              }
            });
  
            return alignmentCounts;
          }
  
          function checkFlexboxConsistency(selector) {
            const elements = document.querySelectorAll(selector);
            const flexboxCounts = { total: elements.length, matching: 0 };
            const flexboxValues = new Set();
  
            elements.forEach(element => {
              const styles = window.getComputedStyle(element);
              const justifyContent = styles.justifyContent;
              const alignItems = styles.alignItems;
  
              if (styles.display === 'flex') {
                flexboxValues.add(`${justifyContent}-${alignItems}`);
              }
            });
  
            flexboxCounts.matching = elements.length === flexboxValues.size ? elements.length : 0;
  
            return flexboxCounts;
          }
  
          function checkSpacingConsistency(selector) {
            const elements = document.querySelectorAll(selector);
            const spacingCounts = { total: elements.length, matching: 0 };
            const spacingValues = new Set();
  
            elements.forEach(element => {
              const styles = window.getComputedStyle(element);
              const margin = `${styles.marginTop}-${styles.marginRight}-${styles.marginBottom}-${styles.marginLeft}`;
              const padding = `${styles.paddingTop}-${styles.paddingRight}-${styles.paddingBottom}-${styles.paddingLeft}`;
  
              spacingValues.add(`${margin}-${padding}`);
            });
  
            spacingCounts.matching = spacingValues.size === 1 ? elements.length : 0;
  
            return spacingCounts;
          }
  
          const selectors = {
            headers: 'h1, h2, h3, h4, h5, h6',
            paragraphs: 'p',
            images: 'img',
            containers: 'div, section, article',
            lists: 'ul, ol, li',
            navigation: 'nav, ul, li'
          };
  
          const report = {};
  
          for (const [key, selector] of Object.entries(selectors)) {
            report[key] = {
              alignment: checkAlignmentCounts(selector),
              flexbox: checkFlexboxConsistency(selector),
              spacing: checkSpacingConsistency(selector)
            };
          }
          return report;
        })();
        
        resolve(consistencyReport);
      } catch (error) {
        console.error('Error in analyzing website styles:', error);
        reject(error);
      }
    });
  };
  
  function calculateTotalScore(report) {
    let totalScore = 0;
    let sectionCount = 0;
  
    for (const elementKey in report) {
      const element = report[elementKey];
      for (const sectionKey in element) {
        const section = element[sectionKey];
        const total = section.total || 0;
        const matching = section.matching || 0;
  
        // Add score for this section
        const score = total === 0 ? 100 : (matching * 100) / total;
        totalScore += score;
        sectionCount++;
      }
    }
  
    // Normalize score
    const normalizedScore = totalScore / sectionCount;
    return normalizedScore;
  }
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const scrapeResponse = await axios.post("http://localhost:8000/scrape", {
        url,
        feature: firstOption,
        sub_feature: secondOption,
      });
      let styleAnalysis = null;
      let postRequests = [];
      switch (secondOption) {
        case "Color Grading":
          postRequests.push(
            axios.post("http://localhost:8000/color_grading", { url })
          );
          break;
        case "Content Style":
          styleAnalysis = await analyzeWebsiteStyles();
          console.log(styleAnalysis)
          console.log(styleAnalysis.headers)
          postRequests.push(
            axios.post("http://localhost:8000/content_style", { url })
          );
          break;
        case "Element Layout":
          postRequests.push(
            axios.post("http://localhost:8000/responsive", { url })
          );
          break;
        case "WebPage Performance":
          postRequests.push(
            axios.post("http://localhost:8000/webpage_performance", { url })
          );
          break;
        case "SEO Grading":
          postRequests.push(
            axios.post("http://localhost:8000/seo_grading", { url })
          );
          break;
        case "Security and Policy":
          postRequests.push(
            axios.post("http://localhost:8000/web_security_analysis", { url })
          );
          break;
        case "Ads Recommendation":
          postRequests.push(
            axios.post("http://localhost:8000/ads_recommendation", { url })
          );
          break;
        default:
          postRequests.push(scrapeResponse);
      }
  
      const responses = await Promise.all(postRequests);
      const combinedData = responses.reduce(
        (acc, response) => ({ ...acc, ...response.data }),
        {}
      );
  
      const finalData = secondOption === "Content Style"
          ? {
            results: {
              ...(styleAnalysis || {}),
              total_score : calculateTotalScore(styleAnalysis),
              numerical_data : {
                total_header_alignment: { title: "Total Header Alignment", value: styleAnalysis.headers.alignment.total || 0 },
                total_paragraph_alignment: { title: "Total Paragraph Alignment", value: styleAnalysis.paragraphs.alignment.total || 0 },
                total_image_alignment: { title: "Total Image Alignment", value: styleAnalysis.images.alignment.total || 0 },
                total_container_alignment: { title: "Total Container Alignment", value: styleAnalysis.containers.alignment.total || 0 },
                total_navigation_alignment: { title: "Total Navigation Alignment", value: styleAnalysis.navigation.alignment.total || 0 },
                matching_header_spacing: { title: "Matching Header Spacing", value: styleAnalysis.headers.spacing.matching || 0 },
                matching_image_spacing: { title: "Matching Image Spacing", value: styleAnalysis.images.spacing.matching || 0 },
                matching_container_flexbox: { title: "Matching Container Flexbox", value: styleAnalysis.containers.flexbox.matching || 0 },
              },
              one_liner_data : [
                { title: "Header Alignment", details: "Header elements are crucial for clear hierarchy and readability." },
                { title: "Paragraph Alignment", details: "Aligned paragraphs ensure content is easy to read." },
                { title: "Image Placement", details: "Image alignment plays a significant role in visual flow." },
                { title: "Container Design", details: "Well-aligned containers improve layout consistency." },
                { title: "Navigation Structure", details: "Aligned navigation items enhance usability." },
                { title: "Spacing Precision", details: "Proper spacing ensures visual appeal and clarity." },
              ],
            },
            }
          : combinedData;
  
      const user = JSON.parse(localStorage.getItem("user"));
      const reportData = {
        user_id: user.user_id,
        feature: firstOption,
        sub_feature: secondOption,
        data: finalData,
        url: url,
      };
  
      await axios.post("http://localhost:8000/save_report", reportData);
  
      navigate("/report", {
        state: { data: finalData, feature: firstOption, sub_feature: secondOption, url },
      });
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  };
  
  return (
    <div className="outer-container" style={{
      backgroundImage: `url(${process.env.PUBLIC_URL + '/leafs-3898442_1920.jpg'})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
      width: '100%',
      height: '100%', // Ensure the background covers the entire container
    }}>
      <div className="dynamic-form-container" style={{
      backgroundImage: `url(${process.env.PUBLIC_URL + '/black-1072366_1920.jpg'})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
      width: '100%',
      height: '100%', // Ensure the background covers the entire container
    }}>
        <h3 className="form-heading">Webanalyzer</h3>
        <form onSubmit={handleSubmit} className="form">
          <div className="form-field">
            <p className="instruction">Start analyzing your website</p>
          </div>

          <div className="form-field">
            <label>URL:</label>
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              required
            />
          </div>

          <div className="form-field">
            <label>First Option:</label>
            <select
              value={firstOption}
              onChange={handleFirstOptionChange}
              required
            >
              <option value="">Select an option</option>
              <option value="User Interface">User Interface</option>
              <option value="User Experience">User Experience</option>
              <option value="Website Security">Website Security</option>
              <option value="SEO">SEO</option>
              <option value="Website Advertisement">Website Advertisement</option>
            </select>
          </div>

          {firstOption && (
            <div className="form-field">
              <label>Second Option:</label>
              <select
                value={secondOption}
                onChange={(e) => setSecondOption(e.target.value)}
                required
              >
                <option value="">Select an option</option>
                {secondOptions.map((option, index) => (
                  <option key={index} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </div>
          )}

          <button type="submit" className="submit-button">
            Generate Report
          </button>
        </form>
      </div>
    </div>
  );
};

export default DynamicForm;
