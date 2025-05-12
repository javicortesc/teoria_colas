# 📊 Simulador de Teoría de Colas M/M/c para Terminales de Contenedores

Un simulador interactivo simple basado en Python y Tkinter para explorar los conceptos de la Teoría de Colas (modelo M/M/c) aplicados a la optimización de operaciones en un terminal de contenedores marítimos. 🚢

Este proyecto permite visualizar cómo diferentes parámetros de llegada y servicio afectan los tiempos de espera y la utilización de recursos, basándose en los conceptos y fórmulas presentadas en el documento **Aplicación de Teoría de Colas en un Terminal de Contenedores Marítimos.pdf**, incluido en este repositorio.

## ✨ Características Principales

*   **Interfaz Gráfica Intuitiva:** Fácil de usar gracias a Tkinter.
*   **Modelo M/M/c:** Simula un sistema de colas con:
    *   Llegadas que siguen una distribución de **P**oisson (M).
    *   Tiempos de servicio que siguen una distribución **E**xponencial (M).
    *   Múltiples **s**ervidores idénticos en paralelo (c).
*   **Parámetros Configurables:**
    *   **λ (Lambda):** Tasa de llegada de camiones (camiones/hora).
    *   **μ (Mu):** Tasa de servicio por servidor (camiones/hora/servidor).
    *   **c:** Número de servidores (grúas/puertas operativas).
*   **Cálculo de Indicadores Clave:**
    *   **ρ (Rho):** Utilización del sistema (%).
    *   **Lq:** Número medio de camiones esperando en la cola.
    *   **Wq:** Tiempo medio de espera en cola (en minutos).
    *   **Ws:** Tiempo total medio en el sistema (espera + servicio, en minutos).
*   **Ejecutable Incluido:** Versión `SimuladorColas.exe` para Windows. ¡No requiere instalación de Python!
*   **Basado en PDF:** Los cálculos y conceptos siguen el ejemplo proporcionado en el PDF adjunto.
*   **Detección de Inestabilidad:** Advierte si los parámetros introducidos (λ ≥ c\*μ) llevarían a una cola teóricamente infinita.

## 🚀 Cómo Usar

Tienes dos maneras de utilizar el simulador:

**Opción 1: Usar el Ejecutable (Recomendado para Windows)**

1.  Descarga el archivo `SimuladorColas.exe`.
2.  Haz doble clic sobre `SimuladorColas.exe`.
3.  Introduce los parámetros λ, μ y c deseados en la interfaz.
4.  Haz clic en "Calcular Indicadores" y observa los resultados.
5.  Puedes usar el botón "Valores Ejemplo PDF" para cargar los datos del ejemplo del documento.

**Opción 2: Ejecutar desde el Código Fuente (Requiere Python)**

1.  Asegúrate de tener Python 3 instalado en tu sistema.
2.  Clona o descarga este repositorio:
    ```bash
    git clone https://github.com/javicortesc/teoria_colas.git
    cd teoria_colas
    ```
3.  (Opcional pero recomendado) Crea y activa un entorno virtual:
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```
4.  El script `main.py` utiliza Tkinter, que normalmente viene incluido con Python, por lo que no deberías necesitar instalar paquetes adicionales.
5.  Ejecuta el script:
    ```bash
    python main.py
    ```
6.  Interactúa con la interfaz gráfica como en la Opción 1.

## 📚 Teoría y Contexto

Este simulador implementa un modelo M/M/c. Para una explicación detallada de la teoría de colas aplicada a este contexto específico de terminales de contenedores, las fórmulas utilizadas (incluyendo la aproximación para Lq mencionada en la interfaz) y el ejemplo numérico base, por favor consulta el documento PDF incluido:

*   **Aplicación de Teoría de Colas en un Terminal de Contenedores Marítimos** 

## ⚙️ Parámetros y Resultados (Resumen)

*   **Entradas (Parámetros):**
    *   `λ (Lambda)`: Frecuencia con la que llegan los camiones.
    *   `μ (Mu)`: Rapidez con la que *un* servidor (grúa/puerta) atiende a un camión.
    *   `c`: Número *total* de servidores (grúas/puertas) trabajando simultáneamente.
*   **Salidas (Indicadores Clave de Rendimiento - KPIs):**
    *   `ρ (Rho)`: Porcentaje del tiempo que los servidores están ocupados.
    *   `Lq`: Cantidad promedio de camiones en la cola de espera.
    *   `Wq`: Tiempo promedio que un camión espera en la cola.
    *   `Ws`: Tiempo promedio total que un camión pasa en el terminal (espera + atención).

## 🛠️ Construcción del Ejecutable

El archivo `SimuladorColas.exe` fue generado usando PyInstaller a partir de `main.py`. Si deseas modificar el código y generar tu propio ejecutable, puedes usar un comando similar a este (en Windows):

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="SimuladorColas" main.py
```
