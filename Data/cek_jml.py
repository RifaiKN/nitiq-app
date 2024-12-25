import os

# def check_subfolder_file_count(parent_directory, expected_count=12):
#     """
#     Memeriksa setiap subfolder dalam parent_directory untuk memastikan jumlah file sama dengan expected_count.
    
#     Args:
#         parent_directory (str): Path ke direktori induk.
#         expected_count (int): Jumlah file yang diharapkan di setiap subfolder.
    
#     Returns:
#         None
#     """
#     # Pastikan direktori induk ada
#     if not os.path.isdir(parent_directory):
#         print(f"Direktori '{parent_directory}' tidak ditemukan.")
#         return
    
#     # Iterasi melalui semua subfolder langsung
#     subfolders = [f.path for f in os.scandir(parent_directory) if f.is_dir()]
    
#     if not subfolders:
#         print(f"Tidak ada subfolder ditemukan dalam direktori '{parent_directory}'.")
#         return
    
#     # Iterasi melalui setiap subfolder dan hitung jumlah file
#     for subfolder in subfolders:
#         # Hitung jumlah file di subfolder
#         file_count = len([f for f in os.listdir(subfolder) if os.path.isfile(os.path.join(subfolder, f))])
        
#         # Cek apakah jumlah file sesuai dengan yang diharapkan
#         if file_count == expected_count:
#             status = "[OK]"
#         else:
#             status = "[WARNING]"
        
#         # Cetak hasilnya
#         print(f"{status} '{os.path.basename(subfolder)}' memiliki {file_count} file.")
        

def check_subfolder_file_count(parent_directory, expected_count=12):
    """
    Memeriksa setiap subfolder dalam parent_directory untuk memastikan jumlah file sama dengan expected_count.
    Hanya menampilkan subfolder yang tidak memenuhi jumlah file yang diharapkan.
    
    Args:
        parent_directory (str): Path ke direktori induk.
        expected_count (int): Jumlah file yang diharapkan di setiap subfolder.
    
    Returns:
        None
    """
    # Pastikan direktori induk ada
    if not os.path.isdir(parent_directory):
        print(f"Direktori '{parent_directory}' tidak ditemukan.")
        return
    
    # Iterasi melalui semua subfolder langsung
    subfolders = [f.path for f in os.scandir(parent_directory) if f.is_dir()]
    
    if not subfolders:
        print(f"Tidak ada subfolder ditemukan dalam direktori '{parent_directory}'.")
        return
    
    # Flag untuk mengecek apakah ada warning
    has_warning = False
    
    # Iterasi melalui setiap subfolder dan hitung jumlah file
    for subfolder in subfolders:
        # Hitung jumlah file di subfolder
        file_count = len([f for f in os.listdir(subfolder) if os.path.isfile(os.path.join(subfolder, f))])
        
        # Cek apakah jumlah file sesuai dengan yang diharapkan
        if file_count != expected_count:
            status = "[WARNING]"
            has_warning = True
            # Cetak hasilnya hanya jika ada warning
            print(f"{status} '{os.path.basename(subfolder)}' memiliki {file_count} file.")
    
    if not has_warning:
        print("Semua subfolder memiliki jumlah file yang sesuai.")

if __name__ == "__main__":
    # Ganti path berikut dengan path ke direktori utama Anda
    parent_dir = r"D:\OneDrive - Universitas Airlangga\! SKRIPSI\Code\Data\data_split\val"
    
    # Panggil fungsi dengan jumlah file yang diharapkan
    check_subfolder_file_count(parent_dir, expected_count=4)
