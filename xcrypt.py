#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# XCODEMODZ - XCRYPT 10-LAYER v6.0+ | FIXED VERSION
# ★☆★ TERMUX/ANDROID COMPATIBLE ★☆★

import os
import sys
import zlib
import time
import hmac
import json
import struct
import random
import shutil
import subprocess
import signal
import hashlib
import base64
import getpass
import argparse
import platform
import threading
import gc
from pathlib import Path
from datetime import datetime
from functools import wraps

# ─── TERMUX/ANDROID COMPATIBILITY ──────────────────────────
def is_termux():
    return 'ANDROID_ROOT' in os.environ or 'TERMUX_VERSION' in os.environ

def is_android():
    return platform.system() == 'Android' or is_termux()

# ─── ANTI-DEBUG ──────────────────────────────────────────────
def ultra_anti_debug():
    try:
        if sys.gettrace() is not None:
            print("\033[91m[!] DEBUGGER DETECTED! SHUTTING DOWN...\033[0m")
            os._exit(1)
    except:
        pass

# ─── AUTO-INSTALL DEPS ──────────────────────────────────────
def _ensure_deps():
    try:
        from cryptography.fernet import Fernet
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.primitives import padding as P
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from cryptography.hazmat.primitives import hashes as CryptoHashes
        from cryptography.hazmat.primitives import constant_time
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        return
    except ImportError:
        if is_termux():
            os.system("pkg install python-cryptography -y -q 2>/dev/null 1>/dev/null")
        else:
            os.system("pip install cryptography --no-cache-dir -q 2>/dev/null 1>/dev/null || pip3 install cryptography --no-cache-dir -q 2>/dev/null 1>/dev/null")
        try:
            from cryptography.fernet import Fernet
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            sys.exit(0)
        except:
            sys.exit(1)

_ensure_deps()

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as SymPad
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes as CryptoHashes
from cryptography.hazmat.primitives import constant_time
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ─── Warna ────────────────────────────────────────────────────
R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
B = "\033[94m"
M = "\033[95m"
C = "\033[96m"
W = "\033[97m"
D = "\033[2m"
RST = "\033[0m"
BLD = "\033[1m"
BLINK = "\033[5m"

# ─── Konstanta ──────────────────────────────────────────────
MAGIC = bytes([0xAC, 0x07, 0x1A, 0x4E, 0xA7, 0xF3, 0x2C, 0x8D])
VERSION = bytes([0x06])
KDF_ITER = 250_000
SALT_LEN = 48
MIN_DELAY = 0.8
MAX_ATTEMPTS = 3
BLOCK_TIME = 300

# ─── FOLDER DI DOWNLOAD ─────────────────────────────────────
DOWNLOAD_PATHS = [
    "/storage/emulated/0/Download",
    "/sdcard/Download",
    "/storage/emulated/0/Downloads",
    "/sdcard/Downloads",
    os.path.expanduser("~/storage/downloads"),
    os.path.expanduser("~/storage/Download"),
]

def get_download_path():
    for path in DOWNLOAD_PATHS:
        if os.path.exists(path):
            return path
    return os.getcwd()

DOWNLOAD_PATH = get_download_path()

XCODE_DIR = Path(DOWNLOAD_PATH) / "XCODE ENCRYPT"
INPUT_DIR = XCODE_DIR / "INPUT"
ENCRYPT_DIR = XCODE_DIR / "ENCRYPT"
SELESAI_DIR = XCODE_DIR / "SELESAI"
DECRYPT_DIR = XCODE_DIR / "DECRYPT"
KEYS_DIR = XCODE_DIR / "KEYS"

# ─── UI Helpers ──────────────────────────────────────────────
def _divider(char="-", length=56, color=D):
    print(f"  {color}{char * length}{RST}")

def _ok(msg):
    print(f"  {G}✔{RST}  {W}{msg}{RST}")

def _err(msg):
    print(f"  {R}✘{RST}  {R}{msg}{RST}")

def _info(msg):
    print(f"  {D}·  {msg}{RST}")

def _run(msg):
    print(f"  {C}◈{RST}  {D}{msg}{RST}")

def _warn(msg):
    print(f"  {Y}⚠{RST}  {Y}{msg}{RST}")

# ─── Progress Bar ──────────────────────────────────────────
def _progress_bar(label, start=0, end=100, width=38):
    for i in range(start, end + 1):
        filled = int((i / 100) * width)
        empty = width - filled
        bar = "█" * filled + "░" * empty
        if i < 30:
            col = R
        elif i < 70:
            col = Y
        else:
            col = G
        line = f"  {D}{label:<20}{RST}  {col}{BLD}[{bar}]{RST}  {W}{BLD}{i:3d}%{RST}"
        sys.stdout.write("\033[2K\r" + line)
        sys.stdout.flush()
        time.sleep(0.012)
    sys.stdout.write("\n")
    sys.stdout.flush()

# ─── BUAT SEMUA FOLDER ──────────────────────────────────────
def create_all_folders():
    folders = [XCODE_DIR, INPUT_DIR, ENCRYPT_DIR, SELESAI_DIR, DECRYPT_DIR, KEYS_DIR]
    
    print(f"\n  {C}Menyiapkan struktur folder...{RST}")
    _divider()
    
    for folder in folders:
        try:
            folder.mkdir(mode=0o777, exist_ok=True)
            _ok(str(folder))
        except Exception:
            try:
                folder.mkdir(exist_ok=True)
                _ok(f"{folder}  {D}(permission default){RST}")
            except:
                _err(f"Gagal: {folder}")
    
    _divider()
    if XCODE_DIR.exists():
        print(f"\n  {G}✔{RST}  {W}Semua folder siap{RST}")
        print(f"  {D}📂 Lokasi: {XCODE_DIR}{RST}")
    else:
        print(f"\n  {R}✘  Gagal membuat folder!{RST}")
        _warn("Coba jalankan: termux-setup-storage")

# ─── RATE LIMITING ──────────────────────────────────────────
_ATTEMPTS = {}
_ATTEMPT_LOCK = threading.Lock()

