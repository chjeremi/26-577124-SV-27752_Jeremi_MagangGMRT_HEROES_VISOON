"""
Script Deteksi ArUco Marker - HEROES GMRT ABU Robocon.

Tujuan:
Membuka feed video dari webcam secara real-time, mendeteksi ArUco marker 
(dictionary DICT_4X4_50), menggambar bounding box, serta menampilkan label 
peran (Standby, Ambil, Lepas, Putar CW, Putar CCW) langsung pada layar video 
dan terminal.
"""

import cv2
import numpy as np

# --- Pemetaan ID Marker ke Peran Robot ---
# Disimpan dalam dictionary supaya maintainable dan gak ada hardcode angka di tengah logika
MARKER_ROLES = {
    0: "Standby",
    1: "Ambil",
    2: "Lepas",
    3: "Putar CW",
    4: "Putar CCW"
}


def main():
    # 1. Inisialisasi ArUco Dictionary
    # Wajib match sama yang digenerate di chev.me/arucogen (4x4, kapasitas 50 ID)
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    
    # 2. Backward & Forward Compatibility Handling
    # OpenCV versi 4.7.0 ke atas ngenalin class `ArucoDetector`.
    # Pengecekan ini bikin script aman dijalankan di OpenCV versi baru maupun lama tanpa throwing AttributeError.
    if hasattr(cv2.aruco, 'ArucoDetector'):
        parameters = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
        use_new_api = True
    else:
        parameters = cv2.aruco.DetectorParameters_create()
        use_new_api = False

    # 3. Setup Capture Device (Webcam)
    # Index 0 = webcam bawaan laptop/USB cam pertama
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Kamera tidak dapat diakses! Cek apakah webcam dipakai aplikasi lain.")
        return

    print("Program berjalan. Arahkan ArUco marker ke kamera.")
    print("Tekan 'q' pada window video untuk menutup program.")

    # Loop utama pembacaan video stream
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Gagal mengambil frame dari webcam.")
            break

        # 4. Deteksi Marker dalam Frame
        # Returns:
        # - corners: Koordinat 4 sudut piksel dari tiap marker yang ketemu
        # - ids: Array ID dari marker
        # - rejected: Kontur segi empat yang terdeteksi tapi bukan ArUco valid
        if use_new_api:
            corners, ids, rejected = detector.detectMarkers(frame)
        else:
            corners, ids, rejected = cv2.aruco.detectMarkers(frame, aruco_dict, parameters=parameters)

        # 5. Visualisasi & Processing (Jalan cuma kalau ada marker terdeteksi)
        if ids is not None and len(ids) > 0:
            # Gambar garis tepi hijau + indikator titik sudut pertama bawaan OpenCV
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

            # Iterasi setiap marker (bisa handle multi-detection dalam 1 frame)
            for i, marker_id in enumerate(ids.flatten()):
                # Ambil nama peran berdasarkan ID. Kalau dapet ID diluar 0-4, fallback ke 'Unknown'
                role = MARKER_ROLES.get(int(marker_id), "Unknown")
                label = f"ID {marker_id} - {role}"

                # Ambil koordinat sudut kiri atas (top-left) marker sebagai acuan posisi teks
                corner = corners[i][0]
                top_left = (int(corner[0][0]), int(corner[0][1]) - 10)

                # Render teks label di atas marker pada layar video
                cv2.putText(
                    frame,
                    label,
                    top_left,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),  # Warna teks: Hijau (BGR)
                    2             # Ketebalan garis font
                )

                # Output log ke terminal/console
                print(f"[DETECTED] {label}")

        # Tampilkan frame yang udah di-overlay ke window GUI
        cv2.imshow("HEROES GMRT - ArUco Detection", frame)

        # Listen keyboard input (Tutup window dengan tombol 'q')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resource kamera & hancurkan GUI window saat loop selesai
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
