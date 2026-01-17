# CSV_QL - Mini SQL Query Engine untuk File CSV

**Tugas Akhir Mata Kuliah Automata dan Teknik Kompilasi**

Program mini query engine yang mengimplementasikan konsep:
- Lexical Analysis (DFA-based Lexer)
- Syntax Analysis (Recursive Descent Parser)
- Abstract Syntax Tree (AST)
- Semantic Analysis
- Intermediate Representation (IR/Query Plan)
- Interpreter/Execution Engine

---

## 🏗️ Arsitektur Sistem

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   INPUT     │    │   LEXER     │    │   PARSER    │
│   Query     │───►│   (DFA)     │───►│   (CFG)     │
│   String    │    │   Tokens    │    │   AST       │
└─────────────┘    └─────────────┘    └─────────────┘
                                            │
                   ┌─────────────┐          ▼
                   │  EXECUTOR   │    ┌─────────────┐
                   │  (Engine)   │◄───│  SEMANTIC   │
                   │  Results    │    │  ANALYZER   │
                   └─────────────┘    └─────────────┘
                         ▲                  │
                         │            ┌─────────────┐
                         └────────────│     IR      │
                                      │ Query Plan  │
                                      └─────────────┘
```

---

## 📜 CONTEXT-FREE GRAMMAR (CFG)

### Notasi BNF

```bnf
<query>       ::= SELECT <columns> FROM <table> <where_opt> <limit_opt>

<columns>     ::= "*" | <column_list>
<column_list> ::= <identifier> | <identifier> "," <column_list>

<table>       ::= <identifier>

<where_opt>   ::= ε | WHERE <expression>
<limit_opt>   ::= ε | LIMIT <number>

<expression>  ::= <or_expr>
<or_expr>     ::= <and_expr> | <and_expr> OR <or_expr>
<and_expr>    ::= <comparison> | <comparison> AND <and_expr>

<comparison>  ::= <leaf> <comp_op> <leaf>
<comp_op>     ::= "=" | "!=" | ">" | "<" | ">=" | "<="

<leaf>        ::= <identifier> | <number> | <string_literal>

