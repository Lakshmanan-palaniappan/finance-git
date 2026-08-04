# Transaction Schema

## Purpose

Streaming banking transactions.

## Frequency

Every 2 Minutes

## Processing

Streaming

## Columns

transaction_id

account_id

transaction_timestamp

transaction_type

amount

currency

merchant_id

channel

branch_id

status

---

Validation

Amount > 0

Account Exists

Timestamp Mandatory