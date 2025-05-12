import tkinter as tk
from tkinter import ttk, messagebox

# --- Lógica del simulador (la misma que antes) ---
def calculate_queue_metrics(lambda_val, mu_val, c_val):
    """
    Calcula las métricas de la teoría de colas para un modelo M/M/c
    basándose en las fórmulas simplificadas del PDF.
    """
    if lambda_val <= 0 or mu_val <= 0 or c_val <= 0:
        return None, "Lambda (λ), mu (μ), y c deben ser valores positivos."
    if not isinstance(c_val, int):
        return None, "El número de servidores (c) debe ser un entero."

    if lambda_val >= c_val * mu_val:
        error_msg = (
            f"¡SISTEMA INESTABLE!\n"
            f"Tasa de llegada (λ={lambda_val:.2f}) es mayor o igual a la capacidad total "
            f"de servicio (c*μ = {c_val*mu_val:.2f}).\n"
            "La cola tendería a crecer indefinidamente. Ajuste los parámetros."
        )
        return None, error_msg

    rho = lambda_val / (c_val * mu_val)
    denominator_Lq = (c_val * mu_val) * (c_val * mu_val - lambda_val)

    if denominator_Lq <= 0:
        # Esta condición debería estar cubierta por la comprobación de estabilidad,
        # pero es una salvaguarda adicional.
        return None, "Error en el cálculo del denominador de Lq. Sistema inestable."

    Lq = (lambda_val**2) / denominator_Lq
    Wq_hours = Lq / lambda_val
    Wq_minutes = Wq_hours * 60
    service_time_hours = 1 / mu_val
    Ws_hours = Wq_hours + service_time_hours
    Ws_minutes = Ws_hours * 60

    return {
        "rho": rho,
        "Lq": Lq,
        "Wq_minutes": Wq_minutes,
        "Ws_minutes": Ws_minutes,
        "lambda": lambda_val,
        "mu": mu_val,
        "c": c_val
    }, None # No error

