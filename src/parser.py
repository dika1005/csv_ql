"""
parser.py - Parser (Syntax Analyzer) untuk CSV_QL

═══════════════════════════════════════════════════════════════════════════════
                        📋 INSTRUKSI PENGISIAN
═══════════════════════════════════════════════════════════════════════════════

Modul ini mengubah daftar token menjadi AST (Abstract Syntax Tree).
Proses ini disebut "parsing" atau "syntax analysis".

TUGAS YANG HARUS DIKERJAKAN:
-----------------------------

1. Buat class Parser dengan method:
   - __init__(self, tokens: list[Token]) -> inisialisasi dengan list token
   - current(self) -> Optional[Token]    -> lihat token saat ini
   - advance(self) -> None               -> maju ke token berikutnya
   - match_token(self, expected: TokenType) -> bool -> cek & makan token
   - parse(self) -> Statement            -> parse query menjadi AST

2. Implementasi parsing untuk:
   - parse_select() -> parse statement SELECT
   - parse_columns() -> parse daftar kolom
   - parse_expression() -> parse ekspresi WHERE
   - parse_logic_or() -> parse operasi OR
   - parse_logic_and() -> parse operasi AND
   - parse_comparison() -> parse operasi perbandingan (=, >, <, dll)
   - parse_leaf() -> parse identifier, number, atau string literal

GRAMMAR (dalam pseudo-BNF):
---------------------------
query       ::= SELECT columns FROM table [WHERE expr] [LIMIT number]
columns     ::= column (',' column)* | '*'
column      ::= IDENTIFIER
table       ::= IDENTIFIER
expr        ::= and_expr (OR and_expr)*
and_expr    ::= cmp_expr (AND cmp_expr)*
cmp_expr    ::= leaf (op leaf)?
op          ::= '=' | '!=' | '>' | '<' | '>=' | '<='
leaf        ::= IDENTIFIER | NUMBER | STRING_LITERAL

REFERENSI:
----------
Lihat file Rust: src/parser.rs

TIPS:
-----
- Gunakan recursive descent parsing (setiap level grammar = satu fungsi)
- Raise exception dengan pesan error yang jelas jika parsing gagal
- Jangan lupa advance() setelah mengkonsumsi token

═══════════════════════════════════════════════════════════════════════════════
"""

from typing import Optional, List
from tokens import Token, TokenType
# from ast_nodes import Statement, Expr, Op  # Uncomment setelah ast_nodes.py selesai


class Parser:
    """
    Parser untuk CSV_QL.
    
    Mengubah list token menjadi AST dengan metode recursive descent.
    """
    
    def __init__(self, tokens: list[Token]):
        """
        Inisialisasi parser.
        
        Args:
            tokens: List token dari lexer
        """
        self.tokens = tokens
        self.pos = 0
    
    # ─────────────────────────────────────────────────────────────────────────
    # HELPER METHODS
    # ─────────────────────────────────────────────────────────────────────────
    
    def current(self) -> Optional[Token]:
        """Dapatkan token saat ini tanpa memajukan posisi."""
        # TODO: Implementasi
        pass
    
    def advance(self) -> None:
        """Majukan posisi ke token berikutnya."""
        # TODO: Implementasi
        pass
    
    def match_token(self, expected: TokenType) -> bool:
        """
        Cek apakah token saat ini sesuai dengan yang diharapkan.
        Jika cocok, maju ke token berikutnya dan return True.
        
        Args:
            expected: Tipe token yang diharapkan
            
        Returns:
            True jika cocok, False jika tidak
        """
        # TODO: Implementasi
        pass
    
    # ─────────────────────────────────────────────────────────────────────────
    # PARSING METHODS
    # ─────────────────────────────────────────────────────────────────────────
    
    def parse(self):  # -> Statement
        """
        Parse query menjadi AST.
        
        Returns:
            Statement AST
            
        Raises:
            Exception: Jika parsing gagal
        """
        # TODO: Implementasi - panggil parse_select()
        pass
    
    def parse_select(self):  # -> Statement
        """
        Parse statement SELECT.
        
        Format: SELECT columns FROM table [WHERE expr] [LIMIT number]
        """
        # TODO: Implementasi
        # 1. Cek & makan token SELECT
        # 2. Parse columns
        # 3. Cek & makan token FROM
        # 4. Ambil nama table (IDENTIFIER)
        # 5. Cek WHERE (opsional) -> parse expression
        # 6. Cek LIMIT (opsional) -> ambil angka
        # 7. Return Statement
        pass
    
    def parse_columns(self) -> List[str]:
        """
        Parse daftar kolom.
        
        Format: column (',' column)* | '*'
        """
        # TODO: Implementasi
        # - Loop: ambil IDENTIFIER atau STAR
        # - Jika ada COMMA, lanjutkan loop
        # - Jika tidak ada COMMA, keluar dari loop
        pass
    
    def parse_expression(self):  # -> Expr
        """Parse ekspresi (entry point untuk WHERE clause)."""
        # TODO: Implementasi - panggil parse_logic_or()
        pass
    
    def parse_logic_or(self):  # -> Expr
        """
        Parse operasi OR (precedence terendah).
        
        Format: and_expr (OR and_expr)*
        """
        # TODO: Implementasi
        pass
    
    def parse_logic_and(self):  # -> Expr
        """
        Parse operasi AND.
        
        Format: cmp_expr (AND cmp_expr)*
        """
        # TODO: Implementasi
        pass
    
    def parse_comparison(self):  # -> Expr
        """
        Parse operasi perbandingan.
        
        Format: leaf (op leaf)?
        """
        # TODO: Implementasi
        pass
    
    def parse_leaf(self):  # -> Expr
        """
        Parse leaf expression (identifier, number, atau string literal).
        """
        # TODO: Implementasi
        # - Cek tipe token saat ini
        # - Jika IDENTIFIER -> return Expr.Identifier
        # - Jika NUMBER -> return Expr.Number
        # - Jika STRING_LITERAL -> return Expr.StringLiteral
        # - Else -> raise error
        pass
