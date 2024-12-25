import streamlit as st
import torch
from torchvision import transforms, models
from PIL import Image
import pandas as pd
import os
import requests
from io import BytesIO
from math import ceil
import base64

st.set_page_config(
    page_title="NITIQ - Nitik Intelligence for Quality Prediction",
    page_icon="🔍"
    )

# Initialize session state if not already set
if 'page' not in st.session_state:
    st.session_state['page'] = 'Landing Page'
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 1

# Function to handle navigation based on query parameters
def handle_navigation():
    query_params = st.query_params
    page = query_params.get('page', 'Landing Page')
    if page in ["Landing Page", "Daftar Motif", "Prediksi Motif"]:
        st.session_state['page'] = page

# Function to navigate pages and update URL query parameters
def navigate(page_name):
    if page_name in ["Landing Page", "Daftar Motif", "Prediksi Motif"]:
        st.session_state['page'] = page_name
        st.query_params.page = page_name
        st.rerun()
    else:
        st.error("Halaman tidak ditemukan.")

# Load class names
class_names = [
    'Arumdalu', 'Brendhi', 'Cakar Ayam', 'Cinde Wilis', 'Gedhangan', 'Jayakirana',
    'Jayakusuma', 'Kawung Nitik', 'Kemukus', 'Klampok Arum', 'Krawitan',
    'Kuncup Kanthil', 'Manggar', 'Mawur', 'Rengganis', 'Sari Mulat', 'Sekar Andhong',
    'Sekar Blimbing', 'Sekar Cengkeh', 'Sekar Dangan', 'Sekar Dhuku', 'Sekar Dlima',
    'Sekar Duren', 'Sekar Gambir', 'Sekar Gayam', 'Sekar Gudhe', 'Sekar Jagung',
    'Sekar Jali', 'Sekar Jeruk', 'Sekar Keben', 'Sekar Kemuning', 'Sekar Kenanga',
    'Sekar Kenikir', 'Sekar Kenthang', 'Sekar Kepel', 'Sekar Ketongkeng',
    'Sekar Lintang', 'Sekar Liring', 'Sekar Manggis', 'Sekar Menur', 'Sekar Mindi',
    'Sekar Mlathi', 'Sekar Mrica', 'Sekar Mundhu', 'Sekar Nangka', 'Sekar Pacar',
    'Sekar Pala', 'Sekar Pijetan', 'Sekar Pudhak', 'Sekar Randhu', 'Sekar Sawo',
    'Sekar Soka', 'Sekar Srengenge', 'Sekar Srigadhing', 'Sekar Tanjung',
    'Sekar Tebu', 'Sritaman', 'Tanjung Gunung', 'Truntum Kurung', 'Worawari Rumpuk'
]

# Load motif data
@st.cache_data
def load_motif_data(csv_path='daftar_motif.csv'):
    df = pd.read_csv(csv_path, sep=";")
    return df

motif_df = load_motif_data()

# Load the model
@st.cache_resource
def load_model():
    model = models.vit_b_16()
    if isinstance(model.heads, torch.nn.Sequential) and len(model.heads) > 0 and isinstance(model.heads[0], torch.nn.Linear):
        in_features = model.heads[0].in_features
    else:
        raise RuntimeError("Unexpected structure of model.heads")
    
    # Replace the classification heads with a new one that includes dropout
    model.heads = torch.nn.Sequential(
        torch.nn.Dropout(0.1),
        torch.nn.Linear(in_features, 60)
    )
    model.load_state_dict(torch.load('model_vit16_run_1_lr0.0001_bs32_dr0.10.pth', map_location=torch.device('cpu')))
    model.eval()
    return model

model = load_model()

