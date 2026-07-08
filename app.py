import streamlit as st
from PIL import Image
import detector

print("Detector berhasil dipanggil")

st.set_page_config(
    page_title="Deteksi Kerusakan Apel",
    page_icon="🍎",
    layout="wide"
)

st.title("🍎 Deteksi Kerusakan Apel")

st.write(
    "Upload gambar apel kemudian klik **Deteksi**."
)

uploaded = st.file_uploader(
    "Pilih gambar",
    type=["jpg","jpeg","png"]
)

if uploaded is not None:

    image = Image.open(uploaded)

    st.image(image, use_container_width=True)

    if st.button("Deteksi"):

        hasil,persen,maskApel,maskRusak = detector.detect(image)

        if hasil=="Apel Rusak":
            st.error(hasil)
        else:
            st.success(hasil)

        st.metric(
            "Persentase Kerusakan",
            f"{persen:.2f}%"
        )

        col1,col2=st.columns(2)

        with col1:
            st.image(maskApel,
                     caption="Mask Apel")

        with col2:
            st.image(maskRusak,
                     caption="Area Rusak")
