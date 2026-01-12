// src/engine.rs

use std::error::Error;
use std::fs::File;
use std::collections::HashMap;
use crate::ast::{Statement, Expr, Op};

// Fungsi utama yang dipanggil main.rs
pub fn execute(query: Statement) -> Result<(), Box<dyn Error>> {
    match query {
        Statement::Select { columns, table, where_clause, limit } => {
            println!("Eksekusi: Membaca file '{}'...", table);
            
            // 1. Buka File CSV
            // Kita pakai library 'csv' yang sudah ada di Cargo.toml
            let file = File::open(&table).map_err(|_| format!("Gagal membuka file: {}", table))?;
            let mut rdr = csv::Reader::from_reader(file);

            // 2. Baca Header (Nama Kolom)
            // Kita butuh tau "umur" itu index ke berapa? 0, 1, atau 2?
            let headers = rdr.headers()?.clone();
            let mut col_map = HashMap::new();
            for (i, h) in headers.iter().enumerate() {
                col_map.insert(h.to_string(), i); // Contoh: "nama" -> 0, "umur" -> 1
            }

            // 3. Loop Data Baris per Baris
            let mut count = 0;
            let mut printed_header = false;

            for result in rdr.records() {
                let record = result?; // Isinya baris data: ["Dika", "20"]

                // 4. Cek WHERE (Filter)
                // Kalau ada syarat, kita cek dulu. Kalau gak lolos, skip (continue).
                if let Some(ref expr) = where_clause {
                    if !eval(expr, &record, &col_map) {
                        continue; 
                    }
                }

                // 5. Print Header (Cuma sekali)
                if !printed_header {
                    println!("Hasil Pencarian:");
                    // Print nama kolom yang diminta user
                    println!("{:?}", columns); 
                    println!("---------------------------");
                    printed_header = true;
                }

                // 6. Print Data Terpilih
                let mut row_output = Vec::new();
                for col_name in &columns {
                    if col_name == "*" {
                        // Kalau *, ambil semua
                        for field in &record {
                            row_output.push(field.to_string());
                        }
                    } else {
                        // Ambil kolom spesifik berdasarkan index
                        if let Some(&idx) = col_map.get(col_name) {
                            if let Some(val) = record.get(idx) {
                                row_output.push(val.to_string());
                            }
                        }
                    }
                }
                println!("{:?}", row_output);

                // 7. Cek LIMIT
                count += 1;
                if let Some(max) = limit {
                    if count >= max {
                        break;
                    }
                }
            }
            println!("---------------------------");
            println!("Total data ditemukan: {}", count);
        }
    }
    Ok(())
}

// --- LOGIC EVALUATOR (The Brain) ---
// Ini fungsi rekursif buat ngecek "Apakah umur > 20?"
fn eval(expr: &Expr, row: &csv::StringRecord, col_map: &HashMap<String, usize>) -> bool {
    match expr {
        // Logika Perbandingan (Binary Operation)
        Expr::BinaryOp { left, op, right } => {
            // Kita perlu ambil NILAI kiri dan kanan
            let left_val = get_value(left, row, col_map);
            let right_val = get_value(right, row, col_map);

            match op {
                Op::GreaterThan => left_val > right_val,
                Op::LessThan => left_val < right_val,
                Op::Equal => (left_val - right_val).abs() < f64::EPSILON, // Cara bandingin float
                Op::NotEqual => (left_val - right_val).abs() > f64::EPSILON,
                Op::GreaterThanOrEq => left_val >= right_val,
                Op::LessThanOrEq => left_val <= right_val,
            }
        }
        _ => false, // Harusnya expr utama selalu BinaryOp di implementasi ini
    }
}

// Helper buat ngambil nilai angka dari CSV atau AST
fn get_value(expr: &Expr, row: &csv::StringRecord, col_map: &HashMap<String, usize>) -> f64 {
    match expr {
        // Kalau ketemu angka di query (misal 20)
        Expr::Number(n) => *n,
        
        // Kalau ketemu kolom (misal "umur"), kita cari di CSV
        Expr::Identifier(col_name) => {
            if let Some(&idx) = col_map.get(col_name) {
                if let Some(val_str) = row.get(idx) {
                    // Coba ubah string CSV jadi float
                    return val_str.parse::<f64>().unwrap_or(0.0);
                }
            }
            0.0 // Default kalau kolom gak ketemu
        }
        _ => 0.0,
    }
}