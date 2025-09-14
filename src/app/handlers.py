import time, uuid
from .bus import bus
from .settings import settings

async def handle_registered(evt: dict, key: str | None):
    if evt.get("type") != "volunteer.registered.v1":
        return
    data = evt.get("data", {})
    vid = data.get("volunteer_id")
    mobile = data.get("mobile")
    locale = data.get("locale", "en-IN")
    if not vid: return

    # Emit onboarding start task (agent will welcome + collect profile)
    task = {
        "type": "onboarding.task.start.v1",
        "id": str(uuid.uuid4()),
        "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "data": {"volunteer_id": vid, "mobile": mobile, "locale": locale}
    }
    await bus.publish(settings.TOPIC_ONBOARDING, key=vid, value=task)