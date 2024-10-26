import React, { useState } from "react";
import CampaignDetails from "./CampaignDetails";

const CampaignCard = ({ campaignDetail }) => {
  const [expanded, setExpanded] = useState(false);
  const toggleExpand = () => setExpanded(!expanded);

  return (
    <div className="mb-6 mx-8 bg-white shadow-lg rounded-lg overflow-hidden border border-gray-200">
      <div
        className="flex justify-between items-center p-6 cursor-pointer"
        onClick={toggleExpand}
      >
        <h2 className="text-2xl font-semibold text-gray-800">
          {campaignDetail.important_parameters.campaign.name}
        </h2>
        <span className="text-gray-600">{expanded ? "▲" : "▼"}</span>
      </div>
      {expanded && <CampaignDetails campaignDetail={campaignDetail} />}
    </div>
  );
};

export default CampaignCard;
