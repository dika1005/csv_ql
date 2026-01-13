mod token;
mod lexer;
mod ast;
mod parser;
mod engine; 

use lexer::Lexer;
use parser::Parser;
use engine::execute;

fn main() {
    // KITA TES LOGIC:
    // Cari yang umurnya DI ATAS 20 -DAN- DI BAWAH 30
    // Harusnya yang keluar cuma: Dika (22), Siti (25), Gita (29)
    let input = "SELECT nama, umur FROM data.csv WHERE umur > 20 AND umur < 30 LIMIT 5";

    println!("---------------------------------------------------");
    println!("INPUT QUERY: \n{}", input);
    println!("---------------------------------------------------");

    // 1. Lexing
    let mut lexer = Lexer::new(input);
    let mut tokens = Vec::new();
    while let Some(token) = lexer.next_token() {
        tokens.push(token);
    }
    
    // 2. Parsing
    let mut parser = Parser::new(tokens);
    let ast = match parser.parse() {
        Ok(tree) => {
            println!("STATUS: Parsing Berhasil ✅");
            // Lihat betapa cantiknya Tree bertingkat ini:
            println!("AST: \n{:#?}", tree); 
            tree
        },
        Err(e) => {
            eprintln!("STATUS: Parsing Gagal ❌\nError: {}", e);
            return;
        }
    };

    println!("---------------------------------------------------");
    println!("STATUS: Menjalankan Engine... 🚀");
    println!("---------------------------------------------------");

    // 3. Execution
    if let Err(e) = execute(ast) {
        eprintln!("Runtime Error: {}", e);
    }
}