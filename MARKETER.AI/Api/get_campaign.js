async function getCampaign({ prompt, languages, locations, budgetAmountMicros }) {
  const url = "http://127.0.0.1:8001/get_campaign"; // Adjusted port if necessary
  const data = {
      prompt,
      languages,
      locations,
      budget_amount_micros: budgetAmountMicros,
  };

  try {
      const response = await fetch(url, {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
      });

      if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const result = await response.json();
      console.log(result.campaigns); // Handle the result as needed
      return result.campaigns; // Return the campaigns for further use
  } catch (error) {
      console.error("Error:", error);
      throw error; // Rethrow the error for handling elsewhere if needed
  }
}

// Example usage
const campaignParams = {
  prompt: "poster for an ad for promoting my restaurant",
  languages: ["English"],
  locations: ["Maharashtra", "ahmendabad"],
  budgetAmountMicros: 500000,
};

getCampaign(campaignParams)
  .then(campaigns => {
      // Handle the received campaigns here if needed
      console.log("Received campaigns:", campaigns);
  })
  .catch(error => {
      // Handle any errors that may have occurred
      console.error("Failed to get campaigns:", error);
  });


  export {getCampaign} 