# METC Hackathon Guardian Sider

## Informasi Peserta

|        |                    |                              |
| :----: | :----------------: | :--------------------------: |
| **No** |      **Nama**      |      **Email Dicoding**      |
|    1   |  RUDY EKO PRASETYA | rudyekoprasetya\@yahoo.co.id |
|    2   | DIMAS ARYA PRATAMA |      da836298\@gmai.com      |


### Topik : Digital Finance
### Ringkasan Eksekutif

Meskipun ribuan situs telah diblokir setiap hari oleh pemerintah, strategi "kucing-kucingan" para pelaku yang menggunakan berbagai teks dan istilah slang untuk mengelabui sistem filter masih menghambat pengawasan judi online di Indonesia. Sebuah sistem klasifikasi teks yang akurat dan efisien secara komputasi diperlukan untuk strategi promosi yang signifikan di portal berita dan kolom komentar media sosial \[1]. Pendekatan berbasis Deep Learning seringkali membutuhkan sumber daya komputasi yang besar dan waktu \[2] inferensi yang lama. Akibatnya, metode alternatif yang lebih sederhana dapat tetap berhasil dalam mengidentifikasi pola kata kunci khusus dalam bahasa Indonesia dengan tingkat kinerja yang lebih tinggi  \[3].

Solusi yang diberikan untuk masalah ini adalah Guardian Sider. Dengan metode TF-IDF (Term Frequency-Inverse Document Frequency) yang digunakan bersama dengan algoritma Random Forest. Tf-IDF sangat baik dalam mengekstraksi fitur kata kunci diskriminatif seperti "gacor", "deposit", dan "maxwin", yang memiliki banyak informasi dalam konteks perjudian \[4], sementara algoritma Random Forest mampu menangani data teks yang sangat besar dengan stabilitas yang luar biasa. Sebagai algoritma kelompok, Random Forest memiliki keunggulan dalam mengurangi risiko overfitting dan memberikan transparansi melalui fitur fitur penting \[5], yang memungkinkan Tujuan dari proyek ini adalah untuk mengevaluasi sejauh mana kombinasi kedua pendekatan ini dapat memberikan deteksi yang akurat dan responsif terhadap dinamika konten judi online di Indonesia. 

### Deskripsi Product/Aplikasi

Sistem Guardian Sider  ini dimaksudkan untuk memberikan perlindungan digital real-time dengan kemampuan untuk mendeteksi konten perjudian online langsung dari layar pengguna. Proses dimulai dengan pengambilan gambar layar secara berkala. Kemudian, teknologi OCR dari pustaka Tesseract digunakan untuk mengubah gambar tersebut menjadi data teks. Tahapan ini sangat penting karena promosi judi online saat ini sering dikemas dalam bentuk visual atau grafis untuk menghindari sensor teks konvensional. Oleh karena itu, pendekatan berbasis penglihatan komputer sekarang menjadi yang paling efektif dalam pengumpulan data. 

Metode TF-IDF digunakan untuk memproses data teks yang berhasil diekstraksi untuk mempertimbangkan kata-kata kunci tertentu yang menunjukkan perjudian dalam bahasa Indonesia. Algoritma Random Forest digunakan untuk mengkategorikan hasil pemrosesan tersebut karena sangat efisien dalam membuat keputusan cepat tanpa membebani sumber daya perangkat keras secara berlebihan. Model ini harus memetakan pola-pola bahasa promosi dan memberikan skor kemungkinan risiko untuk konten yang sedang aktif di layar pengguna. 

Sistem ini mengintegrasikan lapisan verifikasi sekunder melalui keamanan konten Azure AI untuk menjamin tingkat akurasi yang tinggi dan mengurangi kesalahan deteksi (false positive). Jika model lokal (Random Forest) menunjukkan keraguan atau ambiguitas dalam klasifikasi, sistem secara otomatis akan mengirimkan data tersebut ke layanan cloud Azure untuk analisis mendalam. Aplikasi akan mengirimkan peringatan kepada pengguna segera jika konten dikonfirmasi berbahaya, menciptakan ekosistem deteksi yang hibrida, fleksibel, dan responsif terhadap ancaman judi online yang kian berkembang. 

### Fitur Utama dan Teknologi yang Digunakan

