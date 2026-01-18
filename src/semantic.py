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
from typing import Set
# from ast_nodes import Statement, Expr  # Uncomment setelah ast_nodes.py selesai


@dataclass
class SemanticResult:
    """Hasil analisis semantik."""
    valid: bool = True
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)


def analyze(query) -> SemanticResult:  # query: Statement
    """
    Analisis semantik untuk query.
    
    Args:
        query: AST Statement dari parser
        
    Returns:
        SemanticResult dengan status validasi dan pesan error/warning
    """
    errors = []
    warnings = []
    
    # TODO: Implementasi
    # 
    # 1. Cek file CSV ada
    # table = query.table
    # if not os.path.exists(table):
    #     errors.append(f"File '{table}' tidak ditemukan")
    #     return SemanticResult(valid=False, errors=errors, warnings=warnings)
    #
    # 2. Baca header CSV
    # with open(table, 'r') as f:
    #     reader = csv.reader(f)
    #     headers = set(next(reader))
    #
    # 3. Validasi kolom SELECT
    # for col in query.columns:
    #     if col != "*" and col not in headers:
    #         errors.append(f"Kolom '{col}' tidak ada di file '{table}'")
    #
    # 4. Validasi kolom WHERE
    # if query.where_clause:
    #     validate_expr_columns(query.where_clause, headers, errors)
    #
    # 5. Validasi LIMIT
    # if query.limit is not None and query.limit == 0:
    #     warnings.append("LIMIT 0 akan mengembalikan 0 baris")
    #
    # 6. Return hasil
    # return SemanticResult(
    #     valid=len(errors) == 0,
    #     errors=errors,
    #     warnings=warnings
    # )
    
    pass  # Hapus setelah implementasi


def validate_expr_columns(expr, headers: Set[str], errors: list) -> None:  # expr: Expr
    """
    Validasi kolom dalam ekspresi WHERE secara rekursif.
    
    Args:
        expr: Expression dari WHERE clause
        headers: Set nama kolom yang valid
        errors: List untuk menampung error
    """
    # TODO: Implementasi
    #
    # Pattern:
    # - Jika expr adalah Identifier:
    #     - Cek apakah nama kolom ada di headers
    #     - Jika tidak, tambahkan error
    #
    # - Jika expr adalah BinaryOp:
    #     - Rekursif validasi left dan right
    #
    # - Untuk Number, StringLiteral, Literal:
    #     - Tidak perlu validasi (return saja)
    #
    # Contoh dengan isinstance():
    # if isinstance(expr, Identifier):
    #     if expr.name not in headers:
    #         errors.append(f"Kolom '{expr.name}' tidak ada di WHERE clause")
    # elif isinstance(expr, BinaryOp):
    #     validate_expr_columns(expr.left, headers, errors)
    #     validate_expr_columns(expr.right, headers, errors)
    
    pass  # Hapus setelah implementasi