# Validation transforms
val_transforms = transforms.Compose([
    transforms.Resize(size=(224, 224), interpolation=transforms.InterpolationMode.BILINEAR),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Function to display centered logo with link
def display_logo():
    logo_path = "logo.png"  # Replace with the correct path
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        logo_html = f'''
            <a href="?page=Landing Page">
                <img src="data:image/png;base64,{encoded}" width="100" style="display:block;margin-left:auto;margin-right:auto;">
            </a>
        '''
        st.markdown(logo_html, unsafe_allow_html=True)
    else:
        st.warning(f"Gambar logo tidak ditemukan di path: {logo_path}")

# Landing Page
def landing_page():
    display_logo()
    st.title("NITIQ")
    st.markdown("*Nitik Intelligence for Quality Prediction*")
    st.write("Selamat datang di Aplikasi Pengenalan Motif Batik Nitik \"NITIQ\". Berikut adalah tutorial singkat untuk menggunakan aplikasi ini:")

    st.markdown("""
    ### Cara Menggunakan Aplikasi
    1. **Daftar Motif**: Lihat dan pelajari berbagai motif batik yang tersedia.
    2. **Prediksi Motif**: Unggah gambar batik Anda dan aplikasi akan mengklasifikasikannya ke dalam salah satu motif yang telah tersedia.

    Navigasi antar halaman dapat dilakukan menggunakan tombol di bawah ini.
    """)

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Daftar Motif"):
            navigate("Daftar Motif")
    with col2:
        if st.button("Prediksi Motif"):
            navigate("Prediksi Motif")

# Pagination buttons for motif listing
def render_pagination_buttons(total_pages, position):
    cols = st.columns([1, 3, 1])
    with cols[1]:
        col_a, col_b, col_c = st.columns([1, 1.2, 1])
        with col_a:
            if st.button("Sebelumnya", key=f'prev_button_{position}'):
                if st.session_state['current_page'] > 1:
                    st.session_state['current_page'] -= 1
                    st.rerun()
        with col_b:
            st.markdown(f"**Halaman {st.session_state['current_page']} dari {total_pages}**", unsafe_allow_html=True)
        with col_c:
            if st.button("Selanjutnya", key=f'next_button_{position}'):
                if st.session_state['current_page'] < total_pages:
                    st.session_state['current_page'] += 1
                    st.rerun()

# Motif Listing Page with Pagination
def daftar_motif():
    display_logo()
    st.title("Daftar Motif Batik")

    # Navigation button
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Halaman Utama", key='nav_landing_page'):
            navigate("Landing Page")
    with col2:
        if st.button("Prediksi Motif", key='nav_prediksi_motif'):
            navigate("Prediksi Motif")
            
    

    st.write("---")

    # Pagination constants
    batch_size = 6
    row_size = 2

    total_motifs = len(motif_df)
    total_pages = ceil(total_motifs / batch_size)

    # Ensure current_page is within range
    if st.session_state['current_page'] > total_pages:
        st.session_state['current_page'] = total_pages

    # Display pagination buttons above the list
    render_pagination_buttons(total_pages, position='top')

    # Function to display the current page
    def display_page(page_number):
        start_idx = (page_number - 1) * batch_size
        end_idx = start_idx + batch_size
        current_df = motif_df.iloc[start_idx:end_idx]

        # Display motifs in rows
        for i in range(0, len(current_df), row_size):
            cols = st.columns(row_size)
            for j in range(row_size):
                if i + j < len(current_df):
                    row = current_df.iloc[i + j]
                    motif_nama = row['nama']
                    motif_gambar = row['gambar']
                    motif_deskripsi = row['deskripsi']

                    with cols[j]:
                        st.write(f"**Motif:** {motif_nama}")
                        # Display centered image
                        if motif_gambar.startswith('http://') or motif_gambar.startswith('https://'):
                            try:
                                response = requests.get(motif_gambar)
                                image = Image.open(BytesIO(response.content))
                                st.image(image, use_container_width='auto', caption=motif_nama)
                            except Exception as e:
                                st.warning(f"Gagal memuat gambar dari URL: {motif_gambar}. Error: {e}")
                        else:
                            if os.path.exists(motif_gambar):
                                image = Image.open(motif_gambar)
                                st.image(image, use_container_width='auto', caption=motif_nama)
                            else:
                                st.warning(f"Gambar untuk motif {motif_nama} tidak ditemukan di path: {motif_gambar}")
                        # Display description
                        st.write(f"**Keterangan:** {motif_deskripsi}")
                        # st.write("---")

    # Display current page
    display_page(st.session_state['current_page'])

    # Display pagination buttons below the list
    render_pagination_buttons(total_pages, position='bottom')

# Prediction Page
def prediksi_motif():
    display_logo()
    st.title("Prediksi Motif Batik")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Halaman Utama"):
            navigate("Landing Page")
    with col2:
        if st.button("Daftar Motif"):
            navigate("Daftar Motif")

    st.write("---")
    st.write("### Prediksi Motif Batik Nitikmu Sekarang Juga!")

    # Button contoh prediksi
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Contoh 1 - Arumdalu"):
            example_image_path = 'example_arumdalu.JPG'
    with col2:
        if st.button("Contoh 2 - Kawung Nitik"):
            example_image_path = 'example_kawungnitik.jpg'
    
    # File uploader untuk upload manual
    uploaded_file = st.file_uploader("Upload gambar", type=["jpg", "png", "jpeg"], key='file_uploader_prediksi')

    # Prioritas ke contoh jika tombol ditekan
    if 'example_image_path' in locals():
        uploaded_file = example_image_path

    if uploaded_file is not None:
        try:
            if isinstance(uploaded_file, str):
                img = Image.open(uploaded_file).convert("RGB")
            else:
                img = Image.open(uploaded_file).convert("RGB")
            
            st.image(img, caption="Gambar yang Diunggah", width=300)

            # Center crop image
            def center_crop_image(image):
                width, height = image.size
                if width == height:
                    return image  # Already square
                size = min(width, height)
                left = (width - size) / 2
                top = (height - size) / 2
                right = (width + size) / 2
                bottom = (height + size) / 2
                return image.crop((left, top, right, bottom))

            cropped_img = center_crop_image(img)

            # Transform and predict
            img_tensor = val_transforms(cropped_img).unsqueeze(0)
            with st.spinner('Sedang memproses...'):
                with torch.no_grad():
                    output = model(img_tensor)
                    probabilities = torch.nn.functional.softmax(output, dim=1)
                    predicted_class = probabilities.argmax().item()

            predicted_motif = class_names[predicted_class]
            motif_description = motif_df[motif_df['nama'] == predicted_motif]['deskripsi'].values
            motif_description = motif_description[0] if len(motif_description) > 0 else "Deskripsi tidak tersedia."

            st.success(f"**Motif Teridentifikasi:** {predicted_motif}")
            st.write(f"**Makna Motif:** {motif_description}")

        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses gambar: {e}")
    else:
        st.write("Silakan unggah gambar untuk melakukan prediksi atau gunakan contoh prediksi di atas.")

# Call the navigation handler on app load
handle_navigation()

# Display the current page
page = st.session_state['page']

if page == "Landing Page":
    landing_page()
elif page == "Daftar Motif":
    daftar_motif()
elif page == "Prediksi Motif":
    prediksi_motif()
else:
    st.error("Halaman tidak ditemukan.")