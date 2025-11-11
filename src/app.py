from __future__ import annotations

import math
from typing import Any, Dict

from flask import Flask, jsonify

app = Flask(__name__)


def compute_factorial(value: int) -> int:
    """Compute factorial for non-negative integers."""
    if value < 0:
        raise ValueError("El factorial solo está definido para enteros no negativos.")
    return math.factorial(value)


def parity_label(value: int) -> str:
    return "par" if value % 2 == 0 else "impar"


@app.route("/api/numeros/<int:value>", methods=["GET"])
def obtener_informacion_numero(value: int) -> Any:
    try:
        return jsonify(
            {
                "numero": value,
                "factorial": compute_factorial(value),
                "etiqueta": parity_label(value),
            }
        )
    except ValueError as error:
        return jsonify({"error": str(error)}), 400


@app.route("/health", methods=["GET"])
def health_check() -> Dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True)

