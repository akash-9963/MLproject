import React, { useState } from "react";
import "./App.css";
function App() {
  const [formData, setFormData] = useState({
    nitrogen: "",
    phosphorus: "",
    potassium: "",
    temperature: "",
    humidity: "",
    ph: "",
    rainfall: "",
  });
  const [recommendedCrop, setRecommendedCrop] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false); // Add loading state

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Check if any field is empty
    if (Object.values(formData).includes("")) {
      setError("Please fill in all fields!");
      return;
    }

    setLoading(true); // Set loading to true before sending the request
    setError(""); // Clear any previous error

    try {
      // Sending form data to backend for crop recommendation
      const response = await fetch("http://localhost:5000/api/recommend_crop", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (data.recommended_crop) { // Correct field name from backend
        setRecommendedCrop(data.recommended_crop); // Update recommended crop
      } else {
        setError("Something went wrong. Please try again.");
      }
    } catch (err) {
      setError("Error: " + err.message);
    } finally {
      setLoading(false); // Set loading to false after the request completes
    }
  };

  return (
    <div className="App">
      <h1>Crop Recommendation System</h1>
      <form onSubmit={handleSubmit} className="form">
        <div className="input-group">
          <label>Nitrogen (N):</label>
          <input
            type="number"
            name="nitrogen"
            value={formData.nitrogen}
            onChange={handleChange}
          />
        </div>
        <div className="input-group">
          <label>Phosphorus (P):</label>
          <input
            type="number"
            name="phosphorus"
            value={formData.phosphorus}
            onChange={handleChange}
          />
        </div>
        <div className="input-group">
          <label>Potassium (K):</label>
          <input
            type="number"
            name="potassium"
            value={formData.potassium}
            onChange={handleChange}
          />
        </div>
        <div className="input-group">
          <label>Temperature (°C):</label>
          <input
            type="number"
            name="temperature"
            value={formData.temperature}
            onChange={handleChange}
          />
        </div>
        <div className="input-group">
          <label>Humidity (%):</label>
          <input
            type="number"
            name="humidity"
            value={formData.humidity}
            onChange={handleChange}
          />
        </div>
        <div className="input-group">
          <label>pH Level:</label>
          <input
            type="number"
            name="ph"
            value={formData.ph}
            onChange={handleChange}
          />
        </div>
        <div className="input-group">
          <label>Rainfall (mm):</label>
          <input
            type="number"
            name="rainfall"
            value={formData.rainfall}
            onChange={handleChange}
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Loading..." : "Get Recommended Crop"}
        </button>
      </form>

      {error && <div className="error">{error}</div>}
      {recommendedCrop && (
        <div className="result">
          <h2>Recommended Crop: {recommendedCrop}</h2>
          <div className="crop-logo">
            {recommendedCrop === "Wheat" && <img src={wheatLogo} alt="Wheat Logo" />}
            {recommendedCrop === "Rice" && <img src={riceLogo} alt="Rice Logo" />}
            {/* Add more crop logos as necessary */}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
