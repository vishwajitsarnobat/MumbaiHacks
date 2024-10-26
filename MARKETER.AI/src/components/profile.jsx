import React, { useState, useEffect } from "react";
import appwriteService from "../appwrite/config";
import { useSelector } from "react-redux";
import userImage from "../assets/userimage.jpeg"; // Importing the placeholder image

function Profile() {
  const [formData, setFormData] = useState({
    developerToken: "",
    refreshToken: "",
    clientId: "",
    clientSecret: "",
    customerId: "",
    loginCustomerId: "",
    youtubeAPIKey: "",
    InstagramAPIKey: "",
  });

  const userData = useSelector((state) => state.auth.userData);
  const userId = userData ? parseInt(userData.$id, 10) : null;

  useEffect(() => {
    const fetchProfileData = async () => {
      if (userId) {
        try {
          const profile = await appwriteService.getProfile(userId);
          if (profile) {
            setFormData({
              developerToken: profile.developerToken || "",
              refreshToken: profile.refreshToken || "",
              clientId: profile.clientId || "",
              clientSecret: profile.clientSecret || "",
              customerId: profile.customerId || "",
              loginCustomerId: profile.loginCustomerId || "",
              youtubeAPIKey: profile.youtubeAPIKey || "",
              InstagramAPIKey: profile.InstagramAPIKey || "",
            });
          }
        } catch (error) {
          console.error("Error fetching profile data:", error);
        }
      }
    };

    fetchProfileData();
  }, [userId]);

  const handleInputChange = (field) => (event) => {
    setFormData((prev) => ({
      ...prev,
      [field]: event.target.value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const profileData = {
      ...formData,
      userId: userId,
    };

    const result = await appwriteService.createProfile(profileData);
    console.log("Profile created:", result);
  };

  if (!userData) {
    return <div>Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-white p-8">
      <div className="max-w-5xl mx-auto bg-white border border-gray-200 rounded-xl shadow-2xl p-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-black mb-4">Profile</h1>
          <p className="text-gray-600">
            Manage your profile information and credentials
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          <div className="flex flex-col items-center mb-12">
            <div className="relative w-40 h-40 mb-6">
              <img
                src={userImage} // Set as a constant placeholder
                className="w-40 h-40 rounded-full object-cover border-4 border-gray-200"
                alt="User profile placeholder"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Map through fields */}
            {[
              {
                label: "Developer Token",
                field: "developerToken",
                placeholder: "Enter developer token",
              },
              {
                label: "Refresh Token",
                field: "refreshToken",
                placeholder: "Enter refresh token",
              },
              {
                label: "Client ID",
                field: "clientId",
                placeholder: "Enter client ID",
              },
              {
                label: "Client Secret",
                field: "clientSecret",
                placeholder: "Enter client secret",
              },
              {
                label: "Customer ID",
                field: "customerId",
                placeholder: "Enter customer ID",
              },
              {
                label: "Login Customer ID",
                field: "loginCustomerId",
                placeholder: "Enter login customer ID",
              },
              {
                label: "YouTube API Key",
                field: "youtubeAPIKey",
                placeholder: "Enter YouTube API Key",
              },
              {
                label: "Instagram API Key",
                field: "InstagramAPIKey",
                placeholder: "Enter Instagram API Key",
              },
            ].map(({ label, field, placeholder }) => (
              <div key={field} className="space-y-2">
                <label className="text-sm text-gray-800 font-medium block">
                  {label}
                </label>
                <input
                  type="text"
                  value={formData[field]}
                  onChange={handleInputChange(field)}
                  placeholder={placeholder}
                  className="w-full bg-gray-100 text-black border border-gray-300 p-3 rounded-lg focus:outline-none focus:border-gray-600 placeholder-gray-500 transition-all duration-200"
                  required
                />
              </div>
            ))}
          </div>

          <div className="flex justify-center mt-12">
            <button
              type="submit"
              className="px-12 py-3 bg-gray-700 text-white font-bold rounded-lg hover:bg-gray-600 transition-colors"
            >
              Save Changes
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Profile;