# --- Interfaz Gráfica con Tkinter ---
class QueueSimulatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Simulador de Teoría de Colas M/M/c")
        master.geometry("450x450") # Tamaño inicial de la ventana

        ttk.Style().configure("TLabel", padding=5)
        ttk.Style().configure("TButton", padding=5)
        ttk.Style().configure("Header.TLabel", font=("Helvetica", 14, "bold"))
        ttk.Style().configure("Error.TLabel", foreground="red", font=("Helvetica", 10, "italic"))
        ttk.Style().configure("Result.TLabel", font=("Helvetica", 10, "bold"))

        # --- Frame de Entradas ---
        input_frame = ttk.LabelFrame(master, text="Parámetros de Entrada", padding=(10, 5))
        input_frame.pack(padx=10, pady=10, fill="x")

        self.lambda_var = tk.DoubleVar(value=20.0)
        self.mu_var = tk.DoubleVar(value=10.0)
        self.c_var = tk.IntVar(value=3)

        ttk.Label(input_frame, text="Tasa de llegada (λ, camiones/hora):").grid(row=0, column=0, sticky="w")
        self.lambda_entry = ttk.Entry(input_frame, textvariable=self.lambda_var, width=10)
        self.lambda_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(input_frame, text="Tasa de servicio por servidor (μ, cam/hora):").grid(row=1, column=0, sticky="w")
        self.mu_entry = ttk.Entry(input_frame, textvariable=self.mu_var, width=10)
        self.mu_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(input_frame, text="Número de servidores (c):").grid(row=2, column=0, sticky="w")
        self.c_entry = ttk.Entry(input_frame, textvariable=self.c_var, width=10)
        self.c_entry.grid(row=2, column=1, padx=5, pady=2)

        # --- Frame de Botones ---
        button_frame = ttk.Frame(master, padding=(0, 5))
        button_frame.pack()

        self.calculate_button = ttk.Button(button_frame, text="Calcular Indicadores", command=self.calculate_and_display)
        self.calculate_button.pack(side=tk.LEFT, padx=5)

        self.default_button = ttk.Button(button_frame, text="Valores Ejemplo PDF", command=self.set_default_values)
        self.default_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(button_frame, text="Limpiar", command=self.clear_fields)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # --- Frame de Resultados ---
        results_frame = ttk.LabelFrame(master, text="Resultados del Modelo", padding=(10, 5))
        results_frame.pack(padx=10, pady=10, fill="x", expand=True)

        self.rho_label = ttk.Label(results_frame, text="Utilización del sistema (ρ):")
        self.rho_label.grid(row=0, column=0, sticky="w")
        self.rho_value = ttk.Label(results_frame, text="-", style="Result.TLabel")
        self.rho_value.grid(row=0, column=1, sticky="w", padx=5)

        self.lq_label = ttk.Label(results_frame, text="Número medio en cola (Lq):")
        self.lq_label.grid(row=1, column=0, sticky="w")
        self.lq_value = ttk.Label(results_frame, text="-", style="Result.TLabel")
        self.lq_value.grid(row=1, column=1, sticky="w", padx=5)

        self.wq_label = ttk.Label(results_frame, text="Tiempo medio en cola (Wq):")
        self.wq_label.grid(row=2, column=0, sticky="w")
        self.wq_value = ttk.Label(results_frame, text="-", style="Result.TLabel")
        self.wq_value.grid(row=2, column=1, sticky="w", padx=5)

        self.ws_label = ttk.Label(results_frame, text="Tiempo total en sistema (Ws):")
        self.ws_label.grid(row=3, column=0, sticky="w")
        self.ws_value = ttk.Label(results_frame, text="-", style="Result.TLabel")
        self.ws_value.grid(row=3, column=1, sticky="w", padx=5)

        self.status_label = ttk.Label(results_frame, text="", style="Error.TLabel", wraplength=380, justify=tk.LEFT)
        self.status_label.grid(row=4, column=0, columnspan=2, sticky="w", pady=10)

        # Nota sobre el ejemplo
        self.note_label = ttk.Label(master,
                                    text="Nota: Los resultados para Lq (y Wq, Ws) usan la 'Fórmula Básica' del PDF,\n"
                                         "que es una aproximación y puede diferir de los valores exactos M/M/c\n"
                                         "o del ejemplo numérico del PDF si usa una fórmula más precisa.",
                                    font=("Helvetica", 8, "italic"),
                                    justify=tk.CENTER)
        self.note_label.pack(pady=5)

        # Bind Enter key to calculate
        master.bind('<Return>', lambda event: self.calculate_and_display())
        self.lambda_entry.focus_set() # Poner el foco en el primer campo de entrada

    def set_default_values(self):
        self.lambda_var.set(20.0)
        self.mu_var.set(10.0)
        self.c_var.set(3)
        self.clear_results_and_status()
        self.lambda_entry.focus_set()

    def clear_results_and_status(self):
        self.rho_value.config(text="-")
        self.lq_value.config(text="-")
        self.wq_value.config(text="-")
        self.ws_value.config(text="-")
        self.status_label.config(text="")

    def clear_fields(self):
        self.lambda_var.set(0.0)
        self.mu_var.set(0.0)
        self.c_var.set(0)
        self.clear_results_and_status()
        self.lambda_entry.focus_set()


    def calculate_and_display(self):
        self.clear_results_and_status()
        try:
            lambda_val = self.lambda_var.get()
            mu_val = self.mu_var.get()
            c_val = self.c_var.get()
        except tk.TclError:
            messagebox.showerror("Error de Entrada", "Por favor, ingrese valores numéricos válidos.")
            return

        metrics, error_msg = calculate_queue_metrics(lambda_val, mu_val, c_val)

        if error_msg:
            self.status_label.config(text=error_msg)
            # messagebox.showerror("Error de Cálculo", error_msg) # Alternativa con popup
            return

        if metrics:
            self.rho_value.config(text=f"{metrics['rho']:.4f} ({metrics['rho']*100:.2f}%)")
            self.lq_value.config(text=f"{metrics['Lq']:.2f} camiones")
            self.wq_value.config(text=f"{metrics['Wq_minutes']:.2f} minutos")
            self.ws_value.config(text=f"{metrics['Ws_minutes']:.2f} minutos")
            self.status_label.config(text="Cálculo completado.") # Mensaje de éxito
        else:
            # Esto no debería ocurrir si error_msg se maneja correctamente
            self.status_label.config(text="Error desconocido en el cálculo.")


if __name__ == "__main__":
    root = tk.Tk()
    app = QueueSimulatorApp(root)
    root.mainloop()