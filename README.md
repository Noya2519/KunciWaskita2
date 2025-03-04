# KunciWaskita2
Sebuah aplikasi Enkripsi
Persyaratan
Python 3.x sudah terinstal di sistem Anda.

File Python yang ingin diubah menjadi .exe (contoh: KUNCI_WASKITA.py).

Langkah 1: Install PyInstaller
Buka terminal atau command prompt.

Jalankan perintah berikut untuk menginstal PyInstaller:

bash
Copy
pip install pyinstaller
Langkah 2: Buat File Executable
Buka terminal atau command prompt di direktori tempat file Python Anda berada.

Jalankan perintah berikut untuk membuat file .exe:

bash
Copy
pyinstaller --onefile --windowed KUNCI_WASKITA.py
Penjelasan Perintah:

--onefile: Menggabungkan semua file menjadi satu file .exe.

--windowed: Menyembunyikan konsol saat aplikasi dijalankan (opsional, hapus jika Anda ingin melihat konsol).

KUNCI_WASKITA.py: File Python utama Anda.

Setelah proses selesai, PyInstaller akan membuat beberapa folder dan file. File .exe akan berada di folder dist.

Langkah 3: Temukan File Executable
Buka folder dist di direktori proyek Anda.

Di dalam folder dist, Anda akan menemukan file KUNCI_WASKITA.exe.

File inilah yang dapat Anda jalankan atau distribusikan.

Langkah 4: Uji File Executable
Klik dua kali file KUNCI_WASKITA.exe untuk menjalankannya.