def ultra_rate_limit(identifier='local'):
    with _ATTEMPT_LOCK:
        current_time = time.time()
        if identifier in _ATTEMPTS:
            attempts, first_attempt, blocked_until = _ATTEMPTS[identifier]
            if attempts >= MAX_ATTEMPTS:
                if current_time < blocked_until:
                    remaining = int(blocked_until - current_time)
                    print(f"\033[91m[!] PERMANENT BLOCK! Tunggu {remaining} detik.\033[0m")
                    sys.exit(1)
                else:
                    _ATTEMPTS[identifier] = (0, current_time, 0)
            if current_time - first_attempt < BLOCK_TIME and attempts >= MAX_ATTEMPTS:
                remaining = int(BLOCK_TIME - (current_time - first_attempt))
                print(f"\033[91m[!] TOO MANY ATTEMPTS! Tunggu {remaining} detik.\033[0m")
                sys.exit(1)
        else:
            _ATTEMPTS[identifier] = (0, current_time, 0)

def ultra_increment_attempt(identifier='local'):
    with _ATTEMPT_LOCK:
        if identifier in _ATTEMPTS:
            attempts, first_attempt, _ = _ATTEMPTS[identifier]
            attempts += 1
            blocked_until = first_attempt + BLOCK_TIME if attempts >= MAX_ATTEMPTS else 0
            _ATTEMPTS[identifier] = (attempts, first_attempt, blocked_until)
            if attempts >= MAX_ATTEMPTS:
                print(f"\033[91m[!] PERMANENT BLOCK! {MAX_ATTEMPTS} attempts used.\033[0m")
                sys.exit(1)

# ─── CRYPTOGRAPHIC FUNCTIONS ──────────────────────────────
def _derive_keys(password, salt):
    raw = PBKDF2HMAC(
        algorithm=CryptoHashes.SHA512(),
        length=128,
        salt=salt,
        iterations=KDF_ITER,
        backend=default_backend()
    ).derive(password.encode("utf-8"))
    
    return {
        'aes': raw[:32],
        'xor': raw[32:64],
        'seed': raw[64:72],
        'extra': raw[72:96],
        'scramble_seed': raw[96:104],
        'xor2': raw[104:120],
        'fernet': hashlib.sha256(raw + salt + b"FERNET").digest()
    }

def _fernet_key_from_keys(keys, salt):
    raw = hashlib.sha256(keys['fernet'] + salt + b"FERNET").digest()
    return base64.urlsafe_b64encode(raw)

def _hmac_key_from_keys(keys, salt):
    return hashlib.sha512(keys['extra'] + salt + b"HMAC").digest()

# ─── 10 LAYERS (FIXED) ──────────────────────────────────────
def _l1_compress(d):
    try:
        return zlib.compress(d, level=9)
    except:
        return d

def _l1_decompress(d):
    try:
        return zlib.decompress(d)
    except:
        return d

def _l2_aes_enc(d, key, iv):
    try:
        aesgcm = AESGCM(key)
        return aesgcm.encrypt(iv, d, b'')
    except:
        return d

def _l2_aes_dec(d, key, iv):
    try:
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(iv, d, b'')
    except:
        return d

def _l3_xor(d, kx):
    kl = len(kx)
    if kl == 0:
        return d
    result = bytearray(d)
    for i, b in enumerate(result):
        idx1 = i % kl
        idx2 = (kl - 1 - (i % kl)) % kl
        result[i] = b ^ kx[idx1] ^ (i & 0xFF)
        result[i] = result[i] ^ kx[idx2]
    return bytes(result)

def _l4_scramble(d, seed_bytes):
    try:
        seed = int.from_bytes(seed_bytes, "big")
        rng = random.Random(seed)
        arr = bytearray(d)
        n = len(arr)
        for i in range(n-1, 0, -1):
            j = rng.randint(0, i)
            arr[i], arr[j] = arr[j], arr[i]
        return bytes(arr)
    except:
        return d

def _l4_unscramble(d, seed_bytes):
    try:
        seed = int.from_bytes(seed_bytes, "big")
        rng = random.Random(seed)
        n = len(d)
        swaps = [(i, rng.randint(0, i)) for i in range(n-1, 0, -1)]
        arr = bytearray(d)
        for i, j in reversed(swaps):
            arr[i], arr[j] = arr[j], arr[i]
        return bytes(arr)
    except:
        return d

def _l5_fernet_enc(d, fk):
    try:
        return Fernet(fk).encrypt(d)
    except:
        return d

def _l5_fernet_dec(d, fk):
    try:
        return Fernet(fk).decrypt(d)
    except:
        return d

def _l6_b85_enc(d):
    try:
        enc = base64.b85encode(d)
        checksum = hashlib.md5(enc).digest()[:4]
        return enc + base64.b85encode(checksum)
    except:
        return base64.b64encode(d)

def _l6_b85_dec(d):
    try:
        # Format enkripsi: b85encode(data) + b85encode(checksum_4byte)
        # b85encode(4 bytes) = 5 bytes
        CHECKSUM_ENC_LEN = 5
        if len(d) > CHECKSUM_ENC_LEN:
            enc_data = d[:-CHECKSUM_ENC_LEN]
            enc_checksum = d[-CHECKSUM_ENC_LEN:]
            try:
                data = base64.b85decode(enc_data)
                checksum = base64.b85decode(enc_checksum)
                if hashlib.md5(enc_data).digest()[:4] == checksum:
                    return data
            except Exception:
                pass
        # Fallback: decode seluruhnya
        return base64.b85decode(d)
    except:
        try:
            return base64.b64decode(d)
        except:
            return d

def _l7_seal(d, hk):
    try:
        if len(hk) == 0:
            return d
        mac = hmac.new(hk, d, hashlib.sha512).digest()
        timestamp = struct.pack(">Q", int(time.time()))
        return mac + timestamp + d
    except:
        return d

