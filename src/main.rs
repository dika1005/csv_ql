mod token;
mod lexer;
mod ast;
mod parser;
mod engine; // <-- Tambah ini

use lexer::Lexer;
use parser::Parser;
use engine::execute; // <-- Tambah ini

fn main() {
    // Query Tes
    let input = "SELECT nama, umur FROM data.csv WHERE umur > 20 LIMIT 3";
    println!("Query: {}", input);
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
        Ok(res) => res,
        Err(e) => {
            eprintln!("Error Parsing: {}", e);
            return;
        }
    };

    // 3. Execution
    if let Err(e) = execute(ast) {
        eprintln!("Error Eksekusi: {}", e);
    }
}