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

// ANSI Color Codes
const RESET: &str = "\x1b[0m";
const BOLD: &str = "\x1b[1m";
const DIM: &str = "\x1b[2m";
const ITALIC: &str = "\x1b[3m";

const RED: &str = "\x1b[31m";
const GREEN: &str = "\x1b[32m";
const YELLOW: &str = "\x1b[33m";
const BLUE: &str = "\x1b[34m";
const MAGENTA: &str = "\x1b[35m";
const CYAN: &str = "\x1b[36m";
const WHITE: &str = "\x1b[37m";

const BG_BLUE: &str = "\x1b[44m";
const BG_GRAY: &str = "\x1b[48;5;236m";

fn print_banner() {
    println!();
    println!("  {CYAN}{BOLD}╔══════════════════════════════════════════════════════════════╗{RESET}");
    println!("  {CYAN}{BOLD}║{RESET}  {YELLOW}{BOLD}  ██████╗███████╗██╗   ██╗     ██████╗ ██╗     {RESET}         {CYAN}{BOLD}║{RESET}");
    println!("  {CYAN}{BOLD}║{RESET}  {YELLOW}{BOLD} ██╔════╝██╔════╝██║   ██║    ██╔═══██╗██║     {RESET}         {CYAN}{BOLD}║{RESET}");
    println!("  {CYAN}{BOLD}║{RESET}  {YELLOW}{BOLD} ██║     ███████╗██║   ██║    ██║   ██║██║     {RESET}         {CYAN}{BOLD}║{RESET}");
    println!("  {CYAN}{BOLD}║{RESET}  {YELLOW}{BOLD} ██║     ╚════██║╚██╗ ██╔╝    ██║▄▄ ██║██║     {RESET}         {CYAN}{BOLD}║{RESET}");
    println!("  {CYAN}{BOLD}║{RESET}  {YELLOW}{BOLD} ╚██████╗███████║ ╚████╔╝     ╚██████╔╝███████╗{RESET}         {CYAN}{BOLD}║{RESET}");
    println!("  {CYAN}{BOLD}║{RESET}  {YELLOW}{BOLD}  ╚═════╝╚══════╝  ╚═══╝       ╚══▀▀═╝ ╚══════╝{RESET}         {CYAN}{BOLD}║{RESET}");
    println!("  {CYAN}{BOLD}║{RESET}                                                              {CYAN}{BOLD}║{RESET}");
    println!("  {CYAN}{BOLD}║{RESET}  {WHITE}{ITALIC}     Mini SQL Engine untuk Query File CSV{RESET}               {CYAN}{BOLD}║{RESET}");
    println!("  {CYAN}{BOLD}╚══════════════════════════════════════════════════════════════╝{RESET}");
    println!();
}

fn print_help() {
    println!("  {BLUE}{BOLD}📚 BANTUAN PENGGUNAAN{RESET}");
    println!("  {DIM}─────────────────────────────────────────────────────{RESET}");
    println!();
    println!("  {YELLOW}{BOLD}Syntax:{RESET}");
    println!("    SELECT <kolom> FROM <file.csv> [WHERE <kondisi>] [LIMIT n]");
    println!();
    println!("  {YELLOW}{BOLD}Contoh Query:{RESET}");
    println!("    {GREEN}• SELECT * FROM data.csv{RESET}");
    println!("    {GREEN}• SELECT nama, umur FROM data.csv{RESET}");
    println!("    {GREEN}• SELECT * FROM data.csv WHERE umur > 20{RESET}");
    println!("    {GREEN}• SELECT * FROM data.csv WHERE umur > 20 AND umur < 30{RESET}");
    println!("    {GREEN}• SELECT * FROM data.csv WHERE kota = \"Jakarta\"{RESET}");
    println!("    {GREEN}• SELECT * FROM data.csv LIMIT 5{RESET}");
    println!();
    println!("  {YELLOW}{BOLD}Operator:{RESET}");
    println!("    {CYAN}=  !=  >  <  >=  <=  AND  OR{RESET}");
    println!();
    println!("  {YELLOW}{BOLD}Perintah:{RESET}");
    println!("    {MAGENTA}help{RESET}    - Tampilkan bantuan ini");
    println!("    {MAGENTA}clear{RESET}   - Bersihkan layar");
    println!("    {MAGENTA}exit{RESET}    - Keluar dari program");
    println!();
}

fn print_divider() {
    println!("  {DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}");
}

