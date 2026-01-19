"""
dfa.py - Visualisasi DFA Lexer untuk CSV_QL

═══════════════════════════════════════════════════════════════════════════════
                        📋 INSTRUKSI PENGISIAN
═══════════════════════════════════════════════════════════════════════════════

Modul ini berisi visualisasi DFA (Deterministic Finite Automaton) untuk lexer.
DFA adalah mesin state yang digunakan untuk tokenization.

State DFA Lexer:
- q0 (Start)    : State awal
- q1 (InIdent)  : Sedang membaca identifier/keyword
- q2 (InNumber) : Sedang membaca angka
- q3 (InString) : Sedang membaca string literal
- q4 (InOperator): Sedang membaca operator
- qf (Accept)   : State akhir (token selesai)

TUGAS YANG HARUS DIKERJAKAN:
-----------------------------

1. Buat enum DFAState dengan semua state di atas

2. Buat dataclass DFATransition untuk merekam transisi:
   - from_state: DFAState
   - input_char: str
   - to_state: DFAState

3. Buat class DFATracker untuk tracking transisi:
   - __init__: inisialisasi dengan state Start
   - transition(input_char, to_state): record transisi
   - reset(): kembali ke state Start
   - print_transitions(): tampilkan history transisi
   - print_dfa_diagram(): tampilkan diagram DFA (ASCII art)

REFERENSI:
----------
Lihat file Rust: src/dfa.rs

TIPS:
-----
- Modul ini bersifat opsional untuk visualisasi/debugging
- Bisa diintegrasikan ke lexer untuk tracing
- ASCII art diagram sudah disediakan di print_dfa_diagram()

═══════════════════════════════════════════════════════════════════════════════
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import List


class DFAState(Enum):
    """State dalam DFA Lexer."""
    START = auto()       # q0: State awal
    IN_IDENT = auto()    # q1: Sedang baca identifier/keyword
    IN_NUMBER = auto()   # q2: Sedang baca angka
    IN_STRING = auto()   # q3: Sedang baca string literal
    IN_OPERATOR = auto() # q4: Sedang baca operator
    ACCEPT = auto()      # qf: State akhir (token selesai)
    
    def name_short(self) -> str:
        """Nama pendek untuk tampilan."""
        names = {
            DFAState.START: "q0",
            DFAState.IN_IDENT: "q1",
            DFAState.IN_NUMBER: "q2",
            DFAState.IN_STRING: "q3",
            DFAState.IN_OPERATOR: "q4",
            DFAState.ACCEPT: "qf",
        }
        return names.get(self, "?")


@dataclass
class DFATransition:
    """Record transisi DFA."""
    from_state: DFAState
    input_char: str
    to_state: DFAState


class DFATracker:
    """Tracker untuk DFA transitions."""
    
    def __init__(self):
        """Inisialisasi tracker."""
        self.transitions: List[DFATransition] = []
        self.current_state = DFAState.START
    
    def transition(self, input_char: str, to_state: DFAState) -> None:
        """
        Record transisi.
        
        Args:
            input_char: Karakter input yang menyebabkan transisi
            to_state: State tujuan
        """
        self.transitions.append(DFATransition(
            from_state=self.current_state,
            input_char="ws" if input_char.isspace() else input_char,
            to_state=to_state
        ))
        self.current_state = to_state
    
    def reset(self) -> None:
        """Reset ke state awal."""
        self.current_state = DFAState.START
    
    def print_transitions(self) -> None:
        """Tampilkan history transisi."""
        print("\n  🔄 DFA TRANSITIONS:")
        print("  ┌────────────┬───────────┬────────────┐")
        print("  │   From     │   Input   │     To     │")
        print("  ├────────────┼───────────┼────────────┤")
        
        for t in self.transitions:
            from_name = t.from_state.name_short()
            to_name = t.to_state.name_short()
            print(f"  │ {from_name:^10} │ {t.input_char:^9} │ {to_name:^10} │")
        
        print("  └────────────┴───────────┴────────────┘")
    
    @staticmethod
    def print_dfa_diagram() -> None:
        """Tampilkan diagram DFA (ASCII art)."""
        print("""
  📊 DFA DIAGRAM:
  ┌─────────────────────────────────────────────────────────────┐
  │                                                             │
  │          ┌─────────┐                                        │
  │    ┌────►│q1:Ident │────► [KEYWORD/IDENTIFIER]              │
  │    │a-z  └─────────┘                                        │
  │    │                                                        │
  │  ┌─┴──┐   ┌─────────┐                                       │
  │  │ q0 │──►│q2:Number│────► [NUMBER]                         │
  │  │Start│0-9└─────────┘                                       │
  │  └─┬──┘                                                     │
  │    │                                                        │
  │    │"    ┌─────────┐                                        │
  │    └────►│q3:String│────► [STRING_LITERAL]                  │
  │          └─────────┘                                        │
  │    │                                                        │
  │    │=><  ┌─────────┐                                        │
  │    └────►│q4:Oper  │────► [OPERATOR]                        │
  │          └─────────┘                                        │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘
""")
