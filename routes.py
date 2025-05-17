from fastapi import APIRouter, Request, HTTPException, Header
from fastapi.responses import JSONResponse
from telegram_client import app as tg
import os
import inspect

router = APIRouter()

@router.post("/call")
async def call_method(request: Request, x_api_key: str = Header(None)):
    if x_api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API key")

    body = await request.json()
    method = body.get("method")
    params = body.get("params", {})

    if not method:
        raise HTTPException(status_code=400, detail="Missing method")

    async with tg:
        try:
            func = getattr(tg, method)
            result = await func(**params)

            # Если результат имеет .dict(), сериализуем его
            if hasattr(result, "dict") and inspect.ismethod(result.dict):
                result = result.dict()

            return JSONResponse(content={"status": "ok", "result": result})

        except AttributeError:
            raise HTTPException(status_code=400, detail=f"Unknown method: {method}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
