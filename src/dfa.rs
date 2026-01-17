// src/dfa.rs
// Visualisasi DFA untuk Lexer

#![allow(dead_code)]

/// State dalam DFA Lexer
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum DFAState {
    Start,      // q0: State awal
    InIdent,    // q1: Sedang baca identifier/keyword
    InNumber,   // q2: Sedang baca angka
    InString,   // q3: Sedang baca string literal
    InOperator, // q4: Sedang baca operator
    Accept,     // qf: State akhir (token selesai)
}

impl DFAState {
    pub fn name(&self) -> &str {
        match self {
            DFAState::Start => "q0:Start",
            DFAState::InIdent => "q1:Ident",
            DFAState::InNumber => "q2:Number",
            DFAState::InString => "q3:String",
            DFAState::InOperator => "q4:Operator",
            DFAState::Accept => "qf:Accept",
        }
    }
}

/// Record transisi DFA
#[derive(Debug)]
pub struct DFATransition {
    pub from: DFAState,
    pub input: String,
    pub to: DFAState,
}

/// Tracker untuk DFA transitions
pub struct DFATracker {
    pub transitions: Vec<DFATransition>,
    pub current_state: DFAState,
}

impl DFATracker {
    pub fn new() -> Self {
        DFATracker {
            transitions: Vec::new(),
            current_state: DFAState::Start,
        }
    }

    pub fn transition(&mut self, input: char, to: DFAState) {
        self.transitions.push(DFATransition {
            from: self.current_state,
            input: if input.is_whitespace() { "ws".to_string() } else { input.to_string() },
            to,
        });
        self.current_state = to;
    }

    pub fn reset(&mut self) {
        self.current_state = DFAState::Start;
    }

    /// Tampilkan diagram transisi DFA
    pub fn print_transitions(&self) {
        println!("\n  🔄 DFA TRANSITIONS:");
        println!("  ┌────────────┬───────────┬────────────┐");
        println!("  │   From     │   Input   │     To     │");
        println!("  ├────────────┼───────────┼────────────┤");
        
        for t in &self.transitions {
            println!("  │ {:^10} │ {:^9} │ {:^10} │", 
                t.from.name().split(':').next().unwrap_or(""),
                t.input,
                t.to.name().split(':').next().unwrap_or("")
            );
        }
        
        println!("  └────────────┴───────────┴────────────┘");
    }

    /// Tampilkan diagram DFA sederhana (ASCII art)
    pub fn print_dfa_diagram() {
        println!("\n  📊 DFA DIAGRAM:");
        println!("  ┌─────────────────────────────────────────────────────────────┐");
        println!("  │                                                             │");
        println!("  │          ┌─────────┐                                        │");
        println!("  │    ┌────►│q1:Ident │────► [KEYWORD/IDENTIFIER]              │");
        println!("  │    │a-z  └─────────┘                                        │");
        println!("  │    │                                                        │");
        println!("  │  ┌─┴──┐   ┌─────────┐                                       │");
        println!("  │  │ q0 │──►│q2:Number│────► [NUMBER]                         │");
        println!("  │  │Start│0-9└─────────┘                                       │");
        println!("  │  └─┬──┘                                                     │");
        println!("  │    │                                                        │");
        println!("  │    │\"    ┌─────────┐                                        │");
        println!("  │    └────►│q3:String│────► [STRING_LITERAL]                  │");
        println!("  │          └─────────┘                                        │");
        println!("  │    │                                                        │");
        println!("  │    │=><  ┌─────────┐                                        │");
        println!("  │    └────►│q4:Oper  │────► [OPERATOR]                        │");
        println!("  │          └─────────┘                                        │");
        println!("  │                                                             │");
        println!("  └─────────────────────────────────────────────────────────────┘");
    }
}
