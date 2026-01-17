# CSV_QL - Mini SQL untuk File CSV

Program sederhana untuk melakukan query SQL pada file CSV.

## 🚀 Cara Menjalankan

```bash
# Build dulu
cargo build --release

# Jalankan mode interaktif
cargo run

# Atau langsung query dari command line
cargo run "SELECT * FROM data.csv"
```

---

## 📖 SYNTAX YANG DIDUKUNG

### Format Dasar
```sql
SELECT <kolom> FROM <file.csv> [WHERE <kondisi>] [LIMIT n]
```

---

## 📝 CONTOH QUERY

### 1️⃣ Ambil Semua Data
```sql
SELECT * FROM data.csv
```
**Output:** Semua kolom dan baris dari `data.csv`

---

### 2️⃣ Pilih Kolom Tertentu
```sql
SELECT nama, umur FROM data.csv
```
**Output:** Hanya kolom `nama` dan `umur`

```sql
SELECT nama FROM data.csv
```
**Output:** Hanya kolom `nama`

---

### 3️⃣ Filter dengan WHERE

**Perbandingan Angka:**
```sql
SELECT * FROM data.csv WHERE umur > 20
SELECT * FROM data.csv WHERE umur >= 25
SELECT * FROM data.csv WHERE umur < 30
SELECT * FROM data.csv WHERE umur <= 18
SELECT * FROM data.csv WHERE umur = 22
SELECT * FROM data.csv WHERE umur != 25
```

**Perbandingan String (gunakan tanda kutip):**
```sql
SELECT * FROM data.csv WHERE kota = "Jakarta"
SELECT * FROM data.csv WHERE nama = "Budi"
SELECT * FROM data.csv WHERE kota != "Bandung"
```

---

### 4️⃣ Kombinasi Kondisi dengan AND/OR

**AND (semua kondisi harus benar):**
```sql
SELECT * FROM data.csv WHERE umur > 20 AND umur < 30
SELECT * FROM data.csv WHERE kota = "Jakarta" AND umur > 25
```

**OR (salah satu kondisi benar):**
```sql
SELECT * FROM data.csv WHERE kota = "Jakarta" OR kota = "Bandung"
SELECT * FROM data.csv WHERE umur < 20 OR umur > 35
```

**Kombinasi AND dan OR:**
```sql
SELECT * FROM data.csv WHERE umur > 20 AND kota = "Jakarta" OR kota = "Surabaya"
```

---

### 5️⃣ Batasi Hasil dengan LIMIT
```sql
SELECT * FROM data.csv LIMIT 5
SELECT nama, umur FROM data.csv LIMIT 3
SELECT * FROM data.csv WHERE umur > 20 LIMIT 10
```

---

### 6️⃣ Kombinasi Lengkap
```sql
SELECT nama, umur, kota FROM data.csv WHERE umur > 18 AND umur < 35 LIMIT 5
```

---

## ⚙️ OPERATOR YANG DIDUKUNG

| Operator | Fungsi                  | Contoh            |
|----------|-------------------------|-------------------|
| `=`      | Sama dengan             | `umur = 25`       |
| `!=`     | Tidak sama dengan       | `kota != "Jakarta"` |
| `>`      | Lebih besar             | `umur > 20`       |
| `<`      | Lebih kecil             | `umur < 30`       |
| `>=`     | Lebih besar atau sama   | `umur >= 18`      |
| `<=`     | Lebih kecil atau sama   | `umur <= 25`      |
| `AND`    | Dan (kedua kondisi)     | `umur > 20 AND umur < 30` |
| `OR`     | Atau (salah satu)       | `kota = "A" OR kota = "B"` |

---

## 🔧 PERINTAH INTERAKTIF

| Perintah | Fungsi                      |
|----------|-----------------------------|
| `help`   | Tampilkan bantuan           |
| `clear`  | Bersihkan layar terminal    |
| `exit`   | Keluar dari program         |

---

## 📁 Format File CSV

File CSV harus memiliki header di baris pertama:

```csv
nama,umur,kota
Dika,22,Jakarta
Budi,19,Bandung
Siti,25,Surabaya
```

---

## 🧪 Contoh Penggunaan Lengkap

```
csv_ql> SELECT * FROM data.csv
┌───────┬──────┬──────────┐
│ nama  │ umur │   kota   │
├───────┼──────┼──────────┤
│ Dika  │  22  │ Jakarta  │
│ Budi  │  19  │ Bandung  │
│ Siti  │  25  │ Surabaya │
└───────┴──────┴──────────┘
✅ 3 baris ditemukan

csv_ql> SELECT nama FROM data.csv WHERE umur > 20 LIMIT 2
┌───────┐
│ nama  │
├───────┤
│ Dika  │
│ Siti  │
└───────┘
✅ 2 baris ditemukan

csv_ql> exit
👋 Sampai jumpa!
```
