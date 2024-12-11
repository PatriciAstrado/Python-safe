import tkinter as tk
from tkinter import messagebox
import numpy as np
import sympy as sp

epsilon = 8.8541878176 * (10**(-12))
K = 1 / (4 * np.pi * epsilon)

def cargaPuntual(carga, r):
    if r == 0:
        raise ValueError("La distancia r no puede ser cero.")
    potencialElectrico = K * carga / r
    return potencialElectrico

def cargasMultiples(carga_array, r_array):
    potencialElectrico = 0
    if len(carga_array) != len(r_array):
        raise ValueError("Los datos de distancia y cargas tienen que ser la misma cantidad.")
    for carga, r in zip(carga_array, r_array):
        if r == 0:
            raise ValueError("La distancia r no puede ser cero.")
        potencialElectrico += (K * carga / r)
    return potencialElectrico

def cargaLineal(densidad, distancia_final, distancia_inicial, altura):
    if distancia_final == distancia_inicial:
        raise ValueError("La distancia final no puede ser igual a la distancia inicial.")
    sup = distancia_final + sp.sqrt(distancia_final**2 + altura**2)
    inf = distancia_inicial + sp.sqrt(distancia_inicial**2 + altura**2)
    potencialElectrico = densidad * K * sp.log(sup / inf)
    return potencialElectrico

def anilloDeCargas(densidad, Radio, altura):
    distancia_punto = sp.sqrt(Radio**2 + altura**2)
    potencialElectrico = (K * densidad * 2 * np.pi * Radio) / distancia_punto
    return potencialElectrico

def discoDeCargas(densidad, Radio_gus, altura):
    distancia_punto = sp.sqrt(Radio_gus**2 + altura**2)
    potencialElectrico = K * densidad * 2 * np.pi * (distancia_punto - altura)
    return potencialElectrico

def esferaConductoraCargadaUniformemente(carga, radio_obj, Radio_gus):
    if radio_obj <= Radio_gus:
        potencialElectrico = K * carga / radio_obj
    else:
        potencialElectrico = K * carga / Radio_gus
    return potencialElectrico

# Test cases
# Constants
carga = 1e-9  # 1 nC
r = 0.1  # 0.1 meters
densidad = 1e-6  # 1 μC/m
distancia_final = 0.2
distancia_inicial = 0.1
altura = 0.05
Radio = 0.1
Radio_gus = 0.2

# Testing cargaPuntual
print("cargaPuntual:", cargaPuntual(carga, r))

# Testing cargasMultiples
carga_array = [1e-9, -2e-9]
r_array = [0.1, 0.2]
print("cargasMultiples:", cargasMultiples(carga_array, r_array))

# Testing cargaLineal
print("cargaLineal:", cargaLineal(densidad, distancia_final, distancia_inicial, altura))

# Testing anilloDeCargas
print("anilloDeCargas:", anilloDeCargas(densidad, Radio, altura))

# Testing discoDeCargas
print("discoDeCargas:", discoDeCargas(densidad, Radio_gus, altura))

# Testing esferaConductoraCargadaUniformemente
print("esferaConductoraCargadaUniformemente:", esferaConductoraCargadaUniformemente(carga, r, Radio_gus))


