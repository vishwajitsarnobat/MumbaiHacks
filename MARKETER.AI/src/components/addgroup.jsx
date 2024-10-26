import React from "react";

const AdGroupDetails = ({ adGroup, onAdGroupChange }) => {
  return (
    <div className="bg-white shadow-md rounded-lg p-6 mb-6 border border-gray-200">
      <h3 className="text-xl font-semibold text-gray-800 mt-4">Ad Group:</h3>
      <p className="text-gray-700 text-lg mb-4">
        Name:
        <input
          type="text"
          value={adGroup.name}
          onChange={(e) => onAdGroupChange("name", e.target.value)}
          className="border border-gray-300 p-2 rounded ml-2 focus:outline-none focus:ring-2 focus:ring-lightBlue-500"
        />
      </p>
      <p className="text-gray-700 text-lg mb-4">
        CPC Bid: Rupees{" "}
        <input
          type="number"
          value={Math.round(adGroup.cpc_bid_micros / 1000000)}
          onChange={(e) =>
            onAdGroupChange("cpc_bid_micros", e.target.value * 1000000)
          }
          className="border border-gray-300 p-2 rounded ml-2 focus:outline-none focus:ring-2 focus:ring-lightBlue-500"
        />
      </p>
    </div>
  );
};

export default AdGroupDetails;
