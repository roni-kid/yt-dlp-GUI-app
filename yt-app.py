import os
import threading
import customtkinter as ctk
from customtkinter import filedialog
from PIL import Image, ImageTk
import yt_dlp

# --- CONFIGURATION & COLORS (Vibrant, Neon Accents) ---
VIBRANT_CYAN = "#00FFFF" # Primary Accent
VIBRANT_MAGENTA = "#FF00FF" # Secondary Accent
# Transparent Black/Frosted Glass backdrop simulation
GLASS_COLOR = "#0000000D" # VERY low alpha (only works partially on Win)
GLASS_TEXT = "#FFFFFF"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue") # Basis, we will override most

class GlassYtDlpGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Glassmorphism Yt-Dlp")
        self.geometry("560x520")
        self.resizable(False, False)

        # 1. Load Vibrant Background Image (Required for contrast)
        try:
            bg_image = Image.open("background.jpg")
            # Downscale/crop slightly to ensure vibrancy is visible
            bg_image = bg_image.resize((600, 600), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            
            self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
            self.bg_label.place(relx=0.5, rely=0.5, anchor="center")
        except FileNotFoundError:
            print("WARNING: 'background.jpg' not found. Glass effect will be minimal.")
            self.configure(fg_color="#101010") # Dark matte alternative

        # 2. The Frosted Glass Container (Main Panel)
        # We use CTkFrame, but configure its colors manually.
        self.main_frame = ctk.CTkFrame(
            self, 
            corner_radius=20,
            border_width=1, # Suble single pixel white border
            border_color="#FFFFFF1A", # 10% white transparency
            fg_color="#FFFFFF0D" # VERY high transparency for glass feel (requires vibrant BG)
        )
        self.main_frame.pack(pady=40, padx=40, fill="both", expand=True)

        # --- CONTENT INSIDE GLASS ---

        # Title (Vibrant Glow Accent)
        self.label = ctk.CTkLabel(
            self.main_frame, 
            text="Media Transcoder", 
            font=("Verdana", 24, "bold"),
            text_color=VIBRANT_CYAN
        )
        self.label.pack(pady=(25, 20))

        # URL Input
        self.url_entry = ctk.CTkEntry(
            self.main_frame, 
            placeholder_text="Paste Video or Playlist URL...", 
            width=420,
            corner_radius=10,
            border_width=1,
            border_color="#FFFFFF33", # Faint border
            fg_color="#FFFFFF05", # Subtle dark tint
            text_color="#DDDDDD"
        )
        self.url_entry.pack(pady=10)

        # Output Folder Picker
        self.folder_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.folder_frame.pack(pady=5, fill="x", padx=30)

        self.output_path = ctk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.folder_entry = ctk.CTkEntry(
            self.folder_frame, 
            textvariable=self.output_path, 
            width=360,
            corner_radius=10,
            border_width=0,
            fg_color="#FFFFFF05"
        )
        self.folder_entry.pack(side="left", padx=(0, 10))

        self.browse_btn = ctk.CTkButton(
            self.folder_frame, 
            text="📁 Browse", 
            width=80,
            corner_radius=10,
            fg_color="transparent",
            text_color=VIBRANT_MAGENTA,
            border_width=1,
            border_color=VIBRANT_MAGENTA,
            hover_color="#FF00FF1A" # Magenta tint
        )
        self.browse_btn.configure(command=self.select_folder)
        self.browse_btn.pack(side="left")

        # Format & Resolution Dropdowns
        self.opts_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.opts_frame.pack(pady=15)

        dropdown_args = {
            "values": ["Best Available", "2160p (4K)", "1080p", "720p", "480p"],
            "corner_radius": 10,
            "border_width": 1,
            "border_color": "#FFFFFF33",
            "button_color": VIBRANT_CYAN,
            "button_hover_color": VIBRANT_MAGENTA
}

        self.type_menu = ctk.CTkOptionMenu(
            self.opts_frame, 
            values=["Video (MP4)", "Audio (MP3)"], 
            command=self.toggle_resolution_menu,
            **dropdown_args
        )
        self.type_menu.set("Video (MP4)")
        self.type_menu.grid(row=0, column=0, padx=10)

        self.res_menu = ctk.CTkOptionMenu(
            self.opts_frame, 
            values=["Best", "4K", "1080p", "720p", "480p"], 
            **dropdown_args
        )
        self.res_menu.set("Best")
        self.res_menu.grid(row=0, column=1, padx=10)

        # Progress Bar & Status (Thin, Bright Accent)
        self.progress_bar = ctk.CTkProgressBar(
            self.main_frame, 
            width=420,
            height=6,
            corner_radius=2,
            progress_color=VIBRANT_CYAN,
            fg_color="#FFFFFF1A" # Transparent track
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(25, 5))

        self.status_label = ctk.CTkLabel(
            self.main_frame, 
            text="Ready", 
            font=("Arial", 11, "italic"),
            text_color="#BBBBBB"
        )
        self.status_label.pack(pady=5)

        # Download Button (Glowing Vibrant Accent)
        self.download_btn = ctk.CTkButton(
            self.main_frame, 
            text="EXECUTE DOWNLOAD", 
            width=240, 
            height=42, 
            font=("Verdana", 13, "bold"),
            corner_radius=20,
            fg_color=VIBRANT_CYAN,
            text_color="#000000",
            hover_color=VIBRANT_MAGENTA
        )
        self.download_btn.configure(command=self.start_download_thread)
        self.download_btn.pack(pady=(10, 20))

    # --- FUNCTIONALITY (Remains identical to image_4) ---
    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder: self.output_path.set(folder)

    def toggle_resolution_menu(self, choice):
        s = "disabled" if choice == "Audio (MP3)" else "normal"
        self.res_menu.configure(state=s)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            down = d.get('downloaded_bytes', 0)
            if total > 0:
                p = down / total
                s = d.get('_speed_str', 'N/A').strip()
                self.after(0, self.progress_bar.set, p)
                msg = f"Downloading: {p*100:.1f}% | Speed: {s}"
                self.after(0, self.status_label.configure, {"text": msg, "text_color": VIBRANT_CYAN})
        elif d['status'] == 'finished':
            self.after(0, self.progress_bar.set, 1.0)
            self.after(0, self.status_label.configure, {"text": "Processing...", "text_color": VIBRANT_MAGENTA})

    def start_download_thread(self):
        threading.Thread(target=self.run_download, daemon=True).start()

    def run_download(self):
        url = self.url_entry.get().strip()
        out = self.output_path.get().strip()
        if not url: self.status_label.configure(text="URL Required", text_color="red"); return
        self.download_btn.configure(state="disabled")
        self.progress_bar.set(0)
        self.status_label.configure(text="Starting...", text_color="yellow")
        
        opts = {
            'outtmpl': os.path.join(out, '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
            'quiet': True, 'no_warnings': True,
        }
        if self.type_menu.get() == "Audio (MP3)":
            opts.update({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]})
        else:
            res_c = self.res_menu.get()
            res_m = {"4K": "2160", "1080p": "1080", "720p": "720", "480p": "480"}
            if res_c in res_m: h = res_m[res_c]; opts['format'] = f"bv*[height<={h}][ext=mp4]+ba[ext=m4a]/bv*[height<={h}]+ba/b"
            else: opts['format'] = "bv*[ext=mp4]+ba[ext=m4a]/bv*+ba/b"

        try:
            with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([url])
            self.after(0, self.status_label.configure, {"text": "Complete!", "text_color": "green"})
        except Exception as e:
            self.after(0, self.status_label.configure, {"text": f"Error: {str(e)[:30]}...", "text_color": "red"})
        self.after(0, self.download_btn.configure, {"state": "normal"})

if __name__ == "__main__":
    app = GlassYtDlpGUI()
    app.mainloop()