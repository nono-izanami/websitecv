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

/* Background */
.stApp{
    background-color:white;
}

/* Semua teks */
html, body, [class*="css"], [data-testid="stAppViewContainer"] {
    color: black !important;
}

/* Judul */
h1,h2,h3,h4,h5,h6{
    color:black !important;
}

/* Paragraf */
p,span,label,div{
    color:black !important;
}

/* File uploader */
[data-testid="stFileUploader"] label{
    color:black !important;
}

/* Metric */
[data-testid="stMetric"] label,
[data-testid="stMetricValue"]{
    color:black !important;
}

/* Success/Error message */
[data-testid="stAlert"]{
    color:black !important;
}

/* Button */
.stButton>button{
    color:white !important;
    background:#4CAF50;
}

</style>
""", unsafe_allow_html=True)

st.title("Deteksi Kerusakan Apel")

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