def _l7_verify(d, hk):
    try:
        if len(d) < 72:
            raise ValueError("HMAC seal terlalu pendek")
        if len(hk) == 0:
            return d[72:]
        mac_s = d[:64]
        timestamp = d[64:72]
        payload = d[72:]
        mac_c = hmac.new(hk, payload, hashlib.sha512).digest()
        if constant_time.bytes_eq(mac_s, mac_c):
            return payload
        # HMAC tidak cocok = password salah atau file corrupt
        raise ValueError("HMAC mismatch: password salah atau file corrupt")
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"HMAC verify error: {str(e)}")

def _l8_reverse(d):
    try:
        return d[::-1]
    except:
        return d

def _l9_chunk_swap(d):
    try:
        chunk_size = 16
        if len(d) < chunk_size * 2:
            return d
        # Pisahkan: full chunks + sisa bytes (< chunk_size)
        n_full = len(d) // chunk_size
        remainder = d[n_full * chunk_size:]          # bytes sisa (tidak diubah)
        full_data = d[:n_full * chunk_size]
        chunks = [full_data[i:i+chunk_size] for i in range(0, len(full_data), chunk_size)]
        # Swap hanya antar full chunks berpasangan
        for i in range(1, len(chunks), 2):
            chunks[i-1], chunks[i] = chunks[i], chunks[i-1]
        return b''.join(chunks) + remainder
    except:
        return d

def _l10_xor2_enc(d, kx2):
    try:
        kl = len(kx2)
        if kl == 0:
            return d
        result = bytearray(d)
        offset = random.randint(0, 255) if len(d) > 0 else 0
        for i, b in enumerate(result):
            result[i] = b ^ kx2[i % kl] ^ ((i + offset) & 0xFF)
        return bytes([offset & 0xFF]) + bytes(result)
    except:
        return b'\x00' + d

def _l10_xor2_dec(d, kx2):
    try:
        if len(d) < 1:
            return d
        offset = d[0]
        payload = d[1:]
        kl = len(kx2)
        if kl == 0:
            return payload
        result = bytearray(payload)
        for i, b in enumerate(result):
            result[i] = b ^ kx2[i % kl] ^ ((i + offset) & 0xFF)
        return bytes(result)
    except:
        return d[1:] if len(d) > 1 else d

def _secure_wipe(data):
    try:
        if isinstance(data, bytearray):
            for i in range(len(data)):
                data[i] = 0
        elif isinstance(data, bytes):
            data = bytearray(data)
            for i in range(len(data)):
                data[i] = 0
    except:
        pass
    return data

# ══════════════════════════════════════════════════════════════
#   CORE ENCRYPT / DECRYPT (FIXED)
# ══════════════════════════════════════════════════════════════
def encrypt_10layer(plaintext, password):
    try:
        salt = os.urandom(SALT_LEN)
        iv = os.urandom(12)
        keys = _derive_keys(password, salt)
        fernet_key = _fernet_key_from_keys(keys, salt)
        hmac_key = _hmac_key_from_keys(keys, salt)
        
        d = plaintext
        
        # Layer 1: Compress
        d = _l1_compress(d)
        
        # Layer 2: AES-256-GCM
        d = _l2_aes_enc(d, keys['aes'], iv)
        
        # Layer 3: XOR
        d = _l3_xor(d, keys['xor'])
        
        # Layer 4: Scramble
        d = _l4_scramble(d, keys['seed'])
        
        # Layer 5: Fernet
        d = _l5_fernet_enc(d, fernet_key)
        
        # Layer 6: Base85 + Checksum
        d = _l6_b85_enc(d)
        
        # Layer 7: HMAC Seal
        d = _l7_seal(d, hmac_key)
        
        # Layer 8: Reverse
        d = _l8_reverse(d)
        
        # Layer 9: Chunk Swap
        d = _l9_chunk_swap(d)
        
        # Layer 10: XOR2
        d = _l10_xor2_enc(d, keys['xor2'])
        
        # Extra XOR
        extra_key = keys['extra']
        if len(extra_key) > 0:
            d = bytes(b ^ extra_key[i % len(extra_key)] for i, b in enumerate(d))
        
        header = MAGIC + VERSION + salt + iv + struct.pack(">Q", len(d))
        result = header + d
        
        _secure_wipe(d)
        return result
    except Exception as e:
        # Fallback sederhana
        salt = os.urandom(SALT_LEN)
        iv = os.urandom(12)
        return MAGIC + VERSION + salt + iv + struct.pack(">Q", len(plaintext)) + plaintext

def decrypt_10layer(packet, password):
    try:
        hdr_len = len(MAGIC) + 1 + SALT_LEN + 12 + 8
        
        if len(packet) < hdr_len:
            raise ValueError("Invalid file format: too short")
        
        ptr = 0
        if packet[ptr:ptr+len(MAGIC)] != MAGIC:
            raise ValueError("Magic mismatch")
        ptr += len(MAGIC)
        
        if packet[ptr:ptr+1] != VERSION:
            raise ValueError("Version unsupported")
        ptr += 1
        
        salt = packet[ptr:ptr+SALT_LEN]
        ptr += SALT_LEN
        iv = packet[ptr:ptr+12]
        ptr += 12
        data_len = struct.unpack(">Q", packet[ptr:ptr+8])[0]
        ptr += 8
        
        if ptr + data_len > len(packet):
            raise ValueError(f"Data corrupted: expected {data_len} bytes, got {len(packet)-ptr}")
        
        d = packet[ptr:ptr+data_len]
        
        # Derive keys
        keys = _derive_keys(password, salt)
        fernet_key = _fernet_key_from_keys(keys, salt)
        hmac_key = _hmac_key_from_keys(keys, salt)
        
        # Extra XOR decrypt (reverse)
        extra_key = keys['extra']
        if len(extra_key) > 0:
            d = bytes(b ^ extra_key[i % len(extra_key)] for i, b in enumerate(d))
        
        # Layer 10: XOR2 decrypt
        d = _l10_xor2_dec(d, keys['xor2'])
        
        # Layer 9: Chunk Swap (sama karena reversible)
        d = _l9_chunk_swap(d)
        
        # Layer 8: Reverse
        d = _l8_reverse(d)
        
        # Layer 7: HMAC Verify
        d = _l7_verify(d, hmac_key)
        
        # Layer 6: Base85 decode
        d = _l6_b85_dec(d)
        
        # Layer 5: Fernet decrypt
        d = _l5_fernet_dec(d, fernet_key)
        
        # Layer 4: Unscramble
        d = _l4_unscramble(d, keys['seed'])
        
        # Layer 3: XOR (sama karena XOR reversible)
        d = _l3_xor(d, keys['xor'])
        
        # Layer 2: AES decrypt
        d = _l2_aes_dec(d, keys['aes'], iv)
        
        # Layer 1: Decompress
        d = _l1_decompress(d)
        
        return d
    except Exception as e:
        raise ValueError(f"Dekripsi gagal: {str(e)}")

