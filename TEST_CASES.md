# Test Cases - CSV_QL Query Nilai Mahasiswa

## Data Sample (data_nilai.csv)

```csv
nim,nama,mata_kuliah,sks,nilai_huruf,nilai_angka,semester,status
2023001,Ahmad Rizki,Automata dan Teknik Kompilasi,3,A,4.0,5,Lulus
2023002,Budi Santoso,Automata dan Teknik Kompilasi,3,B,3.0,5,Lulus
2023003,Citra Dewi,Automata dan Teknik Kompilasi,3,A,4.0,5,Lulus
...
```

---

## Test Case 1: SELECT Semua Data

**Query:**
```sql
SELECT * FROM ../data_nilai.csv
```

**Expected:** Semua 21 baris data ditampilkan

---

## Test Case 2: SELECT Kolom Tertentu

**Query:**
```sql
SELECT nim, nama, nilai_huruf FROM ../data_nilai.csv
```

**Expected:** 3 kolom (nim, nama, nilai_huruf) dari semua baris

---

## Test Case 3: Filter Mahasiswa Nilai A

**Query:**
```sql
SELECT nama, mata_kuliah FROM ../data_nilai.csv WHERE nilai_huruf = "A"
```

**Expected:** Hanya mahasiswa dengan nilai A

---

## Test Case 4: Filter Mahasiswa Tidak Lulus

**Query:**
```sql
SELECT nim, nama, mata_kuliah, nilai_huruf FROM ../data_nilai.csv WHERE status = "Tidak Lulus"
```

**Expected:** Mahasiswa yang tidak lulus mata kuliah

---

## Test Case 5: Filter dengan Kondisi Numerik

**Query:**
```sql
SELECT nama, nilai_angka FROM ../data_nilai.csv WHERE nilai_angka >= 3.5
```

**Expected:** Mahasiswa dengan nilai >= 3.5

---

## Test Case 6: Kombinasi AND

**Query:**
```sql
SELECT * FROM ../data_nilai.csv WHERE semester = 5 AND nilai_huruf = "A"
```

**Expected:** Mahasiswa semester 5 dengan nilai A

---

## Test Case 7: Kombinasi OR

**Query:**
```sql
SELECT nama, nilai_huruf FROM ../data_nilai.csv WHERE nilai_huruf = "A" OR nilai_huruf = "B"
```

**Expected:** Mahasiswa dengan nilai A atau B

---

## Test Case 8: LIMIT

**Query:**
```sql
SELECT * FROM ../data_nilai.csv LIMIT 5
```

**Expected:** Hanya 5 baris pertama

---

## Test Case 9: Error - Kolom Tidak Ada

**Query:**
```sql
SELECT ipk FROM ../data_nilai.csv
```

**Expected:** Error - kolom 'ipk' tidak ditemukan

---

## Test Case 10: Error - File Tidak Ada

**Query:**
```sql
SELECT * FROM tidak_ada.csv
```

**Expected:** Error - file tidak ditemukan
