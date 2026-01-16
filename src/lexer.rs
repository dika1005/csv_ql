use std::iter::Peekable;
use std::str::Chars;
use crate::token::Token;

pub struct Lexer<'a> {
    input: Peekable<Chars<'a>>,
}

impl<'a> Lexer<'a> {
    pub fn new(input: &'a str) -> Self {
        Lexer {
            input: input.chars().peekable(),
        }
    }

    // Perhatikan: Semua fungsi di bawah ini masuk ke dalam kurung impl Lexer

    pub fn next_token(&mut self) -> Option<Token> {
        self.skip_whitespace();

        match self.input.peek() {
            None => None,
            // Kalau huruf/underscore -> Scan kata
            Some(c) if c.is_ascii_alphabetic() || *c == '_' => Some(self.scan_identifier()),
            // Kalau angka -> Scan nomor
            Some(c) if c.is_ascii_digit() => Some(self.scan_number()),
            // Kalau tanda kutip -> Scan string literal
            Some(&'"') | Some(&'\'') => Some(self.scan_string()),
            // Sisanya simbol
            Some(_) => self.scan_symbol(),
        }
    }

    fn skip_whitespace(&mut self) {
        while let Some(&c) = self.input.peek() {
            if c.is_whitespace() {
                self.input.next(); // Makan spasi
            } else {
                break;
            }
        }
    }

    fn scan_identifier(&mut self) -> Token {
        let mut text = String::new(); // Inisialisasi string dulu

        while let Some(&c) = self.input.peek() {
            // Kita izinkan alphanumeric dan underscore
            if c.is_ascii_alphanumeric() || c == '_' || c == '.' {
                text.push(c);
                self.input.next();
            } else {
                break;
            }
        }

        match text.as_str() {
            "SELECT" | "select" => Token::Select,
            "FROM" | "from" => Token::From,
            "WHERE" | "where" => Token::Where,
            "LIMIT" | "limit" => Token::Limit,
            "OR" | "or" => Token::Or,
            "AND" | "and" => Token::And,
            // "ORDER BY" dihapus dulu karena logic spasi (nanti dihandle Parser)
            _ => Token::Identifier(text),
        }
    }

    fn scan_number(&mut self) -> Token {
        let mut text = String::new();

        while let Some(&c) = self.input.peek() {
            if c.is_ascii_digit() || c == '.' {
                text.push(c);
                self.input.next();
            } else {
                break;
            } 
        }

        let value = text.parse::<f64>().unwrap_or(0.0);
        Token::Number(value)
    }

    fn scan_string(&mut self) -> Token {
        let quote = self.input.next().unwrap(); // Makan tanda kutip pembuka
        let mut text = String::new();

        while let Some(&c) = self.input.peek() {
            if c == quote {
                self.input.next(); // Makan tanda kutip penutup
                break;
            }
            text.push(c);
            self.input.next();
        }

        Token::StringLiteral(text)
    }

    fn scan_symbol(&mut self) -> Option<Token> {
        let c = self.input.next()?;

        match c {
            '*' => Some(Token::Star),
            ',' => Some(Token::Comma),
            '=' => Some(Token::Equal),
            '!' => {
                if let Some(&'=') = self.input.peek() {
                    self.input.next();
                    Some(Token::NotEqual)
                } else {
                    None
                }
            }
            '>' => {
                if let Some(&'=') = self.input.peek() {
                    self.input.next();
                    Some(Token::GreaterThanOrEq)
                } else {
                    Some(Token::GreaterThan)
                }
            }
            '<' => {
                if let Some(&'=') = self.input.peek() {
                    self.input.next();
                    Some(Token::LessThanOrEq)
                } else if let Some(&'>') = self.input.peek() {
                    self.input.next();
                    Some(Token::NotEqual)
                } else {
                    Some(Token::LessThan)
                }
            }
            '"' | '\'' => {
                // Kembalikan karakter dan scan string
                Some(Token::StringLiteral(String::new()))
            }
            _ => None,
        }
    }
}