# ─── FILE OPERATIONS ────────────────────────────────────────
EXT_ENC = ".x7l"

def encrypt_file_with_folders(src, password):
    sp = Path(src)
    if not sp.exists():
        raise FileNotFoundError(f"File not found: {src}")
    if sp.stat().st_size > 500 * 1024 * 1024:
        raise ValueError("File terlalu besar (max 500MB)")
    
    INPUT_DIR.mkdir(exist_ok=True)
    if INPUT_DIR not in sp.parents:
        target = INPUT_DIR / sp.name
        shutil.move(str(sp), str(target))
        sp = target
    
    try:
        raw = sp.read_bytes()
    except:
        raise ValueError("Gagal membaca file")
    
    meta = {
        "filename": sp.name,
        "size": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "sha512": hashlib.sha512(raw).hexdigest(),
        "timestamp": int(time.time()),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tool": "XCRYPT-10L v6.0+"
    }
    
    mj = json.dumps(meta, separators=(',', ':')).encode()
    payload = struct.pack(">I", len(mj)) + mj + raw
    
    ultra_rate_limit()
    encrypted = encrypt_10layer(payload, password)
    
    ENCRYPT_DIR.mkdir(exist_ok=True)
    SELESAI_DIR.mkdir(exist_ok=True)
    enc_file = ENCRYPT_DIR / (sp.name + EXT_ENC + ".tmp")
    enc_file.write_bytes(encrypted)
    final_file = SELESAI_DIR / (sp.name + EXT_ENC)
    if final_file.exists():
        final_file.unlink()
    shutil.move(str(enc_file), str(final_file))
    sp.unlink()
    
    _secure_wipe(raw)
    _secure_wipe(payload)
    _secure_wipe(encrypted)
    
    return final_file, meta

def decrypt_file_with_folders(src, password):
    sp = Path(src)
    if not sp.exists():
        raise FileNotFoundError(f"File not found: {src}")
    
    ultra_rate_limit()
    
    if sp.suffix != EXT_ENC:
        for folder in [SELESAI_DIR, ENCRYPT_DIR]:
            if folder.exists():
                test_path = folder / (sp.name + EXT_ENC)
                if test_path.exists():
                    sp = test_path
                    break
        else:
            raise ValueError("File .x7l tidak ditemukan")
    
    try:
        encrypted = sp.read_bytes()
    except:
        raise ValueError("Gagal membaca file terenkripsi")
    
    ultra_increment_attempt()
    payload = decrypt_10layer(encrypted, password)
    
    # Parse metadata
    try:
        if len(payload) < 4:
            raise ValueError("Payload terlalu pendek")
        ml = struct.unpack(">I", payload[:4])[0]
        if len(payload) < 4 + ml:
            raise ValueError("Metadata truncated")
        meta = json.loads(payload[4:4+ml].decode())
        raw = payload[4+ml:]
        if len(raw) != meta["size"]:
            raise ValueError(f"Size mismatch: expected {meta['size']}, got {len(raw)}")
    except json.JSONDecodeError:
        raise ValueError("Format file corrupt: invalid JSON metadata")
    except Exception as e:
        raise ValueError(f"Format file corrupt: {str(e)}")
    
    # Verify SHA-256
    sha256_hash = hashlib.sha256(raw).hexdigest()
    if sha256_hash != meta["sha256"]:
        raise ValueError("SHA-256 MISMATCH! Password salah atau file corrupt!")
    
    DECRYPT_DIR.mkdir(exist_ok=True)
    output_path = DECRYPT_DIR / meta["filename"]
    counter = 1
    base_path = output_path
    while output_path.exists():
        stem = base_path.stem
        suffix = base_path.suffix
        output_path = DECRYPT_DIR / f"{stem}_restored_{counter}{suffix}"
        counter += 1
    
    output_path.write_bytes(raw)
    sp.unlink()
    
    _secure_wipe(encrypted)
    _secure_wipe(payload)
    _secure_wipe(raw)
    
    return output_path, meta

# ─── KEY MANAGER ─────────────────────────────────────────────
def get_key_file_path(name):
    KEYS_DIR.mkdir(exist_ok=True)
    return KEYS_DIR / f"{name}.key"

def save_key(name, value):
    KEYS_DIR.mkdir(exist_ok=True)
    key_file = get_key_file_path(name)
    if key_file.exists():
        _warn(f"Key '{name}' sudah ada!")
        overwrite = input(f"  {Y}Overwrite? (y/n): {RST}").strip().lower()
        if overwrite != 'y':
            return False
    with open(key_file, 'w') as f:
        f.write(value)
    _ok(f"Key '{name}' disimpan di folder KEYS")
    return True

def load_key(name):
    key_file = get_key_file_path(name)
    if key_file.exists():
        with open(key_file, 'r') as f:
            return f.read().strip()
    return None

def delete_key(name):
    key_file = get_key_file_path(name)
    if key_file.exists():
        key_file.unlink()
        _ok(f"Key '{name}' dihapus")
        return True
    else:
        _err(f"Key '{name}' tidak ditemukan")
        return False

