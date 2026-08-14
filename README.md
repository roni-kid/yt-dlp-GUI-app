# CustomTkinter GUI for yt-dlp

A lightweight, modern desktop graphical interface for **yt-dlp** built with Python and CustomTkinter.

> **Disclaimer & Acknowledgments:**
> This project is purely a graphical user interface (GUI) wrapper. It does not contain core video extraction or downloading logic. All media downloading and stream handling are powered by the open-source [yt-dlp](https://github.com/yt-dlp/yt-dlp) project, and media processing is handled by [FFmpeg](https://ffmpeg.org/). All credit for the backend engine belongs to their respective maintainers.

---

## Features

* **Modern Dark Theme:** Native-looking, responsive interface built with CustomTkinter.
* **Format Selection:** Easily switch between Video (MP4) and Audio-only (MP3) downloads.
* **Custom Resolution Control:** Limit maximum video resolution (4K, 1080p, 720p, 480p, or Best Available).
* **Directory Picker:** Integrated folder browser to select custom download destinations.
* **Real-time Download Status:** Accurate progress bar tracking download percentage, transfer speed, and ETA without GUI freeze.

---

## Project Structure

```text
YouTubeDownloader/
├── yt-app.py                # Main application code
├── requirements.txt         # Python dependencies
├── .gitignore               # Git ignore configuration
├── LICENSE                  # License file
└── README.md                # Project documentation

```

---

## Prerequisites

* **Python 3.10+** installed on your system.
* **FFmpeg** installed and added to your system `PATH` (required for merging audio/video streams and converting to MP3).

### Installing FFmpeg on Windows:

```cmd
winget install Gyan.FFmpeg

```

---

## Installation & Usage

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/yt-dlp-custom-gui.git
cd yt-dlp-custom-gui

```


2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Run the Application:**
```bash
python app.py

```



---

## Building a Standalone Executable (.exe)

To bundle the application into a single executable file for Windows using PyInstaller:

1. **Install PyInstaller:**
```cmd
pip install pyinstaller

```


2. **Build the executable:**
```cmd
pyinstaller --noconsole --onefile --collect-all customtkinter --collect-all yt_dlp app.py

```


3. Locate the compiled executable inside the generated `dist/` directory.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.