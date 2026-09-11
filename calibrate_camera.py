import os
import cv2
import numpy as np

# Configuration
CHESSBOARD_SIZE = (9, 6)  # Jumlah inner corners (kolom, baris)
SQUARE_SIZE_MM = 25.0     # Ukuran 1 kotak hitam/putih dalam mm (sesuaikan jika dicetak)
SAVE_PATH = os.path.join("calibration", "camera_calibration.yml")

def calibrate():
    # Buat direktori calibration jika belum ada
    os.makedirs("calibration", exist_ok=True)

    # Menyiapkan titik 3D objek di dunia nyata (0,0,0), (1,0,0), (2,0,0) ...
    objp = np.zeros((CHESSBOARD_SIZE[0] * CHESSBOARD_SIZE[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:CHESSBOARD_SIZE[0], 0:CHESSBOARD_SIZE[1]].T.reshape(-1, 2)
    objp = objp * SQUARE_SIZE_MM

    # Array untuk menyimpan titik 3D dan titik 2D dari semua gambar
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Kamera tidak dapat dibuka.")
        return

    print("=== PETUNJUK KALIBRASI ===")
    print("1. Arahkan checkerboard ke kamera dari berbagai sudut & jarak.")
    print("2. Tekan 's' atau SPACEBAR saat garis-garis hijau muncul untuk MENGAMBIL SAMPEL.")
    print("3. Ambil minimal 15 - 20 sampel gambar yang bervariasi.")
    print("4. Tekan 'c' jika sudah cukup sampel untuk MENGHITUNG KALIBRASI.")
    print("5. Tekan 'q' untuk keluar tanpa menyimpan.")
    print("==========================")

    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        display_frame = frame.copy()

        # Cari titik sudut papan catur
        found, corners = cv2.findChessboardCorners(gray, CHESSBOARD_SIZE, None)

        if found:
            # Refine corner detection
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            
            # Gambar pola sudut di tampilan
            cv2.drawChessboardCorners(display_frame, CHESSBOARD_SIZE, corners2, found)
            cv2.putText(display_frame, "Ready! Press 'SPACE' to capture", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(display_frame, "Checkerboard not found", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.putText(display_frame, f"Captured Samples: {count}", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        cv2.imshow("Camera Calibration", display_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord(' ') or key == ord('s'):
            if found:
                objpoints.append(objp)
                imgpoints.append(corners2)
                count += 1
                print(f"[+] Sampel ke-{count} berhasil disimpan!")
            else:
                print("[-] Gagal: Checkerboard tidak terdeteksi sempurna.")
        elif key == ord('c'):
            if count < 10:
                print(f"[-] Sampel terlalu sedikit ({count}). Ambil minimal 10-15 sampel!")
            else:
                print("\n[...] Menghitung matriks kalibrasi kamera (tunggu sebentar)...")
                h, w = gray.shape[:2]
                ret_val, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
                    objpoints, imgpoints, (w, h), None, None
                )

                print(f"[SUCCESS] RMS Re-projection Error: {ret_val:.4f} pixels")

                # Menyimpan hasil ke file YAML
                cv_file = cv2.FileStorage(SAVE_PATH, cv2.FILE_STORAGE_WRITE)
                cv_file.write("camera_matrix", camera_matrix)
                cv_file.write("distortion_coefficients", dist_coeffs)
                cv_file.release()

                print(f"[OK] File kalibrasi berhasil disimpan di: {SAVE_PATH}")
                break
        elif key == ord('q'):
            print("Proses dipatalkan.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    calibrate()