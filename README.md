# CSV_QL - Mini Query Engine untuk Data Nilai Mahasiswa

**Studi Kasus: Query Data Nilai Mahasiswa SIMAK/SIAKAD**

Mini SQL query engine berbasis Python untuk menganalisis data nilai mahasiswa dari file CSV. Proyek ini dibuat untuk mata kuliah **Automata dan Teknik Kompilasi**.

## 🎯 Deskripsi Proyek

CSV_QL adalah domain-specific language (DSL) yang memungkinkan pengguna melakukan query terhadap data nilai mahasiswa menggunakan syntax mirip SQL. Proyek ini mengimplementasikan:

- **Lexical Analysis** - Tokenisasi query menggunakan DFA
- **Syntax Analysis** - Parsing dengan CFG dan recursive descent
- **Semantic Analysis** - Validasi kolom dan tipe data
- **Intermediate Representation** - Query plan untuk eksekusi
- **Execution Engine** - Eksekusi query terhadap file CSV

## 📁 Struktur Proyek

```
csv_ql/
├── README.md          📖 Dokumentasi proyek
├── TEST_CASES.md      📋 Test cases untuk pengujian
├── data_nilai.csv     📄 Data nilai mahasiswa (contoh)
├── .gitignore         🚫 Git ignore
│
└── src/               📂 Source code
    ├── main.py        ✅ [SELESAI] Entry point & REPL
    ├── tokens.py      ✅ [SELESAI] Definisi token
    ├── lexer.py       ✅ [SELESAI] Lexical analyzer (DFA)
    ├── ast_nodes.py   📝 [TODO] Abstract Syntax Tree
    ├── parser.py      📝 [TODO] Syntax analyzer (CFG)
    ├── semantic.py    📝 [TODO] Semantic analyzer
    ├── ir.py          📝 [TODO] Intermediate representation
    ├── engine.py      📝 [TODO] Query execution
    └── dfa.py         📝 [TODO] DFA visualization
```

> ⚠️ **CATATAN**: 
> - File `tokens.py` (bukan `token.py`) untuk menghindari konflik dengan module bawaan Python
> - File `ast_nodes.py` (bukan `ast.py`) untuk alasan yang sama

## 🎯 Pembagian Tugas Kelompok

### ✅ Sudah Dikerjakan
| File | Kompiler | Deskripsi |
|------|----------|-----------|
| `tokens.py` | Lexer | Definisi TokenType dan Token |
| `lexer.py` | Lexer | Tokenisasi dengan DFA |
| `main.py` | - | Program utama dan REPL |

### 📋 Tugas untuk Anggota Kelompok

| File | Kompiler | Tingkat Kesulitan | Dependensi |
|------|----------|-------------------|------------|
| `ast_nodes.py` | Parser | ⭐⭐ Mudah | Tidak ada |
| `parser.py` | Parser | ⭐⭐⭐⭐ Sulit | `tokens.py`, `ast_nodes.py` |
| `semantic.py` | Semantic | ⭐⭐⭐ Sedang | `ast_nodes.py` |
| `ir.py` | IR | ⭐⭐ Mudah | `ast_nodes.py` |
| `engine.py` | Execution | ⭐⭐⭐ Sedang | `ast_nodes.py` |
| `dfa.py` | Visualisasi | ⭐ Sangat Mudah | Tidak ada |

### 🔄 Urutan Pengerjaan

1. **ast_nodes.py** (harus dikerjakan pertama!)
2. **parser.py** (butuh ast_nodes.py)
3. **semantic.py** dan **ir.py** (bisa paralel)
4. **engine.py** (butuh ast_nodes.py)
5. **dfa.py** (opsional, bisa kapan saja)

## 🚀 Cara Menjalankan

```bash
cd src

# Test lexer
python lexer.py

# Mode REPL (setelah semua modul selesai)
python main.py

# Mode direct query
python main.py "SELECT * FROM ../data_nilai.csv"
python main.py "SELECT * FROM ../data_nilai.csv" -v  # verbose
```

## 🧪 Contoh Query

```sql
-- Lihat semua data nilai
SELECT * FROM ../data_nilai.csv

-- Filter mahasiswa dengan nilai A
SELECT nama, mata_kuliah FROM ../data_nilai.csv WHERE nilai_huruf = "A"

-- Filter mahasiswa yang tidak lulus
SELECT nim, nama, mata_kuliah FROM ../data_nilai.csv WHERE status = "Tidak Lulus"

-- Kombinasi kondisi
SELECT * FROM ../data_nilai.csv WHERE nilai_angka >= 3.0 AND semester = 5

-- Batasi hasil
SELECT nama, nilai_huruf FROM ../data_nilai.csv LIMIT 5
```

## 📊 Struktur Data CSV

File `data_nilai.csv` berisi kolom:
| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| nim | String | Nomor Induk Mahasiswa |
| nama | String | Nama mahasiswa |
| mata_kuliah | String | Nama mata kuliah |
| sks | Number | Jumlah SKS |
| nilai_huruf | String | Nilai huruf (A, B, C, D, E) |
| nilai_angka | Number | Nilai angka (0.0 - 4.0) |
| semester | Number | Semester pengambilan |
| status | String | Status kelulusan |

## 📝 Cara Mengerjakan

1. Buka file yang menjadi tugas Anda di folder `src/`
2. Baca instruksi di bagian atas file (dalam docstring)
3. Lihat kode TODO yang perlu diisi
4. Uncomment import yang diperlukan setelah dependensi selesai
5. Test dengan menjalankan file secara standalone

## ⚠️ Catatan Penting

- Semua file sudah memiliki skeleton code dan instruksi
- Jangan ubah signature function yang sudah ada
- Pastikan return type sesuai dengan yang diharapkan
- Test file Anda secara individual sebelum integrasi
