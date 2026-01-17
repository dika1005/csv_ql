// src/ir.rs
// Intermediate Representation (IR) - Query Plan sederhana

use crate::ast::{Expr, Op, Statement};

/// Query Plan - representasi langkah eksekusi
#[derive(Debug)]
pub struct QueryPlan {
    pub steps: Vec<PlanStep>,
}

/// Setiap langkah dalam query plan
#[derive(Debug)]
pub enum PlanStep {
    /// Langkah 1: Baca file CSV
    Scan { table: String },
    
    /// Langkah 2: Filter baris (WHERE)
    Filter { condition: String },
    
    /// Langkah 3: Pilih kolom (SELECT)
    Project { columns: Vec<String> },
    
    /// Langkah 4: Batasi hasil (LIMIT)
    Limit { count: usize },
}

/// Konversi AST ke Query Plan (IR)
pub fn ast_to_ir(ast: &Statement) -> QueryPlan {
    let mut steps = Vec::new();

    match ast {
        Statement::Select { columns, table, where_clause, limit } => {
            // Step 1: SCAN - baca tabel
            steps.push(PlanStep::Scan { table: table.clone() });

            // Step 2: FILTER - jika ada WHERE
            if let Some(expr) = where_clause {
                steps.push(PlanStep::Filter { 
                    condition: expr_to_string(expr) 
                });
            }

            // Step 3: PROJECT - pilih kolom
            steps.push(PlanStep::Project { columns: columns.clone() });

            // Step 4: LIMIT - jika ada
            if let Some(n) = limit {
                steps.push(PlanStep::Limit { count: *n });
            }
        }
    }

    QueryPlan { steps }
}

/// Tampilkan Query Plan
pub fn print_query_plan(plan: &QueryPlan) {
    println!("\n  📋 QUERY PLAN (IR):");
    println!("  ┌─────────────────────────────────────────────────┐");
    
    for (i, step) in plan.steps.iter().enumerate() {
        let (icon, desc) = match step {
            PlanStep::Scan { table } => ("📂", format!("SCAN: {}", table)),
            PlanStep::Filter { condition } => ("🔍", format!("FILTER: {}", condition)),
            PlanStep::Project { columns } => ("📊", format!("PROJECT: {}", columns.join(", "))),
            PlanStep::Limit { count } => ("✂️", format!("LIMIT: {}", count)),
        };
        
        println!("  │  {}. {} {}{}│", i + 1, icon, desc, " ".repeat(44 - desc.len().min(44)));
        
        if i < plan.steps.len() - 1 {
            println!("  │       ↓                                        │");
        }
    }
    
    println!("  └─────────────────────────────────────────────────┘");
}

/// Konversi Expr ke string untuk tampilan
fn expr_to_string(expr: &Expr) -> String {
    match expr {
        Expr::Number(n) => n.to_string(),
        Expr::Identifier(s) => s.clone(),
        Expr::StringLiteral(s) => format!("\"{}\"", s),
        Expr::Literal(s) => s.clone(),
        Expr::BinaryOp { left, op, right } => {
            let op_str = match op {
                Op::Equal => "=",
                Op::NotEqual => "!=",
                Op::GreaterThan => ">",
                Op::LessThan => "<",
                Op::GreaterThanOrEq => ">=",
                Op::LessThanOrEq => "<=",
                Op::And => "AND",
                Op::Or => "OR",
            };
            format!("{} {} {}", expr_to_string(left), op_str, expr_to_string(right))
        }
    }
}
