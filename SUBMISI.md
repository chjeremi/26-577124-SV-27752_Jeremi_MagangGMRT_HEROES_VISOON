# Dokumentasi Submisi.md - Tugas Seleksi Subtim Heroes bagian Vision

## Informasi Submisi
- **Nama:** Jeremi Christian
- **NIM:** 26/577124/SV/27752
- **Link Video Demo (YouTube):**[Lihat Video Demo YouTube Shorts](https://youtube.com/shorts/UIpY6-ETXvs?si=NBeKcKc5AaSywxGF)
---

## 1. Ringkasan Fitur

| Kategori | Fitur | Status | Deskripsi Ringkas |
| :--- | :--- | :---: | :--- |
| **Wajib** | Real-time WebCam Stream | ✅ | Membuka feed video webcam tanpa kendala latency. |
| **Wajib** | ArUco Marker Detection | ✅ | Mendeteksi marker dari dictionary `DICT_4X4_50`. |
| **Wajib** | Bounding Box & Labeling | ✅ | Menggambar garis tepi dan menampilkan label peran (0: Standby, 1: Ambil, 2: Lepas, 3: Putar CW, 4: Putar CCW). |
| **Wajib** | Robustness & Multi-Detection | ✅ | Bebas crash jika tidak ada marker dan mendukung banyak marker sekaligus dalam 1 frame. |
| **Bonus** | Camera Calibration | ✅ | Menggunakan checkerboard untuk mendapatkan matriks kamera dan koefisien distorsi. |
| **Bonus** | Pose Estimation | ✅ | Menghitung jarak presisi (cm) dan sudut orientasi (yaw) marker terhadap kamera. |
| **Bonus** | 3D Frame Axes Visualization | ✅ | Menggambar sumbu 3D (X: Merah, Y: Hijau, Z: Biru) di tengah marker. |

---

## 2. Struktur Repositori

```text
penugasan_Vision_heroes/
├── calibration/
│   └── camera_calibration.yml  # File hasil kalibrasi kamera (matriks & distorsi)
├── .gitignore                  # Mengabaikan venv dan file temporary
├── calibrate_camera.py         # Script tambahan untuk proses kalibrasi kamera (checkerboard)
├── detect_markers.py           # Script utama deteksi ArUco & Pose Estimation
├── requirements.txt            # Dependensi library Python
└── SUBMISI.md                  # Dokumentasi laporan submisi ini
```
## 3. Penjelasan Teknis & Alur Kode

* **Inisialisasi & Kompatibilitas API**  
  Kode memanfaatkan fungsi `hasattr(cv2.aruco, 'ArucoDetector')` untuk menjamin kompatibilitas silang (*cross-compatibility*) antara OpenCV versi baru (4.7+) dan versi lama.

* **Mapping Peran Marker**  
  Peran setiap marker dikelola melalui *dictionary* `MARKER_ROLES`. Pendekatan ini mempermudah pemeliharaan kode serta penambahan ID baru tanpa perlu mengubah logika utama program.

* **Pose Estimation & Trigonometri 3D**  
  * **Method:** Menggunakan `cv2.solvePnP` dengan acuan `MARKER_SIZE_CM = 10.0`.
  * **Jarak:** Dihitung menggunakan persamaan jarak Euclidean 3D:
    $$\text{Jarak} = \sqrt{x^2 + y^2 + z^2}$$
  * **Orientasi:** Sudut dihitung dari matriks rotasi (menggunakan `cv2.Rodrigues`) untuk mengekstrak sudut *yaw* relatif terhadap posisi kamera.

---

## 4. Panduan Menjalankan Program

### Prasyarat
* **Python:** 3.9+
* **OS:** Linux (Ubuntu / Debian)

### Langkah-Langkah

1. **Aktifkan Virtual Environment**
   ```bash
   source .venv/bin/activate
   
2. **Jalankan Deteksi Real-Time**
   ```bash
   python3 detect_markers.py

Catatan: Tekan tombol q pada jendela tampilan video untuk menghentikan program.
