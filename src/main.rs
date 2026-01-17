mod ast;
mod dfa;
mod engine;
mod ir;
mod lexer;
mod parser;
mod semantic;
mod token;

use dfa::DFATracker;
use engine::execute_query;
use ir::{ast_to_ir, print_query_plan};
use lexer::Lexer;
use parser::Parser;
use semantic::analyze;
use std::env;
use std::io::{self, Write};

// ═══════════════════════════════════════════════════════════════════════════════
// WARNA TERMINAL (ANSI Escape Codes)
// ═══════════════════════════════════════════════════════════════════════════════
const RESET: &str = "\x1b[0m";
const BOLD: &str = "\x1b[1m";
const CYAN: &str = "\x1b[36m";
const GREEN: &str = "\x1b[32m";
const YELLOW: &str = "\x1b[33m";
const RED: &str = "\x1b[31m";
const WHITE: &str = "\x1b[37m";
const MAGENTA: &str = "\x1b[35m";
const DIM: &str = "\x1b[2m";

// ═══════════════════════════════════════════════════════════════════════════════
// TAMPILAN UI
// ═══════════════════════════════════════════════════════════════════════════════
fn print_banner() {
    println!("\n{CYAN}{BOLD}");
    println!("  ╔═══════════════════════════════════════════════════╗");
    println!("  ║         CSV_QL - Mini SQL untuk File CSV          ║");
    println!("  ╚═══════════════════════════════════════════════════╝");
    println!("{RESET}");
}

