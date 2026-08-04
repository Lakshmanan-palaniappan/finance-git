# Customer Schema

## Purpose

Stores customer master information.

## Source

Customer Management System

## Frequency

Daily

## Processing

Batch

CDC

SCD Type 2

---

## Columns

| Column | Type | Nullable | Description |
|----------|------|----------|-------------|
| customer_id | STRING | No | Customer Identifier |
| first_name | STRING | No | Customer First Name |
| last_name | STRING | No | Customer Last Name |
| dob | DATE | No | Date of Birth |
| gender | STRING | Yes | Gender |
| email | STRING | Yes | Email |
| phone | STRING | No | Phone Number |
| pan | STRING | No | PAN Number |
| aadhaar | STRING | No | Aadhaar Number |
| occupation | STRING | Yes | Occupation |
| annual_income | DECIMAL | Yes | Annual Income |
| branch_id | STRING | No | Home Branch |
| customer_status | STRING | No | Active/Inactive |
| created_date | TIMESTAMP | No | Created Timestamp |
| updated_date | TIMESTAMP | No | Updated Timestamp |

---

## Validation

Customer ID Unique

PAN Unique

Aadhaar Unique

Age > 18