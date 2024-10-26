import React from "react";
import AdGroupDetails from "./AdGroupDetails";

const CampaignDetails = ({ campaignDetail }) => {
  return (
    <div className="px-6 pb-6">
      <p className="text-gray-700 text-lg mb-2">
        Budget: Rupees{" "}
        <input
          type="number"
          value={Math.round(
            campaignDetail.important_parameters.campaign.budget_amount_micros /
              1000000
          )}
          className="border border-gray-300 p-2 rounded ml-2"
        />
      </p>
      <p className="text-gray-700 text-lg mb-2">
        Customer Acquisition:{" "}
        {campaignDetail.important_parameters.campaign.customer_acquisition
          ? "Yes"
          : "No"}
      </p>
      <p className="text-gray-700 text-lg mb-2">
        Locations:{" "}
        {campaignDetail.important_parameters.campaign.locations.join(", ")}
      </p>
      <p className="text-gray-700 text-lg mb-2">
        Languages:{" "}
        {campaignDetail.important_parameters.campaign.languages.join(", ")}
      </p>
      <AdGroupDetails adGroup={campaignDetail.important_parameters.ad_group} />
    </div>
  );
};

export default CampaignDetails;