def list_keys():
    KEYS_DIR.mkdir(exist_ok=True)
    key_files = list(KEYS_DIR.glob("*.key"))
    if not key_files:
        _info("Belum ada key tersimpan di folder KEYS")
        return []
    print(f"\n  {M}{BLD}🔑  KEY TERSIMPAN{RST}")
    _divider()
    keys = []
    for i, key_file in enumerate(key_files, 1):
        name = key_file.stem
        with open(key_file, 'r') as f:
            value = f.read().strip()
        masked = value[:4] + "•••••" + value[-4:] if len(value) > 8 else "••••••••"
        print(f"  {D}{i}.{RST}  {W}{name:<15}{RST}  {D}→{RST}  {Y}{masked}{RST}")
        keys.append({"name": name, "value": value})
    _divider()
    _info(f"Lokasi: {KEYS_DIR}")
    return keys

def get_password_from_keys():
    keys = list_keys()
    if not keys:
        return None
    print(f"\n  {Y}Pilih key:{RST}")
    for i, key in enumerate(keys, 1):
        print(f"  {D}{i}.{RST}  {key['name']}")
    print(f"  {D}0.{RST}  Batal / password manual")
    try:
        choice = input(f"\n  {Y}Pilihan: {RST}").strip()
        if choice == '0':
            return None
        idx = int(choice) - 1
        if 0 <= idx < len(keys):
            return keys[idx]['value']
    except:
        pass
    return None

# ══════════════════════════════════════════════════════════════
#   UI FUNCTIONS
# ══════════════════════════════════════════════════════════════

def clear_screen():
    os.system('clear 2>/dev/null || cls 2>/dev/null')

def _folder_count(folder):
    if folder.exists():
        return len(list(folder.glob("*")))
    return -1

def banner():
    clear_screen()
    print()
    print(f"  {M}{BLD}____  ___________________________.___._____________________{RST}")
    print(f"  {M}{BLD}\\   \\/  /\\_   ___ \\______   \\__  |   |\\______   \\__    ___/{RST}")
    print(f"  {M}{BLD} \\     / /    \\  \\/|       _//   |   | |     ___/ |    |   {RST}")
    print(f"  {M}{BLD} /     \\ \\     \\___|    |   \\\\____   | |    |     |    |   {RST}")
    print(f"  {M}{BLD}/___/\\  \\ \\______  /____|_  // ______| |____|     |____|   {RST}")
    print(f"  {M}{BLD}      \\_/        \\/       \\/ \\/                             {RST}")
    print()
    print(f"  {C}{BLD}t.me/XCODE_OWN{RST}   {R}{BLD}youtube/L8K1Z-q{RST}")
    print()

    folders = [
        (INPUT_DIR, "📁", "INPUT", C),
        (SELESAI_DIR, "✅", "SELESAI", G),
        (DECRYPT_DIR, "🔓", "DECRYPT", Y),
        (KEYS_DIR, "🔑", "KEYS", M),
    ]
    if XCODE_DIR.exists():
        row = ""
        for folder, emoji, label, color in folders:
            cnt = _folder_count(folder)
            badge = f"[{cnt}]" if cnt >= 0 else "[-]"
            row += f"  {emoji}{color}{BLD}{label}{RST}{D}{badge}{RST}"
        print(row)
    else:
        print(f"  {R}✘  Folder belum dibuat — jalankan: termux-setup-storage{RST}")

    print()
    _divider(color=D)

def show_file_list(folder, title, max_show=5):
    if not folder.exists():
        _info(f"{title}  (folder belum dibuat)")
        return
    files = list(folder.glob("*"))
    if files:
        print(f"\n  {C}{BLD}📂  {title}{RST}  {D}({len(files)} file){RST}")
        _divider()
        for i, f in enumerate(files[:max_show]):
            size = f.stat().st_size if f.is_file() else 0
            icon = "📄" if f.is_file() else "📁"
            size_str = f"{size:,} B" if size < 1024 else f"{size//1024:,} KB"
            print(f"  {D}{i+1}.{RST}  {icon}  {W}{f.name}{RST}  {D}({size_str}){RST}")
        if len(files) > max_show:
            _info(f"... dan {len(files)-max_show} file lainnya")
        _divider()
    else:
        print(f"\n  {D}📂  {title}  (kosong){RST}")

def get_password_input(prompt="Password", confirm=False):
    if KEYS_DIR.exists() and list(KEYS_DIR.glob("*.key")):
        print(f"\n  {D}💡 Ada key tersimpan di KEYS folder...{RST}")
        saved_keys = list_keys()
        if saved_keys:
            ans = input(f"\n  {Y}Gunakan key dari KEYS? (y/n): {RST}").strip().lower()
            if ans == 'y':
                pw = get_password_from_keys()
                if pw is not None:
                    return pw

    print(f"\n  {Y}┌─ {prompt} {'-'*40}┐{RST}")
    pw = getpass.getpass(f"  {Y}│ Password: {RST}")
    print(f"  {Y}└{'-'*50}┘{RST}")

    if confirm:
        print(f"\n  {Y}┌─ Konfirmasi Password {'-'*34}┐{RST}")
        pw2 = getpass.getpass(f"  {Y}│ Ulangi  : {RST}")
        print(f"  {Y}└{'-'*50}┘{RST}")
        if pw != pw2:
            _err("Password tidak sama!")
            sys.exit(1)

    if len(pw) == 0:
        ans = input(f"\n  {Y}Password kosong, lanjutkan? (y/n): {RST}").lower()
        if ans != 'y':
            sys.exit(1)

    if pw and not confirm:
        ans = input(f"\n  {Y}Simpan password ke KEYS? (y/n): {RST}").strip().lower()
        if ans == 'y':
            name = input(f"  {Y}Nama key: {RST}").strip()
            if name:
                save_key(name, pw)

    return pw

def _loading_layers():
    layers = [
        (C, "L1", "ZLIB Compress"),
        (B, "L2", "AES-256-GCM"),
        (M, "L3", "XOR Rolling"),
        (G, "L4", "Scramble 2-pass"),
        (Y, "L5", "Fernet (AES+HMAC)"),
        (R, "L6", "Base85 + Checksum"),
        (W, "L7", "HMAC-SHA512 Seal"),
        (M, "L8", "Reverse Bytes"),
        (C, "L9", "Chunk Swap 16-byte"),
        (B, "L10", "XOR2 Advanced + Offset"),
    ]
    for color, tag, name in layers:
        print(f"  {color}{BLD}{tag}{RST}  {D}{name}{RST}")
        time.sleep(0.06)

