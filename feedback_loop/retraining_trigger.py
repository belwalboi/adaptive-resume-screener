from dataclasses import dataclass


@dataclass
class RetrainingStatus:
    ready: bool
    labeled_feedback_count: int
    minimum_required: int
    message: str


class RetrainingTriggerService:
    """
    Placeholder retraining gate.
    For now, this only reports readiness based on labeled feedback volume.
    """

    def __init__(self, minimum_required: int = 100) -> None:
        self.minimum_required = minimum_required

    def evaluate(self, labeled_feedback_count: int) -> RetrainingStatus:
        ready = labeled_feedback_count >= self.minimum_required
        if ready:
            message = "Retraining threshold reached. Integrate your pipeline trigger here."
        else:
            remaining = self.minimum_required - labeled_feedback_count
            message = f"Not enough labeled feedback yet. Need {remaining} more samples."

        return RetrainingStatus(
            ready=ready,
            labeled_feedback_count=labeled_feedback_count,
            minimum_required=self.minimum_required,
            message=message,
        )
