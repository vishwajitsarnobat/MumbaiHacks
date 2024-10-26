import yaml
import os
from google.ads.googleads.client import GoogleAdsClient
import pandas as pd
from fuzzywuzzy import fuzz
import uuid
import requests


# Function to load credentials from YAML file
def load_credentials(file_path):
    with open(file_path, "r") as file:
        credentials = yaml.safe_load(file)
    return credentials


# Campaign creation function
def create_campaign(client, customer_id, campaign_data):
    campaign_service = client.get_service("CampaignService")
    campaign_budget_service = client.get_service("CampaignBudgetService")
    campaign_criterion_service = client.get_service("CampaignCriterionService")

    # Create a campaign budget
    campaign_budget_operation = client.get_type("CampaignBudgetOperation")
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name = "Budget for " + campaign_data["name"]
    campaign_budget.delivery_method = getattr(
        client.enums.BudgetDeliveryMethodEnum.BudgetDeliveryMethod,
        campaign_data["delivery_method"],
    )
    campaign_budget.amount_micros = campaign_data["budget_amount_micros"]

    # Add the budget
    budget_response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id, operations=[campaign_budget_operation]
    )

    # Create the campaign
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.create
    campaign.name = campaign_data["name"]
    campaign.status = getattr(
        client.enums.CampaignStatusEnum.CampaignStatus, campaign_data["status"]
    )
    campaign.advertising_channel_type = getattr(
        client.enums.AdvertisingChannelTypeEnum.AdvertisingChannelType,
        campaign_data["advertising_channel_type"],
    )

    # Set manual CPC bidding strategy if specified
    if campaign_data["manual_cpc"]:
        campaign.manual_cpc.CopyFrom(client.get_type("ManualCpc"))

    # Set the campaign start and end dates
    campaign.start_date = campaign_data["start_date"]
    if campaign_data["end_date"]:
        campaign.end_date = campaign_data["end_date"]

    # Link to the campaign budget
    campaign.campaign_budget = budget_response.results[0].resource_name

    # Set network settings
    campaign.network_settings.target_google_search = campaign_data["network_settings"][
        "target_google_search"
    ]
    campaign.network_settings.target_search_network = campaign_data["network_settings"][
        "target_search_network"
    ]
    campaign.network_settings.target_content_network = campaign_data[
        "network_settings"
    ]["target_content_network"]
    campaign.network_settings.target_partner_search_network = campaign_data[
        "network_settings"
    ]["target_partner_search_network"]

    # Add the campaign
    response = campaign_service.mutate_campaigns(
        customer_id=customer_id, operations=[campaign_operation]
    )
    campaign_resource_name = response.results[0].resource_name
    print(f"Created campaign with resource name: {campaign_resource_name}")

    # Add location criteria to the campaign
    for location_id in campaign_data["locations"]:
        location_operation = client.get_type("CampaignCriterionOperation")
        campaign_criterion = location_operation.create
        campaign_criterion.campaign = campaign_resource_name
        campaign_criterion.location.geo_target_constant = (
            f"geoTargetConstants/{location_id}"
        )
        campaign_criterion_service.mutate_campaign_criteria(
            customer_id=customer_id, operations=[location_operation]
        )
        print(f"Added location criterion with ID: {location_id}")

    # Add language criteria to the campaign
    for language_id in campaign_data["languages"]:
        language_operation = client.get_type("CampaignCriterionOperation")
        campaign_criterion = language_operation.create
        campaign_criterion.campaign = campaign_resource_name
        campaign_criterion.language.language_constant = (
            f"languageConstants/{language_id}"
        )
        campaign_criterion_service.mutate_campaign_criteria(
            customer_id=customer_id, operations=[language_operation]
        )
        print(f"Added language criterion with ID: {language_id}")

    return campaign_resource_name


def fuzzy_match_ids(queries):
    file_path = "filtered_data.csv"  # Update to the actual relative path if necessary
    df = pd.read_csv(file_path)

    def get_ids_fuzzy(query):
        # Define a threshold for matching
        threshold = 90
        matched_ids = []

        # Check matches in the 'Name' column
        for index, row in df.iterrows():
            if fuzz.ratio(row["Name"], query) >= threshold:
                matched_ids.append(row["Criteria ID"])

        # Check matches in the 'Canonical Name' column
        for index, row in df.iterrows():
            if fuzz.ratio(row["Canonical Name"], query) >= threshold:
                matched_ids.append(row["Criteria ID"])

        # Remove duplicates from the matched IDs
        matched_ids = list(set(matched_ids))
        return matched_ids

    # Collect matched IDs for each query into a single list
    results = []
    for query in queries:
        matched_ids = get_ids_fuzzy(query)
        results.extend(matched_ids)

    return results


