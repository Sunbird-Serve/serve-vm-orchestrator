# serve-vm-orchestrator
Consumes domain events (e.g., volunteer.registered.v1) from the event bus.  Manages state machines for each run (onboarding, screening, fulfillment).  Ensures idempotency, persistence, retries, and emits next domain events.  Coordinates which agent should act next, but doesn’t do the actual work.
