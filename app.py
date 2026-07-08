import streamlit as st
from PIL import Image
import detector

print("Detector berhasil dipanggil")

st.set_page_config(
    page_title="Deteksi Kerusakan Apel",
    page_icon="🍎",
    layout="wide"
)

st.markdown("""
<style>

/* Background utama */
.stApp {
    background-color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #f7f7f7;
}

/* Judul */
h1 {
    color: #2E7D32;
    text-align: center;
}

/* Paragraf */
p {
    color: #333333;
}

/* Tombol */
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 25px;
    font-size: 16px;
}

.stButton>button:hover {
    background-color: #388E3C;
    color: white;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background-color: #fafafa;
    border: 2px dashed #4CAF50;
    border-radius: 10px;
    padding: 15px;
}

/* Metric */
[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #dddddd;
    border-radius: 10px;
    padding: 15px;
}

/* Gambar */
img {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

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
