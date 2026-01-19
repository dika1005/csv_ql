"""
engine.py - Query Execution Engine untuk CSV_QL

═══════════════════════════════════════════════════════════════════════════════
                        📋 INSTRUKSI PENGISIAN
═══════════════════════════════════════════════════════════════════════════════

Modul ini mengeksekusi query terhadap file CSV dan mengembalikan hasil.
Engine adalah tahap terakhir dari pipeline kompilasi.

TUGAS YANG HARUS DIKERJAKAN:
-----------------------------

1. Implementasi fungsi execute_query(query: Statement) -> Tuple[List[str], List[List[str]]]
   yang:
   - Membuka file CSV
   - Membaca header (nama kolom)
   - Membaca data baris per baris
   - Mengevaluasi WHERE clause (jika ada)
   - Memilih kolom yang diminta
   - Membatasi hasil sesuai LIMIT (jika ada)
   - Mengembalikan tuple (headers, rows)

2. Implementasi fungsi eval(expr: Expr, row: dict) -> bool
   yang mengevaluasi expression dengan data dari baris CSV:
   - BinaryOp dengan AND -> eval kiri AND eval kanan
   - BinaryOp dengan OR -> eval kiri OR eval kanan
   - BinaryOp dengan perbandingan (=, !=, >, <, >=, <=)
     - Untuk string: bandingkan sebagai string
     - Untuk angka: convert dan bandingkan

3. Implementasi helper functions:
   - get_string_value(expr, row) -> Optional[str]
     Ambil nilai string dari expression
   - get_value(expr, row) -> float
     Ambil nilai numerik dari expression

REFERENSI:
----------
Lihat file Rust: src/engine.rs

TIPS:
-----
- Gunakan module 'csv' bawaan Python: csv.DictReader untuk baca CSV
- DictReader otomatis mapping kolom ke nama
- Perhatikan tipe data: string vs angka
- Untuk perbandingan float, gunakan threshold kecil (epsilon)

═══════════════════════════════════════════════════════════════════════════════
"""

import csv
from typing import Tuple, List, Dict, Optional
from ast_nodes import (Statement, Expr, Op, BinaryOp, Literal, 
                       StringLiteral, Number, Identifier, SelectStatement)


def execute_query(query) -> Tuple[List[str], List[List[str]]]:  # query: Statement
    """
    Eksekusi query dan kembalikan hasil.
    
    Args:
        query: Statement AST dari parser
        
    Returns:
        Tuple berisi (headers, rows)
        - headers: List nama kolom
        - rows: List baris data (setiap baris adalah list string)
        
    Raises:
        Exception: Jika ada error saat eksekusi (file tidak ada, dll)
    """
    
    # TODO: Implementasi
    #
    # 1. Buka file CSV
    with open(query.table, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        # 2. Dapatkan header
        all_headers = list(reader.fieldnames) if reader.fieldnames else []
        
        # 3. Tentukan output headers
        if query.columns == ["*"]:
            output_headers = all_headers
        else:
            output_headers = query.columns
        
        # 4. Proses setiap baris
        results = []
        count = 0
        
        for row in reader:
            # 5. Evaluasi WHERE clause
            if query.where_clause:
                if not eval_expr(query.where_clause, row):
                    continue
            
            # 6. Ambil kolom yang diminta
            if query.columns == ["*"]:
                row_data = [row[col] for col in all_headers]
            else:
                row_data = [row.get(col, "") for col in query.columns]
            
            results.append(row_data)
            
            # 7. Cek LIMIT
            count += 1
            if query.limit and count >= query.limit:
                break
        
        return (output_headers, results)


def eval_expr(expr: Expr, row: Dict[str, str]) -> bool:
    """
    Evaluasi expression dengan data baris.
    
    Args:
        expr: Expression dari WHERE clause
        row: Dictionary data baris (nama kolom -> nilai)
        
    Returns:
        True jika baris memenuhi kondisi, False jika tidak
    """
    
    if isinstance(expr, BinaryOp):
        # LOGIKA (AND / OR)
        if expr.op == Op.AND:
            return eval_expr(expr.left, row) and eval_expr(expr.right, row)
        elif expr.op == Op.OR:
            return eval_expr(expr.left, row) or eval_expr(expr.right, row)
        
        # PERBANDINGAN STRING
        elif expr.op in (Op.EQUAL, Op.NOT_EQUAL):
            left_str = get_string_value(expr.left, row)
            right_str = get_string_value(expr.right, row)
            
            if left_str is not None and right_str is not None:
                if expr.op == Op.EQUAL:
                    return left_str == right_str
                else:
                    return left_str != right_str
            
            # Fallback ke numerik
            left_val = get_value(expr.left, row)
            right_val = get_value(expr.right, row)
            
            if expr.op == Op.EQUAL:
                return abs(left_val - right_val) < 1e-9
            else:
                return abs(left_val - right_val) > 1e-9
        
        # PERBANDINGAN NUMERIK
        else:
            left_val = get_value(expr.left, row)
            right_val = get_value(expr.right, row)
            
            if expr.op == Op.GREATER_THAN:
                return left_val > right_val
            elif expr.op == Op.LESS_THAN:
                return left_val < right_val
            elif expr.op == Op.GREATER_THAN_OR_EQ:
                return left_val >= right_val
            elif expr.op == Op.LESS_THAN_OR_EQ:
                return left_val <= right_val
    
    return False


def get_string_value(expr: Expr, row: Dict[str, str]) -> Optional[str]:
    """
    Ambil nilai string dari expression.
    
    Args:
        expr: Expression (Identifier, StringLiteral, atau Literal)
        row: Dictionary data baris
        
    Returns:
        String value, atau None jika tidak bisa diambil
    """
    
    if isinstance(expr, StringLiteral):
        return expr.value
    elif isinstance(expr, Literal):
        return expr.value
    elif isinstance(expr, Identifier):
        return row.get(expr.name)
    
    return None


def get_value(expr: Expr, row: Dict[str, str]) -> float:
    """
    Ambil nilai numerik dari expression.
    
    Args:
        expr: Expression (Number atau Identifier)
        row: Dictionary data baris
        
    Returns:
        Float value (0.0 jika tidak bisa dikonversi)
    """
    
    if isinstance(expr, Number):
        return expr.value
    elif isinstance(expr, Identifier):
        val_str = row.get(expr.name, "0")
        try:
            return float(val_str)
        except ValueError:
            return 0.0
    
    return 0.0