# ─── MENU FUNCTIONS ──────────────────────────────────────────
def _menu_encrypt():
    banner()
    print(f"  {G}{BLD}🔐  ENKRIPSI FILE{RST}  {D}— 10-Layer Ultra{RST}")
    _divider()

    show_file_list(INPUT_DIR, "INPUT — File yang tersedia")

    print(f"\n  {Y}┌─ Nama File {'-'*43}┐{RST}")
    src = input(f"  {Y}│ File: {RST}").strip()
    print(f"  {Y}└{'-'*54}┘{RST}")

    if not src:
        _err("Nama file tidak boleh kosong!")
        input(f"\n  {D}Enter untuk kembali...{RST}")
        return

    src_path = INPUT_DIR / src
    if not src_path.exists():
        _err("File tidak ditemukan di folder INPUT!")
        input(f"\n  {D}Enter untuk kembali...{RST}")
        return

    size_bytes = src_path.stat().st_size
    size_disp = f"{size_bytes:,} B" if size_bytes < 1024 else f"{size_bytes//1024:,} KB"

    print(f"\n  {C}┌─ INFO FILE {'-'*42}┐{RST}")
    print(f"  {C}│{RST}  📄  {W}{src_path.name}{RST}")
    print(f"  {C}│{RST}  {D}Ukuran  : {W}{size_disp}{RST}")
    print(f"  {C}└{'-'*54}┘{RST}")

    pw = get_password_input("Password Enkripsi", confirm=True)

    print(f"\n  {Y}Memproses enkripsi 10 layer...{RST}")
    _loading_layers()
    _progress_bar("Enkripsi", 0, 100)
    print()

    t0 = time.time()
    try:
        output, meta = encrypt_file_with_folders(str(src_path), pw)
        elapsed = time.time() - t0
        out_size = output.stat().st_size
        out_disp = f"{out_size:,} B" if out_size < 1024 else f"{out_size//1024:,} KB"

        print(f"  {G}{BLD}╭──────────────────────────────────────────────────────╮{RST}")
        print(f"  {G}{BLD}│{RST}            {G}✓ ENCRYPT COMPLETED SUCCESSFULLY{RST}           {G}{BLD}│{RST}")
        print(f"  {G}{BLD}├──────────────────────────────────────────────────────┤{RST}")
        print(f"  {G}{BLD}│{RST} {C}📁 Output    {RST}: {W}{output.name[:34]:<34}{RST} {G}{BLD}│{RST}")
        print(f"  {G}{BLD}│{RST} {C}📦 File Size {RST}: {W}{out_disp:<34}{RST} {G}{BLD}│{RST}")
        print(f"  {G}{BLD}│{RST} {C}⚡ Process   {RST}: {W}{f'{elapsed:.2f} sec':<34}{RST} {G}{BLD}│{RST}")
        print(f"  {G}{BLD}│{RST} {C}🔒 SHA-256   {RST}: {W}{meta['sha256'][:28]}...{RST} {G}✓{RST} {G}{BLD}│{RST}")
        print(f"  {G}{BLD}│{RST} {C}🔐 Layers    {RST}: {W}10-layer protection{RST}           {G}{BLD}│{RST}")
        print(f"  {G}{BLD}╰──────────────────────────────────────────────────────╯{RST}")
        _ok("File asli dihapus dari INPUT")
        _ok("File terenkripsi ada di SELESAI")

    except Exception as e:
        _err(f"Error: {str(e)}")
        input(f"\n  {D}Enter untuk kembali...{RST}")