def create_ad_group(client, customer_id, campaign_resource_name, ad_group_data):
    ad_group_service = client.get_service("AdGroupService")
    campaign_service = client.get_service("CampaignService")

    # Create the ad group
    ad_group_operation = client.get_type("AdGroupOperation")
    ad_group = ad_group_operation.create
    ad_group.name = ad_group_data["name"]
    ad_group.campaign = campaign_service.campaign_path(
        customer_id, campaign_resource_name
    )
    ad_group.status = getattr(
        client.enums.AdGroupStatusEnum.AdGroupStatus, ad_group_data["status"]
    )
    ad_group.type_ = getattr(
        client.enums.AdGroupTypeEnum.AdGroupType, ad_group_data["ad_group_type"]
    )

    # Set bidding strategy
    if ad_group_data["manual_cpc"]:
        ad_group.cpc_bid_micros = ad_group_data["cpc_bid_micros"]

    # Add the ad group
    response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id, operations=[ad_group_operation]
    )
    ad_group_resource_name = response.results[0].resource_name
    print(f"Created ad group with resource name: {ad_group_resource_name}")
    return ad_group_resource_name


def create_ad_text_asset(client, text, pinned_field=None):
    """Create an AdTextAsset.

    Args:
        client: an initialized GoogleAdsClient instance.
        text: text for headlines and descriptions.
        pinned_field: to pin a text asset so it always shows in the ad.

    Returns:
        An AdTextAsset.
    """
    ad_text_asset = client.get_type("AdTextAsset")
    ad_text_asset.text = text
    if pinned_field:
        ad_text_asset.pinned_field = pinned_field
    return ad_text_asset


def create_ad_text_asset_with_customizer(client, customizer_attribute_resource_name):
    """Create an AdTextAsset.
    Args:
        client: an initialized GoogleAdsClient instance.
        customizer_attribute_resource_name: The resource name of the customizer attribute.

    Returns:
        An AdTextAsset.
    """
    ad_text_asset = client.get_type("AdTextAsset")

    # Create this particular description using the ad customizer. Visit
    # https://developers.google.com/google-ads/api/docs/ads/customize-responsive-search-ads#ad_customizers_in_responsive_search_ads
    # for details about the placeholder format. The ad customizer replaces the
    # placeholder with the value we previously created and linked to the
    # customer using CustomerCustomizer.
    ad_text_asset.text = (
        f"Just {{CUSTOMIZER.{customizer_attribute_resource_name}:10USD}}"
    )

    return ad_text_asset


def create_campaign_budget(client, customer_id):
    """Creates campaign budget resource.

    Args:
      client: an initialized GoogleAdsClient instance.
      customer_id: a client customer ID.

    Returns:
      Campaign budget resource name.
    """
    # Create a budget, which can be shared by multiple campaigns.
    campaign_budget_service = client.get_service("CampaignBudgetService")
    campaign_budget_operation = client.get_type("CampaignBudgetOperation")
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name = f"Campaign budget {uuid.uuid4()}"
    campaign_budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
    campaign_budget.amount_micros = 500000

    # Add budget.
    campaign_budget_response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id, operations=[campaign_budget_operation]
    )

    return campaign_budget_response.results[0].resource_name


