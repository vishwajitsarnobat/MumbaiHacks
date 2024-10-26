import React, { useState, useEffect } from "react";
import { useDispatch } from "react-redux";
import {
  CssBaseline,
  Box,
  AppBar,
  Toolbar,
  Container,
  CircularProgress,
  Typography,
} from "@mui/material";
import authService from "./appwrite/auth";
import { login, logout } from "./store/authSlice";
import { Footer, Header } from "./components";
import { Outlet } from "react-router-dom";

function App() {
  const [loading, setLoading] = useState(true);
  const dispatch = useDispatch();

  useEffect(() => {
    authService
      .getCurrentUser()
      .then((userData) => {
        if (userData) {
          dispatch(login({ userData }));
        } else {
          dispatch(logout());
        }
      })
      .finally(() => setLoading(false));
  }, [dispatch]);

  return (
    <>
      <CssBaseline />
      {!loading ? (
        <Box
          sx={{
            minHeight: "100vh",
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            background: "#020617", // Dark gradient
          }}
        >
       

          <Outlet />

          <AppBar
            position="static"
            color="transparent"
            sx={{
              bgcolor: "#2C2C2E", // Dark gray footer background
            }}
          ></AppBar>
        </Box>
      ) : (
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            minHeight: "100vh",
            background: "linear-gradient(to right, #1A1A2E, #33354A)", // Same dark gradient during loading
          }}
        >
          <CircularProgress sx={{ color: "#00A8E1", mb: 2 }} />{" "}
          {/* Sky blue for the loading spinner */}
          <Typography variant="h6" color="#F1F1F1">
            Loading, please wait...
          </Typography>
        </Box>
      )}
    </>
  );
}

export default App;
