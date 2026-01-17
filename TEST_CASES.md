# Test Cases untuk CSV_QL
# Jalankan setiap query di bawah ini untuk testing

# ==============================================================================
# TEST CASE 1: Basic SELECT * (Ambil semua data)
# ==============================================================================
# Input:
SELECT * FROM data.csv

# Expected Output: Semua 10 baris data ditampilkan


# ==============================================================================
# TEST CASE 2: SELECT kolom tertentu
# ==============================================================================
# Input:
SELECT nama, kota FROM data.csv

# Expected Output: Hanya kolom nama dan kota, 10 baris


# ==============================================================================
# TEST CASE 3: WHERE dengan perbandingan numerik
# ==============================================================================
# Input:
SELECT * FROM data.csv WHERE umur > 25

# Expected Output: 4 baris (Andi=30, Eko=40, Gita=29, Indra=35)


# ==============================================================================
# TEST CASE 4: WHERE dengan AND
# ==============================================================================
# Input:
SELECT nama, umur FROM data.csv WHERE umur >= 20 AND umur <= 30

# Expected Output: 5 baris (Dika=22, Siti=25, Andi=30, Fajar=21, Gita=29)


# ==============================================================================
# TEST CASE 5: Kombinasi WHERE + LIMIT
# ==============================================================================
# Input:
SELECT * FROM data.csv WHERE umur > 18 LIMIT 3

# Expected Output: 3 baris pertama yang umur > 18


# ==============================================================================
# TEST CASE BONUS: Error Handling - File tidak ada
# ==============================================================================
# Input:
SELECT * FROM tidak_ada.csv

# Expected Output: Semantic Error: File 'tidak_ada.csv' tidak ditemukan


# ==============================================================================
# TEST CASE BONUS: Error Handling - Kolom tidak ada
# ==============================================================================
# Input:
SELECT nama, alamat FROM data.csv

# Expected Output: Semantic Error: Kolom 'alamat' tidak ada di file 'data.csv'


# ==============================================================================
# Cara menjalankan dengan detail kompilasi (verbose):
# ==============================================================================
# Tambahkan --verbose di akhir query, contoh:
SELECT * FROM data.csv WHERE umur > 25 --verbose

# Ini akan menampilkan:
# [1] LEXICAL ANALYSIS - Daftar tokens
# [2] SYNTAX ANALYSIS - AST yang dihasilkan
# [3] SEMANTIC ANALYSIS - Hasil validasi
# [4] IR GENERATION - Query Plan
# [5] EXECUTION - Hasil query