def create_ad_group_ad(client, customer_id, ad_group_resource_name, ad_data):
    ad_group_ad_service = client.get_service("AdGroupAdService")

    ad_group_ad_operation = client.get_type("AdGroupAdOperation")
    ad_group_ad = ad_group_ad_operation.create
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
    ad_group_ad.ad_group = ad_group_resource_name

    ad_group_ad.ad.final_urls.append(ad_data["final_url"])

    for headline in ad_data["headlines"]:
        ad_group_ad.ad.responsive_search_ad.headlines.append(
            create_ad_text_asset(client, headline)
        )

    for description in ad_data["descriptions"]:
        ad_group_ad.ad.responsive_search_ad.descriptions.append(
            create_ad_text_asset(client, description)
        )

    ad_group_ad.ad.responsive_search_ad.path1 = ad_data.get("path1", "")
    ad_group_ad.ad.responsive_search_ad.path2 = ad_data.get("path2", "")

    # Always set customizer_attribute_name to None
    ad_data["customizer_attribute_name"] = None

    # Add image assets if any
    # if "images" in ad_data:
    #     asset_service = client.get_service("AssetService")
    #     image_assets = []
    #     for image_url in ad_data["images"]:
    #         image_asset_operation = client.get_type("AssetOperation")
    #         image_asset = image_asset_operation.create

    #         # Set the asset type and provide a name for the asset
    #         image_asset.type_ = client.enums.AssetTypeEnum.IMAGE
    #         image_asset.name = f"Image Asset for {image_url.split('/')[-1]}"  # Unique name based on the file name
    #         image_asset.image_asset.data = get_image_bytes(image_url)  # Helper function to fetch image data
    #         image_asset.image_asset.file_size = 600000  # Example size limit in bytes

    #         # Make the API request to create the asset
    #         image_response = asset_service.mutate_assets(customer_id=customer_id, operations=[image_asset_operation])
    #         image_assets.append(image_response.results[0].resource_name)

    #     # Link image assets to the ad
    #     ad_group_ad.ad.responsive_display_ad.marketing_images.extend(image_assets)

    # Submit ad group ad operation
    ad_group_ad_response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id, operations=[ad_group_ad_operation]
    )

    for result in ad_group_ad_response.results:
        print(
            f"Created responsive display ad with resource name "
            f'"{result.resource_name}".'
        )

    return ad_group_ad_response.results[0].resource_name


def get_image_bytes(image_url):
    if image_url.startswith("http://") or image_url.startswith("https://"):
        import requests

        response = requests.get(image_url)
        return response.content if response.status_code == 200 else None
    else:
        # Load from local file
        try:
            with open(image_url, "rb") as img_file:
                return img_file.read()
        except FileNotFoundError:
            print(f"File not found: {image_url}")
            return None


def add_keywords(client, customer_id, ad_group_resource_name, keyword_data):
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")
    operations = []

    match_types = {
        "exact": client.enums.KeywordMatchTypeEnum.EXACT,
        "phrase": client.enums.KeywordMatchTypeEnum.PHRASE,
        "broad": client.enums.KeywordMatchTypeEnum.BROAD,
    }

    for match_key, match_type in match_types.items():
        ad_group_criterion_operation = client.get_type("AdGroupCriterionOperation")
        ad_group_criterion = ad_group_criterion_operation.create
        ad_group_criterion.ad_group = ad_group_resource_name
        ad_group_criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        ad_group_criterion.keyword.text = keyword_data[match_key]
        ad_group_criterion.keyword.match_type = match_type
        operations.append(ad_group_criterion_operation)

    ad_group_criterion_response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id,
        operations=operations,
    )

    for result in ad_group_criterion_response.results:
        print(f"Created keyword {result.resource_name}.")


def main_add_adgroup(client, customer_id, campaign_id, ad_group_data):
    ad_group_service = client.get_service("AdGroupService")
    campaign_service = client.get_service("CampaignService")

    # Create ad group.
    ad_group_operation = client.get_type("AdGroupOperation")
    ad_group = ad_group_operation.create

    # Set the ad group attributes from the ad_group_data dictionary
    ad_group.name = ad_group_data["name"]
    ad_group.status = getattr(client.enums.AdGroupStatusEnum, ad_group_data["status"])
    ad_group.campaign = campaign_service.campaign_path(customer_id, campaign_id)
    ad_group.type_ = getattr(
        client.enums.AdGroupTypeEnum, ad_group_data["ad_group_type"]
    )
    ad_group.cpc_bid_micros = ad_group_data["cpc_bid_micros"]

    # Add the ad group.
    ad_group_response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id, operations=[ad_group_operation]
    )

    resource_name = ad_group_response.results[0].resource_name
    print(f"Created ad group {resource_name}.")

    return resource_name


def get_campaign_id_from_resource_name(resource_name):
    return resource_name.split("/")[-1]


