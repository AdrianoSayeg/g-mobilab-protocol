import sys
import numpy as np
import matplotlib.pyplot as plt

ARCHIVO = sys.argv[1] if len(sys.argv) > 1 else "datos_reales.bin"
N_CANALES = 8
OFFSET_BYTES = 0   # ajusta a mano si el flujo no empieza alineado (debe ser PAR)
FS = 250           # frecuencia de muestreo en Hz
N_MUESTRAS = 250

datos = np.fromfile(ARCHIVO, dtype=np.uint8)


def inicio_senal(d):
    """Indice del primer byte tras el marcador 0x43 0x2b 0x2b, o None."""
    for i in range(2, len(d)):
        if d[i] == 0x2B and d[i - 1] == 0x2B and d[i - 2] == 0x43:
            return i + 1
    return None


ini = inicio_senal(datos)
if ini is not None:
    print(f"La senal empieza en el byte {ini}")
else:
    ini = OFFSET_BYTES
    print(f"Sin marcador; uso OFFSET_BYTES={ini}")

util = datos[ini:]
# Un numero entero de tramas: N_CANALES muestras de 2 bytes cada una
bytes_trama = N_CANALES * 2
util = util[: (len(util) // bytes_trama) * bytes_trama]
senal = util.view("<i2").reshape(-1, N_CANALES)  # una fila por muestra

n = min(N_MUESTRAS, len(senal))
print(f"{len(senal)} muestras por canal ({len(senal) / FS:.2f} s a {FS} Hz); se grafican {n}")
t = np.arange(n) / FS
fig, ax = plt.subplots(N_CANALES, 1, figsize=(12, 10), sharex=True)
for c in range(N_CANALES):
    ax[c].plot(t, senal[:n, c])
    ax[c].set_ylabel(f"Ch{c + 1}")
    ax[c].grid(True)
ax[-1].set_xlabel("s")
plt.tight_layout()
plt.show()
