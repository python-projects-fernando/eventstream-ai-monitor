# FR001: Event Reception

## Goal
Receive an event from an external source (e.g., HTTP webhook) and process it for storage and further handling.

## Actors
- External system (e.g., service emitting events)
- EventStream AI Monitor (system under development)

## Precondition
- The system is running and listening on the configured endpoint.
- The incoming event is valid JSON with required fields.

## Main Success Scenario
1. External system sends a POST request to `/events` with JSON payload
2. System validates the request format and content
3. System creates an `Event` entity from the payload
4. System processes the event (basic validation, timestamping, ID generation)
5. System returns HTTP 201 Created with event ID in response

## Alternative Flows
- **Invalid payload**: System returns HTTP 400 Bad Request with error details
- **Missing required fields**: System returns HTTP 400 Bad Request
- **Server error**: System returns HTTP 500 Internal Server Error

## Postconditions
- Event is created in memory (ready for persistence)
- Event ID is generated and returned to caller
- Event is ready for next steps (storage, AI processing, rule matching)

## Business Rules
- Event ID must be UUID v4
- Timestamp must be UTC
- Source and event_type are required fields
- Payload must be a JSON object

## Technical Constraints
- Must support at least 1000 events/minute during testing
- Latency should be ≤ 5 seconds under normal load
- No authentication required in MVP phase