#![allow(dead_code)]
#[derive(Debug, PartialEq, Clone)] 
pub enum Statement {
    Select {
        columns: Vec<String>,
        table: String,
        where_clause: Option<Expr>,
        limit: Option<usize>,
    },
}

#[derive(Debug, PartialEq, Clone)]
pub enum Expr {
    BinaryOp {
        left: Box<Expr>,
        op: Op,
        right: Box<Expr>,
    },
    Literal(String),
    Number(f64),
    Identifier(String),
}

#[derive(Debug, PartialEq, Clone)]
pub enum Op {
    Equal,
    NotEqual,
    GreaterThan,
    LessThan,
    GreaterThanOrEq,
    LessThanOrEq,
    Or,
    And,
}
