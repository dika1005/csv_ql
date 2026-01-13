use crate::token::Token;
use crate::ast::{Statement, Expr, Op};

// 1. KOREKSI: Definisi Struct harus dipisah!
// Jangan taruh function di dalam sini.
pub struct Parser {
    tokens: Vec<Token>,
    pos: usize,
}

// 2. KOREKSI: Semua fungsi masuk ke dalam blok `impl` ini
impl Parser {
    pub fn new(tokens: Vec<Token>) -> Self {
        Parser { tokens, pos: 0 }
    }

    // --- HELPER METHODS ---

    fn current(&self) -> Option<&Token> {
        self.tokens.get(self.pos)
    }

    fn advance(&mut self) {
        self.pos += 1;
    }

    fn match_token(&mut self, expected: Token) -> bool {
        if let Some(token) = self.current() {
            if token == &expected {
                self.advance();
                return true;
            }
        }
        false
    }

    // --- CORE LOGIC ---

    pub fn parse(&mut self) -> Result<Statement, String> {
        self.parse_select() // Typo fix: prase -> parse
    }

    // KOREKSI: Logic parsing harus ada DI DALAM kurung kurawal fungsi ini
    fn parse_select(&mut self) -> Result<Statement, String> {
        // 3. KOREKSI: Cek SELECT dulu, jangan langsung return Err!
        if !self.match_token(Token::Select) {
            return Err("Query harus diawali dengan SELECT".to_string());
        }

        // Parse Kolom
        let columns = self.parse_columns()?;

        // Cek FROM
        if !self.match_token(Token::From) {
            return Err("Harap sertakan FROM setelah kolom".to_string());
        }

        // Ambil Nama Table
        let table = match self.current() {
            Some(Token::Identifier(name)) => {
                let n = name.clone();
                self.advance();
                n
            }
            _ => return Err("Harap sertakan nama tabel/file setelah FROM".to_string()),
        };

        // Cek WHERE (Opsional)
        let mut where_clause = None;
        if self.match_token(Token::Where) {
            let expr = self.parse_expression()?;
            where_clause = Some(expr);
        }

        // Cek LIMIT (Opsional)
        let mut limit = None;
        if self.match_token(Token::Limit) {
            match self.current() {
                Some(Token::Number(val)) => {
                    limit = Some(*val as usize);
                    self.advance(); // 4. KOREKSI: Jangan lupa advance (makan) angkanya!
                }
                _ => return Err("Limit harus diikuti dengan angka".to_string()),
            }
        }

        Ok(Statement::Select {
            columns,
            table,
            where_clause,
            limit,
        })
    }

    fn parse_columns(&mut self) -> Result<Vec<String>, String> {
        let mut columns = Vec::new();

        loop {
            match self.current() {
                Some(Token::Identifier(name)) => {
                    columns.push(name.clone());
                    self.advance();
                }
                Some(Token::Star) => {
                    columns.push("*".to_string());
                    self.advance();
                }
                _ => return Err("Harap sertakan nama kolom setelah SELECT".to_string()),
            }
            
            // Kalau gak ada koma, berhenti loop
            if !self.match_token(Token::Comma) {
                break;
            }
        }
        Ok(columns)
    }

    fn parse_expression(&mut self) -> Result<Expr, String> {
        self.parse_logic_or()
    }

    fn parse_logic_or(&mut self) -> Result<Expr, String> {
        let mut left = self.parse_logic_and()?;

        while self.match_token(Token::Or) {
            let op = Op::Or;

            let right = self.parse_logic_and()?;

            left = Expr::BinaryOp {
                left: Box::new(left),
                op,
                right: Box::new(right),
            };
        }
        Ok(left)
    }

    fn parse_logic_and(&mut self) -> Result<Expr, String> {
        let mut left = self.parse_comparsion()?;

        while self.match_token(Token::And) {
            let op = Op::And;

            let right = self.parse_comparsion()?;

            left = Expr::BinaryOp {
                left: Box::new(left),
                op,
                right: Box::new(right),
            };
        }
        Ok(left)
    }

    // Typo fix: prase -> parse
    fn parse_comparsion(&mut self) -> Result<Expr, String> {
        let left = self.parse_leaf()?;

        let op = match self.current() {
            Some(Token::Equal) => Op::Equal,
            Some(Token::NotEqual) => Op::NotEqual,
            Some(Token::GreaterThan) => Op::GreaterThan,
            Some(Token::LessThan) => Op::LessThan,
            Some(Token::GreaterThanOrEq) => Op::GreaterThanOrEq,
            Some(Token::LessThanOrEq) => Op::LessThanOrEq,
            _ => return Ok(left), // Kalau gak ada operator, balikin kiri aja
        };

        self.advance(); // Makan operatornya
        let right = self.parse_comparsion()?;

        Ok(Expr::BinaryOp {
            left: Box::new(left),
            op,
            right: Box::new(right),
        })
    }

    fn parse_leaf(&mut self) -> Result<Expr, String> {
        match self.current() {
            Some(Token::Identifier(s)) => {
                let e = Expr::Identifier(s.clone());
                self.advance();
                Ok(e)
            }
            Some(Token::Number(n)) => {
                let e = Expr::Number(*n);
                self.advance();
                Ok(e)
            }
            _ => Err("Harap sertakan identifier atau number".to_string()),
        }
    }
}