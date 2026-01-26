#!/usr/bin/env python3
"""
Script untuk generate MAKALAH_CSV_QL.docx (Max 10 halaman)
Sesuai format ketentuan Project Akhir Automata dan Teknik Kompilasi
Dengan penjelasan pengertian agar mudah dipahami
"""

from docx import Document
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT

def add_heading(doc, text, level=1):
    """Add a heading with proper formatting."""
    heading = doc.add_heading(text, level=level)
    return heading

def add_paragraph(doc, text, bold=False, italic=False):
    """Add a paragraph with optional formatting."""
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    return p

def add_code_block(doc, code):
    """Add a code block with monospace font."""
    p = doc.add_paragraph()
    run = p.add_run(code)
    run.font.name = 'Courier New'
    run.font.size = Pt(9)
    return p

def add_table(doc, headers, rows):
    """Add a table with headers and rows."""
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Table Grid'
    
    # Header row
    hdr_cells = table.rows[0].cells
    for i, header in enumerate(headers):
        hdr_cells[i].text = header
        for paragraph in hdr_cells[i].paragraphs:
            for run in paragraph.runs:
                run.bold = True
    
    # Data rows
    for row_data in rows:
        row_cells = table.add_row().cells
        for i, cell_text in enumerate(row_data):
            row_cells[i].text = str(cell_text)
    
    return table

