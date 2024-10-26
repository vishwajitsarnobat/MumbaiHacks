import React from "react";
import logoImage from "../assets/logo.png"; // Adjust this path to where your logo.png is located

function Logo({ width = "100px" }) {
  return (
    <div
      style={{
        width,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <img
        src={logoImage}
        alt="Logo"
        style={{
          width: "100%", // Use full width of the container
          height: "auto", // Maintain aspect ratio
          borderRadius: "100%", // Optional: add rounded corners
          margin: 10,
        }}
      />
    </div>
  );
}

export default Logo;