fn print_help() {
    println!("
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
     SELECT * FROM data.csv WHERE kota = \"Jakarta\"

  {GREEN}4. Kombinasi kondisi (AND/OR):{RESET}
     SELECT * FROM data.csv WHERE umur > 20 AND umur < 30
     SELECT * FROM data.csv WHERE kota = \"Jakarta\" OR kota = \"Bandung\"

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
");
}

// ═══════════════════════════════════════════════════════════════════════════════
// EKSEKUSI QUERY - Pipeline Kompilasi
// ═══════════════════════════════════════════════════════════════════════════════
fn execute_sql(input: &str, verbose: bool) {
    println!("\n  {DIM}Query: {input}{RESET}");

    // ┌─────────────────────────────────────────────────────────────────────────┐
    // │ TAHAP 1: LEXICAL ANALYSIS (String → Tokens)                            │
    // └─────────────────────────────────────────────────────────────────────────┘
    let mut lexer = Lexer::new(input);
    let tokens: Vec<_> = std::iter::from_fn(|| lexer.next_token()).collect();
    
    if verbose {
        println!("\n  {CYAN}[1] LEXICAL ANALYSIS{RESET}");
        println!("  Tokens: {:?}", tokens);
    }

    // ┌─────────────────────────────────────────────────────────────────────────┐
    // │ TAHAP 2: SYNTAX ANALYSIS / PARSING (Tokens → AST)                      │
    // └─────────────────────────────────────────────────────────────────────────┘
    let mut parser = Parser::new(tokens);
    let ast = match parser.parse() {
        Ok(ast) => ast,
        Err(e) => return println!("  {RED}❌ Parse Error: {e}{RESET}\n"),
    };
    
    if verbose {
        println!("\n  {CYAN}[2] SYNTAX ANALYSIS{RESET}");
        println!("  AST: {:?}", ast);
    }

    // ┌─────────────────────────────────────────────────────────────────────────┐
    // │ TAHAP 3: SEMANTIC ANALYSIS (Validasi AST)                              │
    // └─────────────────────────────────────────────────────────────────────────┘
    match analyze(&ast) {
        Ok(result) => {
            if verbose {
                println!("\n  {CYAN}[3] SEMANTIC ANALYSIS{RESET}");
            }
            
            // Tampilkan warning jika ada
            for warn in &result.warnings {
                println!("  {YELLOW}⚠️ Warning: {warn}{RESET}");
            }
            
            // Stop jika ada error semantik
            if !result.valid {
                for err in &result.errors {
                    println!("  {RED}❌ Semantic Error: {err}{RESET}");
                }
                return;
            }
            
            if verbose {
                println!("  ✓ Validasi OK");
            }
        }
        Err(e) => return println!("  {RED}❌ Semantic Error: {e}{RESET}\n"),
    }

    // ┌─────────────────────────────────────────────────────────────────────────┐
    // │ TAHAP 4: IR GENERATION (AST → Query Plan)                              │
    // └─────────────────────────────────────────────────────────────────────────┘
    let query_plan = ast_to_ir(&ast);
    
    if verbose {
        println!("\n  {CYAN}[4] IR GENERATION{RESET}");
        print_query_plan(&query_plan);
    }

    // ┌─────────────────────────────────────────────────────────────────────────┐
    // │ TAHAP 5: EXECUTION (Jalankan Query Plan)                               │
    // └─────────────────────────────────────────────────────────────────────────┘
    if verbose {
        println!("\n  {CYAN}[5] EXECUTION{RESET}");
    }
    
    match execute_query(ast) {
        Ok((_, rows)) if rows.is_empty() => {
            println!("  {YELLOW}⚠️ Tidak ada data yang cocok.{RESET}\n");
        }
        Ok((headers, rows)) => print_table(&headers, &rows),
        Err(e) => println!("  {RED}❌ Runtime Error: {e}{RESET}\n"),
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// TAMPILKAN TABEL
// ═══════════════════════════════════════════════════════════════════════════════
fn print_table(headers: &[String], rows: &[Vec<String>]) {
    // Hitung lebar kolom
    let widths: Vec<usize> = headers
        .iter()
        .enumerate()
        .map(|(i, h)| {
            let max_data = rows.iter().filter_map(|r| r.get(i)).map(|c| c.len()).max().unwrap_or(0);
            h.len().max(max_data) + 2
        })
        .collect();

    // Fungsi helper untuk buat garis
    let line = |left: &str, mid: &str, right: &str| {
        print!("  {CYAN}{left}");
        for (i, w) in widths.iter().enumerate() {
            print!("{}", "─".repeat(*w));
            print!("{}", if i < widths.len() - 1 { mid } else { right });
        }
        println!("{RESET}");
    };

    // Print tabel
    line("╭", "┬", "╮");
    
    // Header
    print!("  {CYAN}│{RESET}");
    for (i, h) in headers.iter().enumerate() {
        print!("{YELLOW}{BOLD} {:^w$}{RESET}{CYAN}│{RESET}", h, w = widths[i] - 1);
    }
    println!();
    
    line("├", "┼", "┤");

    // Data rows
    for row in rows {
        print!("  {CYAN}│{RESET}");
        for (i, cell) in row.iter().enumerate() {
            if i < widths.len() {
                print!("{WHITE} {:^w$}{RESET}{CYAN}│{RESET}", cell, w = widths[i] - 1);
            }
        }
        println!();
    }
    
    line("╰", "┴", "╯");
    println!("  {GREEN}✅ {} baris ditemukan{RESET}\n", rows.len());
}

// ═══════════════════════════════════════════════════════════════════════════════
// MAIN - Entry Point
// ═══════════════════════════════════════════════════════════════════════════════
fn main() {
    let args: Vec<String> = env::args().collect();

    // Cek flag --verbose atau -v
    let verbose = args.iter().any(|a| a == "--verbose" || a == "-v");
    
    // Mode 1: Direct query dari command line
    // Contoh: csv_ql "SELECT * FROM data.csv"
    // Contoh: csv_ql "SELECT * FROM data.csv" --verbose
    if args.len() > 1 && !args[1].starts_with('-') {
        let query: String = args[1..].iter()
            .filter(|a| *a != "--verbose" && *a != "-v")
            .cloned()
            .collect::<Vec<_>>()
            .join(" ");
        print_banner();
        execute_sql(&query, verbose);
        return;
    }

    // Mode 2: Interactive REPL
    print_banner();
    println!("  Ketik {MAGENTA}help{RESET} untuk bantuan, {MAGENTA}exit{RESET} untuk keluar.");
    println!("  Tambahkan {MAGENTA}--verbose{RESET} di akhir query untuk lihat detail kompilasi.\n");

    loop {
        // Tampilkan prompt
        print!("  {CYAN}{BOLD}csv_ql>{RESET} ");
        io::stdout().flush().unwrap();

        // Baca input
        let mut input = String::new();
        if io::stdin().read_line(&mut input).unwrap_or(0) == 0 {
            break; // EOF
        }

        let input = input.trim();
        let verbose_mode = input.ends_with("--verbose") || input.ends_with("-v");
        let clean_input = input
            .replace("--verbose", "")
            .replace("-v", "")
            .trim()
            .to_string();

        // Proses perintah
        match clean_input.to_lowercase().as_str() {
            "" => continue,
            "exit" | "quit" | "q" => {
                println!("\n  {GREEN}👋 Sampai jumpa!{RESET}\n");
                break;
            }
            "help" | "?" => print_help(),
            "clear" | "cls" => {
                print!("\x1b[2J\x1b[H");
                print_banner();
            }
            "dfa" => DFATracker::print_dfa_diagram(),
            _ => execute_sql(&clean_input, verbose_mode),
        }
    }
}