def create_document():
    doc = Document()
    
    # Set margins untuk hemat ruang
    for section in doc.sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)
    
    # ==================== HALAMAN 1: JUDUL ====================
    doc.add_paragraph()
    doc.add_paragraph()
    
    title = doc.add_heading('', 0)
    title_run = title.add_run('DOKUMEN DESAIN')
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.add_run('PROJECT AKHIR\n').bold = True
    subtitle.add_run('MATA KULIAH AUTOMATA DAN TEKNIK KOMPILASI').bold = True
    
    doc.add_paragraph()
    doc.add_paragraph()
    
    project_title = doc.add_heading('CSV_QL: Mini Query Engine untuk Data Nilai Mahasiswa', level=1)
    project_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    tema = doc.add_paragraph()
    tema.alignment = WD_ALIGN_PARAGRAPH.CENTER
    tema.add_run('Tema: Big Data - Mini Query Engine berbasis SQL').italic = True
    
    doc.add_paragraph()
    doc.add_paragraph()
    doc.add_paragraph()
    doc.add_paragraph()
    
    info = doc.add_paragraph()
    info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    info.add_run('Disusun oleh:\n')
    info.add_run('[Nama Anggota Kelompok]\n\n')
    info.add_run('Tahun Akademik 2025/2026')
    
    doc.add_page_break()
    
    # ==================== HALAMAN 2: DAFTAR ISI ====================
    add_heading(doc, 'DAFTAR ISI', 1)
    
    toc_items = [
        ('1.', 'Deskripsi Tema dan Studi Kasus', '3'),
        ('2.', 'Daftar Token dan Regular Expression', '4'),
        ('3.', 'Sketsa NFA/DFA', '5'),
        ('4.', 'Context-Free Grammar (CFG)', '6'),
        ('5.', 'Desain Parser dan Sketsa AST', '7'),
        ('6.', 'Desain IR dan Alur Eksekusi', '8'),
        ('7.', 'Simulasi Automata (DFA) dan Contoh Input-Output', '9'),
        ('', 'Daftar Pustaka', '10'),
    ]
    
    for num, title, page in toc_items:
        p = doc.add_paragraph()
        if num:
            p.add_run(f'{num} ').bold = True
        p.add_run(f'{title}')
        p.add_run(f' {"." * 50} {page}')
    
    doc.add_page_break()
    
    # ==================== HALAMAN 3: DESKRIPSI TEMA DAN STUDI KASUS ====================
    add_heading(doc, '1. Deskripsi Tema dan Studi Kasus', 1)
    
    add_heading(doc, '1.1 Tema Project: Big Data - Mini Query Engine', 2)
    
    # Pengertian Big Data
    p = doc.add_paragraph()
    p.add_run('Pengertian Big Data: ').bold = True
    p.add_run('Big Data adalah istilah yang menggambarkan volume data yang sangat besar, baik terstruktur maupun tidak terstruktur. Karakteristik Big Data dikenal dengan 3V: Volume (ukuran data besar), Velocity (kecepatan data masuk), dan Variety (keragaman tipe data).')
    
    # Pengertian Query Engine
    p = doc.add_paragraph()
    p.add_run('Pengertian Query Engine: ').bold = True
    p.add_run('Query Engine adalah komponen perangkat lunak yang bertugas memproses dan mengeksekusi query (permintaan data) terhadap sumber data. Query engine menerima perintah dalam bentuk teks, menganalisis strukturnya, dan mengembalikan hasil yang sesuai.')
    
    # Pengertian DSL
    p = doc.add_paragraph()
    p.add_run('Pengertian DSL: ').bold = True
    p.add_run('Domain Specific Language (DSL) adalah bahasa pemrograman yang dirancang khusus untuk domain tertentu. Berbeda dengan bahasa general-purpose seperti Python atau Java, DSL memiliki sintaks yang lebih sederhana dan fokus pada satu tugas spesifik.')
    
    doc.add_paragraph(
        'CSV_QL adalah DSL yang kami kembangkan untuk melakukan query terhadap file CSV '
        'menggunakan sintaks mirip SQL. Proyek ini mengimplementasikan komponen-komponen compiler:'
    )
    doc.add_paragraph('• Lexer - Memecah query menjadi token-token (tokenisasi)')
    doc.add_paragraph('• Parser - Menganalisis struktur dan membangun AST')
    doc.add_paragraph('• Semantic Analyzer - Memvalidasi kebenaran makna query')
    doc.add_paragraph('• IR Generator - Membuat rencana eksekusi (Query Plan)')
    doc.add_paragraph('• Execution Engine - Menjalankan query terhadap data CSV')
    
    add_heading(doc, '1.2 Studi Kasus: Query Data Nilai Mahasiswa SIAKAD', 2)
    doc.add_paragraph(
        'Studi kasus yang dipilih adalah sistem query untuk data nilai mahasiswa dari SIAKAD. '
        'Data disimpan dalam format CSV dengan struktur kolom sebagai berikut:'
    )
    
    add_table(doc,
        ['Kolom', 'Tipe', 'Deskripsi'],
        [
            ['nim', 'String', 'Nomor Induk Mahasiswa'],
            ['nama', 'String', 'Nama lengkap mahasiswa'],
            ['mata_kuliah', 'String', 'Nama mata kuliah yang diambil'],
            ['sks', 'Number', 'Jumlah Satuan Kredit Semester'],
            ['nilai_huruf', 'String', 'Nilai dalam huruf (A, B, C, D, E)'],
            ['nilai_angka', 'Number', 'Nilai dalam angka (0.0 - 4.0)'],
            ['semester', 'Number', 'Semester pengambilan mata kuliah'],
            ['status', 'String', 'Status kelulusan (Lulus/Tidak Lulus)'],
        ]
    )
    
    doc.add_paragraph()
    add_heading(doc, '1.3 Contoh Query CSV_QL', 2)
    doc.add_paragraph('Berikut adalah contoh-contoh query yang dapat dijalankan dengan CSV_QL:')
    add_code_block(doc, '''-- Menampilkan semua data nilai
SELECT * FROM data_nilai.csv

-- Mencari mahasiswa dengan nilai A
SELECT nama, mata_kuliah FROM data_nilai.csv WHERE nilai_huruf = "A"

-- Kombinasi kondisi dengan operator AND
SELECT * FROM data_nilai.csv WHERE nilai_angka >= 3.0 AND semester = 5

-- Membatasi jumlah hasil dengan LIMIT
SELECT nama FROM data_nilai.csv LIMIT 5''')
    
    doc.add_page_break()
    
    # ==================== HALAMAN 4: TOKEN DAN REGEX ====================
    add_heading(doc, '2. Daftar Token dan Regular Expression', 1)
    
    # Pengertian Token
    p = doc.add_paragraph()
    p.add_run('Pengertian Token: ').bold = True
    p.add_run('Token adalah unit terkecil yang bermakna dalam sebuah bahasa pemrograman. Token merupakan hasil dari proses tokenisasi (lexical analysis). Setiap token memiliki tipe dan nilai. Contoh: kata "SELECT" adalah token dengan tipe KEYWORD.')
    
    # Pengertian Regular Expression
    p = doc.add_paragraph()
    p.add_run('Pengertian Regular Expression: ').bold = True
    p.add_run('Regular Expression (Regex) adalah notasi formal untuk mendeskripsikan pola string. Regex digunakan untuk mendefinisikan bagaimana suatu token dikenali. Misalnya, pola [0-9]+ berarti "satu atau lebih digit angka".')
    
    add_heading(doc, '2.1 Daftar Token CSV_QL', 2)
    add_table(doc,
        ['Kategori', 'Token', 'Pattern/Simbol'],
        [
            ['Keywords', 'SELECT, FROM, WHERE, LIMIT, AND, OR', 'Kata kunci SQL'],
            ['Operators', 'EQUAL', '='],
            ['', 'NOT_EQUAL', '!= atau <>'],
            ['', 'GREATER_THAN', '>'],
            ['', 'LESS_THAN', '<'],
            ['', 'GREATER_THAN_OR_EQ', '>='],
            ['', 'LESS_THAN_OR_EQ', '<='],
            ['', 'STAR', '*'],
            ['Literals', 'IDENTIFIER', 'Nama kolom/tabel'],
            ['', 'NUMBER', 'Angka (bulat/desimal)'],
            ['', 'STRING_LITERAL', 'Teks dalam tanda kutip'],
            ['Punctuation', 'COMMA', ','],
        ]
    )
    
    doc.add_paragraph()
    add_heading(doc, '2.2 Regular Expression untuk Setiap Token', 2)
    doc.add_paragraph('Berikut adalah pola regex yang digunakan untuk mengenali setiap jenis token:')
    add_code_block(doc, '''KEYWORD     := SELECT | FROM | WHERE | LIMIT | AND | OR
IDENTIFIER  := [a-zA-Z_][a-zA-Z0-9_.]*   (huruf/underscore, diikuti huruf/angka/titik)
NUMBER      := [0-9]+(\\.[0-9]+)?         (angka bulat atau desimal)
STRING      := "[^"]*" | '[^']*'         (teks dalam tanda kutip)
OPERATOR    := = | != | <> | > | < | >= | <=
SYMBOL      := * | ,
WHITESPACE  := [ \\t\\n\\r]+              (spasi, tab, newline - diabaikan)''')
    
    doc.add_paragraph()
    add_heading(doc, '2.3 Contoh Proses Tokenisasi', 2)
    doc.add_paragraph('Input query:')
    add_code_block(doc, 'SELECT nama FROM data.csv WHERE status = "Lulus"')
    doc.add_paragraph('Hasil tokenisasi:')
    add_code_block(doc, '''Token 1: (KEYWORD, "SELECT")
Token 2: (IDENTIFIER, "nama")
Token 3: (KEYWORD, "FROM")
Token 4: (IDENTIFIER, "data.csv")
Token 5: (KEYWORD, "WHERE")
Token 6: (IDENTIFIER, "status")
Token 7: (OPERATOR, "=")
Token 8: (STRING_LITERAL, "Lulus")''')
    
    doc.add_page_break()
    
    # ==================== HALAMAN 5: SKETSA NFA/DFA ====================
    add_heading(doc, '3. Sketsa NFA/DFA', 1)
    
    # Pengertian DFA
    p = doc.add_paragraph()
    p.add_run('Pengertian DFA: ').bold = True
    p.add_run('DFA (Deterministic Finite Automaton) adalah mesin abstrak yang terdiri dari himpunan state terbatas. DFA memproses input karakter per karakter dan berpindah dari satu state ke state lain berdasarkan fungsi transisi. DFA bersifat deterministik, artinya untuk setiap state dan input, hanya ada satu state tujuan yang mungkin.')
    
    # Pengertian NFA
    p = doc.add_paragraph()
    p.add_run('Pengertian NFA: ').bold = True
    p.add_run('NFA (Non-deterministic Finite Automaton) mirip dengan DFA, tetapi dapat memiliki beberapa transisi untuk input yang sama atau transisi epsilon (tanpa input). NFA dapat dikonversi menjadi DFA yang ekuivalen.')
    
    add_heading(doc, '3.1 Definisi Formal DFA Lexer', 2)
    doc.add_paragraph('DFA untuk lexer CSV_QL didefinisikan sebagai M = (Q, Σ, δ, q0, F):')
    doc.add_paragraph('• Q = {q0, q1, q2, q3, q4, qf} — Himpunan state (6 state)')
    doc.add_paragraph('• Σ = Karakter ASCII — Alphabet input')
    doc.add_paragraph('• δ = Fungsi transisi (lihat tabel di bawah)')
    doc.add_paragraph('• q0 = State awal (START)')
    doc.add_paragraph('• F = {qf} — Himpunan state akhir (accepting state)')
    
    add_heading(doc, '3.2 Diagram DFA Lexer', 2)
    doc.add_paragraph('Berikut adalah diagram transisi DFA untuk lexer CSV_QL:')
    add_code_block(doc, '''
       ┌─────────────────────────────────────────────────────────┐
       │                    DFA LEXER CSV_QL                     │
       ├─────────────────────────────────────────────────────────┤
       │                                                         │
       │      [a-zA-Z_]      ┌────────┐    whitespace/EOF        │
       │     ┌──────────────►│   q1   │────────────────► EMIT    │
       │     │               │ InIdent│    KEYWORD/IDENT         │
       │     │               └───┬────┘                          │
       │     │                   │ [a-zA-Z0-9_.]                 │
       │     │                   └───────┘ (loop)                │
       │   ┌─┴───┐                                               │
       │   │ q0  │   [0-9]   ┌────────┐    whitespace/EOF        │
       │   │START│──────────►│   q2   │────────────────► EMIT    │
       │   └─┬───┘           │ InNum  │       NUMBER             │
       │     │               └───┬────┘                          │
       │     │                   │ [0-9.]                        │
       │     │                   └───────┘ (loop)                │
       │     │                                                   │
       │     │   " atau '    ┌────────┐    " atau '              │
       │     └──────────────►│   q3   │────────────────► EMIT    │
       │     │               │ InStr  │    STRING_LITERAL        │
       │     │               └───┬────┘                          │
       │     │                   │ [karakter lain]               │
       │     │                   └───────┘ (loop)                │
       │     │                                                   │
       │     │   = > < !     ┌────────┐                          │
       │     └──────────────►│   q4   │────────────────► EMIT    │
       │                     │ InOper │       OPERATOR           │
       │                     └────────┘                          │
       └─────────────────────────────────────────────────────────┘
''')
    
    add_heading(doc, '3.3 Tabel Transisi DFA', 2)
    add_table(doc,
        ['State Asal', 'Input', 'State Tujuan', 'Aksi'],
        [
            ['q0 (Start)', 'Huruf a-z, A-Z, _', 'q1 (InIdent)', 'Mulai baca identifier'],
            ['q0', 'Digit 0-9', 'q2 (InNumber)', 'Mulai baca angka'],
            ['q0', 'Tanda kutip " atau \'', 'q3 (InString)', 'Mulai baca string'],
            ['q0', 'Operator = > < !', 'q4 (InOper)', 'Mulai baca operator'],
            ['q0', 'Simbol * atau ,', 'qf (Accept)', 'Emit token simbol'],
            ['q0', 'Whitespace', 'q0', 'Skip (abaikan)'],
            ['q1', 'Huruf/digit/titik', 'q1', 'Lanjut baca identifier'],
            ['q1', 'Karakter lain', 'qf', 'Emit IDENTIFIER/KEYWORD'],
            ['q2', 'Digit atau titik', 'q2', 'Lanjut baca angka'],
            ['q2', 'Karakter lain', 'qf', 'Emit NUMBER'],
            ['q3', 'Bukan tanda kutip', 'q3', 'Lanjut baca string'],
            ['q3', 'Tanda kutip penutup', 'qf', 'Emit STRING_LITERAL'],
        ]
    )
    
    doc.add_page_break()
    
    # ==================== HALAMAN 6: CFG ====================
    add_heading(doc, '4. Context-Free Grammar (CFG)', 1)
    
    # Pengertian CFG
    p = doc.add_paragraph()
    p.add_run('Pengertian CFG: ').bold = True
    p.add_run('Context-Free Grammar (CFG) adalah notasi formal untuk mendefinisikan struktur sintaksis suatu bahasa. CFG terdiri dari: (1) Terminal - simbol dasar/token, (2) Non-terminal - variabel yang dapat diturunkan, (3) Production Rules - aturan penurunan, dan (4) Start Symbol - simbol awal penurunan.')
    
    # Pengertian BNF
    p = doc.add_paragraph()
    p.add_run('Pengertian BNF: ').bold = True
    p.add_run('Backus-Naur Form (BNF) adalah notasi standar untuk menuliskan CFG. Simbol ::= berarti "didefinisikan sebagai", | berarti "atau", dan [...] berarti "opsional".')
    
    add_heading(doc, '4.1 Grammar CSV_QL dalam BNF', 2)
    add_code_block(doc, '''<query>        ::= <select_stmt>

<select_stmt>  ::= SELECT <columns> FROM <table> [<where_clause>] [<limit_clause>]

<columns>      ::= STAR                        -- Simbol * untuk semua kolom
                 | <column_list>               -- Atau daftar kolom spesifik

<column_list>  ::= IDENTIFIER (COMMA IDENTIFIER)*   -- Satu atau lebih nama kolom

<table>        ::= IDENTIFIER                  -- Nama file CSV

<where_clause> ::= WHERE <expression>          -- Klausa filter (opsional)

<limit_clause> ::= LIMIT NUMBER                -- Batasan hasil (opsional)

<expression>   ::= <or_expr>                   -- Ekspresi logika

<or_expr>      ::= <and_expr> (OR <and_expr>)* -- Operasi OR

<and_expr>     ::= <comparison> (AND <comparison>)*  -- Operasi AND

<comparison>   ::= <leaf> [<comp_op> <leaf>]   -- Perbandingan nilai

<comp_op>      ::= EQUAL | NOT_EQUAL | GREATER_THAN | LESS_THAN 
                 | GREATER_THAN_OR_EQ | LESS_THAN_OR_EQ

<leaf>         ::= IDENTIFIER | NUMBER | STRING_LITERAL  -- Nilai dasar''')
    
    add_heading(doc, '4.2 Operator Precedence (Prioritas Operator)', 2)
    doc.add_paragraph('Urutan prioritas operator dari yang terendah ke tertinggi:')
    add_table(doc,
        ['Level', 'Operator', 'Associativity', 'Keterangan'],
        [
            ['1 (terendah)', 'OR', 'Left-to-right', 'Diproses terakhir'],
            ['2', 'AND', 'Left-to-right', 'Diproses setelah perbandingan'],
            ['3 (tertinggi)', '=, !=, >, <, >=, <=', 'Left-to-right', 'Diproses pertama'],
        ]
    )
    
    add_heading(doc, '4.3 Komponen CFG', 2)
    doc.add_paragraph('• Terminal (Token): SELECT, FROM, WHERE, LIMIT, AND, OR, STAR, COMMA, EQUAL, NOT_EQUAL, GREATER_THAN, LESS_THAN, GREATER_THAN_OR_EQ, LESS_THAN_OR_EQ, IDENTIFIER, NUMBER, STRING_LITERAL')
    doc.add_paragraph('• Non-terminal: query, select_stmt, columns, column_list, table, where_clause, limit_clause, expression, or_expr, and_expr, comparison, comp_op, leaf')
    doc.add_paragraph('• Start Symbol: <query>')
    
    doc.add_page_break()
    
    # ==================== HALAMAN 7: PARSER DAN AST ====================
    add_heading(doc, '5. Desain Parser dan Sketsa AST', 1)
    
    # Pengertian Parser
    p = doc.add_paragraph()
    p.add_run('Pengertian Parser: ').bold = True
    p.add_run('Parser adalah komponen compiler yang menganalisis struktur sintaksis dari urutan token. Parser memeriksa apakah urutan token sesuai dengan grammar dan membangun representasi struktur program (biasanya berupa tree).')
    
    # Pengertian Recursive Descent
    p = doc.add_paragraph()
    p.add_run('Pengertian Recursive Descent: ').bold = True
    p.add_run('Recursive Descent adalah teknik parsing top-down dimana setiap non-terminal dalam grammar diimplementasikan sebagai satu fungsi. Fungsi-fungsi ini saling memanggil secara rekursif sesuai dengan aturan grammar.')
    
    add_heading(doc, '5.1 Desain Parser: Recursive Descent (LL(1))', 2)
    doc.add_paragraph('Setiap non-terminal dalam grammar diimplementasikan sebagai fungsi:')
    doc.add_paragraph('• parse() → Fungsi utama, memanggil parse_select()')
    doc.add_paragraph('• parse_select() → Mem-parse "SELECT columns FROM table..."')
    doc.add_paragraph('• parse_columns() → Mem-parse daftar kolom atau simbol *')
    doc.add_paragraph('• parse_expression() → Mem-parse ekspresi dalam WHERE')
    doc.add_paragraph('• parse_logic_or() → Mem-parse operasi logika OR')
    doc.add_paragraph('• parse_logic_and() → Mem-parse operasi logika AND')
    doc.add_paragraph('• parse_comparison() → Mem-parse perbandingan (a = b, x > 5, dll)')
    
    # Pengertian AST
    p = doc.add_paragraph()
    p.add_run('Pengertian AST: ').bold = True
    p.add_run('Abstract Syntax Tree (AST) adalah representasi pohon dari struktur program. Berbeda dengan parse tree yang lengkap, AST hanya menyimpan informasi yang relevan untuk pemrosesan lebih lanjut (semantic analysis, code generation).')
    
    add_heading(doc, '5.2 Sketsa Struktur AST', 2)
    add_code_block(doc, '''SelectStatement                    -- Node utama untuk SELECT query
├── columns: List[str]             -- Daftar kolom: ["nama", "nilai"] atau ["*"]
├── table: str                     -- Nama file CSV: "data_nilai.csv"
├── where_clause: Optional[Expr]   -- Kondisi filter (bisa None jika tidak ada)
│   └── BinaryOp                   -- Operasi biner (perbandingan/logika)
│       ├── left: Expr             -- Operand kiri
│       ├── op: Operator           -- Operator (=, AND, OR, >, <, dll)
│       └── right: Expr            -- Operand kanan
└── limit: Optional[int]           -- Batas hasil (bisa None jika tidak ada)

Tipe Expr (Expression):
• BinaryOp      -- Operasi dengan 2 operand (a = b, x AND y)
• Identifier    -- Nama kolom (contoh: "nama", "nilai_angka")
• Number        -- Nilai angka (contoh: 3.0, 5)
• StringLiteral -- Nilai string (contoh: "Lulus", "A")''')
    
    add_heading(doc, '5.3 Contoh AST untuk Query', 2)
    doc.add_paragraph('Query: SELECT nama FROM data.csv WHERE nilai >= 3.0 AND status = "Lulus"')
    add_code_block(doc, '''SelectStatement
├── columns: ["nama"]
├── table: "data.csv"
├── where_clause:
│   └── BinaryOp (operator: AND)
│       ├── left: BinaryOp (operator: >=)
│       │   ├── left: Identifier("nilai")
│       │   └── right: Number(3.0)
│       └── right: BinaryOp (operator: =)
│           ├── left: Identifier("status")
│           └── right: StringLiteral("Lulus")
└── limit: None''')
    
    doc.add_page_break()
    
    # ==================== HALAMAN 8: IR DAN ALUR EKSEKUSI ====================
    add_heading(doc, '6. Desain IR dan Alur Eksekusi', 1)
    
    # Pengertian IR
    p = doc.add_paragraph()
    p.add_run('Pengertian Intermediate Representation (IR): ').bold = True
    p.add_run('IR adalah representasi antara kode sumber dan kode akhir. IR memudahkan optimasi dan memisahkan front-end (parsing) dari back-end (eksekusi). Dalam query engine, IR berupa Query Plan yang menggambarkan langkah-langkah eksekusi.')
    
    # Pengertian Query Plan
    p = doc.add_paragraph()
    p.add_run('Pengertian Query Plan: ').bold = True
    p.add_run('Query Plan adalah rencana eksekusi yang menjelaskan urutan operasi untuk menjalankan query. Setiap langkah dalam plan melakukan satu operasi spesifik terhadap data.')
    
    add_heading(doc, '6.1 Desain Query Plan (IR)', 2)
    doc.add_paragraph('Query Plan CSV_QL terdiri dari 4 jenis langkah yang dieksekusi secara berurutan:')
    
    add_table(doc,
        ['Step', 'Operasi', 'Deskripsi', 'Contoh'],
        [
            ['1', 'SCAN', 'Membaca seluruh baris dari file CSV', 'SCAN("data.csv")'],
            ['2', 'FILTER', 'Menyaring baris yang memenuhi kondisi WHERE', 'FILTER(status = "Lulus")'],
            ['3', 'PROJECT', 'Memilih kolom yang diminta dalam SELECT', 'PROJECT(["nama", "nilai"])'],
            ['4', 'LIMIT', 'Membatasi jumlah hasil output', 'LIMIT(5)'],
        ]
    )
    
    add_heading(doc, '6.2 Struktur Data Query Plan', 2)
    add_code_block(doc, '''@dataclass
class ScanStep:
    table: str              # Nama file CSV yang dibaca

@dataclass
class FilterStep:
    condition: str          # Kondisi filter dari WHERE clause

@dataclass
class ProjectStep:
    columns: List[str]      # Daftar kolom yang dipilih

@dataclass
class LimitStep:
    count: int              # Jumlah maksimal hasil

@dataclass
class QueryPlan:
    steps: List[PlanStep]   # Urutan langkah eksekusi''')
    
    add_heading(doc, '6.3 Alur Eksekusi (Compilation Pipeline)', 2)
    doc.add_paragraph('Berikut adalah alur lengkap dari query string hingga hasil eksekusi:')
    add_code_block(doc, '''Query String (input pengguna)
        ↓
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│    LEXER    │ → │   PARSER    │ → │  SEMANTIC   │ → │     IR      │ → │   ENGINE    │
│ (Tokenisasi)│   │(Bangun AST) │   │ (Validasi)  │   │(Query Plan) │   │ (Eksekusi)  │
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘
        ↓                ↓                ↓                ↓                 ↓
    Tokens             AST           Validated         QueryPlan        Result Set
  (daftar token)   (pohon sintaks)  (AST valid)    (rencana eksekusi)  (hasil query)''')
    
    add_heading(doc, '6.4 Contoh Query Plan', 2)
    doc.add_paragraph('Query: SELECT nama, nilai FROM data.csv WHERE status = "Lulus" LIMIT 5')
    add_code_block(doc, '''Query Plan yang dihasilkan:
  Step 1: SCAN(table="data.csv")           -- Baca 22 baris dari CSV
  Step 2: FILTER(condition='status="Lulus"') -- 18 baris lolos filter
  Step 3: PROJECT(columns=["nama","nilai"])  -- Pilih 2 kolom
  Step 4: LIMIT(count=5)                     -- Ambil 5 baris pertama
  
  Output: 5 baris × 2 kolom''')
    
    doc.add_page_break()
    
    # ==================== HALAMAN 9: SIMULASI DFA DAN CONTOH ====================
    add_heading(doc, '7. Simulasi Automata (DFA) dan Contoh Input-Output', 1)
    
    add_heading(doc, '7.1 Simulasi DFA Lexer', 2)
    doc.add_paragraph('Berikut adalah simulasi langkah demi langkah DFA saat memproses query:')
    doc.add_paragraph('Input: SELECT nama FROM data.csv')
    
    add_table(doc,
        ['Step', 'State', 'Karakter', 'State Baru', 'Token yang Dihasilkan'],
        [
            ['1-6', 'q0→q1', 'S,E,L,E,C,T', 'q1', '(belum emit)'],
            ['7', 'q1', 'spasi', 'qf→q0', 'KEYWORD("SELECT")'],
            ['8-11', 'q0→q1', 'n,a,m,a', 'q1', '(belum emit)'],
            ['12', 'q1', 'spasi', 'qf→q0', 'IDENTIFIER("nama")'],
            ['13-16', 'q0→q1', 'F,R,O,M', 'q1', '(belum emit)'],
            ['17', 'q1', 'spasi', 'qf→q0', 'KEYWORD("FROM")'],
            ['18-25', 'q0→q1', 'd,a,t,a,.,c,s,v', 'q1', '(belum emit)'],
            ['26', 'q1', 'EOF', 'qf', 'IDENTIFIER("data.csv")'],
        ]
    )
    
    add_heading(doc, '7.2 Contoh Input-Output Program', 2)
    
    doc.add_paragraph('Test Case 1: SELECT semua data')
    add_code_block(doc, '''Input:  SELECT * FROM data_nilai.csv
Output: ✅ 22 baris × 8 kolom ditemukan''')
    
    doc.add_paragraph('Test Case 2: Filter dengan WHERE')
    add_code_block(doc, '''Input:  SELECT nama, mata_kuliah FROM data_nilai.csv WHERE nilai_huruf = "A"
Output: ✅ 7 baris ditemukan
        | nama          | mata_kuliah                    |
        | Ahmad Rizki   | Automata dan Teknik Kompilasi  |
        | Ahmad Rizki   | Struktur Data                  |
        | Citra Dewi    | Automata dan Teknik Kompilasi  |
        | ...           | ...                            |''')
    
    doc.add_paragraph('Test Case 3: Kombinasi kondisi AND')
    add_code_block(doc, '''Input:  SELECT * FROM data_nilai.csv WHERE semester = 5 AND nilai_huruf = "A"
Output: ✅ 3 baris ditemukan''')
    
    doc.add_paragraph('Test Case 4: Menggunakan LIMIT')
    add_code_block(doc, '''Input:  SELECT nama FROM data_nilai.csv LIMIT 3
Output: ✅ 3 baris ditemukan (dibatasi dari 22 total)''')
    
    doc.add_paragraph('Test Case 5: Error Handling - Kolom tidak ada')
    add_code_block(doc, '''Input:  SELECT ipk FROM data_nilai.csv
Output: ❌ Semantic Error: Kolom 'ipk' tidak ditemukan di data_nilai.csv
        Kolom yang tersedia: nim, nama, mata_kuliah, sks, nilai_huruf, 
                             nilai_angka, semester, status''')
    
    doc.add_page_break()
    
    # ==================== HALAMAN 10: DAFTAR PUSTAKA ====================
    add_heading(doc, 'DAFTAR PUSTAKA', 1)
    
    references = [
        'Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). Compilers: Principles, Techniques, and Tools (2nd ed.). Addison-Wesley. — Buku referensi utama tentang teknik kompilasi.',
        'Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). Introduction to Automata Theory, Languages, and Computation (3rd ed.). Pearson. — Referensi teori automata dan bahasa formal.',
        'Grune, D., & Jacobs, C. J. (2007). Parsing Techniques: A Practical Guide (2nd ed.). Springer. — Panduan praktis teknik parsing.',
        'Python Software Foundation. (2024). Python CSV Module Documentation. https://docs.python.org/3/library/csv.html — Dokumentasi modul CSV Python.',
        'Garcia-Molina, H., Ullman, J. D., & Widom, J. (2008). Database Systems: The Complete Book (2nd ed.). Pearson. — Referensi sistem database dan query processing.',
    ]
    
    for i, ref in enumerate(references, 1):
        doc.add_paragraph(f'[{i}] {ref}')
    
    doc.add_paragraph()
    add_heading(doc, 'LAMPIRAN', 1)
    
    add_heading(doc, 'A. Struktur Direktori Proyek', 2)
    add_code_block(doc, '''csv_ql/
├── src/                     # Source code
│   ├── main.py              # Entry point & REPL interaktif
│   ├── tokens.py            # Definisi tipe token
│   ├── lexer.py             # Lexical analyzer (implementasi DFA)
│   ├── ast_nodes.py         # Struktur node AST
│   ├── parser.py            # Syntax analyzer (recursive descent)
│   ├── semantic.py          # Semantic analyzer (validasi)
│   ├── ir.py                # Query plan generator
│   ├── engine.py            # Query execution engine
│   └── dfa.py               # Visualisasi DFA
├── data_nilai.csv           # Data sampel untuk testing
└── README.md                # Dokumentasi proyek''')
    
    add_heading(doc, 'B. Cara Menjalankan Program', 2)
    add_code_block(doc, '''# Masuk ke direktori source
cd csv_ql/src

# Mode REPL (Interactive) - ketik query satu per satu
python main.py

# Mode Direct Query - langsung eksekusi satu query
python main.py "SELECT * FROM ../data_nilai.csv"

# Mode Verbose - tampilkan detail proses kompilasi
python main.py "SELECT * FROM ../data_nilai.csv" -v''')
    
    return doc

if __name__ == '__main__':
    doc = create_document()
    doc.save('MAKALAH_CSV_QL_v2.docx')
    print('✅ MAKALAH_CSV_QL_v2.docx berhasil dibuat! (Max 10 halaman dengan penjelasan)')
