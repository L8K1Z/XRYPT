#!/data/data/com.termux/files/usr/bin/bash

# ─── Warna ──────────────────────────────────────────────────
R='\033[91m'; G='\033[92m'; Y='\033[93m'
B='\033[94m'; M='\033[95m'; C='\033[96m'
W='\033[97m'; D='\033[2m';  RST='\033[0m'
BLD='\033[1m'

clear

echo
printf "              ${W}${BLD}XCRYPT INSTALLER${RST} ${D}v1.0 by XCODEMODZ${RST}\n"
printf "${M}└────────────────────────────────────────────────────┘${RST}\n"
echo

# ─── Progress Bar (single line, no spam) ────────────────────
progress_bar() {
    local label="$1"
    local from=$2
    local to=$3
    local width=38
    local i filled empty bar col

    for ((i=from; i<=to; i++)); do
        filled=$(( (i * width) / 100 ))
        empty=$(( width - filled ))
        bar=""
        for ((f=0; f<filled; f++)); do bar="${bar}█"; done
        for ((e=0; e<empty; e++)); do bar="${bar}░"; done

        if   [ $i -lt 30 ]; then col="${R}"
        elif [ $i -lt 70 ]; then col="${Y}"
        else                      col="${G}"
        fi

        printf "\033[2K\r  ${D}%-20s${RST}  ${col}${BLD}[${bar}]${RST}  ${W}${BLD}%3d%%${RST}" "$label" "$i"
        sleep 0.018
    done
    printf "\n"
}

# ══════════════════════════════════════════════════════
#   STEP 1 · STORAGE PERMISSION
# ══════════════════════════════════════════════════════
printf "  ${M}${BLD}[1/5]${RST}  ${W}Termux Storage Setup${RST}\n"
progress_bar "Akses storage" 0 20
termux-setup-storage 2>/dev/null
if [ $? -eq 0 ]; then
    printf "  ${G}✔${RST}  Akses storage OK\n"
else
    printf "  ${Y}⚠${RST}  Lanjut tanpa konfirmasi\n"
fi
echo

# ══════════════════════════════════════════════════════
#   STEP 2 · UPDATE PACKAGES
# ══════════════════════════════════════════════════════
printf "  ${M}${BLD}[2/5]${RST}  ${W}Update Paket Termux${RST}\n"
progress_bar "Sinkronisasi repo" 20 45
pkg update -y -q 2>/dev/null 1>/dev/null
printf "  ${G}✔${RST}  Repository diperbarui\n"
echo

# ══════════════════════════════════════════════════════
#   STEP 3 · PYTHON3
# ══════════════════════════════════════════════════════
printf "  ${M}${BLD}[3/5]${RST}  ${W}Install Python3${RST}\n"
progress_bar "Install python3" 45 65
pkg install python3 -y -q 2>/dev/null 1>/dev/null
printf "  ${G}✔${RST}  Python3 siap\n"
echo

# ══════════════════════════════════════════════════════
#   STEP 4 · CRYPTOGRAPHY LIBRARY
# ══════════════════════════════════════════════════════
printf "  ${M}${BLD}[4/5]${RST}  ${W}Install Library Cryptography${RST}\n"
progress_bar "Install cryptography" 65 85
pkg install python-cryptography -y -q 2>/dev/null 1>/dev/null
if [ $? -ne 0 ]; then
    pip install cryptography --break-system-packages -q 2>/dev/null 1>/dev/null \
        || pip install cryptography -q 2>/dev/null 1>/dev/null
fi
printf "  ${G}✔${RST}  Library cryptography siap\n"
echo

# ══════════════════════════════════════════════════════
#   STEP 5 · INSTALL BINARY
# ══════════════════════════════════════════════════════
printf "  ${M}${BLD}[5/5]${RST}  ${W}Install XCRYPT Binary${RST}\n"
progress_bar "Pasang binary" 85 100

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -f "$DIR/xcrypt.py" ]; then
    echo
    printf "  ${R}✘  xcrypt.py tidak ditemukan!${RST}\n"
    printf "  ${D}Letakkan xcrypt.py di folder yang sama dengan install.sh${RST}\n"
    echo
    exit 1
fi

cp "$DIR/xcrypt.py" "$PREFIX/bin/xcrypt.py"
chmod +x "$PREFIX/bin/xcrypt.py"

cat > "$PREFIX/bin/xcrypt7" << 'SH'
#!/data/data/com.termux/files/usr/bin/bash
python3 $PREFIX/bin/xcrypt.py "$@"
SH
chmod +x "$PREFIX/bin/xcrypt7"

printf "  ${G}✔${RST}  Binary xcrypt terpasang\n"
echo

# ══════════════════════════════════════════════════════
#   SELESAI
# ══════════════════════════════════════════════════════
printf "  ${D}──────────────────────────────────────────────────────${RST}\n"
echo
printf "\n"
printf "${G}${BLD}✔ xcrypt berhasil diinstall!${RST}\n\n"
echo
printf "  ${Y}${BLD}▶  Jalankan:${RST}  ${C}python xcrypt.py${RST}\n"
echo
