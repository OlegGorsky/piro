from fastapi import APIRouter, Request, HTTPException, Header
from fastapi.responses import JSONResponse
from telegram_client import app as tg
import os
import types

router = APIRouter()


def serialize_result(result):
    # Сериализуем объект с __dict__, исключая приватные поля
    if hasattr(result, "__dict__"):
        return {
            k: v for k, v in result.__dict__.items()
            if not k.startswith("_")
        }
    # Список объектов — сериализуем каждый элемент
    elif isinstance(result, list):
        return [serialize_result(item) for item in result]
    return result


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
            response = func(**params)

            # Если метод вернул async generator — собираем первые 20 элементов
            if isinstance(response, types.AsyncGeneratorType):
                result = []
                i = 0
                async for item in response:
                    result.append(serialize_result(item))
                    i += 1
                    if i >= 20:
                        break
            else:
                result = serialize_result(await response)

            return JSONResponse(content={"status": "ok", "result": result})

        except AttributeError:
            raise HTTPException(status_code=400, detail=f"Unknown method: {method}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
