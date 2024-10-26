import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Header from "./Header/Header";
import { useNavigate } from "react-router-dom";
const ShowCampaignDetails = () => {
  const { id } = useParams(); // Get the ID from the URL
  const [campaignData, setCampaignData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedIndex, setExpandedIndex] = useState(null); // To track which campaign is expanded
  const naviagte = useNavigate();
  // Hardcoded campaign data
  const constantCampaignData = [
    {
      important_parameters: {
        campaign: {
          name: "Holiday Sale 2024",
          budget_amount_micros: 100000000,
          customer_acquisition: true,
          locations: ["USA", "Canada"],
          languages: ["English", "Spanish"],
          start_date: "2024-11-01",
          end_date: "2024-11-30",
        },
        ad_group: {
          name: "Holiday Offers",
          cpc_bid_micros: 15000000,
        },
        ad: {
          final_url: "https://www.example.com/holiday",
          headlines: [
            "Save Big This Holiday!",
            "Exclusive Holiday Deals",
            "Shop Now for Discounts",
          ],
          descriptions: [
            "Get the best offers of the season.",
            "Limited time only - don't miss out!",
          ],
        },
      },
    },
    {
      important_parameters: {
        campaign: {
          name: "New Year Promo 2025",
          budget_amount_micros: 75000000,
          customer_acquisition: false,
          locations: ["Canada", "UK"],
          languages: ["English", "French"],
          start_date: "2024-12-01",
          end_date: "2025-01-15",
        },
        ad_group: {
          name: "New Year Specials",
          cpc_bid_micros: 12000000,
        },
        ad: {
          final_url: "https://www.example.com/newyear",
          headlines: [
            "Welcome 2025 with Discounts!",
            "Celebrate the New Year!",
            "Start the Year Right!",
          ],
          descriptions: [
            "Unmissable New Year promotions.",
            "Join us for amazing offers this January!",
          ],
        },
      },
    },
    {
      important_parameters: {
        campaign: {
          name: "Spring Sale 2025",
          budget_amount_micros: 50000000,
          customer_acquisition: true,
          locations: ["UK", "Germany"],
          languages: ["English", "German"],
          start_date: "2025-03-01",
          end_date: "2025-03-31",
        },
        ad_group: {
          name: "Spring Discounts",
          cpc_bid_micros: 10000000,
        },
        ad: {
          final_url: "https://www.example.com/spring",
          headlines: [
            "Spring Into Savings!",
            "Blooming Deals Await",
            "Shop Spring Specials Now",
          ],
          descriptions: [
            "Find the best spring discounts.",
            "Limited time offers to welcome the season!",
          ],
        },
      },
    },
  ];

  useEffect(() => {
    // Simulating data fetching
    const fetchCampaignDetails = () => {
      setTimeout(() => {
        setCampaignData(constantCampaignData);
        setIsLoading(false);
      }, 1000); // Simulating a 1-second fetch delay
    };

    fetchCampaignDetails();
  }, []);

  const handleInputChange = (index, section, field, value) => {
    setCampaignData((prevCampaigns) => {
      const newCampaigns = [...prevCampaigns];
      newCampaigns[index].important_parameters[section][field] = value;
      return newCampaigns;
    });
  };

  const toggleExpand = (index) => {
    setExpandedIndex(expandedIndex === index ? null : index); // Toggle the expanded index
  };

  const handlePublish = () => {
    // Logic to handle publishing campaigns
    naviagte("/published");
    console.log("Campaigns published");
  };

  if (isLoading)
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-lg font-semibold">Loading...</div>
      </div>
    );

  if (error)
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-lg font-semibold text-red-600">Error: {error}</div>
      </div>
    );

  return (
    <>
      <Header />
      <div className="flex flex-col   min-h-screen bg-gray-50 py-8 ">
        <div className="w-100% flex justify-between items-center mb-4 mx-10">
          {" "}
          {/* Use w-full for full width */}
          <h1 className="text-3xl font-semibold">Ads</h1>
          <button
            onClick={handlePublish}
            className="bg-black text-white px-4 py-2 rounded"
          >
            Publish All
          </button>
        </div>

        {campaignData.map((campaignDetail, index) => (
          <div
            key={index}
            className="mb-6 mx-8 bg-white shadow-lg rounded-lg overflow-hidden border border-gray-200 mx-"
          >
            <div
              className="flex justify-between items-center p-6 cursor-pointer"
              onClick={() => toggleExpand(index)}
            >
              <h2 className="text-2xl font-semibold text-gray-800">
                {campaignDetail.important_parameters.campaign.name}
              </h2>
              <span className="text-gray-600">
                {expandedIndex === index ? "▲" : "▼"}
              </span>
            </div>
            {expandedIndex === index && (
              <div className="px-6 pb-6">
                <p className="text-gray-700 text-lg mb-2">
                  Budget: Rupees{" "}
                  <input
                    type="number"
                    value={Math.round(
                      campaignDetail.important_parameters.campaign
                        .budget_amount_micros / 1000000
                    )}
                    onChange={(e) =>
                      handleInputChange(
                        index,
                        "campaign",
                        "budget_amount_micros",
                        e.target.value * 1000000
                      )
                    }
                    className="border border-gray-300 p-2 rounded ml-2"
                  />
                </p>
                <p className="text-gray-700 text-lg mb-2">
                  Customer Acquisition:{" "}
                  {campaignDetail.important_parameters.campaign
                    .customer_acquisition
                    ? "Yes"
                    : "No"}
                </p>
                <p className="text-gray-700 text-lg mb-2">
                  Locations:{" "}
                  {campaignDetail.important_parameters.campaign.locations.join(
                    ", "
                  )}
                </p>
                <p className="text-gray-700 text-lg mb-2">
                  Languages:{" "}
                  {campaignDetail.important_parameters.campaign.languages.join(
                    ", "
                  )}
                </p>
                <p className="text-gray-700 text-lg mb-2">
                  Start Date:{" "}
                  <input
                    type="date"
                    value={
                      campaignDetail.important_parameters.campaign.start_date
                    }
                    onChange={(e) =>
                      handleInputChange(
                        index,
                        "campaign",
                        "start_date",
                        e.target.value
                      )
                    }
                    className="border border-gray-300 p-2 rounded ml-2"
                  />
                </p>
                <p className="text-gray-700 text-lg mb-2">
                  End Date:{" "}
                  <input
                    type="date"
                    value={
                      campaignDetail.important_parameters.campaign.end_date
                    }
                    onChange={(e) =>
                      handleInputChange(
                        index,
                        "campaign",
                        "end_date",
                        e.target.value
                      )
                    }
                    className="border border-gray-300 p-2 rounded ml-2"
                  />
                </p>

                <h3 className="text-xl font-semibold mt-4">Ad Group:</h3>
                <p className="text-gray-700 text-lg mb-2">
                  Name:
                  <input
                    type="text"
                    value={campaignDetail.important_parameters.ad_group.name}
                    onChange={(e) =>
                      handleInputChange(
                        index,
                        "ad_group",
                        "name",
                        e.target.value
                      )
                    }
                    className="border border-gray-300 p-2 rounded ml-2"
                  />
                </p>
                <p className="text-gray-700 text-lg mb-2">
                  CPC Bid: Rupees{" "}
                  <input
                    type="number"
                    value={Math.round(
                      campaignDetail.important_parameters.ad_group
                        .cpc_bid_micros / 1000000
                    )}
                    onChange={(e) =>
                      handleInputChange(
                        index,
                        "ad_group",
                        "cpc_bid_micros",
                        e.target.value * 1000000
                      )
                    }
                    className="border border-gray-300 p-2 rounded ml-2"
                  />
                </p>

                <h3 className="text-xl font-semibold mt-4">Ad:</h3>
                <p className="text-gray-700 text-lg mb-2">
                  Final URL:
                  <input
                    type="text"
                    value={campaignDetail.important_parameters.ad.final_url}
                    onChange={(e) =>
                      handleInputChange(
                        index,
                        "ad",
                        "final_url",
                        e.target.value
                      )
                    }
                    className="border border-gray-300 p-2 rounded ml-2"
                  />
                </p>
                <div>
                  <h4 className="text-lg font-semibold">Headlines:</h4>
                  {campaignDetail.important_parameters.ad.headlines.map(
                    (headline, hIndex) => (
                      <div key={hIndex} className="mb-2">
                        <input
                          type="text"
                          value={headline}
                          onChange={(e) =>
                            handleInputChange(
                              index,
                              "ad",
                              "headlines",
                              e.target.value,
                              hIndex
                            )
                          }
                          className="border border-gray-300 p-2 rounded"
                        />
                      </div>
                    )
                  )}
                </div>
                <div>
                  <h4 className="text-lg font-semibold">Descriptions:</h4>
                  {campaignDetail.important_parameters.ad.descriptions.map(
                    (description, dIndex) => (
                      <div key={dIndex} className="mb-2">
                        <input
                          type="text"
                          value={description}
                          onChange={(e) =>
                            handleInputChange(
                              index,
                              "ad",
                              "descriptions",
                              e.target.value,
                              dIndex
                            )
                          }
                          className="border border-gray-300 p-2 rounded"
                        />
                      </div>
                    )
                  )}
                </div>

                <p className="text-gray-700 text-lg mb-2">
                  <strong>Confirmation: </strong> Ad settings have been saved
                  successfully!
                </p>
              </div>
            )}
          </div>
        ))}
      </div>
    </>
  );
};

export default ShowCampaignDetails;
