from fastapi import APIRouter, Request, HTTPException, Header
from fastapi.responses import JSONResponse
from telegram_client import app as tg
import os

router = APIRouter()

def serialize_result(result):
    # Если объект имеет __dict__, вернём только сериализуемые поля
    if hasattr(result, "__dict__"):
        return {
            k: v for k, v in result.__dict__.items()
            if not k.startswith("_")
        }
    # Если это список объектов — рекурсивно сериализуем
    elif isinstance(result, list):
        return [serialize_result(item) for item in result]
    return result  # если это просто строка, число и т.д.

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

            serialized = serialize_result(result)

            return JSONResponse(content={"status": "ok", "result": serialized})

        except AttributeError:
            raise HTTPException(status_code=400, detail=f"Unknown method: {method}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
