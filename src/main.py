"""
main.py - Entry Point untuk CSV_QL

Modul ini adalah titik masuk utama program CSV_QL.
Mendukung dua mode:
    1. Direct mode: csv_ql "SELECT * FROM data.csv"
    2. Interactive REPL mode: csv_ql (tanpa argumen)
"""

import sys
from lexer import Lexer
# TODO: Uncomment import berikut setelah modul-modul tersebut selesai diimplementasikan
# from parser import Parser
# from semantic import analyze
# from ir import ast_to_ir, print_query_plan
# from engine import execute_query
from dfa import DFATracker


# ═══════════════════════════════════════════════════════════════════════════════
# WARNA TERMINAL (ANSI Escape Codes)
# ═══════════════════════════════════════════════════════════════════════════════

RESET = "\x1b[0m"
BOLD = "\x1b[1m"
CYAN = "\x1b[36m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
RED = "\x1b[31m"
WHITE = "\x1b[37m"
MAGENTA = "\x1b[35m"
DIM = "\x1b[2m"


# ═══════════════════════════════════════════════════════════════════════════════
# TAMPILAN UI
# ═══════════════════════════════════════════════════════════════════════════════

def print_banner():
    """Tampilkan banner program."""
    print(f"\n{CYAN}{BOLD}")
    print("  ╔═══════════════════════════════════════════════════╗")
    print("  ║         CSV_QL - Mini SQL untuk File CSV          ║")
    print("  ╚═══════════════════════════════════════════════════╝")
    print(f"{RESET}")


def print_help():
    """Tampilkan bantuan penggunaan."""
    print(f"""
{YELLOW}{BOLD}═══════════════════════════════════════════════════════════════════════════════
                            📚 BANTUAN CSV_QL
═══════════════════════════════════════════════════════════════════════════════{RESET}

{CYAN}{BOLD}SYNTAX DASAR:{RESET}
  SELECT <kolom> FROM <file.csv> [WHERE <kondisi>] [LIMIT n]

{CYAN}{BOLD}CONTOH QUERY:{RESET}

  {GREEN}1. Ambil semua data:{RESET}
     SELECT * FROM data.csv

  {GREEN}2. Pilih kolom tertentu:{RESET}
     SELECT nama, umur FROM data.csv

  {GREEN}3. Filter dengan WHERE:{RESET}
     SELECT * FROM data.csv WHERE umur > 20
     SELECT * FROM data.csv WHERE kota = "Jakarta"

  {GREEN}4. Kombinasi kondisi (AND/OR):{RESET}
     SELECT * FROM data.csv WHERE umur > 20 AND umur < 30
     SELECT * FROM data.csv WHERE kota = "Jakarta" OR kota = "Bandung"

  {GREEN}5. Batasi hasil dengan LIMIT:{RESET}
     SELECT * FROM data.csv LIMIT 5
     SELECT nama FROM data.csv WHERE umur > 25 LIMIT 10

{CYAN}{BOLD}OPERATOR YANG DIDUKUNG:{RESET}
  =   (sama dengan)        !=  (tidak sama)
  >   (lebih besar)        <   (lebih kecil)
  >=  (lebih besar/sama)   <=  (lebih kecil/sama)
  AND (dan)                OR  (atau)

{CYAN}{BOLD}PERINTAH REPL:{RESET}
  {MAGENTA}help{RESET}   - Tampilkan bantuan ini
  {MAGENTA}clear{RESET}  - Bersihkan layar  
  {MAGENTA}dfa{RESET}    - Tampilkan diagram DFA lexer
  {MAGENTA}exit{RESET}   - Keluar program

{YELLOW}═══════════════════════════════════════════════════════════════════════════════{RESET}
""")


# ═══════════════════════════════════════════════════════════════════════════════
# EKSEKUSI QUERY - Pipeline Kompilasi
# ═══════════════════════════════════════════════════════════════════════════════

