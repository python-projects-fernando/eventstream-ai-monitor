from fastapi import APIRouter, HTTPException, status
from core.application.ports.input import ProcessEventInputPort
from .schemas.event_schemas import EventRequestSchema, EventResponseSchema


class EventController:
    """
    API adapter for handling event-related endpoints.

    This adapter connects external HTTP requests to the core application
    use cases, implementing the hexagonal architecture pattern.
    """

    def __init__(self, process_event_use_case: ProcessEventInputPort):
        """
        Initialize the controller with the required use case dependency.

        Args:
            process_event_use_case: The use case for processing events
        """
        self._process_event_use_case = process_event_use_case
        self.router = APIRouter()
        self._setup_routes()

    def _setup_routes(self):
        """Configure the API routes for event handling."""
        self.router.add_api_route(
            "/events",
            self._handle_create_event,
            methods=["POST"],
            status_code=status.HTTP_201_CREATED,
            response_model=EventResponseSchema,
            summary="Create a new event",
            description="Receive an event from an external source and process it."
        )

    async def _handle_create_event(self, event_data: EventRequestSchema) -> EventResponseSchema:
        """
        Handle the creation of a new event via HTTP POST.

        Args:
            event_data: The event data received from the request body

        Returns:
            The processed event with assigned ID and timestamp

        Raises:
            HTTPException: If the event data is invalid or processing fails
        """
        try:
            processed_event = await self._process_event_use_case.process(
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