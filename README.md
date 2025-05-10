# Sistema de reconocimiento de placas vehiculares en tiempo real con rasberry pi

Sistema embebido para Raspberry Pi que detecta y reconoce placas vehiculares usando visión por computadora y OCR. Procesa video en tiempo real, identifica regiones de interés, y determina la placa más frecuente usando análisis estadístico.

## Características Principales
- Captura de video en tiempo real con ajuste de cámara.
- Detección de placas usando modelos de Roboflow.
- Recorte automático de regiones detectadas.
- Procesamiento por lotes con OCR integrado.
- Determinación de placa más común por moda estadística.
- Configuración flexible mediante variables de entorno.

## Estructura del Proyecto
- `plate_detector.py`: Archivo de ejecución princiapl.
- `plate_results.txt`: Se utiliza para procesar las imagenes y detectar los textos.
- `cropped_plates/`: Carpeta creada dentro del código y se utiliza para almacenar las placas recortadas.
- `plate_results.txt`: Archivo donde se guardan los resultados del OCR

## Requisitos Previos

### Hardware
- Raspberry Pi 4B (4GB RAM o superior recomendado)
- Cámara compatible (USB o módulo oficial Raspberry Pi)
- Almacenamiento: Mínimo 16GB SD Card (Clase 10 recomendada)
- Conexión a internet para descarga de modelos
- Cuenta para consumo de API en https://universe.roboflow.com/

### Software
- Raspberry Pi OS (64-bit)
- Python 3.11+
- pip 23.0+
- git 2.35+

## Instalación paso a paso

### 1. Clonar Repositorio
```bash
sudo apt-get update && sudo apt-get upgrade -y
git clone https://github.com/HamiltonDiaz/detector-placas-rasberry.git
cd detector-placas-rasberry
```

### 2. Crear archivo .env y agregar la siguiente información
```text
ROBOFLOW_API_URL="https://serverless.roboflow.com"
ROBOFLOW_API_KEY="tu_api_key_aqui/1234567890"
OCR_MODEL_ID="license-ocr-qqq6v/3"
PLATE_DETECTION_MODEL_ID="reconocimiento_de_placas/1"
```

### 3. Configuración y activación del entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip3 install inference-sdk python-dotenv opencv-python 
```

## Ejecución
Estando ubicado dentro de la raíz del proyecto y en el entorno virtual ejecutar:
```bash
python3 plate_detector.py
```



