"""
semantic.py - Semantic Analyzer untuk CSV_QL

═══════════════════════════════════════════════════════════════════════════════
                        📋 INSTRUKSI PENGISIAN
═══════════════════════════════════════════════════════════════════════════════

Modul ini melakukan analisis semantik - validasi query sebelum eksekusi.
Semantic analysis berbeda dari syntax analysis:
- Syntax: "apakah query ini GRAMATIKAL benar?"
- Semantic: "apakah query ini LOGIS dan VALID?"

TUGAS YANG HARUS DIKERJAKAN:
-----------------------------

1. Buat dataclass SemanticResult dengan field:
   - valid: bool           -> apakah query valid
   - errors: list[str]     -> daftar error
   - warnings: list[str]   -> daftar warning

2. Implementasi fungsi analyze(query: Statement) -> SemanticResult
   yang melakukan validasi berikut:
   
   a. Cek apakah file CSV ada
      - Gunakan: os.path.exists(table)
      - Error jika file tidak ditemukan
   
   b. Baca header CSV untuk validasi kolom
      - Gunakan: csv.reader atau pandas
      - Simpan nama kolom dalam set
   
   c. Validasi kolom yang di-SELECT
      - Cek setiap kolom (kecuali *) ada di header
      - Error jika kolom tidak ada
   
   d. Validasi kolom di WHERE clause
      - Traverse expression tree
      - Cek setiap identifier (nama kolom) ada di header
   
   e. Validasi LIMIT
      - Warning jika LIMIT = 0
   
   f. Warning untuk SELECT *
      - Optional: warning jika tabel besar

3. Implementasi helper function validate_expr_columns()
   untuk validasi kolom dalam ekspresi WHERE secara rekursif

REFERENSI:
----------
Lihat file Rust: src/semantic.rs

TIPS:
-----
- Gunakan module 'csv' bawaan Python untuk baca header CSV
- Gunakan os.path.exists() untuk cek file
- Untuk traverse expression tree, gunakan pattern matching atau isinstance()

═══════════════════════════════════════════════════════════════════════════════
"""

import os
import csv
from dataclasses import dataclass, field
from typing import Set, List
from ast_nodes import Statement, Expr, BinaryOp, Identifier, Number, StringLiteral, Literal


@dataclass
class SemanticResult:
    """Hasil analisis semantik."""
    valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


def analyze(query: Statement) -> SemanticResult:
    """
    Analisis semantik untuk query.
    
    Args:
        query: AST Statement dari parser
        
    Returns:
        SemanticResult dengan status validasi dan pesan error/warning
    """
    errors: List[str] = []
    warnings: List[str] = []
    
    # 1. Cek file CSV ada
    table = query.table
    if not os.path.exists(table):
        errors.append(f"File '{table}' tidak ditemukan")
        return SemanticResult(valid=False, errors=errors, warnings=warnings)
    
    # 2. Baca header CSV
    try:
        with open(table, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = set(next(reader))
    except StopIteration:
        errors.append(f"File '{table}' kosong atau tidak memiliki header")
        return SemanticResult(valid=False, errors=errors, warnings=warnings)
    except Exception as e:
        errors.append(f"Gagal membaca file '{table}': {str(e)}")
        return SemanticResult(valid=False, errors=errors, warnings=warnings)
    
    # 3. Validasi kolom SELECT
    for col in query.columns:
        if col != "*" and col not in headers:
            errors.append(f"Kolom '{col}' tidak ada di file '{table}'. Kolom yang tersedia: {', '.join(sorted(headers))}")
    
    # 4. Validasi kolom WHERE
    if query.where_clause is not None:
        validate_expr_columns(query.where_clause, headers, errors, table)
    
    # 5. Validasi LIMIT
    if query.limit is not None:
        if query.limit == 0:
            warnings.append("LIMIT 0 akan mengembalikan 0 baris")
        elif query.limit < 0:
            errors.append("LIMIT tidak boleh negatif")
    
    # 6. Warning untuk SELECT *
    if "*" in query.columns and len(headers) > 10:
        warnings.append(f"SELECT * pada tabel dengan {len(headers)} kolom. Pertimbangkan untuk memilih kolom spesifik.")
    
    # 7. Return hasil
    return SemanticResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )


