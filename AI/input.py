import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from functions import get_advertisement
from datetime import datetime
import base64

# Load the API key from the .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY_YEET")
with open("../templates/campaign_ai_output.json", "r") as file:
    template_json = json.load(file)
template_json_str = json.dumps(template_json, indent=4)
model_name = "gemini-1.5-flash"

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name=model_name)


async def move_outside_content_to_summary(response_text):
    """
    Move any content outside the JSON structure into the summary field.
    """
    # Find the start and end of the JSON structure
    json_start = response_text.find("{")
    json_end = response_text.rfind("}") + 1

    if json_start == -1 or json_end == -1:
        raise ValueError("No JSON structure found in the response text")

    # Extract JSON and outside content
    json_content = response_text[json_start:json_end]
    outside_content = response_text[:json_start] + response_text[json_end:]

    # Parse JSON content
    try:
        json_data = json.loads(json_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON: {e}")

    # Move outside content to summary
    if "summary" in json_data:
        json_data["summary"] += "\n" + outside_content.strip()
    else:
        json_data["summary"] = outside_content.strip()

    return json_data


# f"the summary key's value should have details like why were the decisions made, what benefits they will have and must have a itemized list of language in campaign,campaign name and budget alloted"
async def fill_template(input_json):
    start_date = datetime.today().strftime("%Y-%m-%d")

    formatted_input = (
        f"You are a marketing campaign manager. The user gave the following details:\n\n"
        f"the user wants to {input_json['prompt']}\n"
        f"the user wants to know which locations would be best to target in this region {', '.join(input_json['locations'])}\n\n"
        f"the user wants to target these languages in his campaign {', '.join(input_json['languages'])}\n\n"
        f"the user has also provided a json template which you need to fill as a json."
        f"Template: {template_json_str}\n\n"
        f" you can only use one language per campaign. and set start date as {start_date}."
        f"remember, Don't write anything extra not present in template and fill everything in template and don't give me the input I sent you again in output"
        f"Fill the fields keeping in mind the locations and languages the user, eg if target is mumbai, use keywords like in mumbai."
        f"you need to make the campaign the most successful it can be."
        f"allocate the budget optimal across all campaigns, the budget being {input_json['budget_amount_micros']}"
        f"remember to give all output in json no matter what and no additional fields other than given in template."
        f"dont give any notes,summary etc"
    )

    # Debugging print
    print(f"Formatted input: {formatted_input}")

    response = model.generate_content(formatted_input)
    summary = model.generate_content(
        response.text
        + "create a summary for this.  should have details like why were the decisions made, what benefits they will have and must have a itemized list of language in campaign,campaign name and budget alloted"
    )

    if response:
        print(f"Response text: {response.text}")  # Debugging print
        json_str = response.text
        if json_str.startswith("```json") and json_str.endswith("```"):
            json_str = json_str[7:-3].strip()
        try:
            json_str = await move_outside_content_to_summary(json_str)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return None

        for i in range(len(json_str["campaigns"])):
            json_str["campaigns"][i]["ad"] = {
                "final_url": "",
                "path1": "",
                "path2": "",
                "customizer_attribute_name": "",
            }
            json_str["campaigns"][i]["campaign"]["status"] = "ENABLED"
            json_str["campaigns"][i]["campaign"]["manual_cpc"] = True
            json_str["campaigns"][i]["campaign"]["delivery_method"] = "STANDARD"
            json_str["campaigns"][i]["campaign"]["conversion_goals"] = "Account-default"
            json_str["campaigns"][i]["campaign"]["marketing_objective"] = None
            json_str["campaigns"][i]["campaign"]["start_date"] = start_date

            json_str["campaigns"][i]["ad_group"]["status"] = "ENABLED"

            json_str["campaigns"][i]["ad"]["final_url"] = "https://eg.com"
            json_str["campaigns"][i]["ad"]["path1"] = ""
            json_str["campaigns"][i]["ad"]["path2"] = ""
            json_str["campaigns"][i]["ad"]["customizer_attribute_name"] = None

            targeting = json_str["campaigns"][i]["campaign"]
            details = get_advertisement(
                targeting["locations"],
                "general public",
                input_json["languages"],
                input_json["prompt"],
            )
            details = {
                language: (advert.titles, advert.descriptions, advert.image)
                for language, advert in details.items()
            }
            # {"language": ([title], [description], image)}

            for language in details:
                json_str["campaigns"][i]["ad"]["headlines"] = []
                json_str["campaigns"][i]["ad"]["descriptions"] = []
                base64_image = base64.b64encode(details[language][2]).decode("utf-8")
                json_str["campaigns"][i]["ad"]["images"] = [base64_image]
                for j in range(len(details[language][0])):
                    json_str["campaigns"][i]["ad"]["headlines"].append(
                        details[language][0][j]
                    )
                    json_str["campaigns"][i]["ad"]["descriptions"].append(
                        details[language][1][j]
                    )
        json_str["summary"] = summary.text
        return json_str
    else:
        print("Error: No response from Gemini API")
        return None


# Function to process input and return filled template
async def send_input(input_json):
    filled_template = await fill_template(input_json)
    return filled_template


# Example usage
if __name__ == "__main__":
    import asyncio

    input_json = {
        "prompt": "poster for an ad for promoting my restaurant",
        "languages": ["English"],
        "locations": ["Maharashtra", "ahmendabad"],
        "budget_amount_micros": 500000,
    }

    async def main():
        result = await send_input(input_json)
        print(result)

    asyncio.run(main())
