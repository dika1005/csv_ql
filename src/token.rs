#[derive(Debug, PartialEq, Clone)]
pub enum Token {
    // Keywords
    Select,
    From,
    Where,
    Limit,
    Or,
    And,

    // Operators
    Equal,
    NotEqual,
    GreaterThan,
    LessThan,
    GreaterThanOrEq,
    LessThanOrEq,
    Star,

    // Literal & Identifiers
    Identifier(String),
    Number(f64),
    StringLiteral(String),

    // Punctuation
    Comma,

    // Special
    EOF,
}