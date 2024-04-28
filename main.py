import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

def open_lager():
    show_inventory_window()

def add_to_inventory():
    global add_window, entry_menge, maschinentyp_var, ersatzteil_var

    # Holen der eingegebenen Werte
    maschinentyp = maschinentyp_var.get()
    ersatzteil = ersatzteil_var.get()
    menge_str = entry_menge.get()

    # Überprüfen, ob das Menge-Feld leer ist
    if not menge_str:
        # Fehlermeldung anzeigen und die Funktion verlassen
        messagebox.showerror("Fehler", "Bitte geben Sie eine Menge ein.")
        return

    # Versuche, die Menge in eine Ganzzahl umzuwandeln
    try:
        menge = int(menge_str)
    except ValueError:
        # Fehlermeldung anzeigen, wenn die Eingabe keine Ganzzahl ist
        messagebox.showerror("Fehler", "Ungültige Menge. Bitte geben Sie eine ganze Zahl ein.")
        return

    # Überprüfen, ob der Maschinentyp bereits im Lager existiert
    if maschinentyp not in lager:
        # Wenn nicht, füge den Maschinentyp zum Lager hinzu
        lager[maschinentyp] = {}

    # Füge das Ersatzteil mit der Menge zum Lager hinzu
    lager[maschinentyp][ersatzteil] = menge

    # Schließen des Fensters und Aktualisieren der Anzeige
    add_window.destroy()
    show_inventory()  # Lagerbestände anzeigen

def use_from_inventory():
    global use_window, entry_menge_use, maschinentyp_var, ersatzteil_var

    # Holen der eingegebenen Werte
    maschinentyp = maschinentyp_var.get()
    ersatzteil = ersatzteil_var.get()
    menge_str = entry_menge_use.get()

    # Überprüfen, ob das Menge-Feld leer ist
    if not menge_str:
        # Fehlermeldung anzeigen und die Funktion verlassen
        messagebox.showerror("Fehler", "Bitte geben Sie eine Menge ein.")
        return

    # Versuche, die Menge in eine Ganzzahl umzuwandeln
    try:
        menge = int(menge_str)
    except ValueError:
        # Fehlermeldung anzeigen, wenn die Eingabe keine Ganzzahl ist
        messagebox.showerror("Fehler", "Ungültige Menge. Bitte geben Sie eine ganze Zahl ein.")
        return

    # Überprüfen, ob der Maschinentyp im Lager existiert
    if maschinentyp not in lager or ersatzteil not in lager[maschinentyp]:
        # Wenn nicht, Fehlermeldung anzeigen und die Funktion verlassen
        messagebox.showerror("Fehler", "Das Ersatzteil ist nicht im Lager vorhanden.")
        return

    # Überprüfen, ob genügend Ersatzteile im Lager vorhanden sind
    if lager[maschinentyp][ersatzteil] < menge:
        # Wenn nicht, Fehlermeldung anzeigen und die Funktion verlassen
        messagebox.showerror("Fehler", "Nicht genügend Ersatzteile im Lager vorhanden.")
        return

    # Verwendete Menge von den Lagerbeständen abziehen
    lager[maschinentyp][ersatzteil] -= menge

    # Schließen des Fensters und Aktualisieren der Anzeige
    use_window.destroy()
    show_inventory()  # Lagerbestände anzeigen

def show_inventory():
    # Ausgabe der Lagerbestände
    print("Lagerbestände:")
    for maschinentyp, ersatzteile in lager.items():
        print(f"Maschinentyp: {maschinentyp}")
        for ersatzteil, menge in ersatzteile.items():
            print(f"- {ersatzteil}: {menge}")
        print()  # Leerzeile für bessere Lesbarkeit

def exit_app():
    root.destroy()

# Beispiel Lager
lager = {
    "Maschinentyp1": {
        "Ersatzteil1": 10,
        "Ersatzteil2": 20,
    },
    "Maschinentyp2": {
        "Ersatzteil3": 15,
        "Ersatzteil4": 25,
    }
}

# Hauptfenster erstellen
root = tk.Tk()
root.title("Hauptmenü")
root.geometry("400x267")  # Setze die Größe des Hauptfensters

# Hintergrundbild laden
background_image = Image.open("C:\\Users\\Felix Stangl\\Desktop\\Programiren\\spare-part-manager\\background_image.jpg")
background_photo = ImageTk.PhotoImage(background_image)

# Hintergrundbild als Label im Hauptfenster platzieren
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Knopf für das Lager
btn_lager = tk.Button(root, text="Lager", command=open_lager)
btn_lager.pack(pady=10)

