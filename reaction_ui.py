import tkinter as tk # Untuk membuat frame UI
from PIL import Image, ImageTk # Untuk manipulasi gambar
import os

# Definisikan direktori utama saat ini
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class ReactionUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        # Transparansi Window
        TRANS_COLOR = '#abcdef'
        self.root.attributes("-transparentcolor", TRANS_COLOR)
        self.root.config(bg=TRANS_COLOR)

        # Ukuran Kontainer
        self.window_width = 200
        self.window_height = 200
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Posisi Pojok Kanan Bawah
        x_pos = screen_width - self.window_width - 50
        y_pos = screen_height - self.window_height - 50
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x_pos}+{y_pos}")

        # Frame Utama
        self.main_frame = tk.Frame(self.root, bg=TRANS_COLOR, width=self.window_width, height=self.window_height)
        self.main_frame.pack_propagate(False)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Label GIF (Avatar) - Dikunci di SE (South-East / Kanan Bawah)
        self.img_label = tk.Label(self.main_frame, bg=TRANS_COLOR)
        self.img_label.pack(side=tk.RIGHT, anchor=tk.SE)

        # Load GIF ke Memori
        self.images = {
            "GREETING": self.load_gif("gifts/guardian_greeting.gif"),
            "ANGRY": self.load_gif("gifts/guardian_angry.gif"),
            "DOUBT": self.load_gif("gifts/guardian_doubt.gif")
        }

        self.current_mood = "GREETING"
        self.frame_index = 0

        self.animate_gif()

    # Muat GIF dan mengubah background putih menjadi transparan
    def load_gif(self, filename):
        path = os.path.join(BASE_DIR, filename)
        frames = []
        if os.path.exists(path):
            try:
                gif = Image.open(path)
                
                for i in range(gif.n_frames):
                    gif.seek(i)
                    frame_rgba = gif.copy().convert("RGBA")

                    # Untuk menghapus background putih (jika ada) dan membuatnya transparan
                    data = frame_rgba.getdata()
                    new_data = []
                    for item in data:
                        if item[0] > 240 and item[1] > 240 and item[2] > 240:
                            new_data.append((255, 255, 255, 0))
                        else:
                            new_data.append(item)
                    frame_rgba.putdata(new_data)
                    
                    # Untuk memastikan ukuran frame tidak melebihi kontainer
                    max_size = (self.window_width, self.window_height)
                    frame_rgba.thumbnail(max_size, Image.Resampling.LANCZOS)
                    
                    frames.append(ImageTk.PhotoImage(frame_rgba))
            except Exception as e:
                print(f"Gagal memuat GIF {filename}: {e}")
                
            return frames if frames else [tk.PhotoImage()]
            
        print(f"File {filename} tidak ditemukan!")
        return [tk.PhotoImage()]

    # Animate GIF dengan looping
    def animate_gif(self):
        frames = self.images.get(self.current_mood, [])
        if frames:
            self.img_label.config(image=frames[self.frame_index])
            self.frame_index += 1
            if self.frame_index >= len(frames):
                self.frame_index = 0 
                
        # Kecepatan putaran GIF 
        self.root.after(100, self.animate_gif)

    # Merespon mood dan mengubah GIF sesuai dengan mood yang diberikan
    def reaksi(self, mood):
        mood = mood.upper()
        if mood in self.images and self.images[mood]:
            self.current_mood = mood
            self.frame_index = 0
            
        if hasattr(self, 'timer_reset') and self.timer_reset is not None:
            self.root.after_cancel(self.timer_reset)
            self.timer_reset = None
            
        if mood not in ["GREETING", "DOUBT"]:
            self.timer_reset = self.root.after(5000, self.reset_ke_default)
    
    # Menampilkan pesan peringatan
    def show_warning(self, message):
        warn_win = tk.Toplevel(self.root)
        warn_win.title("Peringatan Keamanan")
        warn_win.geometry("400x270")
        warn_win.attributes("-topmost", True) 
        warn_win.config(bg="#f8d7da") 
        
        # Posisi di tengah layar
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw/2) - (400/2)
        y = (sh/2) - (270/2)
        warn_win.geometry(f"400x270+{int(x)}+{int(y)}")

        # Label Header
        tk.Label(warn_win, text="⚠️ PERINGATAN KEAMANAN ⚠️", 
                 bg="#dc3545", fg="white", font=("Helvetica", 12, "bold"),
                 pady=10).pack(fill=tk.X)

        # Isi Pesan
        tk.Label(warn_win, text=message, 
                 bg="#f8d7da", fg="#721c24", font=("Helvetica", 10),
                 wraplength=350, pady=20).pack()

        # Tombol Tutup
        close_btn = tk.Button(warn_win, text="SAYA MENGERTI", 
                      command=warn_win.destroy,
                      bg="#dc3545", fg="white", 
                      font=("Helvetica", 11, "bold"), 
                      activebackground="#a71d2a", activeforeground="white",
                      relief="flat", 
                      cursor="hand2") 

        close_btn.pack(pady=15, ipadx=40, ipady=5)
        self.root.bell()
        
    # Fungsi untuk mereset ke mood default (GREETING)
    def reset_ke_default(self):
        self.current_mood = "GREETING"
        self.frame_index = 0
        self.timer_reset = None

    # Fungsi untuk menjalankan main loop UI
    def run(self):
        self.root.mainloop()

def init_pet():
    return ReactionUI()