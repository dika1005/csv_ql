mod ast;
mod engine;
mod lexer;
mod parser;
mod token;

use engine::execute_query;
use lexer::Lexer;
use parser::Parser;
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
  {MAGENTA}help{RESET}  - Tampilkan bantuan ini
  {MAGENTA}clear{RESET} - Bersihkan layar  
  {MAGENTA}exit{RESET}  - Keluar program

{YELLOW}═══════════════════════════════════════════════════════════════════════════════{RESET}
");
}

// ═══════════════════════════════════════════════════════════════════════════════
// EKSEKUSI QUERY
// ═══════════════════════════════════════════════════════════════════════════════
fn execute_sql(input: &str) {
    println!("\n  {DIM}Query: {input}{RESET}");

    // 1. Lexing (pecah string jadi tokens)
    let mut lexer = Lexer::new(input);
    let tokens: Vec<_> = std::iter::from_fn(|| lexer.next_token()).collect();

    // 2. Parsing (tokens jadi AST)
    let mut parser = Parser::new(tokens);
    let ast = match parser.parse() {
        Ok(ast) => ast,
        Err(e) => return println!("  {RED}❌ Parse Error: {e}{RESET}\n"),
    };

    // 3. Execute (jalankan query)
    match execute_query(ast) {
        Ok((_, rows)) if rows.is_empty() => {
            println!("  {YELLOW}⚠️ Tidak ada data yang cocok.{RESET}\n");
        }
        Ok((headers, rows)) => print_table(&headers, &rows),
        Err(e) => println!("  {RED}❌ Error: {e}{RESET}\n"),
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

    // Mode 1: Direct query dari command line
    // Contoh: csv_ql "SELECT * FROM data.csv"
    if args.len() > 1 {
        print_banner();
        execute_sql(&args[1..].join(" "));
        return;
    }

    // Mode 2: Interactive REPL
    print_banner();
    println!("  Ketik {MAGENTA}help{RESET} untuk bantuan, {MAGENTA}exit{RESET} untuk keluar.\n");

    loop {
        // Tampilkan prompt
        print!("  {CYAN}{BOLD}csv_ql>{RESET} ");
        io::stdout().flush().unwrap();

        // Baca input
        let mut input = String::new();
        if io::stdin().read_line(&mut input).unwrap_or(0) == 0 {
            break; // EOF
        }

        // Proses perintah
        match input.trim().to_lowercase().as_str() {
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
            _ => execute_sql(input.trim()),
        }
    }
}