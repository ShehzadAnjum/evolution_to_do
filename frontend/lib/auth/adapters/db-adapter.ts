import { Pool, neonConfig } from "@neondatabase/serverless";
import { env } from "../config/env";

/**
 * Neon Postgres database connection for Better-Auth
 * 
 * Based on Better-Auth documentation analysis:
 * - Better-Auth can accept a Pool directly (from postgresql.mdx)
 * - Better-Auth detects PostgreSQL by checking for "connect" method
 * - Neon Pool has "connect" method, so it should work
 * 
 * Configuration:
 * - sslmode=require is required for Neon
 * - fetchConnectionCache helps reuse HTTP connections in serverless
 * - max: 1 is serverless-friendly
 */
neonConfig.fetchConnectionCache = true;

// Ensure sslmode=require is in connection string
const connectionString = env.DATABASE_URL.includes("sslmode=")
  ? env.DATABASE_URL
  : `${env.DATABASE_URL}${env.DATABASE_URL.includes("?") ? "&" : "?"}sslmode=require`;

/**
 * Database Pool for Better-Auth
 * 
 * Better-Auth will:
 * 1. Detect this is a PostgreSQL Pool (has "connect" method)
 * 2. Create PostgresDialect with this pool
 * 3. Create Kysely instance internally
 * 4. Use kyselyAdapter to wrap it
 * 
 * This approach matches the PostgreSQL adapter pattern shown in Better-Auth docs.
 * Passing Pool directly works better than passing a Kysely instance because
 * Better-Auth can properly detect the database type and create the adapter.
 */
export const db = new Pool({
  connectionString,
  // Serverless-friendly settings
  max: 1,
  idleTimeoutMillis: 30_000,
  connectionTimeoutMillis: 30_000,
});

/**
 * Database type for Better-Auth
 * 
 * Note: We export Pool, but Better-Auth will use it to create
 * a Kysely instance internally via its adapter system.
 */
export type Database = typeof db;


