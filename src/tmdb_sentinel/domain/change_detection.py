from tmdb_sentinel.domain.change_event import ChangeEvent
from tmdb_sentinel.domain.snapshot import Snapshot


def detect_change(previous: Snapshot, current: Snapshot) -> ChangeEvent | None:
    if previous.person_id != current.person_id:
        raise ValueError("Snapshots must belong to the same person")

    if previous.biography == current.biography:
        return None

    return ChangeEvent(
        person_id=current.person_id,
        field="biography",
        previous_value=previous.biography,
        current_value=current.biography,
        detected_at=current.observed_at,
    )
