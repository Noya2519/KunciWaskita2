Berikut adalah versi yang lebih terstruktur dan rapi dari README.md untuk proyek KunciWaskita2:

# KunciWaskita2

Sebuah aplikasi Enkripsi.

## Persyaratan

- Python 3.x sudah terinstal di sistem Anda.
- File Python yang ingin diubah menjadi .exe (contoh: `KUNCI_WASKITA.py`).

## Langkah-langkah

### Langkah 1: Install PyInstaller

1. Buka terminal atau command prompt.
2. Jalankan perintah berikut untuk menginstal PyInstaller:
    ```bash
    pip install pyinstaller
    ```

### Langkah 2: Buat File Executable

1. Buka terminal atau command prompt di direktori tempat file Python Anda berada.
2. Jalankan perintah berikut untuk membuat file .exe:
    ```bash
    pyinstaller --onefile --windowed KUNCI_WASKITA.py
    ```

#### Penjelasan Perintah:

- `--onefile`: Menggabungkan semua file menjadi satu file .exe.
- `--windowed`: Menyembunyikan konsol saat aplikasi dijalankan (opsional, hapus jika Anda ingin melihat konsol).
- `KUNCI_WASKITA.py`: File Python utama Anda.

Setelah proses selesai, PyInstaller akan membuat beberapa folder dan file. File .exe akan berada di folder `dist`.

### Langkah 3: Temukan File Executable

1. Buka folder `dist` di direktori proyek Anda.
2. Di dalam folder `dist`, Anda akan menemukan file `KUNCI_WASKITA.exe`.
3. File inilah yang dapat Anda jalankan atau distribusikan.

### Langkah 4: Uji File Executable

1. Klik dua kali file `KUNCI_WASKITA.exe` untuk menjalankannya.

Download versi zip : https://drive.google.com/file/d/17O7aebGyVH2OfmRxNYT_s-ODVoch6E-0/view?usp=sharing
