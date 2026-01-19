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


# ═══════════════════════════════════════════════════════════════════════════════
#                              Op Enum
# ═══════════════════════════════════════════════════════════════════════════════

class Op(Enum):
    """Enum untuk operator perbandingan dan logika"""
    EQUAL = auto()              # =
    NOT_EQUAL = auto()          # != atau <>
    GREATER_THAN = auto()       # >
    LESS_THAN = auto()          # <
    GREATER_THAN_OR_EQ = auto() # >=
    LESS_THAN_OR_EQ = auto()    # <=
    OR = auto()                 # OR
    AND = auto()                # AND


# ═══════════════════════════════════════════════════════════════════════════════
#                              Expr Classes
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class BinaryOp:
    """Operasi biner: left op right"""
    left: 'Expr'
    op: Op
    right: 'Expr'


@dataclass
class Literal:
    """Literal string (tanpa tanda kutip)"""
    value: str


@dataclass
class StringLiteral:
    """String dalam tanda kutip"""
    value: str


@dataclass
class Number:
    """Angka (float)"""
    value: float


@dataclass
class Identifier:
    """Nama kolom/identifier"""
    name: str


# Union type untuk semua jenis Expr
Expr = Union[BinaryOp, Literal, StringLiteral, Number, Identifier]


# ═══════════════════════════════════════════════════════════════════════════════
#                              Statement Classes
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class SelectStatement:
    """
    Representasi SELECT statement
    
    Contoh: SELECT nama, nilai FROM data.csv WHERE nilai > 80 LIMIT 10
    """
    columns: List[str]              # daftar kolom yang di-SELECT
    table: str                      # nama file CSV
    where_clause: Optional[Expr] = None  # kondisi WHERE (opsional)
    limit: Optional[int] = None     # batasan jumlah baris (opsional)


# Statement adalah alias untuk SelectStatement (untuk saat ini)
Statement = SelectStatement
