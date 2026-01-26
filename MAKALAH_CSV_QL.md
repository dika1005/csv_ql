# MAKALAH PROYEK AKHIR
## AUTOMATA DAN TEKNIK KOMPILASI

---

# CSV_QL: Mini Query Engine untuk Data Nilai Mahasiswa

**Tema Project:** Big Data - Mini Query Engine berbasis SQL

---

## DAFTAR ISI

1. [BAB I - Pendahuluan](#bab-i---pendahuluan)
2. [BAB II - Deskripsi Tema dan Studi Kasus](#bab-ii---deskripsi-tema-dan-studi-kasus)
3. [BAB III - Analisis Leksikal (Lexer)](#bab-iii---analisis-leksikal-lexer)
4. [BAB IV - Analisis Sintaksis (Parser)](#bab-iv---analisis-sintaksis-parser)
5. [BAB V - Analisis Semantik](#bab-v---analisis-semantik)
6. [BAB VI - Intermediate Representation (IR)](#bab-vi---intermediate-representation-ir)
7. [BAB VII - Execution Engine](#bab-vii---execution-engine)
8. [BAB VIII - Simulasi Automata (DFA)](#bab-viii---simulasi-automata-dfa)
9. [BAB IX - Pengujian dan Hasil](#bab-ix---pengujian-dan-hasil)
10. [BAB X - Kesimpulan](#bab-x---kesimpulan)
11. [Daftar Pustaka](#daftar-pustaka)

---

## BAB I - Pendahuluan

### 1.1 Latar Belakang

Dalam era digital saat ini, data menjadi aset yang sangat penting dalam berbagai bidang, termasuk pendidikan. Sistem Informasi Akademik (SIMAK/SIAKAD) menghasilkan data dalam jumlah besar, termasuk data nilai mahasiswa yang umumnya disimpan dalam format CSV (Comma-Separated Values).

Untuk menganalisis data tersebut, pengguna biasanya memerlukan pengetahuan tentang bahasa pemrograman atau tools khusus. Hal ini menimbulkan hambatan bagi pengguna non-teknis yang ingin melakukan query sederhana terhadap data.

CSV_QL hadir sebagai solusi berupa **Domain Specific Language (DSL)** yang memungkinkan pengguna melakukan query terhadap file CSV menggunakan sintaks mirip SQL yang lebih familiar dan mudah dipahami.

### 1.2 Rumusan Masalah

1. Bagaimana membangun lexical analyzer berbasis DFA untuk tokenisasi query SQL?
2. Bagaimana merancang parser menggunakan CFG dengan metode recursive descent?
3. Bagaimana mengimplementasikan analisis semantik untuk validasi query?
4. Bagaimana merancang Intermediate Representation (IR) untuk eksekusi query?
5. Bagaimana mengimplementasikan query engine yang dapat mengeksekusi query terhadap file CSV?

### 1.3 Tujuan

1. Mengimplementasikan lexical analyzer berbasis DFA
2. Membangun parser dengan Context-Free Grammar (CFG)
3. Menyusun Abstract Syntax Tree (AST) dan analisis semantik
4. Membangun Intermediate Representation (IR) untuk query plan
5. Mengembangkan execution engine untuk menjalankan query

### 1.4 Batasan Masalah

- Query terbatas pada operasi SELECT
- Mendukung klausa WHERE dengan operator perbandingan dan logika
- Mendukung klausa LIMIT
- File input harus berformat CSV dengan header

---

## BAB II - Deskripsi Tema dan Studi Kasus

### 2.1 Tema Project

Proyek ini mengambil tema **Big Data** dengan fokus membangun **Mini Query Engine** untuk subset SQL. Implementasi mencakup:

- Lexer (tokenisasi query)
- Parser (membangun AST dari token)
- Semantic analyzer (validasi query)
- Intermediate Representation (query plan)
- Execution engine (eksekusi query terhadap CSV)

### 2.2 Studi Kasus

**Studi Kasus: Query Data Nilai Mahasiswa SIMAK/SIAKAD**

Dalam sistem akademik, data nilai mahasiswa sering disimpan dalam format CSV dengan struktur sebagai berikut:

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `nim` | String | Nomor Induk Mahasiswa |
| `nama` | String | Nama mahasiswa |
| `mata_kuliah` | String | Nama mata kuliah |
| `sks` | Number | Jumlah SKS |
| `nilai_huruf` | String | Nilai huruf (A, B, C, D, E) |
| `nilai_angka` | Number | Nilai angka (0.0 - 4.0) |
| `semester` | Number | Semester pengambilan |
| `status` | String | Status kelulusan |

**Contoh Data (`data_nilai.csv`):**
```csv
nim,nama,mata_kuliah,sks,nilai_huruf,nilai_angka,semester,status
2023001,Ahmad Rizki,Automata dan Teknik Kompilasi,3,A,4.0,5,Lulus
2023002,Budi Santoso,Automata dan Teknik Kompilasi,3,B,3.0,5,Lulus
2023003,Citra Dewi,Automata dan Teknik Kompilasi,3,A,4.0,5,Lulus
2023004,Dian Pratama,Automata dan Teknik Kompilasi,3,C,2.0,5,Lulus
2023005,Eka Putri,Automata dan Teknik Kompilasi,3,E,0.0,5,Tidak Lulus
```

### 2.3 Contoh Query

```sql
-- Lihat semua data nilai
SELECT * FROM data_nilai.csv

-- Filter mahasiswa dengan nilai A
SELECT nama, mata_kuliah FROM data_nilai.csv WHERE nilai_huruf = "A"

-- Filter mahasiswa yang tidak lulus
SELECT nim, nama FROM data_nilai.csv WHERE status = "Tidak Lulus"

-- Kombinasi kondisi
SELECT * FROM data_nilai.csv WHERE nilai_angka >= 3.0 AND semester = 5

-- Batasi hasil
SELECT nama, nilai_huruf FROM data_nilai.csv LIMIT 5
```

---

## BAB III - Analisis Leksikal (Lexer)

### 3.1 Daftar Token

Lexer CSV_QL mengenali token-token berikut:

| Kategori | Token | Simbol/Pattern |
|----------|-------|----------------|
| **Keywords** | SELECT | `SELECT` |
| | FROM | `FROM` |
| | WHERE | `WHERE` |
| | LIMIT | `LIMIT` |
| | AND | `AND` |
| | OR | `OR` |
| **Operators** | EQUAL | `=` |
| | NOT_EQUAL | `!=` atau `<>` |
| | GREATER_THAN | `>` |
| | LESS_THAN | `<` |
| | GREATER_THAN_OR_EQ | `>=` |
| | LESS_THAN_OR_EQ | `<=` |
| | STAR | `*` |
| **Literals** | IDENTIFIER | `[a-zA-Z_][a-zA-Z0-9_.]*` |
| | NUMBER | `[0-9]+(\.[0-9]+)?` |
| | STRING_LITERAL | `"[^"]*"` atau `'[^']*'` |
| **Punctuation** | COMMA | `,` |

### 3.2 Regular Expression

Berikut adalah regular expression untuk setiap kategori token:

```
KEYWORD     := SELECT | FROM | WHERE | LIMIT | AND | OR
IDENTIFIER  := [a-zA-Z_][a-zA-Z0-9_.]*
NUMBER      := [0-9]+(\.[0-9]+)?
STRING      := "[^"]*" | '[^']*'
OPERATOR    := = | != | <> | > | < | >= | <=
SYMBOL      := * | ,
WHITESPACE  := [ \t\n\r]+
```

### 3.3 Diagram DFA Lexer

```
                    DFA LEXER CSV_QL
    ┌─────────────────────────────────────────────────────────────┐
    │                                                             │
    │          ┌─────────┐                                        │
    │    ┌────►│q1:Ident │────► [KEYWORD/IDENTIFIER]              │
    │    │a-z  └─────────┘                                        │
    │    │    A-Z, _                                              │
    │    │                                                        │
    │  ┌─┴──┐   ┌─────────┐                                       │
    │  │ q0 │──►│q2:Number│────► [NUMBER]                         │
    │  │Start│0-9└─────────┘                                      │
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
```

**Deskripsi State:**
- **q0 (Start)**: State awal, menunggu input
- **q1 (InIdent)**: Membaca identifier/keyword
- **q2 (InNumber)**: Membaca angka
- **q3 (InString)**: Membaca string literal
- **q4 (InOper)**: Membaca operator
- **qf (Accept)**: State akhir (token selesai)

### 3.4 Tabel Transisi DFA

| State | Input | Next State | Action |
|-------|-------|------------|--------|
| q0 | `[a-zA-Z_]` | q1 | Start identifier |
| q0 | `[0-9]` | q2 | Start number |
| q0 | `"` atau `'` | q3 | Start string |
| q0 | `=><!=` | q4 | Start operator |
| q0 | `*,` | qf | Emit symbol |
| q0 | whitespace | q0 | Skip |
| q1 | `[a-zA-Z0-9_.]` | q1 | Continue identifier |
| q1 | otherwise | qf | Emit IDENTIFIER/KEYWORD |
| q2 | `[0-9.]` | q2 | Continue number |
| q2 | otherwise | qf | Emit NUMBER |
| q3 | `[^"']` | q3 | Continue string |
| q3 | `"` atau `'` | qf | Emit STRING_LITERAL |
| q4 | `=` | qf | Emit compound operator |
| q4 | otherwise | qf | Emit simple operator |

### 3.5 Contoh Tokenisasi

**Input Query:**
```sql
SELECT nama, nilai_huruf FROM data_nilai.csv WHERE status = "Lulus"
```

**Output Tokens:**
```
Token(SELECT)
Token(IDENTIFIER, "nama")
Token(COMMA)
Token(IDENTIFIER, "nilai_huruf")
Token(FROM)
Token(IDENTIFIER, "data_nilai.csv")
Token(WHERE)
Token(IDENTIFIER, "status")
Token(EQUAL)
Token(STRING_LITERAL, "Lulus")
```

---

## BAB IV - Analisis Sintaksis (Parser)

### 4.1 Context-Free Grammar (CFG)

Grammar CSV_QL dalam Backus-Naur Form (BNF):

```bnf
<query>       ::= <select_stmt>

<select_stmt> ::= SELECT <columns> FROM <table> [<where_clause>] [<limit_clause>]

<columns>     ::= STAR | <column_list>

<column_list> ::= IDENTIFIER (COMMA IDENTIFIER)*

<table>       ::= IDENTIFIER

<where_clause> ::= WHERE <expression>

<limit_clause> ::= LIMIT NUMBER

<expression>  ::= <or_expr>

<or_expr>     ::= <and_expr> (OR <and_expr>)*

<and_expr>    ::= <comparison> (AND <comparison>)*

<comparison>  ::= <leaf> [<comp_op> <leaf>]

<comp_op>     ::= EQUAL | NOT_EQUAL | GREATER_THAN | LESS_THAN 
                | GREATER_THAN_OR_EQ | LESS_THAN_OR_EQ

<leaf>        ::= IDENTIFIER | NUMBER | STRING_LITERAL
```

### 4.2 Operator Precedence

| Level | Operator | Associativity |
|-------|----------|---------------|
| 1 (lowest) | OR | Left |
| 2 | AND | Left |
| 3 (highest) | `=`, `!=`, `>`, `<`, `>=`, `<=` | Left |

### 4.3 Metode Parsing: Recursive Descent

Parser menggunakan teknik **Recursive Descent Parsing** yang merupakan implementasi dari LL(1) parser. Setiap non-terminal dalam grammar memiliki fungsi parser yang sesuai.

**Algoritma Parsing:**

```python
def parse(self) -> Statement:
    """Entry point: parse SELECT statement"""
    return self.parse_select()

def parse_select(self) -> SelectStatement:
    """Parse: SELECT columns FROM table [WHERE expr] [LIMIT n]"""
    # Expect SELECT keyword
    if not self.match_token(TokenType.SELECT):
        raise Exception("Expected SELECT")
    
    # Parse column list
    columns = self.parse_columns()
    
    # Expect FROM keyword
    if not self.match_token(TokenType.FROM):
        raise Exception("Expected FROM")
    
    # Parse table name
    table = self.current().value
    self.advance()
    
    # Optional WHERE clause
    where_clause = None
    if self.match_token(TokenType.WHERE):
        where_clause = self.parse_expression()
    
    # Optional LIMIT clause
    limit = None
    if self.match_token(TokenType.LIMIT):
        limit = int(self.current().value)
        self.advance()
    
    return SelectStatement(columns, table, where_clause, limit)

def parse_expression(self) -> Expr:
    """Parse expression (entry point for WHERE)"""
    return self.parse_logic_or()

def parse_logic_or(self) -> Expr:
    """Parse: and_expr (OR and_expr)*"""
    left = self.parse_logic_and()
    while self.match_token(TokenType.OR):
        right = self.parse_logic_and()
        left = BinaryOp(left, Op.OR, right)
    return left

def parse_logic_and(self) -> Expr:
    """Parse: cmp_expr (AND cmp_expr)*"""
    left = self.parse_comparison()
    while self.match_token(TokenType.AND):
        right = self.parse_comparison()
        left = BinaryOp(left, Op.AND, right)
    return left
```

### 4.4 Desain Abstract Syntax Tree (AST)

**Struktur AST:**

```
SelectStatement
├── columns: List[str]          # ["nama", "nilai"] atau ["*"]
├── table: str                  # "data_nilai.csv"
├── where_clause: Optional[Expr]
│   └── BinaryOp
│       ├── left: Expr
│       ├── op: Op
│       └── right: Expr
└── limit: Optional[int]        # 10

Expr = BinaryOp | Identifier | Number | StringLiteral

BinaryOp
├── left: Expr
├── op: Op (EQUAL, NOT_EQUAL, AND, OR, etc.)
└── right: Expr

Identifier
└── name: str

Number
└── value: float

StringLiteral
└── value: str
```

### 4.5 Contoh Parse Tree

**Query:**
```sql
SELECT nama FROM data.csv WHERE nilai >= 3.0 AND status = "Lulus"
```

**AST yang dihasilkan:**
```
SelectStatement
├── columns: ["nama"]
├── table: "data.csv"
├── where_clause:
│   └── BinaryOp (AND)
│       ├── left: BinaryOp (GREATER_THAN_OR_EQ)
│       │   ├── left: Identifier("nilai")
│       │   └── right: Number(3.0)
│       └── right: BinaryOp (EQUAL)
│           ├── left: Identifier("status")
│           └── right: StringLiteral("Lulus")
└── limit: None
```

---

## BAB V - Analisis Semantik

### 5.1 Fungsi Analisis Semantik

Semantic analyzer melakukan validasi untuk memastikan query valid secara semantik sebelum dieksekusi:

1. **Validasi File CSV** - Memeriksa apakah file yang direferensikan ada
2. **Validasi Kolom SELECT** - Memeriksa apakah kolom yang diminta ada dalam file
3. **Validasi Kolom WHERE** - Memeriksa apakah kolom dalam kondisi WHERE ada
4. **Validasi LIMIT** - Memeriksa apakah nilai LIMIT positif

### 5.2 Algoritma Analisis Semantik

```python
def analyze(query: Statement) -> SemanticResult:
    result = SemanticResult()
    
    # 1. Cek apakah file CSV ada
    if not os.path.exists(query.table):
        result.errors.append(f"File '{query.table}' tidak ditemukan")
        result.valid = False
        return result
    
    # 2. Baca header CSV
    with open(query.table) as f:
        reader = csv.reader(f)
        headers = set(next(reader))
    
    # 3. Validasi kolom SELECT
    if query.columns != ["*"]:
        for col in query.columns:
            if col not in headers:
                result.errors.append(f"Kolom '{col}' tidak ada di {query.table}")
                result.valid = False
    
    # 4. Validasi kolom dalam WHERE
    if query.where_clause:
        validate_expr_columns(query.where_clause, headers, result.errors)
    
    # 5. Validasi LIMIT
    if query.limit is not None and query.limit <= 0:
        result.warnings.append("LIMIT <= 0, tidak ada hasil yang dikembalikan")
    
    return result
```

### 5.3 Tabel Simbol

Semantic analyzer membangun tabel simbol dari header CSV:

| Symbol | Type | Source |
|--------|------|--------|
| `nim` | String | CSV Header |
| `nama` | String | CSV Header |
| `mata_kuliah` | String | CSV Header |
| `sks` | Number | CSV Header |
| `nilai_huruf` | String | CSV Header |
| `nilai_angka` | Number | CSV Header |
| `semester` | Number | CSV Header |
| `status` | String | CSV Header |

### 5.4 Contoh Validasi

**Query dengan Error:**
```sql
SELECT ipk FROM data_nilai.csv
```

**Output:**
```
❌ Semantic Error: Kolom 'ipk' tidak ada di data_nilai.csv
```

**Query dengan Warning:**
```sql
SELECT * FROM data_nilai.csv LIMIT 0
```

**Output:**
```
⚠️ Warning: LIMIT <= 0, tidak ada hasil yang dikembalikan
```

---

## BAB VI - Intermediate Representation (IR)

### 6.1 Desain Query Plan

IR dalam CSV_QL direpresentasikan sebagai **Query Plan** yang terdiri dari urutan langkah eksekusi:

| Step | Nama | Deskripsi |
|------|------|-----------|
| 1 | **SCAN** | Baca file CSV |
| 2 | **FILTER** | Filter baris dengan kondisi WHERE |
| 3 | **PROJECT** | Pilih kolom yang diminta |
| 4 | **LIMIT** | Batasi jumlah hasil |

### 6.2 Struktur Data IR

```python
@dataclass
class ScanStep:
    """Langkah 1: Baca file CSV"""
    table: str

@dataclass
class FilterStep:
    """Langkah 2: Filter baris"""
    condition: str  # String representasi kondisi

@dataclass
class ProjectStep:
    """Langkah 3: Pilih kolom"""
    columns: List[str]

@dataclass
class LimitStep:
    """Langkah 4: Batasi hasil"""
    count: int

@dataclass
class QueryPlan:
    """Query Plan - representasi langkah eksekusi"""
    steps: List[PlanStep]
```

### 6.3 Algoritma Konversi AST ke IR

```python
def ast_to_ir(ast: Statement) -> QueryPlan:
    steps = []
    
    # Step 1: SCAN (selalu ada)
    steps.append(ScanStep(table=ast.table))
    
    # Step 2: FILTER (jika ada WHERE)
    if ast.where_clause:
        condition_str = expr_to_string(ast.where_clause)
        steps.append(FilterStep(condition=condition_str))
    
    # Step 3: PROJECT (daftar kolom)
    steps.append(ProjectStep(columns=ast.columns))
    
    # Step 4: LIMIT (jika ada)
    if ast.limit:
        steps.append(LimitStep(count=ast.limit))
    
    return QueryPlan(steps=steps)
```

### 6.4 Alur Eksekusi IR

```
┌───────────────────────────────────────────────────────────────┐
│                        QUERY PLAN                             │
├───────────────────────────────────────────────────────────────┤
│  Step 1: SCAN(data_nilai.csv)                                 │
│      ↓ [Baca 22 baris dari CSV]                               │
│  Step 2: FILTER(status = "Lulus")                             │
│      ↓ [18 baris lolos filter]                                │
│  Step 3: PROJECT([nama, nilai_huruf])                         │
│      ↓ [Pilih 2 kolom]                                        │
│  Step 4: LIMIT(5)                                             │
│      ↓ [Ambil 5 baris pertama]                                │
│  OUTPUT: 5 baris x 2 kolom                                    │
└───────────────────────────────────────────────────────────────┘
```

### 6.5 Contoh Output Query Plan

**Query:**
```sql
SELECT nama, nilai_huruf FROM data_nilai.csv WHERE status = "Lulus" LIMIT 5
```

**Query Plan:**
```
  ═══════════════════════════════════════════════════════
                      📋 QUERY PLAN
  ═══════════════════════════════════════════════════════
  
    ┌───────────────────────────────────────────────────┐
    │ Step 1: SCAN                                      │
    │   └─ Table: data_nilai.csv                        │
    ├───────────────────────────────────────────────────┤
    │ Step 2: FILTER                                    │
    │   └─ Condition: status = "Lulus"                  │
    ├───────────────────────────────────────────────────┤
    │ Step 3: PROJECT                                   │
    │   └─ Columns: [nama, nilai_huruf]                 │
    ├───────────────────────────────────────────────────┤
    │ Step 4: LIMIT                                     │
    │   └─ Count: 5                                     │
    └───────────────────────────────────────────────────┘
```

---

## BAB VII - Execution Engine

### 7.1 Arsitektur Execution Engine

Engine adalah tahap terakhir dari pipeline kompilasi yang mengeksekusi query plan terhadap file CSV.

```
┌─────────────────────────────────────────────────────────────┐
│                    COMPILATION PIPELINE                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Query String                                              │
│        ↓                                                    │
│   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐    │
│   │  LEXER  │ → │ PARSER  │ → │SEMANTIC │ → │   IR    │    │
│   └─────────┘   └─────────┘   └─────────┘   └─────────┘    │
│        ↓             ↓             ↓             ↓          │
│     Tokens         AST         Validated      QueryPlan     │
│                                                    ↓         │
│                                              ┌─────────┐    │
│                                              │ ENGINE  │    │
│                                              └─────────┘    │
│                                                    ↓         │
│                                               Result Set     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Algoritma Eksekusi Query

```python
def execute_query(query: Statement) -> Tuple[List[str], List[List[str]]]:
    """
    Eksekusi query dan kembalikan hasil.
    
    Returns:
        Tuple (headers, rows)
    """
    # 1. Buka file CSV
    with open(query.table, 'r') as f:
        reader = csv.DictReader(f)
        all_headers = list(reader.fieldnames)
        
        # 2. Tentukan output headers
        if query.columns == ["*"]:
            output_headers = all_headers
        else:
            output_headers = query.columns
        
        # 3. Proses setiap baris
        results = []
        count = 0
        
        for row in reader:
            # 4. Evaluasi WHERE clause
            if query.where_clause:
                if not eval_expr(query.where_clause, row):
                    continue
            
            # 5. Ambil kolom yang diminta
            if query.columns == ["*"]:
                row_data = [row[col] for col in all_headers]
            else:
                row_data = [row.get(col, "") for col in query.columns]
            
            results.append(row_data)
            
            # 6. Cek LIMIT
            count += 1
            if query.limit and count >= query.limit:
                break
        
        return (output_headers, results)
```

### 7.3 Evaluasi Expression

```python
def eval_expr(expr: Expr, row: Dict[str, str]) -> bool:
    """Evaluasi expression dengan data baris."""
    
    if isinstance(expr, BinaryOp):
        # Logika AND/OR
        if expr.op == Op.AND:
            return eval_expr(expr.left, row) and eval_expr(expr.right, row)
        elif expr.op == Op.OR:
            return eval_expr(expr.left, row) or eval_expr(expr.right, row)
        
        # Perbandingan
        elif expr.op == Op.EQUAL:
            return get_value(expr.left, row) == get_value(expr.right, row)
        elif expr.op == Op.NOT_EQUAL:
            return get_value(expr.left, row) != get_value(expr.right, row)
        elif expr.op == Op.GREATER_THAN:
            return get_value(expr.left, row) > get_value(expr.right, row)
        elif expr.op == Op.LESS_THAN:
            return get_value(expr.left, row) < get_value(expr.right, row)
        elif expr.op == Op.GREATER_THAN_OR_EQ:
            return get_value(expr.left, row) >= get_value(expr.right, row)
        elif expr.op == Op.LESS_THAN_OR_EQ:
            return get_value(expr.left, row) <= get_value(expr.right, row)
    
    return False
```

---

## BAB VIII - Simulasi Automata (DFA)

### 8.1 DFA Lexer

Lexer CSV_QL menggunakan DFA (Deterministic Finite Automaton) untuk tokenisasi. Berikut adalah definisi formal:

**DFA M = (Q, Σ, δ, q0, F)**

- **Q** = {q0, q1, q2, q3, q4, qf} — Himpunan state
- **Σ** = ASCII characters — Alphabet input
- **δ** = Fungsi transisi (lihat tabel transisi)
- **q0** = State awal
- **F** = {qf} — State akhir (accepting state)

### 8.2 State DFA

```python
class DFAState(Enum):
    START = auto()       # q0: State awal
    IN_IDENT = auto()    # q1: Sedang baca identifier/keyword
    IN_NUMBER = auto()   # q2: Sedang baca angka
    IN_STRING = auto()   # q3: Sedang baca string literal
    IN_OPERATOR = auto() # q4: Sedang baca operator
    ACCEPT = auto()      # qf: State akhir (token selesai)
```

### 8.3 Contoh Simulasi DFA

**Input:** `SELECT nama FROM data.csv`

**Trace Transisi:**

| Step | State | Input | Next State | Token |
|------|-------|-------|------------|-------|
| 1 | q0 | 'S' | q1 | - |
| 2 | q1 | 'E' | q1 | - |
| 3 | q1 | 'L' | q1 | - |
| 4 | q1 | 'E' | q1 | - |
| 5 | q1 | 'C' | q1 | - |
| 6 | q1 | 'T' | q1 | - |
| 7 | q1 | ' ' | qf | **SELECT** |
| 8 | q0 | 'n' | q1 | - |
| 9 | q1 | 'a' | q1 | - |
| 10 | q1 | 'm' | q1 | - |
| 11 | q1 | 'a' | q1 | - |
| 12 | q1 | ' ' | qf | **IDENTIFIER(nama)** |
| ... | ... | ... | ... | ... |

### 8.4 Visualisasi Transisi

```
  🔄 DFA TRANSITIONS:
  ┌────────────┬───────────┬────────────┐
  │   From     │   Input   │     To     │
  ├────────────┼───────────┼────────────┤
  │     q0     │     S     │     q1     │
  │     q1     │     E     │     q1     │
  │     q1     │     L     │     q1     │
  │     q1     │     E     │     q1     │
  │     q1     │     C     │     q1     │
  │     q1     │     T     │     q1     │
  │     q1     │    ws     │     qf     │
  │     q0     │     n     │     q1     │
  │     q1     │     a     │     q1     │
  │     q1     │     m     │     q1     │
  │     q1     │     a     │     q1     │
  │     q1     │    ws     │     qf     │
  └────────────┴───────────┴────────────┘
```

---

## BAB IX - Pengujian dan Hasil

### 9.1 Test Case 1: SELECT Semua Data

**Query:**
```sql
SELECT * FROM data_nilai.csv
```

**Hasil:**
```
╭────────┬───────────────┬─────────────────────────────────┬─────┬────────────┬────────────┬──────────┬─────────────╮
│  nim   │     nama      │          mata_kuliah            │ sks │nilai_huruf │nilai_angka │ semester │   status    │
├────────┼───────────────┼─────────────────────────────────┼─────┼────────────┼────────────┼──────────┼─────────────┤
│2023001 │ Ahmad Rizki   │Automata dan Teknik Kompilasi    │  3  │     A      │    4.0     │    5     │    Lulus    │
│2023001 │ Ahmad Rizki   │         Struktur Data           │  3  │     A      │    4.0     │    3     │    Lulus    │
│ ...    │    ...        │            ...                  │ ... │    ...     │    ...     │   ...    │    ...      │
╰────────┴───────────────┴─────────────────────────────────┴─────┴────────────┴────────────┴──────────┴─────────────╯
✅ 22 baris ditemukan
```

### 9.2 Test Case 2: SELECT Kolom Tertentu

**Query:**
```sql
SELECT nim, nama, nilai_huruf FROM data_nilai.csv
```

**Hasil:**
```
╭────────┬───────────────┬────────────╮
│  nim   │     nama      │nilai_huruf │
├────────┼───────────────┼────────────┤
│2023001 │ Ahmad Rizki   │     A      │
│2023001 │ Ahmad Rizki   │     A      │
│2023001 │ Ahmad Rizki   │     B      │
│ ...    │    ...        │    ...     │
╰────────┴───────────────┴────────────╯
✅ 22 baris ditemukan
```

### 9.3 Test Case 3: Filter dengan WHERE

**Query:**
```sql
SELECT nama, mata_kuliah FROM data_nilai.csv WHERE nilai_huruf = "A"
```

**Hasil:**
```
╭───────────────┬─────────────────────────────────╮
│     nama      │          mata_kuliah            │
├───────────────┼─────────────────────────────────┤
│ Ahmad Rizki   │Automata dan Teknik Kompilasi    │
│ Ahmad Rizki   │         Struktur Data           │
│  Citra Dewi   │Automata dan Teknik Kompilasi    │
│  Citra Dewi   │         Struktur Data           │
│  Citra Dewi   │           Basis Data            │
│ Farhan Akbar  │Automata dan Teknik Kompilasi    │
│Gita Maharani  │         Struktur Data           │
╰───────────────┴─────────────────────────────────╯
✅ 7 baris ditemukan
```

### 9.4 Test Case 4: Mahasiswa Tidak Lulus

**Query:**
```sql
SELECT nim, nama, mata_kuliah, nilai_huruf FROM data_nilai.csv WHERE status = "Tidak Lulus"
```

**Hasil:**
```
╭────────┬──────────────┬─────────────────────────────────┬────────────╮
│  nim   │     nama     │          mata_kuliah            │nilai_huruf │
├────────┼──────────────┼─────────────────────────────────┼────────────┤
│2023004 │Dian Pratama  │         Struktur Data           │     D      │
│2023005 │  Eka Putri   │Automata dan Teknik Kompilasi    │     E      │
│2023005 │  Eka Putri   │           Basis Data            │     D      │
╰────────┴──────────────┴─────────────────────────────────┴────────────╯
✅ 3 baris ditemukan
```

### 9.5 Test Case 5: Kombinasi AND

**Query:**
```sql
SELECT * FROM data_nilai.csv WHERE semester = 5 AND nilai_huruf = "A"
```

**Hasil:**
```
╭────────┬───────────────┬─────────────────────────────────┬─────┬────────────┬────────────┬──────────┬────────╮
│  nim   │     nama      │          mata_kuliah            │ sks │nilai_huruf │nilai_angka │ semester │ status │
├────────┼───────────────┼─────────────────────────────────┼─────┼────────────┼────────────┼──────────┼────────┤
│2023001 │ Ahmad Rizki   │Automata dan Teknik Kompilasi    │  3  │     A      │    4.0     │    5     │ Lulus  │
│2023003 │  Citra Dewi   │Automata dan Teknik Kompilasi    │  3  │     A      │    4.0     │    5     │ Lulus  │
│2023006 │ Farhan Akbar  │Automata dan Teknik Kompilasi    │  3  │     A      │    4.0     │    5     │ Lulus  │
╰────────┴───────────────┴─────────────────────────────────┴─────┴────────────┴────────────┴──────────┴────────╯
✅ 3 baris ditemukan
```

### 9.6 Test Case: Error Handling

**Query dengan Kolom Tidak Ada:**
```sql
SELECT ipk FROM data_nilai.csv
```

**Output:**
```
❌ Semantic Error: Kolom 'ipk' tidak ada di data_nilai.csv
```

**Query dengan File Tidak Ada:**
```sql
SELECT * FROM tidak_ada.csv
```

**Output:**
```
❌ Semantic Error: File 'tidak_ada.csv' tidak ditemukan
```

---

## BAB X - Kesimpulan

### 10.1 Kesimpulan

Proyek CSV_QL berhasil mengimplementasikan mini query engine untuk data nilai mahasiswa dengan menerapkan konsep automata dan teknik kompilasi:

1. **Lexical Analyzer** - Berhasil diimplementasikan menggunakan DFA untuk tokenisasi query SQL dengan mendukung keywords, operators, identifiers, numbers, dan string literals.

2. **Parser** - Berhasil diimplementasikan menggunakan metode Recursive Descent dengan CFG yang mendukung SELECT, FROM, WHERE, dan LIMIT clauses.

3. **Semantic Analyzer** - Berhasil melakukan validasi file CSV, validasi kolom, dan menghasilkan pesan error/warning yang informatif.

4. **Intermediate Representation** - Berhasil membangun query plan yang menggambarkan langkah-langkah eksekusi (SCAN, FILTER, PROJECT, LIMIT).

5. **Execution Engine** - Berhasil mengeksekusi query terhadap file CSV dan mengembalikan hasil yang sesuai.

### 10.2 Saran Pengembangan

1. Mendukung klausa tambahan seperti ORDER BY, GROUP BY, dan HAVING
2. Mendukung fungsi agregat (COUNT, SUM, AVG, MIN, MAX)
3. Mendukung JOIN antar file CSV
4. Optimasi query plan untuk performa lebih baik
5. Mendukung INSERT, UPDATE, DELETE operations

---

## Daftar Pustaka

1. Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Addison-Wesley.

2. Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Pearson.

3. Grune, D., & Jacobs, C. J. (2007). *Parsing Techniques: A Practical Guide* (2nd ed.). Springer.

4. Python Software Foundation. (2024). *Python CSV Module Documentation*. https://docs.python.org/3/library/csv.html

5. Garcia-Molina, H., Ullman, J. D., & Widom, J. (2008). *Database Systems: The Complete Book* (2nd ed.). Pearson.

---

## Lampiran

### A. Struktur Direktori Proyek

```
csv_ql/
├── README.md              📖 Dokumentasi proyek
├── TEST_CASES.md          📋 Test cases
├── MAKALAH_CSV_QL.md      📄 Makalah ini
├── data_nilai.csv         📄 Data sampel
│
└── src/                   📂 Source code
    ├── main.py            ✅ Entry point & REPL
    ├── tokens.py          ✅ Definisi token
    ├── lexer.py           ✅ Lexical analyzer (DFA)
    ├── ast_nodes.py       ✅ Abstract Syntax Tree
    ├── parser.py          ✅ Syntax analyzer (CFG)
    ├── semantic.py        ✅ Semantic analyzer
    ├── ir.py              ✅ Intermediate representation
    ├── engine.py          ✅ Query execution
    └── dfa.py             ✅ DFA visualization
```

### B. Cara Menjalankan Program

```bash
cd csv_ql/src

# Mode REPL (Interactive)
python main.py

# Mode Direct Query
python main.py "SELECT * FROM ../data_nilai.csv"

# Mode Verbose (dengan detail kompilasi)
python main.py "SELECT * FROM ../data_nilai.csv" -v
```

### C. Screenshot Aplikasi

*(Tambahkan screenshot hasil running program)*

---

**Disusun oleh:**

[Nama Anggota Kelompok]

Mata Kuliah: Automata dan Teknik Kompilasi

Tahun Akademik: 2025/2026