def add_local_image_asset(client, customer_id, local_image_path):
    url = "https://gaagl.page.link/Eit5"
    image_content = requests.get(url).content

    asset_service = client.get_service("AssetService")
    asset_operation = client.get_type("AssetOperation")
    asset = asset_operation.create
    asset.type_ = client.enums.AssetTypeEnum.IMAGE
    asset.image_asset.data = image_content
    asset.image_asset.file_size = len(image_content)
    asset.image_asset.mime_type = client.enums.MimeTypeEnum.IMAGE_JPEG
    # Use your favorite image library to determine dimensions
    asset.image_asset.full_size.height_pixels = 315
    asset.image_asset.full_size.width_pixels = 600
    asset.image_asset.full_size.url = url
    # Provide a unique friendly name to identify your asset.
    # When there is an existing image asset with the same content but a different
    # name, the new name will be dropped silently.
    asset.name = "Marketing Image"

    mutate_asset_response = asset_service.mutate_assets(
        customer_id=customer_id, operations=[asset_operation]
    )
    print("Uploaded file(s):")
    for row in mutate_asset_response.results:
        print(f"\tResource name: {row.resource_name}")


# Ensure to call the main function with appropriate client and customer_id


# Main script
def publish_ads(data, credentials):
    client = GoogleAdsClient.load_from_dict(credentials)
    CUSTOMER_ID = "3121181490"

    # Initialize a results object to store messages
    results = {}

    # Fuzzy match locations based on test queries
    test_queries = ["Hyderabad"]
    data["campaign"]["locations"] = fuzzy_match_ids(test_queries)

    # Create campaign
    campaign_resource_name = create_campaign(client, CUSTOMER_ID, data["campaign"])
    campaign_id = get_campaign_id_from_resource_name(campaign_resource_name)
    results["campaign_id"] = campaign_id

    # Create ad group
    ad_group_resource_name = main_add_adgroup(
        client, CUSTOMER_ID, campaign_id, data["ad_group"]
    )
    ad_group_id = get_campaign_id_from_resource_name(ad_group_resource_name)
    results["ad_group_id"] = ad_group_id

    # Create ad
    create_ad_group_ad(client, CUSTOMER_ID, ad_group_resource_name, data["ad"])

    # Add keywords
    # add_keywords(client, CUSTOMER_ID, ad_group_resource_name, keyword_data)

    return results


if __name__ == "__main__":
    # Input data dictionaries
    data = {
        "campaign": {
            "name": "26",
            "status": "PAUSED",
            "advertising_channel_type": "SEARCH",
            "manual_cpc": True,
            "budget_amount_micros": 50000000,
            "delivery_method": "STANDARD",
            "network_settings": {
                "target_google_search": True,
                "target_search_network": False,
                "target_content_network": False,
                "target_partner_search_network": False,
            },
            "locations": [],  # Will be filled later from fuzzy matching
            "languages": [1000],  # Example: English
            "conversion_goals": "Account-default",
            "customer_acquisition": "Bid equally for new and existing customers",
            "marketing_objective": None,  # No marketing objective selected
            "start_date": "2024-10-26",
            "end_date": None,  # No end date set
        },
        "ad_group": {
            "name": "26",  # Provide the ad group name here
            "status": "ENABLED",  # Status can be "ENABLED" or "PAUSED"
            "ad_group_type": "SEARCH_STANDARD",  # Specify the ad group type
            "cpc_bid_micros": 10000000,  # Set the CPC bid in micros
        },
        "ad": {
            "final_url": "https://www.amazon.com/",
            "headlines": [
                "Headline 1 testing",
                "Headline 2 testing",
                "Headline 3 testing",
            ],
            "descriptions": ["Desc 1 testing", "Desc 2 testing"],
            "path1": "all-inclusive",
            "path2": "deals",
            "images": [
                "/home/falcon/Projects/MumbaiHacks/Server/GoogleAds/image.jpeg",
            ],
            "customizer_attribute_name": None,
        },
    }

    # Load credentials from a YAML file
    credentials_path = os.path.join(os.path.dirname(__file__), "credentials.yaml")
    credentials = load_credentials(credentials_path)

    print(credentials)

    # Run the main function with data and credentials and capture the results
    results = publish_ads(data, credentials)

    # You can now access the results object to see all messages
    print(results)  # This will print the collected results with respective keys
