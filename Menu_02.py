
import os
import tkinter as tk
from tkinter import ttk, messagebox

from Calculadora import mount as mount_calculator  # << usa Calculadora.py de abajo

# ================== CONFIG ==================
LOGO_PATH = "logo_uam.png"   # usado también como fallback de icono
ICON_PATH = "uam.ico"        # opcional (Windows)
UI_SCALE = 1.25

# ================== UTILS ==================
def load_logo(path, target_size=(130, 130)):
    if not os.path.exists(path):
        return None
    try:
        from PIL import Image, ImageTk  # type: ignore
        img = Image.open(path).convert("RGBA")
        img.thumbnail(target_size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        try:
            img = tk.PhotoImage(file=path)
            w, h = img.width(), img.height()
            fx = max(1, w // max(1, target_size[0]))
            fy = max(1, h // max(1, target_size[1]))
            if fx > 1 or fy > 1:
                img = img.subsample(fx, fy)
            return img
        except Exception:
            return None

# ================== APP ==================
class MenuUAM(tk.Tk):
    def __init__(self):
        super().__init__()
        # Título e icono (para que no aparezca "tk")
        self.title("Universidad Americana — Calculadora de Matrices")
        self._set_icon()

        self.resizable(True, True)

        # Escalado (fuentes más grandes)
        try:
            self.tk.call("tk", "scaling", UI_SCALE)
        except tk.TclError:
            pass

        # Estado UI
        self._is_fullscreen = False
        self._is_showing_menu = True

        # Paleta
        self.bg_base   = "#eaf3ff"
        self.bg_card   = "#ffffff"
        self.primary   = "#1f4fd6"
        self.primary_h = "#1a43b5"
        self.text_dark = "#0f172a"
        self.muted     = "#334155"

        self._build_styles()

        # Contenedor donde intercambiaremos MENÚ <-> HUB
        self.stage = tk.Frame(self, bg=self.bg_base)
        self.stage.pack(fill="both", expand=True)

        # Render inicial
        self._render_menu()

        # Atajos
        self.bind("<F11>", lambda e: self._toggle_fullscreen())
        self.bind("<Escape>", lambda e: self._handle_escape())

        # Arrancar maximizado (Windows); en otros SO usa geometry grande
        self.after(50, self._maximize)

    # ----- icono / título -----
    def _set_icon(self):
        """Configura icono para la ventana: intenta .ico y luego PNG."""
        # .ico (Windows)
        try:
            if os.path.exists(ICON_PATH):
                self.iconbitmap(ICON_PATH)
        except Exception:
            pass
        # Fallback PNG (mantener referencia para que no se libere)
        try:
            from PIL import Image, ImageTk  # type: ignore
            _png = ImageTk.PhotoImage(file=LOGO_PATH)
            self.iconphoto(True, _png)
            self._icon_ref = _png
        except Exception:
            try:
                _png = tk.PhotoImage(file=LOGO_PATH)
                self.iconphoto(True, _png)
                self._icon_ref = _png
            except Exception:
                pass

    # ----- estilos -----
    def _build_styles(self):
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.configure(bg=self.bg_base)
        self.style.configure(".", background=self.bg_base)

        self.style.configure("Card.TFrame", background=self.bg_card)
        self.style.configure("Title.TLabel", font=("Segoe UI", 36, "bold"),
                             foreground=self.text_dark, background=self.bg_card)
        self.style.configure("SubTitle.TLabel", font=("Segoe UI", 22, "bold"),
                             foreground=self.text_dark, background=self.bg_card)
        self.style.configure("Foot.TLabel", font=("Segoe UI", 11),
                             foreground=self.muted, background=self.bg_card)

        self.style.configure("Primary.TButton", font=("Segoe UI", 18, "bold"), padding=16)
        self.style.map("Primary.TButton",
                       background=[("!disabled", self.primary), ("active", self.primary_h)],
                       foreground=[("!disabled", "white")])

        self.style.configure("Secondary.TButton", font=("Segoe UI", 16), padding=14)
        self.style.map("Secondary.TButton",
                       background=[("!disabled", self.bg_card), ("active", "#f0f4ff")],
                       foreground=[("!disabled", self.text_dark)])

    # ----- helpers -----
    def _clear_stage(self):
        for w in self.stage.winfo_children():
            w.destroy()

    def _maximize(self):
        try:
            self.state("zoomed")  # Windows
        except Exception:
            # fallback: ocupar casi toda la pantalla
            sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
            self.geometry(f"{sw}x{sh}+0+0")

    def _toggle_fullscreen(self):
        self._is_fullscreen = not self._is_fullscreen
        self.attributes("-fullscreen", self._is_fullscreen)

    def _handle_escape(self):
        if self._is_fullscreen:
            self._toggle_fullscreen()
            return
        if self._is_showing_menu:
            self._quit_app()
        else:
            self._render_menu()

    # ----- vistas -----
    def _render_menu(self):
        self._is_showing_menu = True
        self._clear_stage()

        # Layout responsivo: dos filas (header + botones), centradas con padding
        container = tk.Frame(self.stage, bg=self.bg_base)
        container.pack(fill="both", expand=True, padx=40, pady=40)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Tarjeta header
        header_shadow = tk.Frame(container, bg="#dfe9ff")
        header_shadow.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        header = ttk.Frame(header_shadow, style="Card.TFrame", padding=30)
        header.pack(fill="both", expand=True, padx=1, pady=1)

        # Header interno con grid
        header.columnconfigure(0, weight=0)
        header.columnconfigure(1, weight=1)

        self.logo_img = load_logo(LOGO_PATH, target_size=(140, 140))
        if self.logo_img:
            logo = ttk.Label(header, image=self.logo_img, background=self.bg_card)
        else:
            canvas = tk.Canvas(header, width=140, height=140, highlightthickness=0, bg=self.bg_card)
            canvas.create_oval(6, 6, 134, 134, outline="#93c5fd", width=2)
            canvas.create_text(70, 70, text="UAM", fill=self.primary, font=("Segoe UI", 16, "bold"))
            logo = canvas
        logo.grid(row=0, column=0, rowspan=2, padx=(0, 24), pady=6)

        ttk.Label(header, text="UNIVERSIDAD AMERICANA", style="Title.TLabel").grid(row=0, column=1, sticky="w")
        ttk.Label(header, text="CALCULADORA DE MATRICES", style="SubTitle.TLabel").grid(row=1, column=1, sticky="w")

        # Tarjeta acciones
        actions_shadow = tk.Frame(container, bg="#dfe9ff")
        actions_shadow.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        actions = ttk.Frame(actions_shadow, style="Card.TFrame", padding=30)
        actions.pack(fill="both", expand=True, padx=1, pady=1)

        # Botones centrados
        btns = ttk.Frame(actions, style="Card.TFrame")
        btns.pack(pady=10)
        ttk.Button(btns, text="Ingresar a la Calculadora", style="Primary.TButton",
                   command=self._render_hub, width=28).pack(pady=(0, 12))
        ttk.Button(btns, text="Salir del Programa", style="Secondary.TButton",
                   command=self._quit_app, width=28).pack()

        ttk.Label(actions, text="Proyecto de Álgebra Lineal – Ingeniería en Sistemas UAM",
                  style="Foot.TLabel").pack(pady=(16, 0))

    def _render_hub(self):
        self._is_showing_menu = False
        self._clear_stage()
        # Monta el hub (Calculadora) en el mismo contenedor
        mount_calculator(self.stage, on_back=self._render_menu)

    # ----- acciones -----
    def _quit_app(self):
        if messagebox.askokcancel("Salir", "¿Deseas salir del programa?"):
            self.destroy()

# ================== MAIN ==================
if __name__ == "__main__":
    MenuUAM().mainloop()
