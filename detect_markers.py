import cv2
import numpy as np

# Mapping ID Marker ke Peran (Sesuai Spesifikasi Task)
MARKER_ROLES = {
    0: "Standby",
    1: "Ambil",
    2: "Lepas",
    3: "Putar CW",
    4: "Putar CCW"
}

def main():
    # Setup ArUco Dictionary 4x4_50
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    
    # Penanganan kompatibilitas versi OpenCV (4.7+ vs versi lama)
    if hasattr(cv2.aruco, 'ArucoDetector'):
        parameters = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
        use_new_api = True
    else:
        parameters = cv2.aruco.DetectorParameters_create()
        use_new_api = False

    # Inisialisasi Webcam (Index 0 biasanya webcam internal laptop)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Kamera tidak dapat diakses!")
        return

    print("Program berjalan. Tekan 'q' pada window video untuk keluar.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Gagal mengambil frame dari kamera.")
            break

        # 1. Deteksi Marker
        if use_new_api:
            corners, ids, rejected = detector.detectMarkers(frame)
        else:
            corners, ids, rejected = cv2.aruco.detectMarkers(frame, aruco_dict, parameters=parameters)

        # 2. Jika ada marker yang terdeteksi
        if ids is not None and len(ids) > 0:
            # Gambar kotak hijau pada marker
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

            # Iterasi setiap marker yang terdeteksi
            for i, marker_id in enumerate(ids.flatten()):
                # Dapatkan peran berdasarkan ID (Default: 'Unknown' jika ID > 4)
                role = MARKER_ROLES.get(int(marker_id), "Unknown")
                label = f"ID {marker_id} - {role}"

                # Ambil koordinat pojok kiri atas marker untuk posisi teks
                corner = corners[i][0]
                top_left = (int(corner[0][0]), int(corner[0][1]) - 10)

                # Tampilkan label di layar video
                cv2.putText(
                    frame,
                    label,
                    top_left,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

                # Tampilkan output ke console/terminal
                print(f"[DETECTED] {label}")

        # Tampilkan frame di window
        cv2.imshow("HEROES GMRT - ArUco Detection", frame)

        # Tekan tombol 'q' untuk berhenti
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()