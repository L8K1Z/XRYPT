# XCRYPT 10-LAYER v1.0+

Enkripsi file berbasis 10 layer proteksi untuk Termux / Android.  
Dibuat oleh **L8K1Z** — [t.me/XCODE_OWN](https://t.me/XCODE_OWN)

---

## Fitur

- 10 layer enkripsi bertingkat (lihat detail di bawah)
- PBKDF2-SHA512 dengan 250.000 iterasi untuk key derivation
- AES-256-GCM dengan authenticated encryption
- HMAC-SHA512 untuk verifikasi integritas + timestamp
- Verifikasi SHA-256 saat dekripsi
- Rate limiting: maksimal 3 percobaan password per 300 detik
- Key Manager — simpan & kelola password di folder KEYS
- Output file dengan ekstensi `.x7l`
- Kompatibel dengan Termux & Android

---

## Struktur 10 Layer

| Layer | Metode | Keterangan |
|-------|--------|------------|
| L1 | ZLIB Compress | Kompresi level 9 sebelum enkripsi |
| L2 | AES-256-GCM | Authenticated encryption |
| L3 | XOR Rolling | XOR ganda dengan key + offset index |
| L4 | Scramble 2-pass | Pengacakan byte berbasis seed |
| L5 | Fernet (AES+HMAC) | Enkripsi lapis kedua |
| L6 | Base85 + Checksum | Encoding dengan verifikasi MD5 |
| L7 | HMAC-SHA512 Seal | Tanda tangan + timestamp |
| L8 | Reverse Bytes | Pembalikan byte |
| L9 | Chunk Swap 16-byte | Permutasi blok 16 byte |
| L10 | XOR2 Advanced + Offset | XOR dinamis dengan offset acak |

---

## Struktur Folder

Semua folder dibuat otomatis di direktori Download:

```
/storage/emulated/0/Download/XCODE ENCRYPT/
├── INPUT/       ← letakkan file asli di sini sebelum enkripsi
├── ENCRYPT/     ← folder proses sementara
├── SELESAI/     ← hasil enkripsi final (.x7l)
├── DECRYPT/     ← hasil dekripsi
└── KEYS/        ← penyimpanan key/password
```

---

## Instalasi

### 1. Siapkan storage Termux

```bash
termux-setup-storage
```

### 2. Jalankan installer

```bash
bash install.sh
```

Installer akan otomatis:
- Mengatur akses storage
- Update paket Termux
- Install Python3
- Install library `cryptography`
- Mendaftarkan perintah `xcrypt7`

### 3. Jalankan

```bash
xcrypt7
# atau
python3 xcrypt.py
```

---

## Cara Pakai

### Enkripsi File

1. Salin file yang ingin dienkripsi ke folder **INPUT**
2. Jalankan `xcrypt7` → pilih **1 (Encrypt File)**
3. Masukkan nama file dan password
4. Hasil enkripsi (`.x7l`) tersimpan di folder **SELESAI**

### Dekripsi File

1. Pastikan file `.x7l` ada di folder **SELESAI**
2. Jalankan `xcrypt7` → pilih **2 (Decrypt File)**
3. Masukkan nama file dan password yang sama saat enkripsi
4. Hasil dekripsi tersimpan di folder **DECRYPT**

### Key Manager

Pilih menu **3 (Key Manager)** untuk:
- Melihat semua key tersimpan
- Menambah key baru
- Menghapus key
- Generate key 256-bit acak

---

## Format File Terenkripsi

File `.x7l` memiliki struktur header berikut:

```
[MAGIC 8 byte][VERSION 1 byte][SALT 48 byte][IV 12 byte][DATA_LEN 8 byte][DATA ...]
```

Di dalam data tersimpan metadata JSON (nama file asli, ukuran, SHA-256, SHA-512, timestamp) diikuti isi file asli.

---

## Keamanan

- File asli **dihapus** dari folder INPUT setelah enkripsi berhasil
- File `.x7l` **dihapus** dari folder SELESAI setelah dekripsi berhasil
- Memory di-wipe setelah setiap operasi (secure wipe)
- Anti-debug: program berhenti otomatis jika terdeteksi debugger
- Random delay untuk mencegah timing attack
- Salah password 3x → diblokir 300 detik

---

## Changelog

### v1.0+ (Fixed)
- **Bugfix**: `_l6_b85_dec` — decode Base85 sekarang memisahkan data dan checksum dengan benar (sebelumnya gagal karena decode dilakukan sekaligus)
- **Bugfix**: `_l7_verify` — HMAC mismatch sekarang raise `ValueError` dengan pesan jelas, tidak lagi diam-diam meneruskan data rusak
- **Bugfix**: `_l9_chunk_swap` — chunk swap sekarang simetris untuk semua ukuran data; sebelumnya chunk sisa (< 16 byte) ikut di-swap sehingga tidak bisa di-reverse dan menyebabkan dekripsi selalu gagal

---

## Dependensi

| Paket | Instalasi |
|-------|-----------|
| Python 3 | `pkg install python3` |
| cryptography | `pkg install python-cryptography` |

---

## Lisensi

Script ini dibuat untuk keperluan pribadi.  
Dilarang menyebarluaskan ulang tanpa izin dari **L8K1Z**.
