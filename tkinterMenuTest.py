import tkinter as tk


# Función para manejar la búsqueda
def buscar():
    ciudad = ciudad_entry.get()
    pais = pais_entry.get()
    tipo_negocio = tipo_negocio_entry.get()

    # Aquí puedes realizar la búsqueda utilizando los valores de ciudad, país y tipo de negocio

    # Por ahora, solo imprimiremos los valores
    print(f"Ciudad: {ciudad}")
    print(f"País: {pais}")
    print(f"Tipo de Negocio: {tipo_negocio}")


# Crear una ventana
ventana = tk.Tk()
ventana.title("Búsqueda de Negocios")

# Etiqueta y entrada para Ciudad
ciudad_label = tk.Label(ventana, text="Ciudad:")
ciudad_label.pack()
ciudad_entry = tk.Entry(ventana)
ciudad_entry.pack()

# Etiqueta y entrada para País
pais_label = tk.Label(ventana, text="País:")
pais_label.pack()
pais_entry = tk.Entry(ventana)
pais_entry.pack()

# Etiqueta y entrada para Tipo de Negocio
tipo_negocio_label = tk.Label(ventana, text="Tipo de Negocio:")
tipo_negocio_label.pack()
tipo_negocio_entry = tk.Entry(ventana)
tipo_negocio_entry.pack()

# Botón de búsqueda
buscar_button = tk.Button(ventana, text="Buscar", command=buscar)
buscar_button.pack()

# Iniciar la aplicación
ventana.mainloop()