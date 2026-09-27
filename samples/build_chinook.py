#!/usr/bin/env python3
"""Build a tiny Chinook-like SQLite database for the interview demo."""
from __future__ import annotations

import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent / "chinook.sqlite"

DDL = """
DROP TABLE IF EXISTS Invoice;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Customer;

CREATE TABLE Artist (
  ArtistId INTEGER PRIMARY KEY,
  Name TEXT NOT NULL
);
CREATE TABLE Album (
  AlbumId INTEGER PRIMARY KEY,
  Title TEXT NOT NULL,
  ArtistId INTEGER NOT NULL,
  FOREIGN KEY (ArtistId) REFERENCES Artist(ArtistId)
);
CREATE TABLE Track (
  TrackId INTEGER PRIMARY KEY,
  Name TEXT NOT NULL,
  AlbumId INTEGER,
  MediaTypeId INTEGER,
  GenreId INTEGER,
  Composer TEXT,
  Milliseconds INTEGER,
  Bytes INTEGER,
  UnitPrice REAL,
  FOREIGN KEY (AlbumId) REFERENCES Album(AlbumId)
);
CREATE TABLE Customer (
  CustomerId INTEGER PRIMARY KEY,
  FirstName TEXT,
  LastName TEXT,
  Country TEXT
);
CREATE TABLE Invoice (
  InvoiceId INTEGER PRIMARY KEY,
  CustomerId INTEGER NOT NULL,
  InvoiceDate TEXT NOT NULL,
  BillingAddress TEXT,
  BillingCity TEXT,
  BillingState TEXT,
  BillingCountry TEXT,
  BillingPostalCode TEXT,
  Total REAL NOT NULL,
  FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId)
);
"""

ARTISTS = [
    (1, "AC/DC"),
    (2, "Accept"),
    (3, "Aerosmith"),
    (4, "Alanis Morissette"),
    (5, "Alice In Chains"),
]
ALBUMS = [
    (1, "For Those About To Rock We Salute You", 1),
    (2, "Balls to the Wall", 2),
    (3, "Restless and Wild", 2),
    (4, "Let There Be Rock", 1),
    (5, "Big Ones", 3),
    (6, "Jagged Little Pill", 4),
    (7, "Facelift", 5),
]
TRACKS = [
    (1, "For Those About To Rock (We Salute You)", 1, 1, 1, "Young, Young, Scott", 343719, 11170334, 0.99),
    (2, "Balls to the Wall", 2, 1, 1, None, 342562, 5510424, 0.99),
    (3, "Fast As a Shark", 3, 1, 1, "F. Baltes, S. Kaufman, U. Dirkscneider & W. Hoffman", 230619, 3990994, 0.99),
    (4, "Restless and Wild", 3, 1, 1, "F. Baltes, R.A. Smith-Diesel, S. Kaufman, U. Dirkscneider & W. Hoffman", 252051, 4331779, 0.99),
    (5, "Go Down", 4, 1, 1, "AC/DC", 331180, 10847611, 0.99),
    (6, "Dog Eat Dog", 4, 1, 1, "AC/DC", 215196, 7032162, 0.99),
    (7, "Walk On Water", 5, 1, 1, "Steven Tyler, Joe Perry, Jack Blades, Tommy Shaw", 295680, 9719579, 0.99),
    (8, "Love In An Elevator", 5, 1, 1, "Steven Tyler, Joe Perry", 321656, 10552072, 0.99),
    (9, "You Oughta Know", 6, 1, 1, "Alanis Morissette, Glen Ballard", 249234, 8196916, 0.99),
    (10, "Ironic", 6, 1, 1, "Alanis Morissette, Glen Ballard", 229825, 7598866, 0.99),
    (11, "Man in the Box", 7, 1, 1, "Jerry Cantrell, Layne Staley", 286641, 9381028, 0.99),
    (12, "Would?", 7, 1, 1, "Jerry Cantrell", 207673, 6802453, 0.99),
]
CUSTOMERS = [
    (1, "Luís", "Gonçalves", "Brazil"),
    (2, "Leonie", "Köhler", "Germany"),
    (3, "François", "Tremblay", "Canada"),
    (4, "Bjørn", "Hansen", "Norway"),
    (5, "František", "Wichterlová", "Czech Republic"),
]
INVOICES = [
    (1, 1, "2024-01-01", "Av. Brigadeiro Faria Lima, 2170", "São José dos Campos", "SP", "Brazil", "12227-000", 1.98),
    (2, 2, "2024-01-02", "Theodor-Heuss-Straße 34", "Stuttgart", None, "Germany", "70174", 3.96),
    (3, 3, "2024-02-03", "1498 rue Bélanger", "Montréal", "QC", "Canada", "H2G 1A7", 5.94),
    (4, 4, "2024-03-11", "Ullevålsveien 14", "Oslo", None, "Norway", "0171", 0.99),
    (5, 5, "2024-03-24", "Klanova 9/506", "Prague", None, "Czech Republic", "14700", 9.90),
    (6, 1, "2024-04-18", "Av. Brigadeiro Faria Lima, 2170", "São José dos Campos", "SP", "Brazil", "12227-000", 8.91),
]


def main() -> None:
    if DB.exists():
        DB.unlink()
    conn = sqlite3.connect(DB)
    conn.executescript(DDL)
    conn.executemany("INSERT INTO Artist VALUES (?, ?)", ARTISTS)
    conn.executemany("INSERT INTO Album VALUES (?, ?, ?)", ALBUMS)
    conn.executemany(
        "INSERT INTO Track VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", TRACKS
    )
    conn.executemany("INSERT INTO Customer VALUES (?, ?, ?, ?)", CUSTOMERS)
    conn.executemany(
        "INSERT INTO Invoice VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", INVOICES
    )
    conn.commit()
    conn.close()
    print(f"Wrote {DB} ({DB.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
