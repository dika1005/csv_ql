// src/semantic.rs
// Analisis Semantik: Validasi query sebelum eksekusi

use crate::ast::{Expr, Statement};
use std::collections::HashSet;
use std::error::Error;
use std::fs::File;

/// Hasil analisis semantik
#[derive(Debug)]
pub struct SemanticResult {
    pub valid: bool,
    pub errors: Vec<String>,
    pub warnings: Vec<String>,
}

/// Analisis semantik untuk query
pub fn analyze(query: &Statement) -> Result<SemanticResult, Box<dyn Error>> {
    let mut errors = Vec::new();
    let mut warnings = Vec::new();

    match query {
        Statement::Select { columns, table, where_clause, limit } => {
            // 1. Cek file CSV ada
            if !std::path::Path::new(table).exists() {
                errors.push(format!("File '{}' tidak ditemukan", table));
                return Ok(SemanticResult { valid: false, errors, warnings });
            }

            // 2. Baca header CSV untuk validasi kolom
            let file = File::open(table)?;
            let mut rdr = csv::Reader::from_reader(file);
            let headers: HashSet<String> = rdr
                .headers()?
                .iter()
                .map(|h| h.to_string())
                .collect();

            // 3. Validasi kolom yang di-SELECT
            for col in columns {
                if col != "*" && !headers.contains(col) {
                    errors.push(format!("Kolom '{}' tidak ada di file '{}'", col, table));
                }
            }

            // 4. Validasi kolom di WHERE clause
            if let Some(expr) = where_clause {
                validate_expr_columns(expr, &headers, &mut errors);
            }

            // 5. Validasi LIMIT
            if let Some(n) = limit {
                if *n == 0 {
                    warnings.push("LIMIT 0 akan mengembalikan 0 baris".to_string());
                }
            }

            // 6. Warning untuk SELECT *
            if columns.len() == 1 && columns[0] == "*" && columns.len() > 5 {
                warnings.push("SELECT * pada tabel besar bisa lambat".to_string());
            }
        }
    }

    Ok(SemanticResult {
        valid: errors.is_empty(),
        errors,
        warnings,
    })
}

/// Validasi kolom dalam ekspresi WHERE
fn validate_expr_columns(expr: &Expr, headers: &HashSet<String>, errors: &mut Vec<String>) {
    match expr {
        Expr::Identifier(name) => {
            if !headers.contains(name) {
                errors.push(format!("Kolom '{}' tidak ada di WHERE clause", name));
            }
        }
        Expr::BinaryOp { left, right, .. } => {
            validate_expr_columns(left, headers, errors);
            validate_expr_columns(right, headers, errors);
        }
        _ => {} // Number, StringLiteral, Literal tidak perlu validasi
    }
}
