import React, { useEffect, useState } from "react";
import { Box, List, ListItem, Typography, Grid, Button } from "@mui/material";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import Login from "../components/Login";
import CampaignCard from "../components/CompaingCard";
import { Header } from "../components";
import { Query } from "appwrite";

import conf from "../conf/conf";
import service from "../appwrite/config";

function Home() {
  const authStatus = useSelector((state) => state.auth.status);
  const userData = useSelector((state) => state.auth.userData);
  const navigate = useNavigate();
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);

  // Typing effect state for the second line
  const [typedText, setTypedText] = useState("");
  const fullText =
    "Transform your campaigns with AI that understands India's diversity";

  useEffect(() => {
    let currentIndex = 0;
    const typingInterval = setInterval(() => {
      if (currentIndex < fullText.length) {
        setTypedText((prev) => prev + fullText[currentIndex]);
        currentIndex++;
      } else {
        clearInterval(typingInterval);
      }
    }, 100);

    return () => clearInterval(typingInterval);
  }, []);

  // Fetch user's campaigns
  useEffect(() => {
    const fetchCampaigns = async () => {
      if (authStatus && userData) {
        try {
          const response = await service.databases.listDocuments(
            conf.appwriteDatabaseId,
            conf.appwriteCampaignCollectionId,
            [Query.equal("userId", userData.$id)]
          );

          // Transform the database documents into the campaign format expected by CampaignCard
          const formattedCampaigns = response.documents.map((doc) => ({
            id: doc.$id,
            name: doc.title,
            status: "Active", // You might want to add a status field to your database schema
            budget: doc.budget,
            // If you don't have these fields in your database, you could either add them
            // or use placeholder values
            impressions: 0,
            clicks: 0,
            ...doc,
          }));

          setCampaigns(formattedCampaigns);
        } catch (error) {
          console.error("Error fetching campaigns:", error);
        } finally {
          setLoading(false);
        }
      }
    };

    fetchCampaigns();
  }, [authStatus, userData]);

  if (!authStatus) {
    return (
      <Box
        sx={{
          width: "100%",
          minHeight: "100vh",
          display: "flex",
          bgcolor: "#ffffff",
          color: "#000000",
        }}
      >
        <Grid container sx={{ height: "100vh" }}>
          <Grid item xs={12} md={6}>
            <Box
              sx={{
                height: "100%",
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                padding: 6,
                bgcolor: "#ffffff",
              }}
            >
              <Typography
                variant="h2"
                sx={{
                  fontWeight: "bold",
                  color: "#000000",
                  marginBottom: 2,
                  fontSize: { xs: "1.5rem", md: "2.5rem" },
                }}
              >
                AI-Powered Marketing
                <br />
                for India
              </Typography>

              <Typography
                variant="h5"
                sx={{
                  color: "#18181b",
                  marginBottom: 6,
                  lineHeight: 1.6,
                }}
              >
                {typedText}
              </Typography>

              <Grid container spacing={4}>
                {/* Other content omitted for brevity */}
              </Grid>
            </Box>
          </Grid>

          <Grid
            item
            xs={12}
            md={6}
            display="flex"
            justifyContent="center"
            alignItems="center"
            sx={{
              bgcolor: "#ffffff",
              padding: 4,
            }}
          >
            <Login />
          </Grid>
        </Grid>
      </Box>
    );
  }

  return (
    <>
      <div style={{ borderWidth: "1px", borderColor: "black" }}>
        <Header />
      </div>
      <Box sx={{ width: "100%", py: 4, bgcolor: "#ffffff" }}>
        <Box
          display="flex"
          justifyContent="space-between"
          mx={5}
          alignItems="center"
        >
          <Typography variant="h4" fontWeight="bold" color="#000000" mb={2}>
            Campaigns
          </Typography>

          <Button
            variant="contained"
            sx={{
              backgroundColor: "black",
              color: "#FFFFFF",
              borderRadius: "20px",
              padding: "10px 20px",
            }}
            onClick={() => navigate("/add-compaign")}
          >
            Add Campaign
          </Button>
        </Box>

        <List>
          {loading ? (
            <Typography variant="body1" sx={{ textAlign: "center", py: 4 }}>
              Loading campaigns...
            </Typography>
          ) : campaigns.length === 0 ? (
            <Typography variant="body1" sx={{ textAlign: "center", py: 4 }}>
              No campaigns found. Create your first campaign!
            </Typography>
          ) : (
            campaigns.map((campaign) => (
              <ListItem key={campaign.id} sx={{ padding: 0 }}>
                <CampaignCard campaign={campaign} />
              </ListItem>
            ))
          )}
        </List>
      </Box>
    </>
  );
}

export default Home;