def show_inventory_window():
    global inventory_window, inventory_text
    # Ein Fenster zum Anzeigen der Lagerbestände öffnen
    inventory_window = tk.Toplevel(root)
    inventory_window.title("Lagerbestände")

    # Lagerbestände im Textfeld anzeigen
    inventory_text = tk.Text(inventory_window, height=20, width=50)
    inventory_text.pack(padx=10, pady=10)
    inventory_text.config(state=tk.NORMAL)
    inventory_text.insert(tk.END, "Lagerbestände:\n\n")
    for maschinentyp, ersatzteile in lager.items():
        inventory_text.insert(tk.END, f"Maschinentyp: {maschinentyp}\n")
        for ersatzteil, menge in ersatzteile.items():
            inventory_text.insert(tk.END, f"- {ersatzteil}: {menge}\n")
        inventory_text.insert(tk.END, "\n")  # Leerzeile für bessere Lesbarkeit
    inventory_text.config(state=tk.DISABLED)  # Textfeld schreibgeschützt machen

    # Schließen Knopf für das Lagerbestände-Fenster
    btn_close_inventory = tk.Button(inventory_window, text="Schließen", command=inventory_window.destroy)
    btn_close_inventory.pack()

# Knopf um Ersatzteile hinzuzufügen
def open_add_window():
    global add_window, entry_menge, maschinentyp_var, ersatzteil_var, ersatzteil_dropdown
    add_window = tk.Toplevel(root)
    add_window.title("Ersatzteil hinzufügen")

    tk.Label(add_window, text="Maschinentyp:").grid(row=0, column=0, padx=5, pady=5)
    maschinentyp_var = tk.StringVar()
    maschinentyp_dropdown = ttk.Combobox(add_window, textvariable=maschinentyp_var)
    maschinentyp_dropdown['values'] = list(lager.keys())
    maschinentyp_dropdown.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(add_window, text="Ersatzteil:").grid(row=1, column=0, padx=5, pady=5)
    ersatzteil_var = tk.StringVar()
    ersatzteil_dropdown = ttk.Combobox(add_window, textvariable=ersatzteil_var)
    ersatzteil_dropdown.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(add_window, text="Menge:").grid(row=2, column=0, padx=5, pady=5)
    entry_menge = tk.Entry(add_window)
    entry_menge.grid(row=2, column=1, padx=5, pady=5)

    btn_add = tk.Button(add_window, text="Hinzufügen", command=add_to_inventory)
    btn_add.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

    maschinentyp_dropdown.bind("<<ComboboxSelected>>", update_ersatzteile_dropdown)

def update_ersatzteile_dropdown(event):
    selected_maschinentyp = maschinentyp_var.get()
    ersatzteil_dropdown['values'] = list(lager[selected_maschinentyp].keys())

btn_add_ersatzteil = tk.Button(root, text="Ersatzteil hinzufügen", command=open_add_window)
btn_add_ersatzteil.pack(pady=10)

# Knopf um Ersatzteile zu verwenden
def open_use_window():
    global use_window, entry_menge_use, maschinentyp_var, ersatzteil_var, ersatzteil_dropdown
    use_window = tk.Toplevel(root)
    use_window.title("Ersatzteil verwenden")

    tk.Label(use_window, text="Maschinentyp:").grid(row=0, column=0, padx=5, pady=5)
    maschinentyp_var = tk.StringVar()
    maschinentyp_dropdown = ttk.Combobox(use_window, textvariable=maschinentyp_var)
    maschinentyp_dropdown['values'] = list(lager.keys())
    maschinentyp_dropdown.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(use_window, text="Ersatzteil:").grid(row=1, column=0, padx=5, pady=5)
    ersatzteil_var = tk.StringVar()
    ersatzteil_dropdown = ttk.Combobox(use_window, textvariable=ersatzteil_var)
    ersatzteil_dropdown.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(use_window, text="Menge:").grid(row=2, column=0, padx=5, pady=5)
    entry_menge_use = tk.Entry(use_window)
    entry_menge_use.grid(row=2, column=1, padx=5, pady=5)

    btn_use = tk.Button(use_window, text="Verwenden", command=use_from_inventory)
    btn_use.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

    maschinentyp_dropdown.bind("<<ComboboxSelected>>", update_ersatzteile_dropdown)

btn_use_ersatzteil = tk.Button(root, text="Ersatzteil verwenden", command=open_use_window)
btn_use_ersatzteil.pack(pady=10)

# Beenden Knopf
btn_exit = tk.Button(root, text="Beenden", command=exit_app)
btn_exit.pack(pady=10)

root.mainloop()
