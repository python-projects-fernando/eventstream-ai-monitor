from fastapi import APIRouter, Depends, status, HTTPException

from core.application.ports.input import ProcessEventInputPort
from .schemas import EventRequestSchema, EventResponseSchema
from .dependencies import get_process_event_use_case

router = APIRouter(tags=["events"])

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=EventResponseSchema,
    summary="Create a new event",
    description="Receive an event from an external source and process it."
)
async def handle_create_event(
    event_data: EventRequestSchema,
    process_event_uc: ProcessEventInputPort = Depends(get_process_event_use_case)
):
    try:
        processed_event = await process_event_uc.process(
            source=event_data.source,
            event_type=event_data.event_type,
            payload=event_data.payload
        )
        return EventResponseSchema.model_validate(processed_event)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process event: {str(e)}"
        )