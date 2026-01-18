"""
token.py - Definisi Token untuk CSV_QL

Modul ini berisi semua jenis token yang didukung oleh lexer.
Token adalah unit terkecil dari bahasa query (seperti kata kunci, operator, identifier, dll).
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Union


class TokenType(Enum):
    """Enum untuk tipe-tipe token yang didukung oleh CSV_QL"""
    
    # Keywords (Kata Kunci SQL)
    SELECT = auto()
    FROM = auto()
    WHERE = auto()
    LIMIT = auto()
    OR = auto()
    AND = auto()
    
    # Operators (Operator)
    EQUAL = auto()           # =
    NOT_EQUAL = auto()       # != atau <>
    GREATER_THAN = auto()    # >
    LESS_THAN = auto()       # <
    GREATER_THAN_OR_EQ = auto()  # >=
    LESS_THAN_OR_EQ = auto()     # <=
    STAR = auto()            # * (untuk SELECT *)
    
    # Literals & Identifiers
    IDENTIFIER = auto()      # nama kolom, nama file, dll
    NUMBER = auto()          # angka (integer atau float)
    STRING_LITERAL = auto()  # string dalam tanda kutip "..." atau '...'
    
    # Punctuation (Tanda Baca)
    COMMA = auto()           # ,
    
    # Special
    EOF = auto()             # End of File/Input


@dataclass
class Token:
    """
    Representasi sebuah token.
    
    Attributes:
        type: Tipe token (dari enum TokenType)
        value: Nilai token (untuk IDENTIFIER, NUMBER, STRING_LITERAL)
    """
    type: TokenType
    value: Union[str, float, None] = None
    
    def __repr__(self) -> str:
        if self.value is not None:
            return f"Token({self.type.name}, {self.value!r})"
        return f"Token({self.type.name})"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Token):
            return self.type == other.type and self.value == other.value
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# MAPPING KEYWORDS
# ═══════════════════════════════════════════════════════════════════════════════

KEYWORDS = {
    "SELECT": TokenType.SELECT,
    "select": TokenType.SELECT,
    "FROM": TokenType.FROM,
    "from": TokenType.FROM,
    "WHERE": TokenType.WHERE,
    "where": TokenType.WHERE,
    "LIMIT": TokenType.LIMIT,
    "limit": TokenType.LIMIT,
    "OR": TokenType.OR,
    "or": TokenType.OR,
    "AND": TokenType.AND,
    "and": TokenType.AND,
}


def get_keyword_token(text: str) -> Token | None:
    """
    Cek apakah text adalah keyword, kalau iya kembalikan Token-nya.
    
    Args:
        text: String yang akan dicek
        
    Returns:
        Token jika text adalah keyword, None jika bukan
    """
    if text in KEYWORDS:
        return Token(KEYWORDS[text])
    return None
