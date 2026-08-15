from pathlib import Path
from datetime import datetime
import joblib
import json


# Diretórios
EXPORTS_DIR = Path("exports")
MODELS_DIR = EXPORTS_DIR / "models"

MODELS_DIR.mkdir(parents=True, exist_ok=True)


def save_model(model, model_name: str = "modelo", metadata: dict | None = None):
    """
    Salva um modelo treinado e seus metadados.
    """

    model_path = MODELS_DIR / f"{model_name}.pkl"
    metadata_path = MODELS_DIR / f"{model_name}.json"

    joblib.dump(model, model_path)

    info = {
        "nome": model_name,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "arquivo": str(model_path),
    }

    if metadata:
        info.update(metadata)

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=4, ensure_ascii=False)

    return model_path


def load_model(model_name: str = "modelo"):
    """
    Carrega um modelo salvo.
    """

    model_path = MODELS_DIR / f"{model_name}.pkl"

    if not model_path.exists():
        raise FileNotFoundError(f"Modelo '{model_name}' não encontrado.")

    return joblib.load(model_path)


def list_models():
    """
    Lista todos os modelos disponíveis.
    """

    return sorted(arquivo.stem for arquivo in MODELS_DIR.glob("*.pkl"))


def load_metadata(model_name: str = "modelo"):
    """
    Carrega os metadados de um modelo.
    """

    metadata_path = MODELS_DIR / f"{model_name}.json"

    if not metadata_path.exists():
        return None

    with open(metadata_path, "r", encoding="utf-8") as f:
        return json.load(f)


def delete_model(model_name: str):
    """
    Remove um modelo salvo.
    """

    model_path = MODELS_DIR / f"{model_name}.pkl"
    metadata_path = MODELS_DIR / f"{model_name}.json"

    if model_path.exists():
        model_path.unlink()

    if metadata_path.exists():
        metadata_path.unlink()
