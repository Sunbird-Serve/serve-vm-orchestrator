import asyncio, uvicorn, logging
from fastapi import FastAPI
from .settings import settings
from .bus import bus
from .handlers import handle_registered

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
app = FastAPI(title="serve-vm-orchestrator")

@app.get("/healthz")
def healthz(): return {"ok": True}

async def consume_loop():
    await bus.start_producer()
    await bus.start_consumer(settings.TOPIC_INBOUND, group_id=settings.SERVICE_NAME)
    try:
        async for msg in bus.consumer:
            evt, key = msg.value, msg.key
            try:
                await handle_registered(evt, key)
            except Exception:
                logging.exception("error handling message")
    finally:
        await bus.stop()

@app.on_event("startup")
async def on_startup():
    app.state.task = asyncio.create_task(consume_loop())

@app.on_event("shutdown")
async def on_shutdown():
    app.state.task.cancel()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT)