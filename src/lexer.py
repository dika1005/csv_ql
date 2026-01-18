"""
lexer.py - Lexical Analyzer untuk CSV_QL

Modul ini mengubah string input query menjadi daftar token.
Proses ini disebut "tokenization" atau "lexical analysis".

Contoh:
    Input:  "SELECT nama FROM data.csv"
    Output: [Token(SELECT), Token(IDENTIFIER, "nama"), Token(FROM), Token(IDENTIFIER, "data.csv")]
"""

from typing import Optional, Iterator
from tokens import Token, TokenType, get_keyword_token


class Lexer:
    """
    Lexer (Lexical Analyzer) untuk CSV_QL.
    
    Mengubah string input menjadi tokens dengan metode next_token().
    Bisa juga digunakan sebagai iterator untuk mendapatkan semua tokens.
    """
    
    def __init__(self, input_text: str):
        """
        Inisialisasi lexer dengan input string.
        
        Args:
            input_text: Query string yang akan di-tokenize
        """
        self.input = input_text
        self.pos = 0  # Posisi karakter saat ini
    
    def peek(self) -> Optional[str]:
        """
        Lihat karakter saat ini tanpa memajukan posisi.
        
        Returns:
            Karakter saat ini, atau None jika sudah di akhir input
        """
        if self.pos >= len(self.input):
            return None
        return self.input[self.pos]
    
    def advance(self) -> Optional[str]:
        """
        Ambil karakter saat ini dan majukan posisi.
        
        Returns:
            Karakter saat ini, atau None jika sudah di akhir input
        """
        if self.pos >= len(self.input):
            return None
        char = self.input[self.pos]
        self.pos += 1
        return char
    
    def skip_whitespace(self) -> None:
        """Lewati semua whitespace (spasi, tab, newline)."""
        while self.peek() is not None and self.peek().isspace():
            self.advance()
    
    def scan_identifier(self) -> Token:
        """
        Scan identifier atau keyword.
        
        Identifier bisa berisi huruf, angka, underscore, dan titik.
        Jika identifier adalah keyword (SELECT, FROM, dll), kembalikan token keyword.
        
        Returns:
            Token IDENTIFIER atau token keyword
        """
        text = ""
        
        while self.peek() is not None:
            c = self.peek()
            # Izinkan alphanumeric, underscore, dan titik (untuk nama file)
            if c.isalnum() or c == '_' or c == '.':
                text += c
                self.advance()
            else:
                break
        
        # Cek apakah ini keyword
        keyword_token = get_keyword_token(text)
        if keyword_token:
            return keyword_token
        
        # Bukan keyword, jadi identifier biasa
        return Token(TokenType.IDENTIFIER, text)
    
    def scan_number(self) -> Token:
        """
        Scan angka (integer atau float).
        
        Returns:
            Token NUMBER dengan nilai float
        """
        text = ""
        
        while self.peek() is not None:
            c = self.peek()
            if c.isdigit() or c == '.':
                text += c
                self.advance()
            else:
                break
        
        # Parse ke float
        try:
            value = float(text)
        except ValueError:
            value = 0.0
        
        return Token(TokenType.NUMBER, value)
    
    def scan_string(self) -> Token:
        """
        Scan string literal (dalam tanda kutip " atau ').
        
        Returns:
            Token STRING_LITERAL dengan nilai string
        """
        quote = self.advance()  # Makan tanda kutip pembuka (" atau ')
        text = ""
        
        while self.peek() is not None:
            c = self.peek()
            if c == quote:
                self.advance()  # Makan tanda kutip penutup
                break
            text += c
            self.advance()
        
        return Token(TokenType.STRING_LITERAL, text)
    
    def scan_symbol(self) -> Optional[Token]:
        """
        Scan simbol/operator.
        
        Returns:
            Token operator, atau None jika simbol tidak dikenal
        """
        c = self.advance()
        
        if c == '*':
            return Token(TokenType.STAR)
        elif c == ',':
            return Token(TokenType.COMMA)
        elif c == '=':
            return Token(TokenType.EQUAL)
        elif c == '!':
            # Cek apakah != 
            if self.peek() == '=':
                self.advance()
                return Token(TokenType.NOT_EQUAL)
            return None
        elif c == '>':
            # Cek apakah >=
            if self.peek() == '=':
                self.advance()
                return Token(TokenType.GREATER_THAN_OR_EQ)
            return Token(TokenType.GREATER_THAN)
        elif c == '<':
            # Cek apakah <= atau <>
            if self.peek() == '=':
                self.advance()
                return Token(TokenType.LESS_THAN_OR_EQ)
            elif self.peek() == '>':
                self.advance()
                return Token(TokenType.NOT_EQUAL)
            return Token(TokenType.LESS_THAN)
        
        return None
    
    def next_token(self) -> Optional[Token]:
        """
        Dapatkan token berikutnya dari input.
        
        Returns:
            Token berikutnya, atau None jika sudah di akhir input
        """
        self.skip_whitespace()
        
        c = self.peek()
        
        if c is None:
            return None
        
        # Kalau huruf atau underscore -> Scan identifier/keyword
        if c.isalpha() or c == '_':
            return self.scan_identifier()
        
        # Kalau angka -> Scan number
        if c.isdigit():
            return self.scan_number()
        
        # Kalau tanda kutip -> Scan string literal
        if c == '"' or c == "'":
            return self.scan_string()
        
        # Sisanya simbol/operator
        return self.scan_symbol()
    
    def tokenize(self) -> list[Token]:
        """
        Tokenize seluruh input dan kembalikan sebagai list.
        
        Returns:
            List semua token dari input
        """
        tokens = []
        while True:
            token = self.next_token()
            if token is None:
                break
            tokens.append(token)
        return tokens
    
    def __iter__(self) -> Iterator[Token]:
        """Memungkinkan lexer digunakan sebagai iterator."""
        return self
    
    def __next__(self) -> Token:
        """Mendapatkan token berikutnya (untuk iterator protocol)."""
        token = self.next_token()
        if token is None:
            raise StopIteration
        return token


# ═══════════════════════════════════════════════════════════════════════════════
# CONTOH PENGGUNAAN (untuk testing)
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Contoh penggunaan lexer
    query = 'SELECT nama, umur FROM data.csv WHERE umur > 20'
    
    print(f"Query: {query}")
    print("\nTokens:")
    
    lexer = Lexer(query)
    for token in lexer:
        print(f"  {token}")
