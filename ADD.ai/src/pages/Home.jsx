import React, { useEffect, useState } from "react";
import appwriteService from "../appwrite/config";
import { Container, PostCard } from "../components";
import { Typography, Box, Grid } from "@mui/material";

function Home() {
  const [posts, setPosts] = useState([]);

  // Define your colors
  const background = "linear-gradient(to right, #FFFFFF, #FFB6C1, #FFD7C4)";
  const cardGradient = "linear-gradient(135deg, #FFD7C4, #C4D7FF)";
  const textColor = "#FFFFFF"; // White text color
  const cardTextColor = "#1C1C1E"; // Dark text color for better contrast

  useEffect(() => {
    appwriteService.getPosts().then((posts) => {
      if (posts) {
        setPosts(posts.documents);
      }
    });
  }, []);

  if (posts.length === 0) {
    return (
      <Box
        sx={{
          width: "100%",
          py: 4,
          mt: 2,
          textAlign: "center",
          bgcolor: background,
        }}
      >
        <Container>
          <Box>
            <Typography variant="h5" fontWeight="bold" color={textColor}>
              Login to read posts
            </Typography>
          </Box>
        </Container>
      </Box>
    );
  }

  return (
    <Box sx={{ width: "100%", py: 4, bgcolor: background }}>
      <Container>
        <Grid container spacing={3}>
          {posts.map((post) => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={post.$id}>
              <PostCard
                {...post}
                sx={{
                  bgcolor: cardGradient, // Gradient background for post cards
                  border: `1px solid #FFD7C4`, // Light peach border for better visibility
                  color: cardTextColor, // Dark text color for cards
                  borderRadius: "8px", // Slightly rounded corners
                  padding: "16px", // Add some padding
                  transition: "transform 0.3s",
                  "&:hover": {
                    transform: "scale(1.05)", // Scale effect on hover
                    boxShadow: `0 8px 40px rgba(0, 0, 0, 0.7)`, // Increased shadow on hover
                  },
                }}
              />
            </Grid>
          ))}
        </Grid>
      </Container>  
    </Box>
  );
}

export default Home;