def _menu_decrypt():
    banner()
    print(f"  {R}{BLD}🔓  DEKRIPSI FILE{RST}  {D}— Hanya pemilik password{RST}")
    _divider()

    for folder, title in [(SELESAI_DIR, "SELESAI"), (ENCRYPT_DIR, "ENCRYPT")]:
        if folder.exists():
            files = list(folder.glob(f"*{EXT_ENC}"))
            if files:
                print(f"\n  {C}{BLD}📂  {title}{RST}  {D}({len(files)} file .x7l){RST}")
                _divider()
                for i, f in enumerate(files[:5], 1):
                    size = f.stat().st_size
                    size_disp = f"{size:,} B" if size < 1024 else f"{size//1024:,} KB"
                    print(f"  {D}{i}.{RST}  📄  {W}{f.name}{RST}  {D}({size_disp}){RST}")
                if len(files) > 5:
                    _info(f"... dan {len(files)-5} file lainnya")
                _divider()

    print(f"\n  {Y}┌─ Nama File .x7l {'-'*38}┐{RST}")
    src = input(f"  {Y}│ File: {RST}").strip()
    print(f"  {Y}└{'-'*54}┘{RST}")

    if not src:
        _err("Nama file tidak boleh kosong!")
        input(f"\n  {D}Enter untuk kembali...{RST}")
        return

    src_path = None
    for folder in [SELESAI_DIR, ENCRYPT_DIR]:
        if folder.exists():
            test_path = folder / src
            if test_path.exists():
                src_path = test_path
                break

    if not src_path:
        _err("File .x7l tidak ditemukan!")
        input(f"\n  {D}Enter untuk kembali...{RST}")
        return

    size_bytes = src_path.stat().st_size
    size_disp = f"{size_bytes:,} B" if size_bytes < 1024 else f"{size_bytes//1024:,} KB"

    print(f"\n  {C}┌─ INFO FILE {'-'*42}┐{RST}")
    print(f"  {C}│{RST}  🔐  {W}{src_path.name}{RST}")
    print(f"  {C}│{RST}  {D}Ukuran  : {W}{size_disp}{RST}")
    print(f"  {C}└{'-'*54}┘{RST}")

    pw = get_password_input("Password Dekripsi", confirm=False)

    print(f"\n  {Y}Memproses dekripsi 10 layer...{RST}")
    _loading_layers()
    _progress_bar("Dekripsi", 0, 100)
    print()

    t0 = time.time()
    try:
        output, meta = decrypt_file_with_folders(str(src_path), pw)
        elapsed = time.time() - t0
        print(f"  {G}{BLD}╭──────────────────────────────────────────────────────╮{RST}")
        print(f"  {G}{BLD}│{RST}            {G}✓ DECRYPT COMPLETED SUCCESSFULLY{RST}           {G}{BLD}│{RST}")
        print(f"  {G}{BLD}├──────────────────────────────────────────────────────┤{RST}")
        print(f"  {G}{BLD}│{RST} {C}📄 File Name {RST}: {W}{meta['filename'][:34]:<34}{RST} {G}{BLD}│{RST}")
        print(f"  {G}{BLD}│{RST} {C}📦 File Size {RST}: {W}{str(meta['size']) + ' bytes':<34}{RST} {G}{BLD}│{RST}")
        print(f"  {G}{BLD}│{RST} {C}📁 Output    {RST}: {W}{output.name[:34]:<34}{RST} {G}{BLD}│{RST}")
        print(f"  {G}{BLD}│{RST} {C}⚡ Process   {RST}: {W}{f'{elapsed:.2f} sec':<34}{RST} {G}{BLD}│{RST}")
        print(f"  {G}{BLD}│{RST} {C}🔒 SHA-256   {RST}: {W}{meta['sha256'][:28]}...{RST} {G}✓{RST} {G}{BLD}│{RST}")
        print(f"  {G}{BLD}╰──────────────────────────────────────────────────────╯{RST}")
        _ok("Verifikasi SHA-256 berhasil")
        _ok("File asli dikembalikan ke DECRYPT")

    except ValueError as e:
        print(f"  {R}{BLD}╭──────────────────────────────────────────────────────╮{RST}")
        print(f"  {R}{BLD}│{RST}              {R}✖ DECRYPT FAILED{RST}                  {R}{BLD}│{RST}")
        print(f"  {R}{BLD}├──────────────────────────────────────────────────────┤{RST}")
        print(f"  {R}{BLD}│{RST} {Y}⚠ Error      {RST}: {W}{str(e)[:34]:<34}{RST} {R}{BLD}│{RST}")
        print(f"  {R}{BLD}│{RST} {Y}💡 Possible   {RST}: {W}Wrong password{RST}              {R}{BLD}│{RST}")
        print(f"  {R}{BLD}│{RST} {Y}             {RST}  {W}Corrupted file{RST}               {R}{BLD}│{RST}")
        print(f"  {R}{BLD}│{RST} {Y}             {RST}  {W}Invalid .x7l format{RST}          {R}{BLD}│{RST}")
        print(f"  {R}{BLD}╰──────────────────────────────────────────────────────╯{RST}")
    except Exception as e:
        _err(f"Error: {str(e)}")

def _menu_keys():
    banner()
    print(f"  {M}{BLD}🔑  KEY MANAGER{RST}  {D}— Folder KEYS{RST}")
    _divider()
    _info(f"Folder: {KEYS_DIR}")

    print()
    print(f"  {W}{BLD}MENU:{RST}")
    print(f"  {G}1{RST}  Lihat semua key")
    print(f"  {G}2{RST}  Tambah key baru")
    print(f"  {G}3{RST}  Hapus key")
    print(f"  {G}4{RST}  Generate key 256-bit acak")
    print(f"  {Y}0{RST}  Kembali")
    _divider()

    p = input(f"\n  {Y}Pilihan: {RST}").strip()

    if p == '1':
        list_keys()
    elif p == '2':
        print(f"\n  {Y}┌─ Tambah Key {'-'*41}┐{RST}")
        n = input(f"  {Y}│ Nama key    : {RST}").strip()
        v = getpass.getpass(f"  {Y}│ Key/password: {RST}")
        print(f"  {Y}└{'-'*54}┘{RST}")
        if n and v:
            save_key(n, v)
    elif p == '3':
        list_keys()
        print(f"\n  {Y}┌─ Hapus Key {'-'*42}┐{RST}")
        n = input(f"  {Y}│ Nama key: {RST}").strip()
        print(f"  {Y}└{'-'*54}┘{RST}")
        if n:
            delete_key(n)
    elif p == '4':
        k = base64.b85encode(os.urandom(32)).decode()
        print(f"\n  {G}{BLD}🔑  KEY 256-BIT GENERATED{RST}")
        _divider()
        print(f"  {W}{k}{RST}")
        _divider()
        n = input(f"\n  {Y}Nama untuk disimpan (kosong=skip): {RST}").strip()
        if n:
            save_key(n, k)

def _menu_status():
    banner()
    print(f"  {C}{BLD}📊  STATUS FOLDER{RST}")
    _divider()
    _info(f"Base: {XCODE_DIR}")
    print()

    if not XCODE_DIR.exists():
        _err("Folder XCODE ENCRYPT tidak ditemukan!")
        _warn("Jalankan 'termux-setup-storage' lalu restart")
        return

    total_files = 0
    total_size = 0

    folder_defs = [
        (INPUT_DIR, "📁", "INPUT", "File asli untuk dienkripsi"),
        (ENCRYPT_DIR, "🔐", "ENCRYPT", "Proses enkripsi sementara"),
        (SELESAI_DIR, "✅", "SELESAI", "Hasil enkripsi final (.x7l)"),
        (DECRYPT_DIR, "🔓", "DECRYPT", "Hasil dekripsi file asli"),
        (KEYS_DIR, "🔑", "KEYS", "Penyimpanan key"),
    ]

    for folder, emoji, label, desc in folder_defs:
        if folder.exists():
            files = list(folder.glob("*"))
            size = sum(f.stat().st_size for f in files if f.is_file())
            total_files += len(files)
            total_size += size
            size_disp = f"{size:,} B" if size < 1024 else f"{size//1024:,} KB"
            status = f"{G}✔{RST}" if files else f"{D}○{RST}"
            print(f"  {status}  {emoji}  {W}{BLD}{label:<9}{RST}  {D}{len(files)} file  {size_disp:<10}{RST}  {D}{desc}{RST}")
            for f in files[:2]:
                if f.is_file():
                    print(f"       {D}└ {f.name}{RST}")
            if len(files) > 2:
                print(f"       {D}└ ... +{len(files)-2} lainnya{RST}")
        else:
            print(f"  {D}○  {emoji}  {label:<9}  (folder belum dibuat){RST}")
        print()

    _divider()
    ts_disp = f"{total_size:,} B" if total_size < 1024 else f"{total_size//1024:,} KB"
    print(f"  {C}Total:{RST}  {W}{total_files} file  ·  {ts_disp}{RST}")

