from dataclasses import dataclass


@dataclass
class RetrainingStatus:
    ready: bool
    labeled_feedback_count: int
    minimum_required: int
    message: str


class RetrainingTriggerService:
    """
    Reports whether the adaptive retraining pipeline has enough reviewed
    feedback to justify another training cycle.
    """

    def __init__(self, minimum_required: int = 100) -> None:
        self.minimum_required = minimum_required

    def evaluate(self, labeled_feedback_count: int) -> RetrainingStatus:
        ready = labeled_feedback_count >= self.minimum_required
        if ready:
            message = "Enough labeled feedback is available for adaptive retraining."
        else:
            remaining = self.minimum_required - labeled_feedback_count
            message = f"Not enough labeled feedback yet. Need {remaining} more reviewed samples."

        return RetrainingStatus(
            ready=ready,
            labeled_feedback_count=labeled_feedback_count,
            minimum_required=self.minimum_required,
            message=message,
        )
