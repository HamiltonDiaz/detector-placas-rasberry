"""
Módulo para lectura de texto en placas detectadas usando OCR.

Funcionalidades principales:
- Procesa imágenes de placas recortadas
- Extrae texto usando modelo de OCR
- Elimina duplicados y caracteres no válidos
- Guarda resultados en archivo de texto
"""
import glob
import os
import cv2
from inference_sdk import InferenceHTTPClient
from config import Config
from collections import defaultdict

class PlateTextReader:
    """Clase para manejar la lectura de texto en placas detectadas"""
    
    def __init__(self):
        self.config = Config()
        self.client = InferenceHTTPClient(
            api_url=self.config.API_URL,
            api_key=self.config.API_KEY
        )
        
    def _process_predictions(self, predictions):
        """Procesa las predicciones del modelo OCR y extrae caracteres válidos"""
        characters = []
        for prediction in predictions.get('predictions', []):
            x = int(prediction['x'] - prediction['width'] / 2)
            char = prediction['class'].upper()
            
            if char.isalnum():
                characters.append((x, char))
        
        return sorted(characters, key=lambda x: x[0])
    
    def _remove_duplicates(self, characters):
        """Elimina caracteres duplicados y agrupa cercanos"""
        filtered = []
        prev_x = -self.config.MIN_CHARACTER_DISTANCE
        
        for x, char in characters:
            if x - prev_x > self.config.MIN_CHARACTER_DISTANCE:
                filtered.append(char)
                prev_x = x
        return filtered
    
    def process_plate_images(self):
        """Procesa todas las imágenes de placas en el directorio de salida"""
        plate_images = sorted(glob.glob(os.path.join(self.config.OUTPUT_DIR, "plate_*.jpg")))
        
        with open(self.config.RESULTS_FILE, 'a', encoding='utf-8') as results_file:
            for img_path in plate_images:
                result = self.client.infer(img_path, model_id=self.config.OCR_MODEL)
                raw_characters = self._process_predictions(result)
                cleaned_text = self._remove_duplicates(raw_characters)
                plate_text = ''.join(cleaned_text[:6])  # Asume placas de 6 caracteres
                
                print(f"{os.path.basename(img_path)}: {plate_text}")
                results_file.write(f"{os.path.basename(img_path)}: {plate_text}\n")
        
        self._cleanup_processed_images(plate_images)
    
    def _cleanup_processed_images(self, processed_images):
        """Elimina las imágenes ya procesadas"""
        for img_path in processed_images:
            try:
                os.remove(img_path)
            except Exception as e:
                print(f"Error eliminando {img_path}: {str(e)}")

if __name__ == "__main__":
    reader = PlateTextReader()
    reader.process_plate_images()
    print(f"Resultados guardados en {Config.RESULTS_FILE}")