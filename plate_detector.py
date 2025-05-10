"""
Módulo principal para detección de placas en tiempo real.

Funcionalidades:
- Captura video de cámara
- Detecta placas usando modelo de visión por computadora
- Recorta y guarda regiones detectadas
- Ejecuta OCR periódicamente en lotes de placas
- Calcula placa más frecuente por moda
"""
import cv2
import os
import subprocess
import sys
from inference_sdk import InferenceHTTPClient
from config import Config
from collections import Counter

class PlateDetector:
    """Clase principal para detección de placas en tiempo real"""
    
    def __init__(self):
        self.config = Config()
        self.client = InferenceHTTPClient(
            api_url=self.config.API_URL,
            api_key=self.config.API_KEY
        )
        self.frame_count = 0
        self.camera = cv2.VideoCapture(self.config.CAMERA_INDEX)
        os.makedirs(self.config.OUTPUT_DIR, exist_ok=True)
    
    def _process_frame(self, frame):
        """Procesa un frame individual buscando placas"""
        temp_file = "temp_frame.jpg"
        cv2.imwrite(temp_file, frame)
        
        
        predictions = self.client.infer(temp_file, model_id=self.config.PLATE_DETECTION_MODEL)
        best_plate = self._get_best_plate(predictions)
        
        if best_plate:
            self._save_cropped_plate(best_plate, frame) 
            self._process_batch_if_needed()
        print("_process_frame")
        os.remove(temp_file)
    
    def _get_best_plate(self, predictions):
        print(f"\n🔍 Respuesta completa del modelo:\n{predictions}")  # Debug clave
        best_plate = None
        best_confidence = 0.0
        
        for pred in predictions.get('predictions', []):
            if pred.get('class') == 'license-plate':
                # Verificar claves existentes
                if 'x' not in pred or 'y' not in pred or 'width' not in pred or 'height' not in pred:
                    print("⚠️ Predicción no contiene coordenadas válidas")
                    continue
                    
                confidence = pred.get('confidence', 0.0)
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_plate = pred
        
        return best_plate
    
    def _save_cropped_plate(self, plate_data, frame):
        """Guarda la región usando coordenadas directas"""
        try:
            x_center = plate_data['x']
            y_center = plate_data['y']
            width = plate_data['width']
            height = plate_data['height']
            
            x1 = int(x_center - width / 2)
            y1 = int(y_center - height / 2)
            x2 = int(x_center + width / 2)
            y2 = int(y_center + height / 2)
            
            cropped = frame[y1:y2, x1:x2]
            save_path = os.path.join(self.config.OUTPUT_DIR, f"plate_{self.frame_count}.jpg")
            cv2.imwrite(save_path, cropped)
            self.frame_count += 1
            print(f"✅ Placa recortada guardada: {save_path}")
            
        except KeyError as e:
            print(f"❌ Error: Clave faltante en los datos - {str(e)}")
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
    
    def _process_batch_if_needed(self):
        """Ejecuta OCR cuando se acumula un lote de placas"""
        if self.frame_count % self.config.PROCESSING_BATCH_SIZE == 0:
            print(f"Procesando lote de {self.config.PROCESSING_BATCH_SIZE} placas...")
            subprocess.run([sys.executable, "plate_text_reader.py"], check=True)
            self._show_most_common_plate()
            print("_process_batch_if_needed")
    
    def _show_most_common_plate(self):
        """Muestra la placa más frecuente del último lote"""
        try:
            with open(self.config.RESULTS_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()[-self.config.PROCESSING_BATCH_SIZE:]
            
            plates = [line.split(": ")[-1].strip() for line in lines if ": " in line]
            if plates:
                counter = Counter(plates)
                most_common = counter.most_common(1)[0][0]
                print(f"\nPlaca más detectada: {most_common}\n")

            print("_show_most_common_plate")
        except FileNotFoundError:
            print("Archivo de resultados no encontrado")
    
    def run(self):
        """Inicia el loop principal de captura de video"""
        print("Sistema activo - Presione 'Q' para salir")
        try:
            while True:
                ret, frame = self.camera.read()
                if not ret:
                    break
                
                self._process_frame(frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            self.camera.release()
            cv2.destroyAllWindows()
            print(f"Total de placas procesadas: {self.frame_count}")

if __name__ == "__main__":
    detector = PlateDetector()
    detector.run()
