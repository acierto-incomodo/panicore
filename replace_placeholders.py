#!/usr/bin/env python3
import os
import sys

# ================= CONFIGURACIÓN =================
# Define aquí los valores reales por los que quieres reemplazar los marcadores.
REPLACEMENTS = {
    "{NAME}": "Panicore",       # Nombre visible del juego
    "{ID}": "panicore",         # ID usado en rutas/carpetas (sin espacios)
    "{REMOVE}": "Panicore.exe",  # Nombre del ejecutable/proceso a cerrar
    "{GITHUB}": "panicore",
    "{OLDREMOVE}": "",
    "{OLDDIR}": "",
}

# Extensiones de archivos que se escanearán (para evitar dañar binarios o imágenes)
ALLOWED_EXTENSIONS = {".py", ".iss", ".txt", ".md", ".bat", ".ps1", ".sh", ".json"}
# =================================================

def replace_in_file(file_path):
    try:
        # Intentamos leer el archivo como UTF-8
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content = content
        changes_count = 0
        
        # Realizamos los reemplazos
        for key, value in REPLACEMENTS.items():
            if key in new_content:
                count = new_content.count(key)
                new_content = new_content.replace(key, value)
                changes_count += count
        
        # Si hubo cambios, sobrescribimos el archivo
        if changes_count > 0:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"[✔] Modificado ({changes_count} cambios): {file_path}")
        
    except UnicodeDecodeError:
        # Si el archivo no es UTF-8 (probablemente binario), lo ignoramos silenciosamente
        pass
    except Exception as e:
        print(f"[✘] Error procesando {file_path}: {e}")

def main():
    root_dir = os.getcwd()
    script_name = os.path.basename(__file__)
    
    print(f"--- Iniciando reemplazo de variables en: {root_dir} ---")
    print(f"Buscando marcadores: {list(REPLACEMENTS.keys())}")
    print(f"Reemplazando por: {list(REPLACEMENTS.values())}\n")

    # Recorremos todos los archivos y carpetas recursivamente
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Excluir carpetas que no deben tocarse para evitar errores o lentitud
        # Modifica esta lista si necesitas que entre en alguna de estas
        ignored_dirs = [".git", "venv", "__pycache__", "build", "dist", "WinDownloads", "downloads", "game", "snap"]
        for ignore in ignored_dirs:
            if ignore in dirnames:
                dirnames.remove(ignore)

        for filename in filenames:
            # Ignorar este mismo script para que no se reemplace a sí mismo
            if filename == script_name:
                continue
            
            # Verificar extensión permitida
            _, ext = os.path.splitext(filename)
            if ext.lower() in ALLOWED_EXTENSIONS:
                full_path = os.path.join(dirpath, filename)
                replace_in_file(full_path)

    print("\n--- Proceso completado ---")

if __name__ == "__main__":
    main()
