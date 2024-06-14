# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 14:30:17 2023

@author: yaboniav
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
def seleccionar_opcion_desde_menu():
    opcion_seleccionada = ""

    def aceptar_seleccion():
        nonlocal opcion_seleccionada
        opcion_seleccionada = combo.get()
        messagebox.showinfo('Opción seleccionada', f'Has seleccionado: {opcion_seleccionada}')
        ventana.destroy()

    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title('Seleccionar opción')

    # Personalizar el aspecto
    ventana.geometry("450x250")  # Tamaño de la ventana
    ventana.configure(bg='#ecf5f4')  # Color de fondo
    
    # Agregamos el texto "Seleccione el equipo de trabajo"
    label = ttk.Label(ventana, text="Seleccione el equipo de trabajo", font=("Arial", 14), background='#ecf5f4', foreground="black")
    label.pack(pady=10)

    # Crear y configurar el combobox
    opciones = [
        "1. Automatización",
        "2. Compra de bien futuro",
        "3. Electrificación Rural CENS",
        "4. Exp & Rep",
        "5. Sub & Lin",
        "6. Gestión de Activos",
        "7. Pérdidas",
        "8. Mtto",
        "9. San Roque",
        "10.Compensación capacitiva 115 kV"
    ]
    
    estilo = ttk.Style()
    estilo.theme_use('default')
    estilo.configure("TCombobox",
                     background="#e1e1e1",
                     fieldbackground="#e1e1e1",
                     foreground="black",
                     font=("Arial", 12))
    
    combo = ttk.Combobox(ventana, values=opciones, style="TCombobox")
    combo.pack(pady=40)

    # Botón para aceptar la selección
    estilo.configure("TButton", 
                     font=("Arial", 12),
                     background="#43e634",
                     foreground="white",
                     padding=10)
    boton_aceptar = ttk.Button(ventana, text="Aceptar", command=aceptar_seleccion, style="TButton")
    boton_aceptar.pack(pady=20)

    # Ejecutar el bucle principal
    ventana.mainloop()
    # Especificar la ruta donde deseas crear la carpeta
    path = f"D:/validador/{opcion_seleccionada}"

    # Verificar si la carpeta ya existe
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Carpeta '{path}' creada exitosamente!")
    else:
        print(f"La carpeta '{path}' ya existe.")  
    return opcion_seleccionada

    