"""
ast_nodes.py - Abstract Syntax Tree untuk CSV_QL

CATATAN: File ini dinamakan ast_nodes.py (bukan ast.py) untuk menghindari
konflik dengan module 'ast' bawaan Python.

═══════════════════════════════════════════════════════════════════════════════
                        📋 INSTRUKSI PENGISIAN
═══════════════════════════════════════════════════════════════════════════════

Modul ini berisi definisi AST (Abstract Syntax Tree) untuk query SQL.
AST adalah representasi struktur query yang sudah di-parse.

TUGAS YANG HARUS DIKERJAKAN:
-----------------------------

1. Buat class/dataclass Statement dengan variant Select yang memiliki field:
   - columns: List[str]       -> daftar kolom yang di-SELECT
   - table: str               -> nama file CSV
   - where_clause: Optional[Expr] -> kondisi WHERE (opsional)
   - limit: Optional[int]     -> batasan jumlah baris (opsional)

2. Buat class/dataclass Expr untuk ekspresi, dengan tipe:
   - BinaryOp: operasi biner (left, op, right)
   - Literal: literal string
   - StringLiteral: string dalam tanda kutip
   - Number: angka (float)
   - Identifier: nama kolom

3. Buat enum Op untuk operator:
   - Equal, NotEqual
   - GreaterThan, LessThan
   - GreaterThanOrEq, LessThanOrEq
   - Or, And

REFERENSI:
----------
Lihat file Rust: src/ast.rs

CONTOH STRUKTUR:
---------------
@dataclass
class SelectStatement:
    columns: list[str]
    table: str
    where_clause: Optional['Expr'] = None
    limit: Optional[int] = None

class Op(Enum):
    EQUAL = auto()
    NOT_EQUAL = auto()
    # ... dst

═══════════════════════════════════════════════════════════════════════════════
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, Union, List


# TODO: Implementasi Op enum di sini
# class Op(Enum):
#     ...


# TODO: Implementasi Expr class/dataclass di sini
# Hint: Bisa menggunakan Union type atau class inheritance


# TODO: Implementasi Statement class/dataclass di sini
# Hint: Untuk saat ini, cukup SelectStatement saja


pass  # Hapus ini setelah implementasi selesai
