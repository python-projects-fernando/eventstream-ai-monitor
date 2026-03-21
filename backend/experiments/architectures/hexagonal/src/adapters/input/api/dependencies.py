from fastapi import Depends

from core.application.ports.output import EventRepositoryOutputPort
from core.application.use_cases import ProcessEventUseCase
from adapters.output.database.postgres_dependencies import get_postgresql_event_repository


def get_process_event_use_case(
    event_repo: EventRepositoryOutputPort = Depends(get_postgresql_event_repository)
):
    return ProcessEventUseCase(event_repository=event_repo)