# Crear la interfaz gráfica
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Potencial Eléctrico")

        self.scenarios = ["Carga Puntual", "Cargas Múltiples", "Carga Lineal", "Anillo de Cargas", "Disco de Cargas", "Esfera Conductora Cargada Uniformemente"]

        self.label_scenario = tk.Label(root, text="Selecciona el Escenario")
        self.label_scenario.grid(row=0, column=0)
        self.scenario_var = tk.StringVar(root)
        self.scenario_var.set(self.scenarios[0])
        self.option_menu = tk.OptionMenu(root, self.scenario_var, *self.scenarios, command=self.update_fields)
        self.option_menu.grid(row=0, column=1)

        self.entries = {}
        self.labels = {}

        self.common_fields = {
            "Carga (C)": "carga",
            "Distancia (m)": "distancia",
            "Densidad (C/m)": "densidad",
            "Distancia Final (m)": "distancia_final",
            "Distancia Inicial (m)": "distancia_inicial",
            "Altura (m)": "altura",
            "Radio (m)": "radio",
            "Radio Gausiano (m)": "radio_gus",
            "Radio del Objeto (m)": "radio_obj"
        }

        self.button_calcular = tk.Button(root, text="Calcular", command=self.calcular)
        self.button_calcular.grid(row=20, column=0, columnspan=2)

        self.label_resultado = tk.Label(root, text="Resultado: ")
        self.label_resultado.grid(row=21, column=0, columnspan=2)

        self.update_fields()

    def update_fields(self, *args):
        for label in self.labels.values():
            label.grid_remove()
        for entry in self.entries.values():
            entry.grid_remove()

        self.labels = {}
        self.entries = {}

        scenario = self.scenario_var.get()
        if scenario == "Carga Puntual":
            fields = ["Carga (C)", "Distancia (m)"]
        elif scenario == "Cargas Múltiples":
            fields = ["Cargas (C) (separadas por comas)", "Distancias (m) (separadas por comas)"]
        elif scenario == "Carga Lineal":
            fields = ["Densidad (C/m)", "Distancia Final (m)", "Distancia Inicial (m)", "Altura (m)"]
        elif scenario == "Anillo de Cargas":
            fields = ["Densidad (C/m)", "Radio (m)", "Altura (m)"]
        elif scenario == "Disco de Cargas":
            fields = ["Densidad (C/m)", "Radio Gausiano (m)", "Altura (m)"]
        elif scenario == "Esfera Conductora Cargada Uniformemente":
            fields = ["Carga (C)", "Radio del Objeto (m)", "Radio Gausiano (m)"]

        for i, field in enumerate(fields):
            label = tk.Label(self.root, text=field)
            label.grid(row=i+1, column=0)
            entry = tk.Entry(self.root)
            entry.grid(row=i+1, column=1)
            self.labels[field] = label
            self.entries[field] = entry

    def calcular(self):
        scenario = self.scenario_var.get()
        try:
            if scenario == "Carga Puntual":
                carga = float(self.entries["Carga (C)"].get())
                distancia = float(self.entries["Distancia (m)"].get())
                resultado = cargaPuntual(carga, distancia)
            elif scenario == "Cargas Múltiples":
                cargas = list(map(float, self.entries["Cargas (C) (separadas por comas)"].get().split(',')))
                distancias = list(map(float, self.entries["Distancias (m) (separadas por comas)"].get().split(',')))
                resultado = cargasMultiples(cargas, distancias)
            elif scenario == "Carga Lineal":
                densidad = float(self.entries["Densidad (C/m)"].get())
                distancia_final = float(self.entries["Distancia Final (m)"].get())
                distancia_inicial = float(self.entries["Distancia Inicial (m)"].get())
                altura = float(self.entries["Altura (m)"].get())
                resultado = cargaLineal(densidad, distancia_final, distancia_inicial, altura)
            elif scenario == "Anillo de Cargas":
                densidad = float(self.entries["Densidad (C/m)"].get())
                radio = float(self.entries["Radio (m)"].get())
                altura = float(self.entries["Altura (m)"].get())
                resultado = anilloDeCargas(densidad, radio, altura)
            elif scenario == "Disco de Cargas":
                densidad = float(self.entries["Densidad (C/m)"].get())
                radio_gus = float(self.entries["Radio Gausiano (m)"].get())
                altura = float(self.entries["Altura (m)"].get())
                resultado = discoDeCargas(densidad, radio_gus, altura)
            elif scenario == "Esfera Conductora Cargada Uniformemente":
                carga = float(self.entries["Carga (C)"].get())
                radio_obj = float(self.entries["Radio del Objeto (m)"].get())
                radio_gus = float(self.entries["Radio Gausiano (m)"].get())
                resultado = esferaConductoraCargadaUniformemente(carga, radio_obj, radio_gus)

            self.label_resultado.config(text=f"Resultado: {resultado} V")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
