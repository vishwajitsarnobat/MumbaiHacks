import React from "react";
import { Box, Typography, Button, Divider } from "@mui/material";
import VisibilityIcon from "@mui/icons-material/Visibility";
import { Link } from "react-router-dom"; // Import Link from react-router-dom

function CampaignCard({ campaign }) {
  return (
    <Link
      to={`/show-campaign-details/${campaign.id}`} // Use the campaign's ID for dynamic routing
      style={{ textDecoration: "none", width: "100%", margin: "10px 50px" }} // Remove default link styling and set width to 100%
    >
      <Box
        sx={{
          backgroundColor: "#FFFFFF", // White background
          color: "black", // Black text
          borderRadius: "10px",
          border: "2px solid #000", // Black border
          padding: "20px", // Increased padding for a spacious feel
          width: "100%", // Ensure the Box takes full width
          margin: "10px", // Use vertical margin to avoid left-right margin issues
          display: "flex",
          flexDirection: "column",
          boxShadow: 2, // Added shadow for depth
          transition: "transform 0.2s", // Transition for hover effect
          "&:hover": {
            transform: "scale(1.02)", // Slight zoom on hover
            boxShadow: 4, // Enhanced shadow on hover
          },
        }}
      >
        {/* Campaign Title */}
        <Typography variant="h6" fontWeight="bold" noWrap sx={{ mb: 1 }}>
          {campaign.name} {/* Assume campaign has a name */}
        </Typography>
        <Divider sx={{ my: 1, borderColor: "#4A4A4A" }} /> {/* Divider color */}
        {/* Campaign Type and Languages */}
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            mt: 1,
          }}
        >
          <Typography variant="body2" color="#A9A9A9">
            Type: {campaign.campaignType}{" "}
            {/* Assume campaign has a campaignType */}
          </Typography>
          <Typography variant="body2" color="#A9A9A9">
            Languages:{" "}
            {Array.isArray(campaign.languages)
              ? campaign.languages.join(", ") // Safely join languages
              : "N/A"}{" "}
            {/* Fallback in case languages isn't an array */}
          </Typography>
        </Box>
        {/* Analytics Button */}
        <Box
          sx={{
            display: "flex",
            justifyContent: "flex-end", // Align button to the right
            mt: 2, // Add top margin for spacing
          }}
        >
          <Button
            variant="contained"
            startIcon={<VisibilityIcon />}
            sx={{
              backgroundColor: "black", // Light peach background
              color: "#FFFFF", // Dark text
              fontWeight: "bold",
              ":hover": {
                backgroundColor: "grey", // Lighter peach on hover
                boxShadow: 2, // Added shadow on hover
              },
              padding: "10px 16px", // Adjusted padding
              borderRadius: "20px", // Rounded edges
            }}
          >
            View Analytics
          </Button>
        </Box>
      </Box>
    </Link>
  );
}

export default CampaignCard;
