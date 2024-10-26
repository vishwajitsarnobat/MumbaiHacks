import React from "react";
import CampaignCard from "./CompaingCard"; // Ensure this path matches your file structure

function LoggedinHome() {
  const campaigns = [
    {
      id: 1,
      name: "Winter Sale Campaign",
      status: "Active",
      budget: "$5000",
      impressions: "100,000",
      clicks: "3,500",
    },
    {
      id: 2,
      name: "Holiday Special Campaign",
      status: "Paused",
      budget: "$3000",
      impressions: "80,000",
      clicks: "2,100",
    },
    {
      id: 3,
      name: "New Year Kickoff",
      status: "Active",
      budget: "$7000",
      impressions: "120,000",
      clicks: "4,500",
    },
    {
      id: 4,
      name: "Summer Clearance",
      status: "Completed",
      budget: "$2500",
      impressions: "50,000",
      clicks: "1,500",
    },
    {
      id: 5,
      name: "Spring Collection Launch",
      status: "Active",
      budget: "$6000",
      impressions: "90,000",
      clicks: "3,200",
    },
  ];

  return (
    <div style={{ padding: "20px", backgroundColor: "#F5F5F5" }}>
      <h2 style={{ textAlign: "center" }}>Campaigns Overview</h2>
      <div
        style={{ display: "flex", flexWrap: "wrap", justifyContent: "center" }}
      >
        {campaigns.map((campaign) => (
          <CampaignCard
            key={campaign.id}
            name={campaign.name}
            status={campaign.status}
            budget={campaign.budget}
            impressions={campaign.impressions}
            clicks={campaign.clicks}
          />
        ))}
      </div>
    </div>
  );
}

export default LoggedinHome;
