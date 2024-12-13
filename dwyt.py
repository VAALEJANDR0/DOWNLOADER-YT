import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import os
import sys
import threading

# Asegurarse de que FFmpeg esté disponible en el ejecutable
if getattr(sys, 'frozen', False):  # Si se está ejecutando desde el EXE
    ffmpeg_path = os.path.join(sys._MEIPASS, 'ffmpeg.exe')  # Ruta interna del ejecutable
else:  # Si se está ejecutando desde el script en desarrollo
    ffmpeg_path = "C:/ffmpeg/ffmpeg.exe"  # Ruta fija de FFmpeg

# Agregar FFmpeg al PATH
os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)

def download_video():
    # Obtener los enlaces de la tabla
    links = [tree.item(item)['values'][0] for item in tree.get_children()]
    if not links:
        messagebox.showerror("Error", "No hay enlaces para descargar.")
        return

    output_path = folder_path.get()
    if not output_path:
        messagebox.showerror("Error", "Por favor, selecciona una carpeta para guardar los archivos.")
        return

    # Opciones para yt-dlp
    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # Define el nombre del archivo descargado
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',  # Forzar descarga en formato MP4
        'noplaylist': True,  # Descargar solo un video, no listas de reproducción
        'merge_output_format': 'mp4',  # Asegurarse de que el archivo final sea MP4
        'audioquality': 0,  # Mejor calidad de audio posible
    }

    # Función para descargar cada video en un hilo separado
    def download_thread(link):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(link, download=True)
                title = info_dict.get('title', 'Video')
                tree.insert("", "end", values=(link, "Descargado"))
        except Exception as e:
            tree.insert("", "end", values=(link, f"Error: {e}"))

    # Usamos hilos para no bloquear la interfaz mientras se descargan los videos
    for link in links:
        tree.insert("", "end", values=(link, "Descargando..."))
        threading.Thread(target=download_thread, args=(link,)).start()

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)

def add_link():
    link = link_var.get()
    if link:
        tree.insert("", "end", values=(link, "Pendiente"))
        link_var.set("")  # Limpiar el campo de entrada

# Configuración de la ventana principal
root = tk.Tk()
root.title("Downloader DWYT")
root.geometry("900x900")
root.resizable(True, True)

# Establecer el ícono de la aplicación
icon_path = "C:/Users/rvent/Desktop/DOWNLOADER-YT/music.ico"
root.iconbitmap(icon_path)

# Variables
link_var = tk.StringVar()
folder_path = tk.StringVar()
quality_var = tk.StringVar(value="720p")

# Interfaz gráfica
tk.Label(root, text="Descargador de Videos de YouTube", font=("Arial", 18, "bold")).pack(pady=20)

tk.Label(root, text="Ingresa el enlace del video:", font=("Arial", 14)).pack(pady=10)
tk.Entry(root, textvariable=link_var, width=60, font=("Arial", 12)).pack(pady=10)

# Botón para agregar el enlace a la lista
tk.Button(root, text="Agregar Enlace", command=add_link, bg="#4CAF50", fg="white", font=("Arial", 14), width=20).pack(pady=10)

tk.Label(root, text="Selecciona la calidad del video:", font=("Arial", 14)).pack(pady=10)
quality_options = ["360p", "720p", "1080p"]
ttk.Combobox(root, textvariable=quality_var, values=quality_options, state="readonly", width=20, font=("Arial", 12)).pack(pady=10)

tk.Label(root, text="Selecciona la carpeta de destino:", font=("Arial", 14)).pack(pady=10)
tk.Entry(root, textvariable=folder_path, width=60, state="readonly", font=("Arial", 12)).pack(pady=10)

# Botón para seleccionar la carpeta
tk.Button(root, text="Seleccionar Carpeta", command=browse_folder, bg="#4CAF50", fg="white", font=("Arial", 14), width=20).pack(pady=10)

# Botón de descarga
tk.Button(root, text="Descargar Todos", command=download_video, bg="#4CAF50", fg="white", font=("Arial", 16), width=20, height=2).pack(pady=20)

# Crear el marco de la tabla y las barras de desplazamiento
frame = tk.Frame(root)
frame.pack(pady=10, fill="both", expand=True)

# Crear las barras de desplazamiento
vsb = tk.Scrollbar(frame, orient="vertical")
vsb.pack(side="right", fill="y")

hsb = tk.Scrollbar(frame, orient="horizontal")
hsb.pack(side="bottom", fill="x")

# Crear la tabla con las barras de desplazamiento
columns = ("Enlace", "Estado")
tree = ttk.Treeview(frame, columns=columns, show="headings", height=10, yscrollcommand=vsb.set, xscrollcommand=hsb.set)
tree.heading("Enlace", text="Enlace")
tree.heading("Estado", text="Estado")
tree.pack(side="left", fill="both", expand=True)

# Configurar las barras de desplazamiento
vsb.config(command=tree.yview)
hsb.config(command=tree.xview)

tk.Label(root, text="Creador: Alejandro Alvarenga ©", font=("Arial", 18, "bold")).pack(pady=20)

# Iniciar la aplicación
root.mainloop()
