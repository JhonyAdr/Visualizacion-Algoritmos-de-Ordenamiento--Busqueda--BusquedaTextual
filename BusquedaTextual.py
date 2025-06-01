import tkinter as tk
from tkinter import scrolledtext, messagebox, font
import time


class TextSearchApp:
    def __init__(self, root):
        self.root = root
        root.title("Buscador de Texto")
        root.geometry("800x600")

        # Estilo
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=11)
        text_font = font.Font(family="Consolas", size=10)  # O Courier New, etc.

        # --- Frame para la entrada de texto ---
        text_frame = tk.Frame(root, padx=10, pady=10)
        text_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(text_frame, text="Pegue o escriba el texto aquí:").pack(anchor="w")
        self.text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, height=15, font=text_font)
        self.text_area.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        # Configurar tag para resaltar
        self.text_area.tag_configure("highlight", background="yellow", foreground="black")
        self.text_area.tag_configure("current_highlight", background="orange", foreground="black")

        # --- Frame para la búsqueda ---
        search_frame = tk.Frame(root, padx=10, pady=5)
        search_frame.pack(fill=tk.X)

        tk.Label(search_frame, text="Palabra a buscar:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<Return>", self.perform_search_event)  # Buscar con Enter

        self.case_sensitive_var = tk.BooleanVar(value=False)  # Por defecto, insensible
        tk.Checkbutton(search_frame, text="Sensible a Mayús/Minús", variable=self.case_sensitive_var).pack(side=tk.LEFT,
                                                                                                           padx=5)

        self.search_button = tk.Button(search_frame, text="Buscar", command=self.perform_search)
        self.search_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(search_frame, text="Limpiar Búsqueda", command=self.clear_search)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.current_match_index = -1
        self.matches_positions = []

        self.next_button = tk.Button(search_frame, text="Siguiente", command=self.next_match, state=tk.DISABLED)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.prev_button = tk.Button(search_frame, text="Anterior", command=self.previous_match, state=tk.DISABLED)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        # --- Frame para resultados ---
        result_frame = tk.Frame(root, padx=10, pady=5)
        result_frame.pack(fill=tk.X)
        self.result_label = tk.Label(result_frame, text="Resultados aparecerán aquí.", anchor="w", justify=tk.LEFT)
        self.result_label.pack(fill=tk.X)

    def clear_search(self):
        self.text_area.tag_remove("highlight", "1.0", tk.END)
        self.text_area.tag_remove("current_highlight", "1.0", tk.END)
        self.search_entry.delete(0, tk.END)
        self.result_label.config(text="Búsqueda limpiada.")
        self.current_match_index = -1
        self.matches_positions = []
        self.next_button.config(state=tk.DISABLED)
        self.prev_button.config(state=tk.DISABLED)

    def perform_search_event(self, event):  # Para el <Return>
        self.perform_search()

    def perform_search(self):
        search_term = self.search_entry.get()
        text_content = self.text_area.get("1.0", tk.END)

        # Limpiar resaltados previos y reinicializar
        self.text_area.tag_remove("highlight", "1.0", tk.END)
        self.text_area.tag_remove("current_highlight", "1.0", tk.END)
        self.matches_positions = []
        self.current_match_index = -1

        if not search_term:
            messagebox.showwarning("Entrada vacía", "Por favor, ingrese un término de búsqueda.")
            self.result_label.config(text="Ingrese un término para buscar.")
            self.next_button.config(state=tk.DISABLED)
            self.prev_button.config(state=tk.DISABLED)
            return

        if not text_content.strip():
            messagebox.showwarning("Texto vacío", "No hay texto en el área para buscar.")
            self.result_label.config(text="No hay texto para buscar.")
            self.next_button.config(state=tk.DISABLED)
            self.prev_button.config(state=tk.DISABLED)
            return

        start_time = time.perf_counter()  # Tiempo de alta precisión

        count = 0
        start_index = "1.0"  # Tkinter Text widget index (line.char)

        # La búsqueda en el widget Text es bastante eficiente
        # Usa Tcl bajo el capó, que a su vez podría usar Boyer-Moore o similar.
        # El parámetro 'nocase' es útil aquí.
        is_case_sensitive = self.case_sensitive_var.get()

        while True:
            # El método search devuelve la posición inicial o None si no se encuentra
            # 'count=length_var' se puede usar para obtener la longitud exacta del match (útil para regex)
            pos = self.text_area.search(search_term, start_index, stopindex=tk.END, nocase=not is_case_sensitive)
            if not pos:
                break

            # Calcular la posición final
            # pos es algo como "line.char", ej: "3.10"
            # length es la longitud del término de búsqueda
            # end_pos será "pos + longitud del search_term caracteres"
            end_pos = f"{pos}+{len(search_term)}c"

            self.text_area.tag_add("highlight", pos, end_pos)
            self.matches_positions.append((pos, end_pos))
            count += 1
            start_index = end_pos  # Continuar la búsqueda desde el final del match actual

        end_time = time.perf_counter()
        execution_time_ms = (end_time - start_time) * 1000

        if count > 0:
            self.result_label.config(
                text=f"Palabra '{search_term}' encontrada {count} veces.\nTiempo de búsqueda: {execution_time_ms:.4f} ms."
            )
            self.current_match_index = 0
            self.highlight_current_match()
            self.next_button.config(state=tk.NORMAL if count > 1 else tk.DISABLED)
            self.prev_button.config(state=tk.DISABLED)  # Ya estamos en el primero
        else:
            self.result_label.config(
                text=f"Palabra '{search_term}' no encontrada.\nTiempo de búsqueda: {execution_time_ms:.4f} ms."
            )
            self.next_button.config(state=tk.DISABLED)
            self.prev_button.config(state=tk.DISABLED)

    def highlight_current_match(self):
        if not self.matches_positions or self.current_match_index < 0:
            return

        # Quitar el resaltado especial anterior
        self.text_area.tag_remove("current_highlight", "1.0", tk.END)

        # Aplicar resaltado especial al actual
        pos_start, pos_end = self.matches_positions[self.current_match_index]
        self.text_area.tag_add("current_highlight", pos_start, pos_end)
        self.text_area.see(pos_start)  # Asegurarse de que el match esté visible

        # Actualizar estado de botones
        num_matches = len(self.matches_positions)
        self.prev_button.config(state=tk.NORMAL if self.current_match_index > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.current_match_index < num_matches - 1 else tk.DISABLED)

    def next_match(self):
        if self.current_match_index < len(self.matches_positions) - 1:
            self.current_match_index += 1
            self.highlight_current_match()

    def previous_match(self):
        if self.current_match_index > 0:
            self.current_match_index -= 1
            self.highlight_current_match()


if __name__ == "__main__":
    root = tk.Tk()
    app = TextSearchApp(root)

    # Texto de ejemplo para probar
    sample_text = """Este es un texto de ejemplo para realizar una búsqueda.
La palabra ejemplo aparece varias veces en este texto de ejemplo.
Python es un lenguaje de programación popular. Python, Python, python!
Búsqueda en Tkinter es interesante. ejemplo final.
"""
    app.text_area.insert("1.0", sample_text)

    root.mainloop()