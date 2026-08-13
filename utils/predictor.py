"""Prediction utilities for GridGuard AI."""

from typing import Any

import numpy as np
import pandas as pd
import xgboost as xgb


DEFAULT_CLASS_MAPPING = {
    0: "Critical",
    1: "Poor",
    2: "Good",
    3: "Excellent",
}


def normalize_class_mapping(
    class_mapping: dict[str, Any] | dict[int, Any] | None,
) -> dict[int, str]:
    """Convert metadata class keys to integer labels."""

    if not class_mapping:
        return DEFAULT_CLASS_MAPPING.copy()

    normalized_mapping: dict[int, str] = {}

    for key, value in class_mapping.items():
        normalized_mapping[int(key)] = str(value)

    return normalized_mapping


def create_input_dataframe(
    feature_values: dict[str, float],
    feature_names: list[str],
) -> pd.DataFrame:
    """Create a one-row DataFrame in the model's feature order."""

    missing_features = [
        feature
        for feature in feature_names
        if feature not in feature_values
    ]

    if missing_features:
        raise ValueError(
            "Missing feature values: "
            + ", ".join(missing_features)
        )

    ordered_values = {
        feature: float(feature_values[feature])
        for feature in feature_names
    }

    return pd.DataFrame([ordered_values])


def predict_transformer_health(
    model: xgb.XGBClassifier,
    input_data: pd.DataFrame,
    class_mapping: dict[int, str],
) -> dict[str, Any]:
    """Generate a predicted class and class probabilities."""

    predicted_label = int(model.predict(input_data)[0])

    probability_array = np.asarray(
        model.predict_proba(input_data)[0],
        dtype=float,
    )

    probabilities = {
        class_mapping.get(
            class_index,
            f"Class {class_index}",
        ): float(probability)
        for class_index, probability in enumerate(
            probability_array
        )
    }

    predicted_class = class_mapping.get(
        predicted_label,
        f"Class {predicted_label}",
    )

    confidence = float(
        probability_array[predicted_label]
    )

    return {
        "predicted_label": predicted_label,
        "predicted_class": predicted_class,
        "confidence": confidence,
        "probabilities": probabilities,
        "input_data": input_data,
    }


def get_maintenance_guidance(
    predicted_class: str,
) -> list[str]:
    """Return condition-based maintenance recommendations."""

    recommendations = {
        "Critical": [
            "Arrange immediate technical inspection.",
            "Repeat dissolved-gas analysis to verify the condition.",
            "Prepare the transformer for urgent corrective maintenance.",
            "Increase monitoring frequency until the fault is resolved.",
        ],
        "Poor": [
            "Schedule a detailed condition assessment.",
            "Repeat oil and dissolved-gas testing within a short interval.",
            "Investigate abnormal gases and oil-quality indicators.",
            "Plan preventive maintenance before further deterioration.",
        ],
        "Good": [
            "Continue scheduled preventive maintenance.",
            "Monitor important gas and oil-quality trends.",
            "Repeat diagnostic testing at the normal maintenance interval.",
            "Investigate any rapidly changing measurement trends.",
        ],
        "Excellent": [
            "Continue routine transformer monitoring.",
            "Maintain the existing preventive-maintenance schedule.",
            "Perform periodic dissolved-gas and oil-quality testing.",
            "Retain the current measurement as a healthy baseline.",
        ],
    }

    return recommendations.get(
        predicted_class,
        [
            "Review the transformer measurements.",
            "Seek further technical assessment.",
        ],
    )