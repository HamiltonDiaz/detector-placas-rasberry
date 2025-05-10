"""
Módulo de configuración: carga variables de entorno y configuraciones globales.
"""
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    """Clase que almacena todas las configuraciones de la aplicación"""
    API_URL = os.getenv("ROBOFLOW_API_URL")
    API_KEY = os.getenv("ROBOFLOW_API_KEY")
    OCR_MODEL = os.getenv("OCR_MODEL_ID")
    PLATE_DETECTION_MODEL = os.getenv("PLATE_DETECTION_MODEL_ID")
    RESULTS_FILE = "plate_results.txt"
    OUTPUT_DIR = "cropped_plates"
    CAMERA_INDEX = 0  # 0 para cámara predeterminada
    PROCESSING_BATCH_SIZE = 15
    MIN_CHARACTER_DISTANCE = 15  # Distancia mínima entre caracteres en píxeles
