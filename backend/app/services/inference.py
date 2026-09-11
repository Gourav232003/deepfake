"""
Model inference wiring for image/video face classification.

STATUS: PLACEHOLDER. Per ImplementationPlan.md item 1 ("Model provenance"),
this scaffold does NOT ship a trained EfficientNet-B0 weight file — training
on FaceForensics++/Celeb-DF/DFDC is a separate, substantial effort. This
module defines the real interface the rest of the app depends on, backed by
an untrained network, so the full pipeline (upload -> faces -> preprocess ->
"classify" -> Grad-CAM -> UI) is demonstrable end-to-end.

Every response that flows from here must be labeled as coming from an
untrained/placeholder model — never presented as a real accuracy claim.
This module must be swapped for real trained weights before any accuracy
claim is made to a user. See Rules.md: "Never fabricate model performance."
"""
from dataclasses import dataclass

import torch
import torch.nn as nn
from torchvision.models import efficientnet_b0

PLACEHOLDER_MODEL_NOTICE = (
    "This result was produced by an untrained placeholder model for "
    "pipeline demonstration purposes and is not a real accuracy claim."
)


@dataclass
class FacePrediction:
    probability_fake: float
    model_notice: str


class DeepfakeImageClassifier:
    """
    Wraps an EfficientNet-B0 backbone with a binary classification head.
    Loads real trained weights if a checkpoint path is configured; otherwise
    falls back to randomly-initialized weights and flags every result as a
    placeholder.
    """

    def __init__(self, checkpoint_path: str | None = None, device: str = "cpu"):
        self.device = device
        self.is_placeholder = checkpoint_path is None
        self.model = efficientnet_b0(weights=None)
        in_features = self.model.classifier[1].in_features
        self.model.classifier[1] = nn.Linear(in_features, 1)  # single logit: P(fake)

        if checkpoint_path:
            state_dict = torch.load(checkpoint_path, map_location=device)
            self.model.load_state_dict(state_dict)

        self.model.eval()
        self.model.to(device)

    @torch.no_grad()
    def predict(self, face_tensor: torch.Tensor) -> FacePrediction:
        """
        face_tensor: preprocessed face, shape (1, 3, 224, 224), already
        normalized to the model's expected input distribution.
        """
        logit = self.model(face_tensor.to(self.device))
        probability_fake = torch.sigmoid(logit).item()
        return FacePrediction(
            probability_fake=probability_fake,
            model_notice=PLACEHOLDER_MODEL_NOTICE if self.is_placeholder else "",
        )


def aggregate_video_probability(frame_probabilities: list[float]) -> float:
    """
    Fixed aggregation formula per PRD.md / Rules.md — do not substitute
    another aggregation method without updating both docs and this comment.

        final_probability = 0.6 * mean(frame_probabilities)
                           + 0.4 * max(frame_probabilities)
    """
    if not frame_probabilities:
        raise ValueError("Cannot aggregate an empty list of frame probabilities.")
    mean_p = sum(frame_probabilities) / len(frame_probabilities)
    max_p = max(frame_probabilities)
    return 0.6 * mean_p + 0.4 * max_p
