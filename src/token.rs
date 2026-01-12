#[derive(Debug, PartialEq, Clone)]
#[allow(dead_code)]
pub enum Token {
        //keywords
        Select,
        From,
        Where,
        Limit,
        Or,
        And,
        OrderBy,
        GroupBy,

        //operators
        Equal,
        NotEqual,
        GreaterThan,
        LessThan,
        GreaterThanOrEq,
        LessThanOrEq,
        Star,

        //literal & identifiers
        Identifier(String),
        Number(f64),

        //punctuation
        Comma,

        ///special
        EOF,
    }