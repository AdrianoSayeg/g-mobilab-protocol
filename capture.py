import time
import serial

PUERTO = "/dev/rfcomm0"
SALIDA = "datos_reales.bin"
DURACION_S = 5
MASCARA = b"\xff\x00\xff"  # 8 canales analogicos


def enviar(ser, datos, esperado):
    """Envia bytes y avisa (sin abortar) si la respuesta no es la esperada."""
    ser.write(datos)
    resp = ser.read(len(esperado))  # usa el timeout del puerto
    if resp != esperado:
        print(f"AVISO: tras {datos.hex(' ')} esperaba {esperado.hex(' ')} y llego {resp.hex(' ')}")


ser = serial.Serial(PUERTO, timeout=1)
datos = bytearray()
try:
    # GT_OpenDevice
    enviar(ser, b"\x78\x7a\x76", b"\x2b")
    enviar(ser, b"\x76", b"\x2b")

    # GT_InitChannels
    enviar(ser, b"\x76", b"\x2b")
    enviar(ser, b"\x43" + MASCARA, b"\x43")

    ser.reset_input_buffer()

    # START
    ser.write(b"\x61")
    fin = time.time() + DURACION_S
    while time.time() < fin:
        # bloquea hasta que llegue al menos 1 byte (o venza el timeout)
        datos.extend(ser.read(max(1, ser.in_waiting)))

    # STOP + cierre (0x62 0x76 seguidos, como en tu documento).
    # Hasta que el amplificador responda, aun pueden llegar bytes del flujo,
    # asi que se lee todo y se revisa que termine en cinco 0x2b.
    ser.write(b"\x62\x76")
    cola = bytearray()
    limite = time.time() + 1.0
    while time.time() < limite:
        cola.extend(ser.read(max(1, ser.in_waiting)))
    if not cola.endswith(b"\x2b" * 5):
        print(f"AVISO: el cierre no termino en cinco 0x2b; ultimos bytes: {bytes(cola[-8:]).hex(' ')}")
finally:
    ser.close()  # siempre se cierra el puerto, aunque haya un error

with open(SALIDA, "wb") as f:
    f.write(datos)
print(f"{len(datos)} bytes guardados en {SALIDA}")