<identifier>  ::= [a-zA-Z_][a-zA-Z0-9_.]*
<number>      ::= [0-9]+(\.[0-9]+)?
<string_literal> ::= '"' [^"]* '"' | "'" [^']* "'"
```

### Diagram Syntax (Railroad)

```
SELECT ──► columns ──► FROM ──► table ──┬──► WHERE ──► expr ──┬──► LIMIT ──► num ──►
                                        │                     │
                                        └─────────────────────┴────────────────────►
```

---

## 🔄 DFA DIAGRAM (Lexer)

```
                    ┌─────────────────────────────────────────────────────────────┐
                    │                      DFA LEXER                              │
                    ├─────────────────────────────────────────────────────────────┤
                    │                                                             │
                    │          ┌─────────┐                                        │
                    │    ┌────►│q1:Ident │────► [KEYWORD/IDENTIFIER]              │
                    │    │a-z  └────┬────┘                                        │
                    │    │          │a-z,0-9,_                                    │
                    │    │          ▼──────┘                                      │
                    │  ┌─┴──┐                                                     │
                    │  │ q0 │   ┌─────────┐                                       │
                    │  │Start──►│q2:Number│────► [NUMBER]                         │
                    │  └─┬──┘0-9└────┬────┘                                       │
                    │    │          │0-9,.                                        │
                    │    │          ▼──────┘                                      │
                    │    │                                                        │
                    │    │"    ┌─────────┐                                        │
                    │    └────►│q3:String│────► [STRING_LITERAL]                  │
                    │          └────┬────┘                                        │
                    │    │          │ [^"]                                        │
                    │    │          ▼──────┘                                      │
                    │    │=><                                                     │
                    │    └────►[q4:Operator]──► [OPERATOR]                        │
                    │                                                             │
                    └─────────────────────────────────────────────────────────────┘

State Transitions:
- q0 (Start)    : State awal
- q1 (Ident)    : Membaca identifier/keyword (a-z, A-Z, _, 0-9)
- q2 (Number)   : Membaca angka (0-9, .)
- q3 (String)   : Membaca string literal (antara " atau ')
- q4 (Operator) : Membaca operator (=, !=, >, <, >=, <=)
```

---

## 🎯 TOKEN DEFINITION

| Token Type      | Regular Expression       | Contoh           |
|-----------------|--------------------------|------------------|
| SELECT          | `SELECT\|select`         | SELECT           |
| FROM            | `FROM\|from`             | FROM             |
| WHERE           | `WHERE\|where`           | WHERE            |
| LIMIT           | `LIMIT\|limit`           | LIMIT            |
| AND             | `AND\|and`               | AND              |
| OR              | `OR\|or`                 | OR               |
| IDENTIFIER      | `[a-zA-Z_][a-zA-Z0-9_.]*`| nama, data.csv   |
| NUMBER          | `[0-9]+(\.[0-9]+)?`      | 25, 3.14         |
| STRING_LITERAL  | `"[^"]*"\|'[^']*'`       | "Jakarta"        |
| STAR            | `\*`                     | *                |
| EQUAL           | `=`                      | =                |
| NOT_EQUAL       | `!=`                     | !=               |
| GREATER         | `>`                      | >                |
| LESS            | `<`                      | <                |
| GREATER_EQ      | `>=`                     | >=               |
| LESS_EQ         | `<=`                     | <=               |
| COMMA           | `,`                      | ,                |

---

## 🌳 ABSTRACT SYNTAX TREE (AST)

### Struktur AST

```rust
// Statement (Root Node)
Statement::Select {
    columns: Vec<String>,      // Kolom yang dipilih
    table: String,             // Nama file CSV
    where_clause: Option<Expr>,// Kondisi filter (opsional)
    limit: Option<usize>,      // Batas hasil (opsional)
}

// Expression Node (untuk WHERE clause)
Expr::BinaryOp {
    left: Box<Expr>,           // Operand kiri
    op: Op,                    // Operator
    right: Box<Expr>,          // Operand kanan
}
Expr::Identifier(String)       // Nama kolom
Expr::Number(f64)              // Nilai numerik
Expr::StringLiteral(String)    // Nilai string
```

### Contoh AST

Query: `SELECT nama, umur FROM data.csv WHERE umur > 20 AND kota = "Jakarta" LIMIT 5`

```
                    Select
                    /    \
            columns       table: "data.csv"
           /      \              |
       "nama"   "umur"      where_clause
                                 |
                              BinaryOp (AND)
                             /            \
                    BinaryOp (>)      BinaryOp (=)
                    /       \         /        \
              Ident       Number   Ident    StringLit
              "umur"       20      "kota"   "Jakarta"
```

---

## 📊 INTERMEDIATE REPRESENTATION (IR)

Query Plan yang dihasilkan sebelum eksekusi:

```
Query: SELECT nama FROM data.csv WHERE umur > 20 LIMIT 5

📋 QUERY PLAN (IR):
┌─────────────────────────────────────────────────┐
│  1. 📂 SCAN: data.csv                           │  ← Baca file
│       ↓                                         │
│  2. 🔍 FILTER: umur > 20                        │  ← Filter WHERE
│       ↓                                         │
│  3. 📊 PROJECT: nama                            │  ← Pilih kolom
│       ↓                                         │
│  4. ✂️ LIMIT: 5                                 │  ← Batasi hasil
└─────────────────────────────────────────────────┘
```

---

## 🚀 Cara Menjalankan

```bash
# Build
cargo build --release

# Mode Interaktif (REPL)
cargo run

# Direct Query
cargo run -- "SELECT * FROM data.csv"

# Dengan Detail Kompilasi (verbose)
cargo run -- "SELECT * FROM data.csv" --verbose
```

---

## 📝 CONTOH QUERY

### 1. Ambil Semua Data
```sql
SELECT * FROM data.csv
```

### 2. Pilih Kolom Tertentu
```sql
SELECT nama, umur FROM data.csv
```

### 3. Filter dengan WHERE
```sql
SELECT * FROM data.csv WHERE umur > 20
SELECT * FROM data.csv WHERE kota = "Jakarta"
```

### 4. Kombinasi AND/OR
```sql
SELECT * FROM data.csv WHERE umur > 20 AND umur < 30
SELECT * FROM data.csv WHERE kota = "Jakarta" OR kota = "Bandung"
```

### 5. Dengan LIMIT
```sql
SELECT * FROM data.csv LIMIT 5
SELECT nama FROM data.csv WHERE umur > 25 LIMIT 10
```

---

## 🔧 Perintah REPL

| Perintah    | Fungsi                           |
|-------------|----------------------------------|
| `help`      | Tampilkan bantuan                |
| `clear`     | Bersihkan layar                  |
| `dfa`       | Tampilkan diagram DFA            |
| `exit`      | Keluar program                   |
| `--verbose` | Tambahkan di akhir query untuk detail |

---

## 📁 Struktur Project

```
csv_ql/
├── Cargo.toml          # Konfigurasi project
├── README.md           # Dokumentasi
├── data.csv            # Contoh data
└── src/
    ├── main.rs         # Entry point + REPL
    ├── token.rs        # Definisi Token
    ├── lexer.rs        # Lexical Analyzer (DFA)
    ├── ast.rs          # Abstract Syntax Tree
    ├── parser.rs       # Syntax Analyzer (CFG)
    ├── semantic.rs     # Semantic Analyzer
    ├── ir.rs           # Intermediate Representation
    ├── dfa.rs          # DFA Visualization
    └── engine.rs       # Query Executor
```

---

## ✅ Komponen yang Diimplementasi

| Komponen                | File         | Status |
|-------------------------|--------------|--------|
| Token & Regex           | token.rs     | ✅     |
| Lexer (DFA-based)       | lexer.rs     | ✅     |
| Parser (Recursive Desc) | parser.rs    | ✅     |
| AST                     | ast.rs       | ✅     |
| Semantic Analyzer       | semantic.rs  | ✅     |
| IR / Query Plan         | ir.rs        | ✅     |
| DFA Visualization       | dfa.rs       | ✅     |
| Interpreter/Executor    | engine.rs    | ✅     |
