# tools/publish_registered.py
import sys, json, time, os, asyncio
from aiokafka import AIOKafkaProducer

BROKERS = os.getenv("KAFKA_BROKERS", "localhost:19092")
TOPIC = os.getenv("TOPIC_INBOUND", "serve.vm.inbound")

async def main(vol_id, mobile, locale):
    print(f"Using brokers: {BROKERS}  topic: {TOPIC}")
    producer = AIOKafkaProducer(
        bootstrap_servers=BROKERS,
        value_serializer=lambda v: json.dumps(v).encode(),
        key_serializer=lambda k: k.encode()
    )
    await producer.start()
    try:
        evt = {
            "type":"volunteer.registered.v1",
            "id":"dev-"+vol_id,
            "time":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "source":"dev",
            "datacontenttype":"application/json",
            "data":{"volunteer_id":vol_id, "mobile":mobile, "locale":locale, "tenant":"UP"}
        }
        await producer.send_and_wait(TOPIC, key=vol_id, value=evt)
        print("Published volunteer.registered.v1 for", vol_id)
    finally:
        await producer.stop()

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv)>3 else "en-IN"))
