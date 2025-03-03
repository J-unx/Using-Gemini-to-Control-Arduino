import tkinter as tk
from tkinter import messagebox
import os
import sounddevice as sd
import scipy.io.wavfile as wav
from datetime import datetime
import numpy as np
import time
import serial
import json
from google import genai

class Textovoz:
    def __init__(self):
        self.cliente = genai.Client(api_key="TU_API_KEY")
        self.carpeta = "temp"
        self.ultimo_audio = None
        self.stream = None
        self.audio_buffer = []  # Buffer para acumular datos de audio
        self.samplerate = 44100
        self.crear_directorios()
        self.promp = open("promp.txt").read()

    def crear_directorios(self):
        if not os.path.exists(self.carpeta):
            os.makedirs(self.carpeta)

    def limpiar_temp(self):
        try:
            with os.scandir(self.carpeta) as entries:
                for entry in entries:
                    if entry.is_file():
                        os.remove(entry.path)
        except Exception as e:
            print(f"Error al limpiar la carpeta: {e}")

    def generar_nombre(self):
        return datetime.now().strftime("%H%M%S") + ".wav"

    def callback_audio(self, indata, frames, time, status):
        if status:
            print(status)
        self.audio_buffer.append(indata.copy())

    def iniciar_grabacion(self):
        self.audio_buffer = []
        try:
            self.stream = sd.InputStream(
                samplerate=self.samplerate,
                channels=2,
                dtype='int16',
                callback=self.callback_audio
            )
            self.stream.start()
            print("Grabación iniciada")
        except Exception as e:
            print(f"Error al iniciar grabación: {e}")
            messagebox.showerror("Error", f"Error al iniciar grabación:\n{e}")

    def detener_grabacion(self, nombre_archivo):
        try:
            if self.stream is not None:
                self.stream.stop()
                self.stream.close()
                print("Grabación detenida")
        except Exception as e:
            print(f"Error al detener grabación: {e}")
            messagebox.showerror(f"Error al detener grabación:\n{e}")
        
        try:
            if self.audio_buffer:
                audio_data = np.concatenate(self.audio_buffer, axis=0)
                ruta = os.path.join(self.carpeta, nombre_archivo)
                wav.write(ruta, self.samplerate, audio_data)
                print(f"Audio guardado correctamente en {ruta}")
                self.ultimo_audio = ruta
            else:
                print("El buffer de audio está vacío")
                messagebox.showwarning("El buffer de audio está vacío")
        except Exception as e:
            print(f"Error al guardar audio: {e}")
            messagebox.showerror(f"Error al guardar audio:\n{e}")

    def gemini_voz(self):
        if self.ultimo_audio and os.path.exists(self.ultimo_audio):
            try:
                myfile = self.cliente.files.upload(file=self.ultimo_audio)
                response = self.cliente.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=[self.promp, myfile]
                )
                return response.text
            except Exception as e:
                print(f"Error en gemini_voz: {e}")
                messagebox.showerror("Error", f"Error en gemini_voz:\n{e}")
        else:
            messagebox.showwarning("Advertencia", "No se encontró un archivo de audio válido para procesar.")
            
    def mandar_info(self, comandos):
        try:
            ser = serial.Serial("COM3", 9600, timeout=1) # Aqui puedes cambiar el puerto en el cual tengas tu arduino,
            time.sleep(1)                                
            for cmd in comandos:
                cmd_str = f"{cmd['motor']},{cmd['direccion']},{cmd['duracion']}\n"
                ser.write(cmd_str.encode())
                print(f"Enviando comandos {cmd_str.strip()}")
                time.sleep(int(cmd['duracion']) / 1000.0 + 0.5)
            ser.close()
        except Exception as e:
            print(f"Error al enviar comandos: {e}")

    
    
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Grabación de Voz con Tkinter")
        self.geometry("400x200")
        self.textovoz = Textovoz()
        self.recording = False  
        self.crear_widgets()

    def crear_widgets(self):
        self.toggle_button = tk.Button(self, text="Iniciar Grabación", command=self.definir_estado, width=20, height=2)
        self.toggle_button.pack(pady=20)
        self.status_label = tk.Label(self, text="Presione el botón para iniciar la grabación")
        self.status_label.pack(pady=10)

    def definir_estado(self):
        if not self.recording:
            self.textovoz.iniciar_grabacion()
            self.recording = True
            self.toggle_button.config(text="Detener Grabación")
            self.status_label.config(text="Grabando...")
        else:
            nombre_archivo = self.textovoz.generar_nombre()
            self.textovoz.detener_grabacion(nombre_archivo)
            self.recording = False
            self.toggle_button.config(text="Iniciar Grabación")
            self.status_label.config(text=f"Grabación detenida y guardada como {nombre_archivo}")
            resultado = self.textovoz.gemini_voz()
            print(resultado)
            if resultado:
                try:
                    #cmss = 
                    comandos = json.loads(resultado)
                    self.textovoz.mandar_info(comandos)
                except Exception as e:
                    print(f"Error al procesar comando de gemini {e}")


def main():
    tex = Textovoz()
    tex.limpiar_temp()
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()
