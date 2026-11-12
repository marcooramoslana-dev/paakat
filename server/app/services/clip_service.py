import logging
from typing import List, Tuple

import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class CLIPService:
    """Clasificador zero-shot basado en CLIP (no requiere reentrenamiento)."""

    def __init__(self) -> None:
        self._model = None
        self._processor = None
        self._device = "cpu"
        self._loaded = False

    @property
    def loaded(self) -> bool:
        return self._loaded

    @property
    def device(self) -> str:
        return self._device

    def load(self) -> None:
        if self._loaded:
            return

        settings = get_settings()
        device = settings.clip_device
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"

        logger.info("Cargando CLIP '%s' en %s", settings.clip_model_name, device)
        self._model = CLIPModel.from_pretrained(settings.clip_model_name)
        self._model.to(device)
        self._model.eval()
        self._processor = CLIPProcessor.from_pretrained(settings.clip_model_name)
        self._device = device
        self._loaded = True
        logger.info("CLIP cargado correctamente")

    def classify(
        self,
        image: Image.Image,
        labels: List[str],
        prompts: List[str],
        top_k: int = 3,
    ) -> List[Tuple[str, float]]:
        """Devuelve [(label, prob), ...] ordenado de mayor a menor."""
        if not labels:
            return []
        self.load()

        inputs = self._processor(
            text=prompts,
            images=image.convert("RGB"),
            return_tensors="pt",
            padding=True,
        )
        inputs = {key: value.to(self._device) for key, value in inputs.items()}

        with torch.no_grad():
            logits = self._model(**inputs).logits_per_image

        probs = logits.softmax(dim=1)[0].detach().cpu().tolist()
        ranked = sorted(zip(labels, probs), key=lambda pair: pair[1], reverse=True)
        return [(label, float(prob)) for label, prob in ranked[: max(top_k, 1)]]


clip_service = CLIPService()
