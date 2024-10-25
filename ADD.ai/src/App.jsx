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
            background: "linear-gradient(to right, #FFFFFF, #FFB6C1, #FFD7C4)", // Gradient from white to light pink to soft peach
          }}
        >
          <Header />
          <Container component="main" sx={{ flex: 1, py: 3, color: "#FFFFFF" }}>
            <Outlet />
          </Container>
          <AppBar
            position="static"
            color="transparent"
            sx={{ bgcolor: "#2C2C2E" }}
          >
            <Footer />
          </AppBar>
        </Box>
      ) : (
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            minHeight: "100vh",
            background: "linear-gradient(to right, #FFFFFF, #FFB6C1, #FFD7C4)", // Same gradient during loading
          }}
        >
          <CircularProgress sx={{ color: "#003366", mb: 2 }} />
          <Typography variant="h6" color="#FFFFFF">
            Loading, please wait...
          </Typography>
        </Box>
      )}
    </>
  );
}

export default App;
