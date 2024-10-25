from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from input import send_input

app = FastAPI()


@app.post("/get_campaign")
async def get_campaign(request):
    try:
        result = await send_input(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
