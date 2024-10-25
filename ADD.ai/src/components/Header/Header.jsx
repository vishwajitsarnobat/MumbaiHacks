import { Container, Logo, LogoutBtn } from "../index";
import React from "react";
import { AppBar, Toolbar, Button, Box } from "@mui/material";
import { useSelector } from "react-redux";
import { useNavigate, Link } from "react-router-dom";

function Header() {
  const authStatus = useSelector((state) => state.auth.status);
  const navigate = useNavigate();

  const navItems = [
    { name: "Home", slug: "/", active: true },
    { name: "Login", slug: "/login", active: !authStatus },
    { name: "Signup", slug: "/signup", active: !authStatus },
    { name: "All Posts", slug: "/all-posts", active: authStatus },
    { name: "Add Post", slug: "/add-post", active: authStatus },
  ];

  return (
    <AppBar
      position="static"
      sx={{
        background: "linear-gradient(to right, #C4D7FF, #FFD7C4)", // Gradient for the AppBar
        boxShadow: "none",
      }}
    >
      <Container>
        <Toolbar>
          <Box sx={{ display: "flex", alignItems: "center", mr: 4 }}>
            <Link to="/">
              <Logo width="70px" />
            </Link>
          </Box>
          <Box
            sx={{ flexGrow: 1, display: "flex", justifyContent: "flex-end" }}
          >
            {navItems.map(
              (item) =>
                item.active && (
                  <Button
                    key={item.name}
                    onClick={() => navigate(item.slug)}
                    sx={{
                      mx: 1,
                      color: "#1C1C1E", // Dark text for contrast
                      backgroundColor: "#FFF4B5", // Light yellow color for buttons
                      ":hover": { backgroundColor: "#FFD7C4" }, // Light peach on hover
                      borderRadius: "20px",
                      fontWeight: "bold",
                      textTransform: "none",
                    }}
                  >
                    {item.name}
                  </Button>
                )
            )}
            {authStatus && (
              <Box ml={2}>
                <LogoutBtn />
              </Box>
            )}
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
}

export default Header;
