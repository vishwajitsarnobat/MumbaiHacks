from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from input import send_input
from typing import List, Dict, Any
from API_ads import publish_ads

app = FastAPI()


class Campaign(BaseModel):
    name: str
    advertising_channel_type: str
    budget_amount_micros: int
    network_settings: Dict[str, bool]
    locations: List[str]
    languages: List[str]
    conversion_goals: str
    customer_acquisition: bool
    marketing_objective: Any
    start_date: str
    end_date: str


class AdGroup(BaseModel):
    name: str
    ad_group_type: str
    cpc_bid_micros: int


class Ad(BaseModel):
    final_url: str
    path1: str
    path2: str
    customizer_attribute_name: Any
    headlines: List[str]
    descriptions: List[str]
    images: List[str]


class PublishAdsRequest(BaseModel):
    campaign: Campaign
    ad_group: AdGroup
    ad: Ad


class CampaignRequest(BaseModel):
    prompt: str
    languages: List[str]
    locations: List[str]
    budget_amount_micros: int


@app.post("/get_campaign")
async def get_campaign(request: CampaignRequest):
    try:
        result = await send_input(request.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/publish_ads")
async def publish_ads_endpoint(request: PublishAdsRequest, credentials: Dict[str, Any]):
    try:
        results = publish_ads(request.dict(), credentials)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
