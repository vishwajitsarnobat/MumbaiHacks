import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";

function PublishedSuccessfully() {
  const navigate = useNavigate();

  useEffect(() => {
    // Navigate to the home page after 3 seconds
    const timer = setTimeout(() => {
      navigate("/"); // Adjust the path based on your routing setup
    }, 3000);

    // Cleanup the timer on component unmount
    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>Published Successfully!</h1>
      <p style={styles.message}>
        Your campaign has been published. You will be redirected to the home
        page shortly.
      </p>
    </div>
  );
}

// Styles for the component
const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
    backgroundColor: "#f9f9f9", // Background color
    textAlign: "center",
  },
  heading: {
    color: "#00A8E1", // Accent color
  },
  message: {
    color: "#333", // Dark text for contrast
  },
};

export default PublishedSuccessfully;
