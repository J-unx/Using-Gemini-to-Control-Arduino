#  Control de Motores por Voz sin comandos pre programados

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Arduino-Compatible-brightgreen.svg" alt="Arduino Compatible">
  <img src="https://img.shields.io/badge/Gemini%20API-Powered-orange.svg" alt="Gemini API">
</div>

##  Descripción

Este proyecto es un sistema integrado que permite controlar motores físicos a través de comandos de voz. La aplicación graba tu voz, la procesa utilizando la API de Gemini 2.0, y traduce las instrucciones verbales en comandos para motores Arduino.

El sistema consta de tres componentes principales:
- Una aplicación de Python para grabar y procesar audio
- Un backend de procesamiento de lenguaje natural con Gemini AI
- Un sketch de Arduino para controlar los motores físicos

##  Características

-  Grabación de voz en tiempo real
-  Procesamiento mediante Gemini AI
- Control de motores dual (A y B)
-  Instrucciones de dirección (izquierda/derecha)
-  Control de duración para cada movimiento

## Requisitos previos

### Hardware
- Placa Arduino
- 2 motores DC con controlador (L298N o similar)
- Cables de conexión
- Micrófono para PC

### Software
- Python 3.8+
- Arduino IDE
- Bibliotecas necesarias (ver instalación)

##  Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/J-unx/Using-Gemini-to-Control-Arduino.git
```

### 2. Crear un entorno virtual (recomendado)

#### En Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### En macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Arduino

1. Abrir Arduino IDE
2. Cargar el archivo `Arduino_comandos_motor.ino`
3. Seleccionar la placa y puerto correctos
4. Subir el código a la placa

### 5. Configurar la API de Gemini

1. Obtén una clave API de Gemini en [Google AI Studio](https://ai.google.dev/)
2. Reemplaza la clave en el archivo `main.py`:
   ```python
   self.cliente = genai.Client(api_key="TU_CLAVE_API_AQUI")
   ```

##  Uso

1. Conecta tu Arduino al puerto USB
2. Asegúrate de que el puerto COM en `main.py` sea el correcto:
   ```python
   ser = serial.Serial("COM3", 9600, timeout=1)  # Ajusta según tu sistema
   ```
3. Ejecuta la aplicación:
   ```bash
   python main.py
   ```
4. Presiona el botón "Iniciar Grabación" y habla claramente
5. Presiona "Detener Grabación" para procesar tu comando

### Comandos de voz de ejemplo

- "Mueve el motor A a la izquierda durante 5 segundos"
- "Motor B a la derecha por 2 segundos"
- "Motor A y B a la izquierda por 3 segundos"

##  Archivo requirements.txt

Instala los paquetes del archivo `requirements.txt` :

```cmd
pip install -r requirements.txt   
```

##  Configuración de pines Arduino

El código está configurado para usar los siguientes pines en Arduino:
- Motor A: Pines 22, 23
- Motor B: Pines 24, 25

Puedes modificar esta configuración en el archivo `Arduino_comandos_motor.ino`:

```cpp
const int motorPins[numMotores][pinsPorMotor] = {
  {22, 23}, // Motor A
  {24, 25}  // Motor B
};
```

##  Notas sobre el desarrollo

El archivo `Arduino_comandos_motor.ino` fue generado completamente con IA.

## ⚠️ Solución de problemas

- **Error de puerto COM**: Asegúrate de usar el puerto correcto en la línea `ser = serial.Serial("COM3", 9600, timeout=1)`
- **No se detecta el micrófono**: Verifica la configuración de audio de tu sistema
- **Error de API**: Verifica que la clave de API sea válida y esté correctamente configurada

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cualquier cambio que te gustaría realizar (O propuesta de implementacion de este proyecto).
