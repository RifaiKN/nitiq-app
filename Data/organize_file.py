import os
import shutil
from pathlib import Path

def organize_images_ordered_split(source_dir, target_dir, train_ratio=0.75):
    """
    Mengorganisir gambar ke dalam folder train dan val berdasarkan urutan nama file.

    Args:
        source_dir (str): Path ke folder sumber yang berisi semua gambar.
        target_dir (str): Path ke folder target tempat gambar akan diorganisir.
        train_ratio (float): Proporsi data untuk training set (default: 0.75).
    """
    source = Path(source_dir)
    target = Path(target_dir)

    # Membuat folder target jika belum ada
    (target / 'train').mkdir(parents=True, exist_ok=True)
    (target / 'val').mkdir(parents=True, exist_ok=True)

    # Mendefinisikan ekstensi file gambar yang akan diproses
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

    # Mengumpulkan semua file gambar
    all_files = [f for f in source.iterdir() if f.is_file() and f.suffix.lower() in image_extensions]

    # Mengorganisir file berdasarkan kelas
    class_to_files = {}
    for file_path in all_files:
        # Split nama file berdasarkan spasi (tanpa argumen untuk mengabaikan spasi ekstra)
        parts = file_path.stem.split()

        # Pastikan nama file sesuai dengan format yang diharapkan
        if len(parts) < 3:
            print(f"Skipping file '{file_path.name}' karena tidak sesuai dengan format yang diharapkan.")
            continue

        # Ekstrak nama kelas (semua kata setelah indeks dan sebelum nomor gambar)
        class_name = ' '.join(parts[1:-1])

        # Debugging: Tampilkan nama kelas yang diekstrak
        print(f"Ekstrak kelas: '{class_name}' dari file '{file_path.name}'")

        # Tambahkan file ke kelas yang sesuai
        if class_name not in class_to_files:
            class_to_files[class_name] = []
        class_to_files[class_name].append(file_path)

    # Mengorganisir dan membagi data ke dalam train dan val
    for class_name, files in class_to_files.items():
        # Urutkan file berdasarkan nama
        sorted_files = sorted(files, key=lambda x: x.name)

        # Tentukan jumlah training dan validation
        total = len(sorted_files)
        train_count = int(total * train_ratio)
        val_count = total - train_count

        # Bagi file menjadi train dan val
        train_files = sorted_files[:train_count]
        val_files = sorted_files[train_count:]

        # Buat folder kelas di dalam train dan val
        train_class_dir = target / 'train' / class_name
        val_class_dir = target / 'val' / class_name
        train_class_dir.mkdir(parents=True, exist_ok=True)
        val_class_dir.mkdir(parents=True, exist_ok=True)

        # Pindahkan file ke folder train
        for file_path in train_files:
            destination = train_class_dir / file_path.name
            try:
                shutil.move(str(file_path), str(destination))
                print(f"Memindahkan '{file_path.name}' ke folder 'train/{class_name}'.")
            except Exception as e:
                print(f"Gagal memindahkan '{file_path.name}': {e}")

        # Pindahkan file ke folder val
        for file_path in val_files:
            destination = val_class_dir / file_path.name
            try:
                shutil.move(str(file_path), str(destination))
                print(f"Memindahkan '{file_path.name}' ke folder 'val/{class_name}'.")
            except Exception as e:
                print(f"Gagal memindahkan '{file_path.name}': {e}")

    print("\nProses pengorganisasian selesai.")

if __name__ == "__main__":
    # Tentukan path ke folder sumber dan target
    source_directory = 'data'          # Ganti dengan path folder sumber Anda
    target_directory = 'data_split'    # Ganti dengan path folder target yang diinginkan

    # Panggil fungsi untuk mengorganisir gambar dengan pembagian terurut
    organize_images_ordered_split(source_directory, target_directory, train_ratio=0.75)