fn execute_sql(input: &str) {
    println!();
    println!("  {BLUE}{BOLD}📝 Query:{RESET} {WHITE}{input}{RESET}");
    print_divider();

    // Lexing
    let mut lexer = Lexer::new(input);
    let mut tokens = Vec::new();
    while let Some(token) = lexer.next_token() {
        tokens.push(token);
    }

    // Parsing
    let mut parser = Parser::new(tokens);
    match parser.parse() {
        Ok(ast) => {
            // Execute
            match execute_query(ast) {
                Ok((headers, rows)) => {
                    if rows.is_empty() {
                        println!("  {YELLOW}⚠️  Tidak ada data yang cocok dengan query.{RESET}");
                    } else {
                        print_table(&headers, &rows);
                    }
                }
                Err(e) => {
                    println!("  {RED}{BOLD}❌ Runtime Error:{RESET} {RED}{e}{RESET}");
                }
            }
        }
        Err(e) => {
            println!("  {RED}{BOLD}❌ Parse Error:{RESET} {RED}{e}{RESET}");
        }
    }
    println!();
}

fn print_table(headers: &[String], rows: &[Vec<String>]) {
    // Calculate column widths
    let mut widths: Vec<usize> = headers.iter().map(|h| h.len()).collect();
    for row in rows {
        for (i, cell) in row.iter().enumerate() {
            if i < widths.len() && cell.len() > widths[i] {
                widths[i] = cell.len();
            }
        }
    }

    // Add padding
    for w in &mut widths {
        *w += 2;
    }

    // Print top border
    print!("  {CYAN}╭");
    for (i, w) in widths.iter().enumerate() {
        print!("{}", "─".repeat(*w));
        if i < widths.len() - 1 {
            print!("┬");
        }
    }
    println!("╮{RESET}");

    // Print headers
    print!("  {CYAN}│{RESET}");
    for (i, header) in headers.iter().enumerate() {
        print!("{BG_GRAY}{YELLOW}{BOLD} {:^width$}{RESET}", header, width = widths[i] - 1);
        print!("{CYAN}│{RESET}");
    }
    println!();

    // Print header separator
    print!("  {CYAN}├");
    for (i, w) in widths.iter().enumerate() {
        print!("{}", "─".repeat(*w));
        if i < widths.len() - 1 {
            print!("┼");
        }
    }
    println!("┤{RESET}");

    // Print rows
    for (row_idx, row) in rows.iter().enumerate() {
        let bg = if row_idx % 2 == 0 { "" } else { "\x1b[48;5;234m" };
        print!("  {CYAN}│{RESET}");
        for (i, cell) in row.iter().enumerate() {
            if i < widths.len() {
                print!("{bg}{WHITE} {:^width$}{RESET}", cell, width = widths[i] - 1);
                print!("{CYAN}│{RESET}");
            }
        }
        println!();
    }

    // Print bottom border
    print!("  {CYAN}╰");
    for (i, w) in widths.iter().enumerate() {
        print!("{}", "─".repeat(*w));
        if i < widths.len() - 1 {
            print!("┴");
        }
    }
    println!("╯{RESET}");

    // Print summary
    println!();
    println!("  {GREEN}{BOLD}✅ {}{RESET} {GREEN}baris ditemukan{RESET}", rows.len());
}

fn main() {
    let args: Vec<String> = env::args().collect();

    // Direct query mode: csv_ql "SELECT * FROM data.csv"
    if args.len() > 1 {
        let query = args[1..].join(" ");
        print_banner();
        execute_sql(&query);
        return;
    }

    // Interactive REPL mode
    print_banner();
    println!("  {WHITE}Ketik {MAGENTA}{BOLD}help{RESET}{WHITE} untuk bantuan, {MAGENTA}{BOLD}exit{RESET}{WHITE} untuk keluar.{RESET}");
    println!();

    loop {
        print!("  {CYAN}{BOLD}csv_ql>{RESET} ");
        io::stdout().flush().unwrap();

        let mut input = String::new();
        match io::stdin().read_line(&mut input) {
            Ok(0) => break, // EOF
            Ok(_) => {
                let input = input.trim();
                if input.is_empty() {
                    continue;
                }

                match input.to_lowercase().as_str() {
                    "exit" | "quit" | "q" => {
                        println!();
                        println!("  {GREEN}👋 Sampai jumpa!{RESET}");
                        println!();
                        break;
                    }
                    "help" | "?" => {
                        println!();
                        print_help();
                    }
                    "clear" | "cls" => {
                        print!("\x1b[2J\x1b[H");
                        print_banner();
                    }
                    _ => {
                        execute_sql(input);
                    }
                }
            }
            Err(e) => {
                println!("  {RED}Error membaca input: {e}{RESET}");
                break;
            }
        }
    }
}