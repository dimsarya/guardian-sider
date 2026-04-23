# Library-library yang dibutuhkan
import requests 
import time 

import sys

import joblib  # Untuk memuat model dan vectorizer yang sudah dilatih

import mss # Untuk menangkap layar
import pytesseract # Untuk OCR (Optical Character Recognition)
from PIL import Image # Untuk manipulasi gambar 

import threading # Untuk menjalankan monitoring layar di thread terpisah

import reaction_ui # Untuk UI

import ctypes # Untuk mengatur DPI Awareness di Windows

# Konfigurasi Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Memaksa Windows agar mengunci DPI aplikasi
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# Konfigurasi API 
AZURE_ENDPOINT = "YOUR_AZURE_ENDPOINT"
AZURE_KEY = "YOUR_AZURE_KEY"

# Muat model dan vectorizer yang sudah dilatih
try:
    model = joblib.load('models/model_final.pkl')
    vectorizer = joblib.load('models/tfidf_vectorizer.pkl')
except:
    print("Gagal memuat model! Pastikan file .pkl tersedia.")
    sys.exit()

# Fungsi pendeteksi 
def analyze_content(text):
    # Kata-kata kunci yang umum digunakan dalam konten "Situs Berbahaya"
    blacklist = ['slot', 'gacor', 'wd', 'togel', 'kasino', 'casino', 
                 'jackpot', 'deposit', 'withdraw', 'bonus', 'promo', 
                 'live casino', 'maxwin', 'spin', 'bonus', 'hoki', 
                 'menang', 'link', 'daftar', 'login', 'situs', 'agen', 
                 'terpercaya', 'prediksi', 'tebak'
                ]

    # Jika ditemukan kata-kata kunci, langsung tandai sebagai "Situs Berbahaya"
    if any(word in text.lower() for word in blacklist):
        return "Situs Berbahaya", 1.0, "HARD_RULE"

    # Model Lokal AI
    vec = vectorizer.transform([text.lower()])
    prob = model.predict_proba(vec)[0]
    hasil = model.predict(vec)[0]
    confidence = max(prob)

    # Jika confidence rendah, tandai sebagai "Ragu-Ragu" kemudian trigger Azure AI Content Safety
    if confidence < 0.85:
        return "Ragu-Ragu", confidence, "TRIGGER_AZURE"
    
    label = "Situs Berbahaya" if hasil == 1 else "Situs Aman"
    return label, confidence, "LOCAL_AI"

# Memanggil Azure Content Safety untuk analisis lebih dalam jika model lokal ragu-ragu
def call_azure_content_safety(text):
    # URL dan header untuk API Azure Content Safety
    # URL Example :
    url = f"{AZURE_ENDPOINT}/contentsafety/text:analyze?api-version=2023-10-01"
    
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/json"
    }
    
    # Payload Azure Content Safety
    payload = {"text": text}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        if response.status_code == 200:
            result = response.json()

            categories = result.get('categoriesAnalysis', [])
            is_dangerous = any(cat.get('severity', 0) > 0 for cat in categories)
            
            if is_dangerous:
                return "Situs Berbahaya", 1.0, "AZURE_CLOUD"
            else:
                return "Situs Aman", 1.0, "AZURE_CLOUD"
    except Exception as e:
        print(f"Gagal terkoneksi dengan Azure: {e}")
    
    return "Timeout", 0.0, "ERROR_AZURE"

# Memonitoring layar 
def screen_monitoring_loop(avatar_sider):
    with mss.mss() as sct:
        while True:
            # Ambil Layar
            sct.shot(output="sct.png")
            
            # OCR (Baca teks dari gambar)
            try:
                extracted_text = pytesseract.image_to_string(Image.open("sct.png"), lang='ind+eng')
            except:
                extracted_text = ""
            
            if len(extracted_text.strip()) > 5:
                label, score, source = analyze_content(extracted_text)
                
                # Jika model lokal ragu-ragu, langsung panggil Azure Content Safety untuk analisis lebih dalam
                if label == "Ragu-Ragu":
                    print(f"ML Ragu ({score:.2%}). Menghubungkan ke Azure...")
                    label, score, source = call_azure_content_safety(extracted_text)

                # Reaksi UI 
                if label == "Situs Berbahaya":
                    avatar_sider.reaksi("ANGRY")
                    avatar_sider.show_warning("Teridentifikasi terdapat situs berbahaya oleh sistem keamanan kami. Segera tutup situs tersebut dan pastikan untuk tidak memasukkan informasi pribadi apapun!")
                    print(f"Hasil: {label} ({score:.2%}) via {source}")
                
                elif label == "Situs Aman":
                    avatar_sider.reaksi("GREETING")
                    print(f"Hasil: {label} ({score:.2%}) via {source}")
                
                else:
                    avatar_sider.reaksi("DOUBT") 
                    print(f"Hasil: Tidak diketahui via {source}")

            # Waktu tunggu sebelum pengambilan berikutnya 
            time.sleep(5)

# Jalankan program utama
if __name__ == "__main__":
    avatar_sider = reaction_ui.init_pet()
    threading.Thread(target=lambda: screen_monitoring_loop(avatar_sider), daemon=True).start()
    avatar_sider.root.mainloop()