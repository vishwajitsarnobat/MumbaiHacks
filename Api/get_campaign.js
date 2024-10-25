const axios = require("axios");

async function getCampaign(request) {
  try {
    const response = await axios.post(
      "http://127.0.0.1:8000/get_campaign",
      request,
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error(
      "Error:",
      error.response ? error.response.data : error.message
    );
    throw error;
  }
}
