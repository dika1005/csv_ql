# CSV_QL Python - Mini SQL untuk File CSV

Versi Python dari CSV_QL untuk query file CSV dengan syntax SQL sederhana.

## 📁 Struktur Proyek

```
csv_ql/
├── README.md          📖 Dokumentasi & instruksi
├── TEST_CASES.md      📋 Test cases untuk pengujian
├── data.csv           📄 File CSV contoh untuk testing
├── .gitignore         🚫 Git ignore
│
└── src/               📂 Source code
    ├── main.py        ✅ [SELESAI] Entry point & REPL
    ├── tokens.py      ✅ [SELESAI] Definisi token
    ├── lexer.py       ✅ [SELESAI] Lexical analyzer
    ├── ast_nodes.py   📝 [TODO] Abstract Syntax Tree
    ├── parser.py      📝 [TODO] Syntax analyzer
    ├── semantic.py    📝 [TODO] Semantic analyzer
    ├── ir.py          📝 [TODO] Intermediate representation
    ├── engine.py      📝 [TODO] Query execution
    └── dfa.py         📝 [TODO] DFA visualization (opsional)
```

> ⚠️ **CATATAN**: 
> - File token dinamakan `tokens.py` (bukan `token.py`) untuk menghindari konflik dengan module bawaan Python
> - File AST dinamakan `ast_nodes.py` (bukan `ast.py`) untuk alasan yang sama

## 🎯 Pembagian Tugas Kelompok

### ✅ Sudah Dikerjakan
- **tokens.py** - Definisi TokenType dan Token
- **lexer.py** - Lexer untuk tokenization
- **main.py** - Program utama dan REPL

### 📋 Tugas untuk Anggota Kelompok

| File | Deskripsi | Tingkat Kesulitan | Dependensi |
|------|-----------|-------------------|------------|
| `ast_nodes.py` | Definisi AST (Statement, Expr, Op) | ⭐⭐ Mudah | Tidak ada |
| `parser.py` | Parser token → AST | ⭐⭐⭐⭐ Sulit | `tokens.py`, `ast_nodes.py` |
| `semantic.py` | Validasi query | ⭐⭐⭐ Sedang | `ast_nodes.py` |
| `ir.py` | Query plan | ⭐⭐ Mudah | `ast_nodes.py` |
| `engine.py` | Eksekusi query CSV | ⭐⭐⭐ Sedang | `ast_nodes.py` |
| `dfa.py` | Visualisasi DFA | ⭐ Sangat Mudah | Tidak ada |

### 🔄 Urutan Pengerjaan yang Disarankan

1. **ast_nodes.py** (harus dikerjakan pertama!)
2. **parser.py** (butuh ast_nodes.py)
3. **semantic.py** dan **ir.py** (bisa paralel, butuh ast_nodes.py)
4. **engine.py** (butuh ast_nodes.py)
5. **dfa.py** (opsional, bisa kapan saja)

## 🚀 Cara Menjalankan

```bash
# Masuk ke folder src
cd src

# Test lexer saja
python lexer.py

# Jalankan program (setelah semua modul selesai)
python main.py                              # Mode REPL
python main.py "SELECT * FROM ../data.csv"  # Mode direct
python main.py "SELECT * FROM ../data.csv" -v  # Dengan verbose
```

## 📝 Cara Mengerjakan

1. Buka file yang menjadi tugas Anda di folder `src/`
2. Baca instruksi di bagian atas file (dalam docstring)
3. Lihat kode TODO yang perlu diisi
4. Uncomment import yang diperlukan setelah dependensi selesai
5. Test dengan menjalankan file secara standalone

## 🧪 Contoh Query untuk Testing

```sql
SELECT * FROM ../data.csv
SELECT nama, umur FROM ../data.csv
SELECT * FROM ../data.csv WHERE umur > 20
SELECT * FROM ../data.csv WHERE kota = "Jakarta"
SELECT * FROM ../data.csv WHERE umur > 20 AND umur < 30
SELECT * FROM ../data.csv LIMIT 5
```

## ⚠️ Catatan Penting

- Semua file sudah memiliki skeleton code dan instruksi
- Jangan ubah signature function yang sudah ada
- Pastikan return type sesuai dengan yang diharapkan
- Test file Anda secara individual sebelum integrasi
- File `data.csv` ada di root project (gunakan `../data.csv` dari folder src)
