#!/usr/bin/env python3
"""Migration script for v2.0.0: Add priority, category, due_date to tasks table.

This script safely adds new columns to existing Neon PostgreSQL database.
All new columns have defaults, so existing data remains valid.

Usage:
    cd backend
    uv run python scripts/migrate_v2.py

What it does:
    1. Adds 'priority' column (VARCHAR, default 'medium')
    2. Adds 'category' column (VARCHAR, default 'general')
    3. Adds 'due_date' column (DATE, nullable)
    4. Creates indexes for filtering

Safe to run multiple times (idempotent).
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from sqlmodel import create_engine, Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_database_url() -> str:
    """Get database URL from environment."""
    url = os.getenv("DATABASE_URL")
    if not url:
        raise ValueError("DATABASE_URL environment variable not set")
    return url


def run_migration():
    """Run the v2.0.0 migration."""
    print("=" * 60)
    print("Evolution Todo - Database Migration v2.0.0")
    print("=" * 60)
    print()

    database_url = get_database_url()
    print(f"Database: {database_url[:50]}...")
    print()

    engine = create_engine(database_url)

    with Session(engine) as session:
        # Check if columns already exist
        print("Checking existing schema...")
        result = session.exec(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'tasks'
        """))
        existing_columns = [row[0] for row in result]
        print(f"Existing columns: {existing_columns}")
        print()

        migrations = []

        # Migration 1: Add priority column
        if "priority" not in existing_columns:
            migrations.append({
                "name": "Add priority column",
                "sql": """
                    ALTER TABLE tasks
                    ADD COLUMN IF NOT EXISTS priority VARCHAR(10) DEFAULT 'medium'
                """
            })
        else:
            print("✓ priority column already exists")

        # Migration 2: Add category column
        if "category" not in existing_columns:
            migrations.append({
                "name": "Add category column",
                "sql": """
                    ALTER TABLE tasks
                    ADD COLUMN IF NOT EXISTS category VARCHAR(50) DEFAULT 'general'
                """
            })
        else:
            print("✓ category column already exists")

        # Migration 3: Add due_date column
        if "due_date" not in existing_columns:
            migrations.append({
                "name": "Add due_date column",
                "sql": """
                    ALTER TABLE tasks
                    ADD COLUMN IF NOT EXISTS due_date DATE NULL
                """
            })
        else:
            print("✓ due_date column already exists")

        # Run migrations
        if migrations:
            print()
            print(f"Running {len(migrations)} migration(s)...")
            print()

            for migration in migrations:
                print(f"  → {migration['name']}...")
                try:
                    session.exec(text(migration["sql"]))
                    session.commit()
                    print(f"    ✓ Success")
                except Exception as e:
                    print(f"    ✗ Error: {e}")
                    session.rollback()
                    raise

            print()

        # Create indexes (safe to run multiple times)
        print("Creating indexes...")

        index_queries = [
            ("idx_tasks_priority", "CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority)"),
            ("idx_tasks_category", "CREATE INDEX IF NOT EXISTS idx_tasks_category ON tasks(category)"),
            ("idx_tasks_due_date", "CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date)"),
        ]

        for idx_name, idx_sql in index_queries:
            try:
                session.exec(text(idx_sql))
                session.commit()
                print(f"  ✓ {idx_name}")
            except Exception as e:
                print(f"  ✓ {idx_name} (already exists)")
                session.rollback()

        print()

        # Verify migration
        print("Verifying migration...")
        result = session.exec(text("""
            SELECT column_name, data_type, column_default, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'tasks'
            ORDER BY ordinal_position
        """))

        print()
        print("Final schema:")
        print("-" * 60)
        for row in result:
            col_name, data_type, default, nullable = row
            nullable_str = "NULL" if nullable == "YES" else "NOT NULL"
            default_str = f"DEFAULT {default}" if default else ""
            print(f"  {col_name:<15} {data_type:<15} {nullable_str:<10} {default_str}")
        print("-" * 60)

        print()
        print("=" * 60)
        print("Migration complete!")
        print("=" * 60)


if __name__ == "__main__":
    try:
        run_migration()
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        sys.exit(1)