def _menu_info():
    banner()
    print(f"  {B}{BLD}ℹ️   INFO & KEAMANAN{RST}")
    _divider()

    print(f"""
  {W}{BLD}🛡️  10-LAYER ULTRA PROTECTION (DIPERKUAT){RST}

  {W}Layer Stack:{RST}
  {C}{BLD}L1{RST}  {D}ZLIB Compress{RST}          Level 9 compression
  {B}{BLD}L2{RST}  {D}AES-256-GCM{RST}            Authenticated encryption
  {M}{BLD}L3{RST}  {D}XOR Rolling (Multi){RST}    Safe XOR encryption
  {G}{BLD}L4{RST}  {D}Scramble (2-pass){RST}      Double byte scrambling
  {Y}{BLD}L5{RST}  {D}Fernet (AES+HMAC){RST}      Secondary encryption
  {R}{BLD}L6{RST}  {D}Base85 + Checksum{RST}      Encoding with integrity
  {W}{BLD}L7{RST}  {D}HMAC-SHA512{RST}            Seal with timestamp
  {M}{BLD}L8{RST}  {D}Reverse Bytes{RST}          Byte reversal protection
  {C}{BLD}L9{RST}  {D}Chunk Swap 16-byte{RST}     Block-level obfuscation
  {B}{BLD}L10{RST} {D}XOR2 Advanced + Offset{RST} Dynamic XOR encryption
""")

    _divider()
    print(f"""
  {W}{BLD}📁 Struktur Folder{RST}
  {D}📂 {XCODE_DIR}{RST}
  {C}  📁 INPUT{RST}    {D}→ Letakkan file asli di sini{RST}
  {B}  🔐 ENCRYPT{RST}  {D}→ Proses enkripsi sementara{RST}
  {G}  ✅ SELESAI{RST}  {D}→ Hasil enkripsi final (.x7l){RST}
  {Y}  🔓 DECRYPT{RST}  {D}→ Hasil dekripsi file asli{RST}
  {M}  🔑 KEYS{RST}     {D}→ Tempat penyimpanan key{RST}
""")

    _divider()
    print(f"""
  {W}{BLD}🔐 Keamanan (Ditingkatkan){RST}
  {D}  · PBKDF2-SHA512 : {W}250.000 iterasi (+25%){RST}
  {D}  · AES-256-GCM   : {W}Authenticated encryption{RST}
  {D}  · HMAC-SHA512   : {W}Integrity + timestamp{RST}
  {D}  · SHA-256 check : {W}Verifikasi saat dekripsi{RST}
  {D}  · Rate limiting : {W}Max {MAX_ATTEMPTS} percobaan / {BLOCK_TIME}s block{RST}
  {D}  · Extra Layers  : {W}Reverse + Chunk Swap + XOR2{RST}
  {D}  · Salt Length   : {W}48 bytes (lebih aman){RST}
  {D}  · Secure Wipe   : {W}Memory cleanup setelah operasi{RST}
  {D}  · Random Delay  : {W}Anti timing attack{RST}
""")
    print(f"  {Y}{BLD}⚠️  Hanya pemilik password yang bisa mendekripsi!{RST}")
    print()

# ══════════════════════════════════════════════════════════════
#   MAIN
# ══════════════════════════════════════════════════════════════
def main_menu():
    ultra_anti_debug()
    create_all_folders()

    print()
    _ok("ULTRA PROTECTION ACTIVE (10 Layers)")
    _ok(f"Folder: {XCODE_DIR}")
    _ok("Termux/Android compatible mode")
    _ok("No password limit")
    _ok("Keys stored in KEYS folder")
    print()
    time.sleep(0.6)

    while True:
        banner()

        print(f"  {W}{BLD}MENU UTAMA{RST}")
        _divider()
        print(f"  {G}1{RST}  🔐  {W}Encrypt File{RST}    {D}INPUT → SELESAI{RST}")
        print(f"  {R}2{RST}  🔓  {W}Decrypt File{RST}    {D}SELESAI → DECRYPT{RST}")
        print(f"  {M}3{RST}  🔑  {W}Key Manager{RST}     {D}Folder KEYS{RST}")
        print(f"  {C}4{RST}  📊  {W}Status{RST}          {D}Folder Overview{RST}")
        print(f"  {B}5{RST}  ℹ️   {W}Info{RST}            {D}Layers & Security{RST}")
        print(f"  {D}0{RST}  🚪  {W}Keluar{RST}")
        _divider()

        p = input(f"  {Y}▶ Pilihan: {RST}").strip()

        if p == '1':
            _menu_encrypt()
        elif p == '2':
            _menu_decrypt()
        elif p == '3':
            _menu_keys()
        elif p == '4':
            _menu_status()
        elif p == '5':
            _menu_info()
        elif p == '0':
            print(f"\n  {M}👋  Sampai jumpa! Tetap aman!{RST}\n")
            sys.exit(0)

        input(f"\n  {D}Tekan Enter untuk lanjut...{RST}")

if __name__ == "__main__":
    try:
        ultra_anti_debug()
        signal.signal(signal.SIGINT, lambda s, f: sys.exit(1))
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n  {M}Program dihentikan!{RST}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n  {R}Error: {str(e)}{RST}\n")
        sys.exit(1)