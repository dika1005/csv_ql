"""
ir.py - Intermediate Representation (Query Plan) untuk CSV_QL

═══════════════════════════════════════════════════════════════════════════════
                        📋 INSTRUKSI PENGISIAN
═══════════════════════════════════════════════════════════════════════════════

Modul ini mengubah AST menjadi Query Plan (IR - Intermediate Representation).
Query Plan adalah representasi langkah-langkah eksekusi yang akan dilakukan.

Contoh Query Plan untuk "SELECT nama FROM data.csv WHERE umur > 20 LIMIT 5":
    1. SCAN: data.csv
    2. FILTER: umur > 20
    3. PROJECT: nama
    4. LIMIT: 5

TUGAS YANG HARUS DIKERJAKAN:
-----------------------------

1. Buat enum PlanStep dengan variant:
   - Scan: membaca file CSV (field: table)
   - Filter: filter baris dengan kondisi (field: condition)
   - Project: pilih kolom tertentu (field: columns)
   - Limit: batasi jumlah hasil (field: count)

2. Buat dataclass QueryPlan dengan field:
   - steps: list[PlanStep]

3. Implementasi fungsi ast_to_ir(ast: Statement) -> QueryPlan
   yang mengubah AST menjadi urutan langkah:
   - Step 1: SCAN (selalu ada, dari nama table)
   - Step 2: FILTER (jika ada WHERE clause)
   - Step 3: PROJECT (dari daftar kolom)
   - Step 4: LIMIT (jika ada LIMIT)

4. Implementasi fungsi print_query_plan(plan: QueryPlan)
   untuk menampilkan query plan dengan format yang bagus

5. Implementasi helper function expr_to_string(expr: Expr) -> str
   untuk mengubah expression menjadi string (untuk tampilan FILTER)

REFERENSI:
----------
Lihat file Rust: src/ir.rs

TIPS:
-----
- Urutan step mempengaruhi hasil! (SCAN -> FILTER -> PROJECT -> LIMIT)
- Untuk print_query_plan, bisa gunakan emoji untuk visualisasi

═══════════════════════════════════════════════════════════════════════════════
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Union
# from ast_nodes import Statement, Expr, Op  # Uncomment setelah ast_nodes.py selesai


# ═══════════════════════════════════════════════════════════════════════════════
# PLAN STEP TYPES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ScanStep:
    """Langkah 1: Baca file CSV."""
    table: str


@dataclass
class FilterStep:
    """Langkah 2: Filter baris berdasarkan kondisi."""
    condition: str


@dataclass
class ProjectStep:
    """Langkah 3: Pilih kolom tertentu."""
    columns: List[str]


@dataclass
class LimitStep:
    """Langkah 4: Batasi jumlah hasil."""
    count: int


# Union type untuk semua jenis step
PlanStep = Union[ScanStep, FilterStep, ProjectStep, LimitStep]


@dataclass
class QueryPlan:
    """Query Plan - representasi langkah eksekusi."""
    steps: List[PlanStep]


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def ast_to_ir(ast) -> QueryPlan:  # ast: Statement
    """
    Konversi AST ke Query Plan (IR).
    
    Args:
        ast: Statement AST dari parser
        
    Returns:
        QueryPlan dengan urutan langkah eksekusi
    """
    steps = []
    
    # TODO: Implementasi
    #
    # 1. SCAN - selalu ada
    # steps.append(ScanStep(table=ast.table))
    #
    # 2. FILTER - jika ada WHERE
    # if ast.where_clause:
    #     steps.append(FilterStep(condition=expr_to_string(ast.where_clause)))
    #
    # 3. PROJECT - pilih kolom
    # steps.append(ProjectStep(columns=ast.columns))
    #
    # 4. LIMIT - jika ada
    # if ast.limit:
    #     steps.append(LimitStep(count=ast.limit))
    #
    # return QueryPlan(steps=steps)
    
    return QueryPlan(steps=[])  # Hapus setelah implementasi


def print_query_plan(plan: QueryPlan) -> None:
    """
    Tampilkan Query Plan dengan format yang bagus.
    
    Args:
        plan: QueryPlan yang akan ditampilkan
    """
    print("\n  📋 QUERY PLAN (IR):")
    print("  ┌─────────────────────────────────────────────────┐")
    
    # TODO: Implementasi
    #
    # for i, step in enumerate(plan.steps):
    #     if isinstance(step, ScanStep):
    #         icon, desc = "📂", f"SCAN: {step.table}"
    #     elif isinstance(step, FilterStep):
    #         icon, desc = "🔍", f"FILTER: {step.condition}"
    #     elif isinstance(step, ProjectStep):
    #         icon, desc = "📊", f"PROJECT: {', '.join(step.columns)}"
    #     elif isinstance(step, LimitStep):
    #         icon, desc = "✂️", f"LIMIT: {step.count}"
    #     
    #     # Print step dengan padding
    #     padding = " " * max(0, 44 - len(desc))
    #     print(f"  │  {i + 1}. {icon} {desc}{padding}│")
    #     
    #     # Arrow untuk step berikutnya
    #     if i < len(plan.steps) - 1:
    #         print("  │       ↓                                        │")
    
    print("  └─────────────────────────────────────────────────┘")


def expr_to_string(expr) -> str:  # expr: Expr
    """
    Konversi Expr ke string untuk tampilan.
    
    Args:
        expr: Expression yang akan dikonversi
        
    Returns:
        String representasi dari expression
    """
    # TODO: Implementasi
    #
    # if isinstance(expr, Number):
    #     return str(expr.value)
    # elif isinstance(expr, Identifier):
    #     return expr.name
    # elif isinstance(expr, StringLiteral):
    #     return f'"{expr.value}"'
    # elif isinstance(expr, BinaryOp):
    #     op_map = {
    #         Op.EQUAL: "=",
    #         Op.NOT_EQUAL: "!=",
    #         Op.GREATER_THAN: ">",
    #         Op.LESS_THAN: "<",
    #         Op.GREATER_THAN_OR_EQ: ">=",
    #         Op.LESS_THAN_OR_EQ: "<=",
    #         Op.AND: "AND",
    #         Op.OR: "OR",
    #     }
    #     left_str = expr_to_string(expr.left)
    #     right_str = expr_to_string(expr.right)
    #     op_str = op_map.get(expr.op, "?")
    #     return f"{left_str} {op_str} {right_str}"
    
    return ""  # Hapus setelah implementasi
