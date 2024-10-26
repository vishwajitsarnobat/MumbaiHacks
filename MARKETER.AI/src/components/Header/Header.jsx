import { Container, LogoutBtn } from "../index";
import React from "react";
import {
  AppBar,
  Toolbar,
  Button,
  Box,
  Typography,
  Avatar,
} from "@mui/material";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import userImage from "../../assets/userimage.jpeg"; // Import user image

function Header() {
  const authStatus = useSelector((state) => state.auth.status);
  const userData = useSelector((state) => state.auth.userData); // Access user data from Redux
  const navigate = useNavigate();

  return (
    <AppBar
      position="static"
      sx={{
        background: "#FFFFFF", // White background for AppBar
        boxShadow: "none",
      }}
    >
      <Toolbar>
        {authStatus && (
          <Box display="flex" alignItems="center" sx={{ mr: 2 }}>
            <Avatar
              src={userImage}
              alt="User"
              sx={{
                width: 50, // Increase width
                height: 50, // Increase height
                mr: 1,
                border: "2px solid black", // Border width and color
              }}
            />
            <Typography
              variant="h6" // Adjust typography to h6 for a larger font
              sx={{
                color: "black",
                fontWeight: "bold",
                fontSize: "1.5rem", // Larger font size
                marginLeft: "10px",
              }}
            >
              {userData?.name || "User"} {/* Display username */}
            </Typography>
          </Box>
        )}
        <Box sx={{ flexGrow: 1 }} /> {/* Spacer to push items to the right */}
        {authStatus && (
          <>
            <Button
              onClick={() => navigate("/profile")}
              sx={{
                mx: 1,
                backgroundColor: "black",
                color: "#FFFFFF",
                borderRadius: "20px",
                fontWeight: "bold",
                fontSize: 16,
                textTransform: "none",
                width: "105px",
                transition: "background-color 0.2s ease",
                ":hover": {
                  backgroundColor: "#B0B3B8",
                },
              }}
            >
              Profile
            </Button>
            <LogoutBtn />
          </>
        )}
      </Toolbar>
    </AppBar>
  );
}

export default Header;