def validate_expr_columns(expr: Expr, headers: Set[str], errors: List[str], table: str) -> None:
    """
    Validasi kolom dalam ekspresi WHERE secara rekursif.
    
    Args:
        expr: Expression dari WHERE clause
        headers: Set nama kolom yang valid
        errors: List untuk menampung error
        table: Nama file untuk pesan error
    """
    # Jika expr adalah Identifier (nama kolom)
    if isinstance(expr, Identifier):
        if expr.name not in headers:
            errors.append(f"Kolom '{expr.name}' di WHERE clause tidak ada di file '{table}'")
    
    # Jika expr adalah BinaryOp (operasi biner)
    elif isinstance(expr, BinaryOp):
        # Rekursif validasi left dan right
        validate_expr_columns(expr.left, headers, errors, table)
        validate_expr_columns(expr.right, headers, errors, table)
    
    # Untuk Number, StringLiteral, Literal - tidak perlu validasi
    elif isinstance(expr, (Number, StringLiteral, Literal)):
        pass  # Literal values tidak perlu validasi


# ═══════════════════════════════════════════════════════════════════════════════
# CONTOH PENGGUNAAN (untuk testing)
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    from lexer import Lexer
    from parser import Parser
    
    # Gunakan path relatif dari folder src
    # Catatan: Lexer mendukung path seperti "data_nilai.csv" atau "folder/file.csv"
    # tapi tidak mendukung ".." karena titik ganda diparsing berbeda
    
    # Test cases dengan file data_nilai.csv
    queries = [
        # Valid queries (path relatif dari root project)
        ("SELECT * FROM data_nilai.csv", "c:/Codingan/csv_ql"),
        ("SELECT nim, nama, nilai_huruf FROM data_nilai.csv", "c:/Codingan/csv_ql"),
        ('SELECT nama FROM data_nilai.csv WHERE status = "Lulus"', "c:/Codingan/csv_ql"),
        ("SELECT * FROM data_nilai.csv WHERE nilai_angka >= 3.0 AND semester = 5", "c:/Codingan/csv_ql"),
        
        # Invalid queries (untuk testing error handling)
        ("SELECT * FROM file_tidak_ada.csv", None),
        ("SELECT kolom_salah FROM data_nilai.csv", "c:/Codingan/csv_ql"),
        ('SELECT nama FROM data_nilai.csv WHERE kolom_tidak_ada = "test"', "c:/Codingan/csv_ql"),
        ("SELECT * FROM data_nilai.csv LIMIT 0", "c:/Codingan/csv_ql"),
    ]
    
    print("=" * 70)
    print("                    SEMANTIC ANALYZER TEST")
    print("=" * 70)
    
    for item in queries:
        if isinstance(item, tuple):
            query, cwd = item
        else:
            query, cwd = item, None
        
        # Change directory jika perlu
        if cwd:
            original_cwd = os.getcwd()
            os.chdir(cwd)
        
        print(f"\nQuery: {query}")
        print("-" * 55)
        
        try:
            # Tokenize
            lexer = Lexer(query)
            tokens = lexer.tokenize()
            
            # Parse
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Semantic Analysis
            result = analyze(ast)
            
            # Print hasil
            if result.valid:
                print("  ✅ Query VALID")
            else:
                print("  ❌ Query TIDAK VALID")
            
            for err in result.errors:
                print(f"    ❌ Error: {err}")
            
            for warn in result.warnings:
                print(f"    ⚠️ Warning: {warn}")
            
        except Exception as e:
            print(f"  ❌ Exception: {e}")
        
        finally:
            # Restore directory
            if cwd:
                os.chdir(original_cwd)
    
    print("\n" + "=" * 70)
    print("                    TEST SELESAI")
    print("=" * 70)
