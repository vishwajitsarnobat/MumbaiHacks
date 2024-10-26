import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import appwriteService from "../appwrite/config";
import { useSelector } from "react-redux";
import Header from "./Header/Header";

const languagesList = [
  { name: "English", code: "en" },
  { name: "Hindi", code: "hi" },
  { name: "Marathi", code: "mr" },
  { name: "Spanish", code: "es" },
  { name: "French", code: "fr" },
];

const campaignTypes = [
  { name: "Ad", code: "ad" },
  { name: "Post", code: "post" },
];

const AddCampaignForm = () => {
  const { register, handleSubmit, setValue } = useForm();
  const [selectedLanguages, setSelectedLanguages] = useState([]);
  const [campaignType, setCampaignType] = useState("");
  const [addresses, setAddresses] = useState([]);
  const [newAddress, setNewAddress] = useState("");
  const [budget, setBudget] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const userData = useSelector((state) => state.auth.userData);

  const handleLanguageSelect = (name) => {
    setSelectedLanguages((prev) =>
      prev.includes(name)
        ? prev.filter((lang) => lang !== name)
        : [...prev, name]
    );
  };

  const handleCampaignTypeSelect = (code) => {
    setCampaignType((prev) => (prev === code ? "" : code));
    setValue("campaignType", code);
    if (code !== "ad") {
      setBudget("");
    }
  };

  const handleAddressKeyPress = (event) => {
    if (event.key === "Enter" && newAddress.trim() !== "") {
      event.preventDefault();
      setAddresses([...addresses, newAddress.trim()]);
      setNewAddress("");
    }
  };

  const removeAddress = (address) => {
    setAddresses(addresses.filter((addr) => addr !== address));
  };

  const onSubmit = async (data) => {
    setIsLoading(true);
    const campaignData = {
      ...data,
      campaignType,
      languages: selectedLanguages,
      addresses,
      budget: parseInt(budget, 10),
      userId: userData.$id,
    };

    try {
      const newCampaign = await appwriteService.createCampaign(campaignData);
      console.log(Object.keys(newCampaign));
      if (newCampaign) {
        // Navigate to the show campaign details page with the document ID
        navigate(`/show-campaign-details/${newCampaign.$id}`, {
          state: { campaignData: newCampaign },
        });
      }
    } catch (error) {
      console.error("Error creating campaign:", error);
      alert("An error occurred. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <Header />
      <div className="p-8 bg-white border border-gray-200">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-semibold text-black mb-2">
            Create Campaign
          </h1>
          <p className="text-gray-700 mb-8 border-l-2 border-gray-300 pl-2 pr-4">
            Please fill in the details below to create your campaign.
          </p>
          <div>
            <label className="text-sm text-black block mb-2 font-medium">
              Campaign Description
            </label>
            <textarea
              {...register("description", { required: true })}
              className="w-full bg-white border border-black/30 px-4 py-2 text-black focus:border-black outline-none transition-colors h-32 hover:border-black"
              placeholder="Describe your campaign"
            />
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
            {/* Campaign Type */}
            <div>
              <label className="text-sm text-black block mb-3 font-medium">
                Campaign Type
              </label>
              <div className="flex flex-wrap gap-3">
                {campaignTypes.map((type) => (
                  <button
                    key={type.code}
                    type="button"
                    onClick={() => handleCampaignTypeSelect(type.code)}
                    className={`px-4 py-2 border transition-all rounded-full 
                    ${
                      campaignType === type.code
                        ? "bg-black text-white border-black"
                        : "bg-white text-black border-black/30 hover:border-black"
                    }
                    hover:bg-gray-300`}
                  >
                    {type.name}
                  </button>
                ))}
              </div>
              <input
                type="hidden"
                {...register("campaignType", { required: true })}
                value={campaignType}
              />
            </div>

            {/* Budget Input */}
            {campaignType === "ad" && (
              <div>
                <label className="text-sm text-black block mb-2 font-medium">
                  Budget
                </label>
                <input
                  type="number"
                  value={budget}
                  onChange={(e) => setBudget(e.target.value)}
                  className="w-full bg-white border border-black/30 px-4 py-2 text-black focus:border-black outline-none transition-colors hover:border-black"
                  placeholder="Enter budget"
                  required
                />
              </div>
            )}

            {/* Languages */}
            <div>
              <label className="text-sm text-black block mb-3 font-medium">
                Languages
              </label>
              <div className="flex flex-wrap gap-3">
                {languagesList.map((lang) => (
                  <button
                    key={lang.code}
                    type="button"
                    onClick={() => handleLanguageSelect(lang.name)}
                    className={`px-4 py-2 border transition-all rounded-full 
                    ${
                      selectedLanguages.includes(lang.name)
                        ? "bg-black text-white border-black"
                        : "bg-white text-black border-black/30 hover:border-black"
                    }
                    hover:bg-gray-300`}
                  >
                    {lang.name}
                  </button>
                ))}
              </div>
            </div>

            {/* Campaign Details */}
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="text-sm text-black block mb-2 font-medium">
                  Campaign Title
                </label>
                <input
                  type="text"
                  {...register("title", { required: true })}
                  className="w-full bg-white border border-black/30 px-4 py-2 text-black focus:border-black outline-none transition-colors hover:border-black"
                  placeholder="Enter campaign title"
                />
              </div>
            </div>

            {/* Addresses */}
            <div>
              <h2 className="text-xl font-semibold text-black mb-4">
                Addresses
              </h2>
              <label className="text-sm text-black block mb-2 font-medium">
                State, City
              </label>
              <input
                type="text"
                value={newAddress}
                onChange={(e) => setNewAddress(e.target.value)}
                onKeyPress={handleAddressKeyPress}
                className="w-full bg-white border border-black/30 px-4 py-2 text-black focus:border-black outline-none transition-colors hover:border-black"
                placeholder="Enter state, city and press Enter"
              />

              {addresses.length > 0 && (
                <div className="mt-4">
                  <h3 className="text-sm font-medium text-black mb-2">
                    Added Addresses
                  </h3>
                  <div className="space-y-2">
                    {addresses.map((addr) => (
                      <div
                        key={addr}
                        className="flex justify-between items-center border border-black/10 p-3 hover:bg-gray-100"
                      >
                        <span className="text-black">{addr}</span>
                        <button
                          type="button"
                          onClick={() => removeAddress(addr)}
                          className="text-black/70 hover:text-black transition-colors"
                        >
                          Delete
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4">
              <button
                type="submit"
                className="px-6 py-2 bg-black text-white hover:bg-gray-800 transition-colors rounded-full"
                disabled={isLoading}
              >
                {isLoading ? "Saving..." : "Generate"}
              </button>
              <button
                type="button"
                className="px-6 py-2 border border-black/30 text-black hover:border-black transition-colors rounded-full"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
};

export default AddCampaignForm;
