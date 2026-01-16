// src/engine.rs

use crate::ast::{Expr, Op, Statement};
use std::collections::HashMap;
use std::error::Error;
use std::fs::File;

/// Eksekusi query dan kembalikan hasil sebagai (headers, rows)
pub fn execute_query(query: Statement) -> Result<(Vec<String>, Vec<Vec<String>>), Box<dyn Error>> {
    match query {
        Statement::Select {
            columns,
            table,
            where_clause,
            limit,
        } => {
            // 1. Buka File CSV
            let file =
                File::open(&table).map_err(|_| format!("Gagal membuka file: {}", table))?;
            let mut rdr = csv::Reader::from_reader(file);

            // 2. Baca Header (Nama Kolom)
            let headers = rdr.headers()?.clone();
            let mut col_map = HashMap::new();
            for (i, h) in headers.iter().enumerate() {
                col_map.insert(h.to_string(), i);
            }

            // 3. Tentukan kolom output
            let output_headers: Vec<String> = if columns.len() == 1 && columns[0] == "*" {
                headers.iter().map(|s| s.to_string()).collect()
            } else {
                columns.clone()
            };

            // 4. Loop Data Baris per Baris
            let mut count = 0;
            let mut results: Vec<Vec<String>> = Vec::new();

            for result in rdr.records() {
                let record = result?;

                // 5. Cek WHERE (Filter)
                if let Some(ref expr) = where_clause {
                    if !eval(expr, &record, &col_map) {
                        continue;
                    }
                }

                // 6. Ambil Data Terpilih
                let mut row_output = Vec::new();
                for col_name in &columns {
                    if col_name == "*" {
                        for field in &record {
                            row_output.push(field.to_string());
                        }
                    } else if let Some(&idx) = col_map.get(col_name) {
                        if let Some(val) = record.get(idx) {
                            row_output.push(val.to_string());
                        }
                    }
                }
                results.push(row_output);

                // 7. Cek LIMIT
                count += 1;
                if let Some(max) = limit {
                    if count >= max {
                        break;
                    }
                }
            }

            Ok((output_headers, results))
        }
    }
}

fn eval(expr: &Expr, row: &csv::StringRecord, col_map: &HashMap<String, usize>) -> bool {
    match expr {
        Expr::BinaryOp { left, op, right } => {
            match op {
                // KELOMPOK 1: LOGIKA (AND / OR)
                Op::And => {
                    let left_is_correct = eval(left, row, col_map);
                    let right_is_correct = eval(right, row, col_map);
                    left_is_correct && right_is_correct
                }
                Op::Or => {
                    let left_is_correct = eval(left, row, col_map);
                    let right_is_correct = eval(right, row, col_map);
                    left_is_correct || right_is_correct
                }

                // KELOMPOK 2: PERBANDINGAN STRING (untuk Identifier vs StringLiteral)
                Op::Equal | Op::NotEqual => {
                    // Cek apakah ini perbandingan string
                    if let (Some(left_str), Some(right_str)) =
                        (get_string_value(left, row, col_map), get_string_value(right, row, col_map))
                    {
                        match op {
                            Op::Equal => left_str == right_str,
                            Op::NotEqual => left_str != right_str,
                            _ => false,
                        }
                    } else {
                        // Fallback ke perbandingan numerik
                        let left_val = get_value(left, row, col_map);
                        let right_val = get_value(right, row, col_map);
                        match op {
                            Op::Equal => (left_val - right_val).abs() < f64::EPSILON,
                            Op::NotEqual => (left_val - right_val).abs() > f64::EPSILON,
                            _ => false,
                        }
                    }
                }

                // KELOMPOK 3: PERBANDINGAN NUMERIK
                _ => {
                    let left_val = get_value(left, row, col_map);
                    let right_val = get_value(right, row, col_map);

                    match op {
                        Op::GreaterThan => left_val > right_val,
                        Op::LessThan => left_val < right_val,
                        Op::GreaterThanOrEq => left_val >= right_val,
                        Op::LessThanOrEq => left_val <= right_val,
                        _ => false,
                    }
                }
            }
        }
        _ => false,
    }
}

// Helper untuk mengambil nilai string dari ekspresi
fn get_string_value(expr: &Expr, row: &csv::StringRecord, col_map: &HashMap<String, usize>) -> Option<String> {
    match expr {
        Expr::StringLiteral(s) => Some(s.clone()),
        Expr::Literal(s) => Some(s.clone()),
        Expr::Identifier(col_name) => {
            if let Some(&idx) = col_map.get(col_name) {
                row.get(idx).map(|s| s.to_string())
            } else {
                None
            }
        }
        _ => None,
    }
}

// Helper untuk mengambil nilai numerik dari ekspresi
fn get_value(expr: &Expr, row: &csv::StringRecord, col_map: &HashMap<String, usize>) -> f64 {
    match expr {
        Expr::Number(n) => *n,
        Expr::Identifier(col_name) => {
            if let Some(&idx) = col_map.get(col_name) {
                if let Some(val_str) = row.get(idx) {
                    return val_str.parse::<f64>().unwrap_or(0.0);
                }
            }
            0.0
        }
        _ => 0.0,
    }
}