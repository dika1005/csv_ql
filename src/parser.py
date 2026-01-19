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
from ast_nodes import Statement, SelectStatement, Expr, Op, BinaryOp, Identifier, Number, StringLiteral


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
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]
    
    def advance(self) -> None:
        """Majukan posisi ke token berikutnya."""
        if self.pos < len(self.tokens):
            self.pos += 1
    
    def match_token(self, expected: TokenType) -> bool:
        """
        Cek apakah token saat ini sesuai dengan yang diharapkan.
        Jika cocok, maju ke token berikutnya dan return True.
        
        Args:
            expected: Tipe token yang diharapkan
            
        Returns:
            True jika cocok, False jika tidak
        """
        token = self.current()
        if token is not None and token.type == expected:
            self.advance()
            return True
        return False
    
    # ─────────────────────────────────────────────────────────────────────────
    # PARSING METHODS
    # ─────────────────────────────────────────────────────────────────────────
    
    def parse(self) -> Statement:
        """
        Parse query menjadi AST.
        
        Returns:
            Statement AST
            
        Raises:
            Exception: Jika parsing gagal
        """
        return self.parse_select()
    
    def parse_select(self) -> Statement:
        """
        Parse statement SELECT.
        
        Format: SELECT columns FROM table [WHERE expr] [LIMIT number]
        """
        # 1. Cek & makan token SELECT
        if not self.match_token(TokenType.SELECT):
            raise Exception("Expected SELECT keyword")
        
        # 2. Parse columns
        columns = self.parse_columns()
        
        # 3. Cek & makan token FROM
        if not self.match_token(TokenType.FROM):
            raise Exception("Expected FROM keyword")
        
        # 4. Ambil nama table (IDENTIFIER)
        token = self.current()
        if token is None or token.type != TokenType.IDENTIFIER:
            raise Exception("Expected table name (identifier)")
        table = token.value
        self.advance()
        
        # 5. Cek WHERE (opsional) -> parse expression
        where_clause: Optional[Expr] = None
        if self.match_token(TokenType.WHERE):
            where_clause = self.parse_expression()
        
        # 6. Cek LIMIT (opsional) -> ambil angka
        limit: Optional[int] = None
        if self.match_token(TokenType.LIMIT):
            token = self.current()
            if token is None or token.type != TokenType.NUMBER:
                raise Exception("Expected number after LIMIT")
            limit = int(token.value)
            self.advance()
        
        # 7. Return Statement
        return SelectStatement(
            columns=columns,
            table=table,
            where_clause=where_clause,
            limit=limit
        )
    
    def parse_columns(self) -> List[str]:
        """
        Parse daftar kolom.
        
        Format: column (',' column)* | '*'
        """
        columns: List[str] = []
        
        # Loop: ambil IDENTIFIER atau STAR
        while True:
            token = self.current()
            
            if token is None:
                break
            
            # Cek STAR (*)
            if token.type == TokenType.STAR:
                columns.append("*")
                self.advance()
            # Cek IDENTIFIER
            elif token.type == TokenType.IDENTIFIER:
                columns.append(token.value)
                self.advance()
            else:
                break
            
            # Jika ada COMMA, lanjutkan loop
            if not self.match_token(TokenType.COMMA):
                break
        
        if len(columns) == 0:
            raise Exception("Expected at least one column")
        
        return columns
    
    def parse_expression(self) -> Expr:
        """Parse ekspresi (entry point untuk WHERE clause)."""
        return self.parse_logic_or()
    
    def parse_logic_or(self) -> Expr:
        """
        Parse operasi OR (precedence terendah).
        
        Format: and_expr (OR and_expr)*
        """
        left = self.parse_logic_and()
        
        while self.match_token(TokenType.OR):
            right = self.parse_logic_and()
            left = BinaryOp(left=left, op=Op.OR, right=right)
        
        return left
    
    def parse_logic_and(self) -> Expr:
        """
        Parse operasi AND.
        
        Format: cmp_expr (AND cmp_expr)*
        """
        left = self.parse_comparison()
        
        while self.match_token(TokenType.AND):
            right = self.parse_comparison()
            left = BinaryOp(left=left, op=Op.AND, right=right)
        
        return left
    
    def parse_comparison(self) -> Expr:
        """
        Parse operasi perbandingan.
        
        Format: leaf (op leaf)?
        """
        left = self.parse_leaf()
        
        # Cek operator perbandingan
        token = self.current()
        if token is None:
            return left
        
        op: Optional[Op] = None
        
        if token.type == TokenType.EQUAL:
            op = Op.EQUAL
        elif token.type == TokenType.NOT_EQUAL:
            op = Op.NOT_EQUAL
        elif token.type == TokenType.GREATER_THAN:
            op = Op.GREATER_THAN
        elif token.type == TokenType.LESS_THAN:
            op = Op.LESS_THAN
        elif token.type == TokenType.GREATER_THAN_OR_EQ:
            op = Op.GREATER_THAN_OR_EQ
        elif token.type == TokenType.LESS_THAN_OR_EQ:
            op = Op.LESS_THAN_OR_EQ
        
        # Jika ada operator, parse right operand
        if op is not None:
            self.advance()  # Makan operator
            right = self.parse_leaf()
            return BinaryOp(left=left, op=op, right=right)
        
        return left
    
    def parse_leaf(self) -> Expr:
        """
        Parse leaf expression (identifier, number, atau string literal).
        """
        token = self.current()
        
        if token is None:
            raise Exception("Unexpected end of input")
        
        # Jika IDENTIFIER -> return Identifier
        if token.type == TokenType.IDENTIFIER:
            self.advance()
            return Identifier(name=token.value)
        
        # Jika NUMBER -> return Number
        if token.type == TokenType.NUMBER:
            self.advance()
            return Number(value=token.value)
        
        # Jika STRING_LITERAL -> return StringLiteral
        if token.type == TokenType.STRING_LITERAL:
            self.advance()
            return StringLiteral(value=token.value)
        
        raise Exception(f"Unexpected token: {token}")


# ═══════════════════════════════════════════════════════════════════════════════
# CONTOH PENGGUNAAN (untuk testing)
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    from lexer import Lexer
    
    # Test cases
    queries = [
        "SELECT * FROM data.csv",
        "SELECT nama, nilai FROM data.csv",
        'SELECT nama FROM data.csv WHERE status = "Lulus"',
        "SELECT * FROM data.csv WHERE nilai > 80",
        "SELECT * FROM data.csv WHERE nilai >= 3.0 AND semester = 5",
        "SELECT * FROM data.csv WHERE status = \"Lulus\" OR nilai_huruf = \"A\"",
        "SELECT nama, nilai FROM data.csv LIMIT 5",
        'SELECT * FROM data.csv WHERE status = "Tidak Lulus" LIMIT 10',
    ]
    
    print("=" * 70)
    print("                    PARSER TEST")
    print("=" * 70)
    
    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 50)
        
        try:
            # Tokenize
            lexer = Lexer(query)
            tokens = lexer.tokenize()
            
            # Parse
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Print AST
            print(f"  Columns: {ast.columns}")
            print(f"  Table: {ast.table}")
            print(f"  Where: {ast.where_clause}")
            print(f"  Limit: {ast.limit}")
            print("  ✅ Parsing berhasil!")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("                    TEST SELESAI")
    print("=" * 70)