Pengoperasian Guardian Sider dimulai dengan mengeksekusi skrip utama di lingkungan Python. Ini akan mengaktifkan seluruh modul latar belakang, termasuk pengawasan layar dan mesin klasifikasi, secara otomatis. Pengguna dapat melakukan aktivitas digital seperti biasa setelah aplikasi berjalan, seperti melihat situs web dan berinteraksi melalui platform pesan singkat. Sistem akan mengambil gambar dari area aktif secara periodik dan otomatis, mengubah elemen visual menjadi data teks menggunakan teknologi Tesseract OCR. Kemudian, data teks tersebut diproses secara instan oleh model klasifikasi lokal berbasis TF-IDF dan Random Forest untuk mengidentifikasi apakah konten tersebut dianggap sebagai perjudian online. 

Setiap kali analisis model lokal menemukan ambiguitas atau ambang batas probabilitas yang menunjukkan keraguan, sistem cerdas akan mengirimkan data ke Keamanan Konten Azure AI untuk verifikasi tambahan. Setiap konten dievaluasi dengan tingkat akurasi yang lebih tinggi untuk menghindari kesalahan deteksi berkat integrasi kecerdasan buatan berbasis cloud ini. Guardian Sider akan segera mengirimkan peringatan formal pada layar pengguna jika sistem hibrida ini mengonfirmasi bahwa konten yang ditampilkan di layar mengandung unsur judi online. Ini akan memberikan informasi tentang potensi ancaman untuk menjaga keamanan ekosistem digital secara real-time. 



|                  |                             |                                                                                                                  |
| :--------------: | :-------------------------: | :--------------------------------------------------------------------------------------------------------------: |
|     Komponen     |          Teknologi          |                                                       Peran                                                      |
|   Vision Engine  |      **Tesseract OCR**      |           Mengubah informasi visual (gambar promosi, spanduk, teks di layar) menjadi data teks mentah.           |
|  Text Processing |       **Scikit-learn**      |              Melakukan cleaning, tokenization, dan transformasi teks menggunakan TF-IDF Vectorizer.              |
|  Classification  |      **Random Forest**      |            Algoritma ensemble lokal yang memutuskan apakah teks mengandung konten judi secara instan.            |
| Cloud Validation | **Azure AI Content Safety** | Digunakan sebagai API eksternal untuk melakukan analisis mendalam jika model lokal mendeteksi ambiguitas tinggi. |

### Cara Penggunaan Product

1. Clone Project dari Github
```bash
   git clone https://github.com/dimsarya/guardian-sider.git
```

2. Masuk ke project 
```bash
cd guardian-sider
```

3. Buat Environment

```bash
python -m venv venv
```

4. Aktivasi Virtual environment
```bash
source venv/bin/activate
```

5. Lakukan install library

```bash
pip install -r requiremenst.txt
```

6. Jalankan aplikasi

```bash
python3 guardian_sider.py
```

7. Setelah skrip berjalan, berikut adalah apa yang terjadi di balik layar

   1. **Background Capture:** Aplikasi menggunakan `PyAutoGUI` untuk mengambil gambar layar setiap 5 detik.

   2. **OCR Processing:** `Tesseract` mengekstraksi setiap kata yang muncul pada jendela aktif (browser atau chat).

   3. **Local Analysis:** Teks dimasukkan ke model **Random Forest**.

      1. _Hasil Pasti:_ Jika probabilitas konten judi > 0.85, notifikasi langsung muncul.

      2. _Hasil Ragu-ragu:_ Jika probabilitas antara 0.5 - 0.7, sistem mengirimkan teks ke **Azure AI Content Safety**.

   4. **Display Notification:** Jika terkonfirmasi berbahaya, sistem akan memanggil fungsi untuk memunculkan notifikasi pop-up di layar pengguna:


### Rerefensi

\[1] IJAIDM, "Performance Evaluation of Support Vector Machine and Random Forest for Classifying Online Gambling Spam Comments in Indonesian-language YouTube Data," _Indonesian Journal of Artificial Intelligence and Data Mining_, vol. 9, no. 1, 2026.

\[2] "Comparative Study of Feature Extraction Methods for Indonesian Illegal Content Detection: TF-IDF vs. Word2Vec," _Procedia Computer Science_, vol. 269, pp. 979-992, 2025.

\[3] IIETA, "A Deep Learning and AutoML-Based Multimodal Text Extraction Framework for Detecting Online Gambling Advertisements in Indonesian Social Media," _International Journal of Safety and Security Engineering_, vol. 14, no. 2, 2024.

\[4] M. C. T. Manullang et al., "Optimizing Random Forest Classifier for Cybercrime Content Detection using TF-IDF Vectorization," _Journal of Applied Informatics and Computing_, vol. 9, no. 1, 2025.

\[5] Meswari and Ritonga, "Analysis of the Phenomenon of Online Gambling Among University Students: Trends and Financial Challenges," _Jurnal Ar-Rasyid_, vol. 3, no. 2, 2023.
