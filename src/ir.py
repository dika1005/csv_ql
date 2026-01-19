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
from ast_nodes import Statement, Expr, Op, BinaryOp, Identifier, Number, StringLiteral


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

def ast_to_ir(ast: Statement) -> QueryPlan:
    """
    Konversi AST ke Query Plan (IR).
    
    Args:
        ast: Statement AST dari parser
        
    Returns:
        QueryPlan dengan urutan langkah eksekusi
    """
    steps: List[PlanStep] = []
    
    # 1. SCAN - selalu ada (langkah pertama: baca file CSV)
    steps.append(ScanStep(table=ast.table))
    
    # 2. FILTER - jika ada WHERE clause (filter sebelum project untuk efisiensi)
    if ast.where_clause is not None:
        steps.append(FilterStep(condition=expr_to_string(ast.where_clause)))
    
    # 3. PROJECT - pilih kolom yang diminta
    steps.append(ProjectStep(columns=ast.columns))
    
    # 4. LIMIT - jika ada batasan jumlah hasil
    if ast.limit is not None:
        steps.append(LimitStep(count=ast.limit))
    
    return QueryPlan(steps=steps)


def print_query_plan(plan: QueryPlan) -> None:
    """
    Tampilkan Query Plan dengan format yang bagus.
    
    Args:
        plan: QueryPlan yang akan ditampilkan
    """
    print("\n  📋 QUERY PLAN (IR):")
    print("  ┌─────────────────────────────────────────────────┐")
    
    for i, step in enumerate(plan.steps):
        # Tentukan icon dan deskripsi berdasarkan tipe step
        if isinstance(step, ScanStep):
            icon, desc = "📂", f"SCAN: {step.table}"
        elif isinstance(step, FilterStep):
            icon, desc = "🔍", f"FILTER: {step.condition}"
        elif isinstance(step, ProjectStep):
            icon, desc = "📊", f"PROJECT: {', '.join(step.columns)}"
        elif isinstance(step, LimitStep):
            icon, desc = "✂️", f"LIMIT: {step.count}"
        else:
            icon, desc = "❓", "UNKNOWN"
        
        # Print step dengan padding agar rapi
        padding = " " * max(0, 44 - len(desc))
        print(f"  │  {i + 1}. {icon} {desc}{padding}│")
        
        # Arrow untuk step berikutnya (kecuali step terakhir)
        if i < len(plan.steps) - 1:
            print("  │       ↓                                        │")
    
    print("  └─────────────────────────────────────────────────┘")


def expr_to_string(expr: Expr) -> str:
    """
    Konversi Expr ke string untuk tampilan.
    
    Args:
        expr: Expression yang akan dikonversi
        
    Returns:
        String representasi dari expression
    """
    # Mapping operator ke simbol string
    op_map = {
        Op.EQUAL: "=",
        Op.NOT_EQUAL: "!=",
        Op.GREATER_THAN: ">",
        Op.LESS_THAN: "<",
        Op.GREATER_THAN_OR_EQ: ">=",
        Op.LESS_THAN_OR_EQ: "<=",
        Op.AND: "AND",
        Op.OR: "OR",
    }
    
    # Handle berdasarkan tipe expression
    if isinstance(expr, Number):
        # Angka: tampilkan sebagai string
        # Jika bilangan bulat, hilangkan .0
        if expr.value == int(expr.value):
            return str(int(expr.value))
        return str(expr.value)
    
    elif isinstance(expr, Identifier):
        # Identifier: tampilkan nama kolom
        return expr.name
    
    elif isinstance(expr, StringLiteral):
        # String literal: tampilkan dengan tanda kutip
        return f'"{expr.value}"'
    
    elif isinstance(expr, BinaryOp):
        # Binary operation: rekursif ke kiri dan kanan
        left_str = expr_to_string(expr.left)
        right_str = expr_to_string(expr.right)
        op_str = op_map.get(expr.op, "?")
        
        # Tambah kurung untuk AND/OR agar jelas precedence
        if expr.op in (Op.AND, Op.OR):
            return f"({left_str} {op_str} {right_str})"
        return f"{left_str} {op_str} {right_str}"
    
    return ""  # Fallback untuk tipe yang tidak dikenal


# ═══════════════════════════════════════════════════════════════════════════════
# CONTOH PENGGUNAAN (untuk testing)
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    from lexer import Lexer
    from parser import Parser
    
    # Test cases
    queries = [
        "SELECT * FROM data.csv",
        "SELECT nama, nilai FROM data.csv",
        'SELECT nama FROM data.csv WHERE status = "Lulus"',
        "SELECT * FROM data.csv WHERE nilai > 80",
        "SELECT * FROM data.csv WHERE nilai >= 3.0 AND semester = 5",
        'SELECT * FROM data.csv WHERE status = "Lulus" OR nilai_huruf = "A"',
        "SELECT nama, nilai FROM data.csv LIMIT 5",
        'SELECT * FROM data.csv WHERE status = "Tidak Lulus" LIMIT 10',
    ]
    
    print("=" * 70)
    print("                    IR (QUERY PLAN) TEST")
    print("=" * 70)
    
    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 55)
        
        try:
            # Tokenize
            lexer = Lexer(query)
            tokens = lexer.tokenize()
            
            # Parse
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Convert to IR
            ir = ast_to_ir(ast)
            
            # Print Query Plan
            print_query_plan(ir)
            print("  ✅ Konversi ke IR berhasil!")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("                    TEST SELESAI")
    print("=" * 70)
