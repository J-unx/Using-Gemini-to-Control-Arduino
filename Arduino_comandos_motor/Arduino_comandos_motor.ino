// ========================================================
// Arduino_comandos_motor.ino
// --------------------------------------------------------
// Descripción:
//   Controla dos motores (A y B) a través de comandos enviados
//   desde la PC por medio del puerto serial. Cada comando tiene
//   el formato: "motor,direccion,duracion"
//   Ejemplo de comando: "A,left,1000"
// --------------------------------------------------------
// Comandos:
//   - motor: "A" o "B"
//   - direccion: "left" o "right"
//   - duracion: duración en milisegundos (valor numérico)
// ========================================================

// Número de motores conectados
const int numMotores = 2; // Cantidad de motores

// Número de pines usados por cada motor (por defecto 2: IN1 e IN2)
const int pinsPorMotor = 2;

// Pines asignados a cada motor: [motor][pin]
// Motor A: pines 22 y 23
// Motor B: pines 24 y 25
const int motorPins[numMotores][pinsPorMotor] = {
  {22, 23}, // Motor A
  {24, 25}  // Motor B
};

void setup() {
  // Configuración de pines para cada motor como salidas
  for (int i = 0; i < numMotores; i++) {
    for (int j = 0; j < pinsPorMotor; j++) {
      pinMode(motorPins[i][j], OUTPUT);
      digitalWrite(motorPins[i][j], HIGH); // Se inicia en HIGH
    }
  }
  
  // Inicialización del puerto serial para recibir comandos
  Serial.begin(9600);
  Serial.println("Sistema iniciado. Esperando comandos...");
}

void loop() {
  // Verifica si hay datos disponibles en el puerto serial
  if (Serial.available() > 0) {
    // Lee la línea completa hasta encontrar un salto de línea
    String input = Serial.readStringUntil('\n');
    input.trim(); // Elimina espacios en blanco
    if (input.length() > 0) {
      processCommand(input); // Procesa el comando recibido
    }
  }
}

// Función para procesar y ejecutar el comando recibido
// Formato esperado: "motor,direccion,duracion"
// Ejemplo: "A,left,1000"
void processCommand(String command) {
  // Se buscan las comas que separan los distintos parámetros
  int index1 = command.indexOf(',');
  int index2 = command.indexOf(',', index1 + 1);
  
  // Validación del formato: deben existir dos comas
  if (index1 == -1 || index2 == -1) {
    Serial.println("Error: Formato incorrecto");
    return;
  }
  
  // Se extraen los parámetros: motor, dirección y duración
  String motorStr = command.substring(0, index1);
  String dirStr = command.substring(index1 + 1, index2);
  String durStr = command.substring(index2 + 1);
  
  // Convierte el parámetro de duración a un número (milisegundos)
  long duration = durStr.toInt();
  
  // Determina el índice del motor según el parámetro
  int motorIndex = -1;
  if (motorStr == "A") {
    motorIndex = 0;
  } else if (motorStr == "B") {
    motorIndex = 1;
  } else {
    Serial.println("Error: Motor desconocido");
    return;
  }
  
  // Imprime en el monitor serial los parámetros recibidos
  Serial.print("Ejecutando comando -> Motor: ");
  Serial.print(motorStr);
  Serial.print(" | Dirección: ");
  Serial.print(dirStr);
  Serial.print(" | Duración: ");
  Serial.println(duration);
  
  // Configura la dirección del motor
  if (dirStr == "left") {
    digitalWrite(motorPins[motorIndex][0], LOW);
    digitalWrite(motorPins[motorIndex][1], HIGH);
  } else if (dirStr == "right") {
    digitalWrite(motorPins[motorIndex][0], HIGH);
    digitalWrite(motorPins[motorIndex][1], LOW);
  } else {
    Serial.println("Error: Dirección desconocida");
    return;
  }
  
  // Mantiene el estado del motor por el tiempo especificado
  delay(duration);
  
  // Apaga ambos pines del motor para detenerlo
  digitalWrite(motorPins[motorIndex][0], LOW);
  digitalWrite(motorPins[motorIndex][1], LOW);
  
  Serial.println("Comando ejecutado.");
}