def execute_sql(input_query: str, verbose: bool = False):
    """
    Eksekusi query SQL melalui pipeline kompilasi.
    
    Pipeline:
        1. Lexical Analysis (String → Tokens)
        2. Syntax Analysis/Parsing (Tokens → AST)
        3. Semantic Analysis (Validasi AST)
        4. IR Generation (AST → Query Plan)
        5. Execution (Jalankan Query Plan)
    
    Args:
        input_query: Query SQL yang akan dieksekusi
        verbose: Jika True, tampilkan detail setiap tahap
    """
    print(f"\n  {DIM}Query: {input_query}{RESET}")
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ TAHAP 1: LEXICAL ANALYSIS (String → Tokens)                            │
    # └─────────────────────────────────────────────────────────────────────────┘
    lexer = Lexer(input_query)
    tokens = lexer.tokenize()
    
    if verbose:
        print(f"\n  {CYAN}[1] LEXICAL ANALYSIS{RESET}")
        print(f"  Tokens: {tokens}")
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ TAHAP 2: SYNTAX ANALYSIS / PARSING (Tokens → AST)                      │
    # └─────────────────────────────────────────────────────────────────────────┘
    parser = Parser(tokens)
    try:
        ast = parser.parse()
    except Exception as e:
        print(f"  {RED}❌ Parse Error: {e}{RESET}\n")
        return
    
    if verbose:
        print(f"\n  {CYAN}[2] SYNTAX ANALYSIS{RESET}")
        print(f"  AST: {ast}")
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ TAHAP 3: SEMANTIC ANALYSIS (Validasi AST)                              │
    # └─────────────────────────────────────────────────────────────────────────┘
    try:
        result = analyze(ast)
        
        if verbose:
            print(f"\n  {CYAN}[3] SEMANTIC ANALYSIS{RESET}")
        
        # Tampilkan warning jika ada
        for warn in result.warnings:
            print(f"  {YELLOW}⚠️ Warning: {warn}{RESET}")
        
        # Stop jika ada error semantik
        if not result.valid:
            for err in result.errors:
                print(f"  {RED}❌ Semantic Error: {err}{RESET}")
            return
        
        if verbose:
            print("  ✓ Validasi OK")
            
    except Exception as e:
        print(f"  {RED}❌ Semantic Error: {e}{RESET}\n")
        return
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ TAHAP 4: IR GENERATION (AST → Query Plan)                              │
    # └─────────────────────────────────────────────────────────────────────────┘
    query_plan = ast_to_ir(ast)
    
    if verbose:
        print(f"\n  {CYAN}[4] IR GENERATION{RESET}")
        print_query_plan(query_plan)
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ TAHAP 5: EXECUTION (Jalankan Query Plan)                               │
    # └─────────────────────────────────────────────────────────────────────────┘
    if verbose:
        print(f"\n  {CYAN}[5] EXECUTION{RESET}")
    
    try:
        headers, rows = execute_query(ast)
        
        if not rows:
            print(f"  {YELLOW}⚠️ Tidak ada data yang cocok.{RESET}\n")
        else:
            print_table(headers, rows)
            
    except Exception as e:
        print(f"  {RED}❌ Runtime Error: {e}{RESET}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# TAMPILKAN TABEL
# ═══════════════════════════════════════════════════════════════════════════════

def print_table(headers: list[str], rows: list[list[str]]):
    """
    Tampilkan hasil query dalam format tabel.
    
    Args:
        headers: List nama kolom
        rows: List baris data
    """
    # Hitung lebar kolom
    widths = []
    for i, h in enumerate(headers):
        max_data = max((len(row[i]) if i < len(row) else 0 for row in rows), default=0)
        widths.append(max(len(h), max_data) + 2)
    
    # Fungsi helper untuk buat garis
    def line(left: str, mid: str, right: str):
        print(f"  {CYAN}{left}", end="")
        for i, w in enumerate(widths):
            print("─" * w, end="")
            print(mid if i < len(widths) - 1 else right, end="")
        print(f"{RESET}")
    
    # Print tabel
    line("╭", "┬", "╮")
    
    # Header
    print(f"  {CYAN}│{RESET}", end="")
    for i, h in enumerate(headers):
        print(f"{YELLOW}{BOLD} {h:^{widths[i]-1}}{RESET}{CYAN}│{RESET}", end="")
    print()
    
    line("├", "┼", "┤")
    
    # Data rows
    for row in rows:
        print(f"  {CYAN}│{RESET}", end="")
        for i, cell in enumerate(row):
            if i < len(widths):
                print(f"{WHITE} {cell:^{widths[i]-1}}{RESET}{CYAN}│{RESET}", end="")
        print()
    
    line("╰", "┴", "╯")
    print(f"  {GREEN}✅ {len(rows)} baris ditemukan{RESET}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN - Entry Point
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Fungsi utama program."""
    args = sys.argv[1:]
    
    # Cek flag --verbose atau -v
    verbose = "--verbose" in args or "-v" in args
    
    # Hapus flag dari argumen
    query_args = [a for a in args if a not in ("--verbose", "-v")]
    
    # Mode 1: Direct query dari command line
    # Contoh: python main.py "SELECT * FROM data.csv"
    if query_args:
        query = " ".join(query_args)
        print_banner()
        execute_sql(query, verbose)
        return
    
    # Mode 2: Interactive REPL
    print_banner()
    print(f"  Ketik {MAGENTA}help{RESET} untuk bantuan, {MAGENTA}exit{RESET} untuk keluar.")
    print(f"  Tambahkan {MAGENTA}--verbose{RESET} di akhir query untuk lihat detail kompilasi.\n")
    
    while True:
        try:
            # Tampilkan prompt
            user_input = input(f"  {CYAN}{BOLD}csv_ql>{RESET} ")
        except EOFError:
            break
        except KeyboardInterrupt:
            print()
            continue
        
        user_input = user_input.strip()
        
        # Cek verbose mode
        verbose_mode = user_input.endswith("--verbose") or user_input.endswith("-v")
        clean_input = user_input.replace("--verbose", "").replace("-v", "").strip()
        
        # Proses perintah
        cmd = clean_input.lower()
        
        if cmd == "":
            continue
        elif cmd in ("exit", "quit", "q"):
            print(f"\n  {GREEN}👋 Sampai jumpa!{RESET}\n")
            break
        elif cmd in ("help", "?"):
            print_help()
        elif cmd in ("clear", "cls"):
            print("\x1b[2J\x1b[H", end="")
            print_banner()
        elif cmd == "dfa":
            DFATracker.print_dfa_diagram()
        else:
            execute_sql(clean_input, verbose_mode)


if __name__ == "__main__":
    main()
