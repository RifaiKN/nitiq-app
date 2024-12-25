import os
import shutil

def copy_directory_structure(src, dest):
    for root, dirs, files in os.walk(src):
        # Hitung path relatif dari direktori sumber
        rel_path = os.path.relpath(root, src)
        # Tentukan path tujuan
        dest_path = os.path.join(dest, rel_path)
        # Buat direktori di tujuan jika belum ada
        os.makedirs(dest_path, exist_ok=True)
        print(f"Direktori dibuat: {dest_path}")

if __name__ == "__main__":
    src_directory = 'D:/OneDrive - Universitas Airlangga/! SKRIPSI/Code/Data/data_split/train'
    dest_directory = 'D:/OneDrive - Universitas Airlangga/! SKRIPSI/Code/Data/data_split/test'
    
    copy_directory_structure(src_directory, dest_directory)
    print("Struktur direktori berhasil disalin.")