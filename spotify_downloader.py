import os
import sys
import subprocess
import shutil

def check_dependencies():
    """Controlla e installa automaticamente le dipendenze se mancanti."""
    if not shutil.which("spotdl"):
        print("[*] Installazione di spotdl in corso...")
        subprocess.run([sys.executable, "-m", "pip", "install", "spotdl", "-q"], check=True)
    
    if not shutil.which("ffmpeg"):
        print("[*] Configurazione automatica di FFmpeg...")
        subprocess.run(["spotdl", "--download-ffmpeg"], check=True)

def main():
    check_dependencies()

    # Prende l'URL dagli argomenti CLI o lo richiede all'utente
    if len(sys.argv) > 1:
        playlist_url = sys.argv[1].strip()
    else:
        print("\n" + "=" * 50)
        print("       SPOTIFY PLAYLIST DOWNLOADER")
        print("=" * 50)
        playlist_url = input("\nIncolla il link della playlist Spotify: ").strip()

    if not playlist_url:
        print("[!] Errore: nessun URL fornito.")
        sys.exit(1)

    # Imposta la cartella di output con il nome della playlist
    output_pattern = "{list-name}/{artists} - {title}.{output-ext}"

    print(f"\n[*] Download avviato alla massima qualità (320kbps + metadati/copertina)...")
    cmd = [
        "spotdl",
        "download",
        playlist_url,
        "--output", output_pattern,
        "--format", "mp3",
        "--bitrate", "auto",
        "--generate-lrc",
        "--threads", "4"
    ]

    try:
        subprocess.run(cmd, check=True)
        print("\n[+] Playlist scaricata con successo nella rispettiva cartella!")
    except subprocess.CalledProcessError:
        print("\n[!] Si è verificato un errore durante l'estrazione delle tracce.")
    except KeyboardInterrupt:
        print("\n[!] Operazione interrotta dall'utente.")

if __name__ == "__main__":
    main()
