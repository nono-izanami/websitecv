import cv2
import numpy as np
from PIL import Image

from skimage.filters import threshold_otsu
from skimage.morphology import remove_small_objects
from scipy.ndimage import binary_fill_holes

def detect(image):
    print("MASUK FUNCTION DETECT")

    # -------------------------------
    # Konversi PIL ke OpenCV
    # -------------------------------
    img = np.array(image)

    print("Ukuran gambar:", img.shape)

    # -------------------------------
    # Konversi PIL ke OpenCV
    # -------------------------------
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # -------------------------------
    # Resize 300x300
    # (MATLAB : imresize)
    # -------------------------------
    imgResize = cv2.resize(img, (300,300))

    # -------------------------------
    # Grayscale
    # (MATLAB : rgb2gray)
    # -------------------------------
    gray = cv2.cvtColor(imgResize, cv2.COLOR_BGR2GRAY)

    # -------------------------------
    # Median Filter
    # (MATLAB : medfilt2)
    # -------------------------------
    hasilFilter = cv2.medianBlur(gray,3)

       # -------------------------------
    # Ambil channel hijau
    # (MATLAB : imgResize(:,:,2))
    # -------------------------------

    green = imgResize[:,:,1]

    # ==========================================
    # Segmentasi Apel (Background Putih)
    # ==========================================

    gray = cv2.cvtColor(imgResize, cv2.COLOR_BGR2GRAY)

    hasilFilter = cv2.medianBlur(gray,3)

    # Threshold untuk memisahkan background putih
    _, bw_apel = cv2.threshold(
        hasilFilter,
        240,
        255,
        cv2.THRESH_BINARY_INV
    )

    # Fill hole
    bw_apel = binary_fill_holes(bw_apel > 0)

    # Hapus objek kecil
    bw_apel = remove_small_objects(
        bw_apel,
        min_size=500
    )

    bw_apel = bw_apel.astype(np.uint8)

    # Ambil objek terbesar
    numLabels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        bw_apel,
        connectivity=8
    )

    if numLabels > 1:

        largest = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])

        bw_apel = (labels == largest).astype(np.uint8)

    maskApel = (bw_apel * 255).astype(np.uint8)

    # ==========================================
    # Konversi ke HSV
    # ==========================================

    hsv = cv2.cvtColor(imgResize, cv2.COLOR_BGR2HSV)

    # OpenCV:
    # H : 0-179
    # S : 0-255
    # V : 0-255

    S = hsv[:,:,2] / 255.0
    V = hsv[:,:,3] / 255.0

    # ==========================================
    # Deteksi area rusak
    # Sama seperti MATLAB
    # ==========================================

    bw_rusak = (V < 0.6) & (S < 0.8)

    # hanya area apel
    bw_rusak = bw_rusak & (bw_apel > 0)

    # hapus noise kecil
    bw_rusak = remove_small_objects(
        bw_rusak,
        min_size=800
    )

    # fill hole
    bw_rusak = binary_fill_holes(bw_rusak)

    kernel = np.ones((5,5),np.uint8)

    bw_rusak = cv2.morphologyEx(
        bw_rusak.astype(np.uint8),
        cv2.MORPH_OPEN,
        kernel
    )

    maskRusak = bw_rusak * 255

    # ==========================================
    # Hitung luas
    # ==========================================

    area_apel = np.sum(bw_apel)

    area_rusak = np.sum(bw_rusak)

    persen = (area_rusak / area_apel) * 100

    if persen < 5:
        hasil = "Apel Tidak Rusak"
    else:
        hasil = "Apel Rusak"

    print("Area apel:", area_apel)
    print("Area rusak:", area_rusak)
    print("Persen:", persen)

    return (
        hasil,
        persen,
        Image.fromarray(maskApel),
        Image.fromarray(maskRusak)
    )
