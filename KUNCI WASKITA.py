import os
import base64
import hashlib
import customtkinter as ctk
from tkinter import filedialog, messagebox
from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Fungsi untuk menghasilkan kunci
def generate_key(key, algo):
    if algo == "AES":
        return hashlib.sha256(key.encode()).digest()
    elif algo == "DES":
        return hashlib.md5(key.encode()).digest()[:8]
    elif algo == "RC4":
        return hashlib.sha256(key.encode()).digest()[:16]
    else:
        return key.encode()

# Simple XOR
def xor_encrypt(text, key):
    key_cycle = (key * (len(text) // len(key) + 1))[:len(text)]
    encrypted_bytes = bytes(a ^ b for a, b in zip(text.encode(), key_cycle.encode()))
    return base64.b64encode(encrypted_bytes).decode()

def xor_decrypt(text, key):
    try:
        text = base64.b64decode(text.encode())
    except Exception:
        return "Invalid XOR-encrypted text"
    key_cycle = (key * (len(text) // len(key) + 1))[:len(text)]
    decrypted_bytes = bytes(a ^ b for a, b in zip(text, key_cycle.encode()))
    return decrypted_bytes.decode(errors='ignore')

# RC4 Cipher
def rc4_encrypt(text, key):
    S = list(range(256))
    j = 0
    key = generate_key(key, "RC4")
    key = [key[i % len(key)] for i in range(256)]
    for i in range(256):
        j = (j + S[i] + key[i]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    encrypted_bytes = []
    for char in text.encode():
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        encrypted_bytes.append(char ^ S[(S[i] + S[j]) % 256])
    return base64.b64encode(bytes(encrypted_bytes)).decode()

def rc4_decrypt(text, key):
    return rc4_encrypt(text, key)  # RC4 decryption is the same as encryption

# DES Cipher
def des_encrypt(text, key, mode="ECB"):
    key = generate_key(key, "DES")
    if mode == "ECB":
        cipher = DES.new(key, DES.MODE_ECB)
    elif mode == "CBC":
        iv = get_random_bytes(8)
        cipher = DES.new(key, DES.MODE_CBC, iv)
    elif mode == "CTR":
        ctr = Counter.new(64, initial_value=int.from_bytes(get_random_bytes(8), byteorder='big'))
        cipher = DES.new(key, DES.MODE_CTR, counter=ctr)
    padded_text = pad(text.encode(), DES.block_size)
    encrypted_bytes = cipher.encrypt(padded_text)
    return base64.b64encode(encrypted_bytes).decode()

def des_decrypt(text, key, mode="ECB"):
    key = generate_key(key, "DES")
    text = base64.b64decode(text.encode())
    if mode == "ECB":
        cipher = DES.new(key, DES.MODE_ECB)
    elif mode == "CBC":
        iv = text[:8]
        cipher = DES.new(key, DES.MODE_CBC, iv)
        text = text[8:]
    elif mode == "CTR":
        ctr = Counter.new(64, prefix=text[:8])
        cipher = DES.new(key, DES.MODE_CTR, counter=ctr)
        text = text[8:]
    decrypted_bytes = cipher.decrypt(text)
    return unpad(decrypted_bytes, DES.block_size).decode()

# AES Cipher
def aes_encrypt(text, key, mode="CBC"):
    key = generate_key(key, "AES")
    if mode == "ECB":
        cipher = AES.new(key, AES.MODE_ECB)
    elif mode == "CBC":
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
    elif mode == "CTR":
        ctr = Counter.new(128, initial_value=int.from_bytes(get_random_bytes(16), byteorder='big'))
        cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    padded_text = pad(text.encode(), AES.block_size)
    encrypted_bytes = cipher.encrypt(padded_text)
    return base64.b64encode(encrypted_bytes).decode()

def aes_decrypt(text, key, mode="CBC"):
    key = generate_key(key, "AES")
    text = base64.b64decode(text.encode())
    if mode == "ECB":
        cipher = AES.new(key, AES.MODE_ECB)
    elif mode == "CBC":
        iv = text[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        text = text[16:]
    elif mode == "CTR":
        ctr = Counter.new(128, prefix=text[:16])
        cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
        text = text[16:]
    decrypted_bytes = cipher.decrypt(text)
    return unpad(decrypted_bytes, AES.block_size).decode()

# GUI Application
class CryptoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Encryption & Decryption App")
        self.geometry("500x600")
        self.configure(bg="#0a0f25")

        self.label = ctk.CTkLabel(self, text="Pilih file atau masukkan teks:", text_color="white")
        self.label.pack(pady=5)
        
        self.text_entry = ctk.CTkTextbox(self, height=100, width=400)
        self.text_entry.pack(pady=5)
        
        self.file_button = ctk.CTkButton(self, text="Pilih File", command=self.select_file, fg_color="#1e3a8a")
        self.file_button.pack(pady=5)
        
        self.key_label = ctk.CTkLabel(self, text="Masukkan kunci:", text_color="white")
        self.key_label.pack(pady=5)
        self.key_entry = ctk.CTkEntry(self, show="*")
        self.key_entry.pack(pady=5)
        
        self.method_var = ctk.StringVar(value="AES")
        self.method_menu = ctk.CTkComboBox(self, variable=self.method_var, values=["AES", "DES", "RC4", "XOR"], fg_color="#1e3a8a")
        self.method_menu.pack(pady=5)
        
        self.mode_var = ctk.StringVar(value="CBC")
        self.mode_menu = ctk.CTkComboBox(self, variable=self.mode_var, values=["ECB", "CBC", "CTR"], fg_color="#1e3a8a")
        self.mode_menu.pack(pady=5)
        
        self.encrypt_button = ctk.CTkButton(self, text="Enkripsi", command=self.encrypt, fg_color="#1e3a8a")
        self.encrypt_button.pack(pady=5)
        
        self.decrypt_button = ctk.CTkButton(self, text="Dekripsi", command=self.decrypt, fg_color="#1e3a8a")
        self.decrypt_button.pack(pady=5)
        
        self.result_label = ctk.CTkLabel(self, text="Hasil:", text_color="white")
        self.result_label.pack(pady=5)
        self.result_text = ctk.CTkTextbox(self, height=100, width=400)
        self.result_text.pack(pady=5)
        
        self.selected_file = None
    
    def select_file(self):
        self.selected_file = filedialog.askopenfilename()
        if self.selected_file:
            messagebox.showinfo("File Dipilih", f"File: {self.selected_file}")
    
    def encrypt(self):
        key = self.key_entry.get()
        method = self.method_var.get()
        mode = self.mode_var.get()
        if not key:
            messagebox.showerror("Error", "Kunci harus diisi!")
            return
        if self.selected_file:
            try:
                with open(self.selected_file, "rb") as file:
                    file_data = file.read().decode()
                if method == "AES":
                    result = aes_encrypt(file_data, key, mode)
                elif method == "DES":
                    result = des_encrypt(file_data, key, mode)
                elif method == "RC4":
                    result = rc4_encrypt(file_data, key)
                elif method == "XOR":
                    result = xor_encrypt(file_data, key)
                with open(self.selected_file + ".enc", "w") as file:
                    file.write(result)
                messagebox.showinfo("Sukses", f"File terenkripsi: {self.selected_file}.enc")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal mengenkripsi: {str(e)}")
        else:
            text = self.text_entry.get("1.0", "end").strip()
            if not text:
                messagebox.showerror("Error", "Masukkan teks atau pilih file!")
                return
            if method == "AES":
                result = aes_encrypt(text, key, mode)
            elif method == "DES":
                result = des_encrypt(text, key, mode)
            elif method == "RC4":
                result = rc4_encrypt(text, key)
            elif method == "XOR":
                result = xor_encrypt(text, key)
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", result)
    
    def decrypt(self):
        key = self.key_entry.get()
        method = self.method_var.get()
        mode = self.mode_var.get()
        if not key:
            messagebox.showerror("Error", "Kunci harus diisi!")
            return
        if self.selected_file:
            try:
                with open(self.selected_file, "r") as file:
                    file_data = file.read()
                if method == "AES":
                    result = aes_decrypt(file_data, key, mode)
                elif method == "DES":
                    result = des_decrypt(file_data, key, mode)
                elif method == "RC4":
                    result = rc4_decrypt(file_data, key)
                elif method == "XOR":
                    result = xor_decrypt(file_data, key)
                with open(self.selected_file.replace(".enc", ""), "w") as file:
                    file.write(result)
                messagebox.showinfo("Sukses", f"File didekripsi: {self.selected_file.replace('.enc', '')}")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal mendekripsi: {str(e)}")
        else:
            text = self.text_entry.get("1.0", "end").strip()
            if not text:
                messagebox.showerror("Error", "Masukkan teks atau pilih file!")
                return
            if method == "AES":
                result = aes_decrypt(text, key, mode)
            elif method == "DES":
                result = des_decrypt(text, key, mode)
            elif method == "RC4":
                result = rc4_decrypt(text, key)
            elif method == "XOR":
                result = xor_decrypt(text, key)
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", result)

if __name__ == "__main__":
    app = CryptoApp()
    app.mainloop()