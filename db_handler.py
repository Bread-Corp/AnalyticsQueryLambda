import os
import pymssql # This will be provided by your pymssql-layer
from collections import Counter

# Global variable to hold our database connection for reuse
db_connection = None

def get_db_connection():
    """
    Establishes or reuses a database connection using credentials from environment variables.
    """
    global db_connection
    if db_connection:
        try:
            db_connection.autocommit(True)
            cursor = db_connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            print("Reusing existing database connection.")
            return db_connection
        except Exception as e:
            print(f"Stale connection detected, reconnecting. Reason: {e}")
            db_connection = None

    print("Connecting directly to RDS instance with credentials from environment variables.")
    try:
        db_connection = pymssql.connect(
            server=os.environ.get('DB_ENDPOINT'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            database=os.environ.get('DB_NAME'),
            port=1433,
            autocommit=True
        )
        print("Database connection established successfully.")
        return db_connection
    except Exception as e:
        print(f"ERROR: Failed to establish new database connection: {e}")
        raise # Re-raise the exception to be caught by the main handler

def fetch_public_status_breakdown(cursor):
    """
    Fetches and calculates the real-time status breakdown for all tenders.
    Returns the final corrected counts and the breakdown list.
    """
    print("Fetching status breakdown from DB...")
    # Get initial counts from the 'Status' column
    status_sql = "SELECT Status, COUNT(*) as value FROM dbo.BaseTender GROUP BY Status;"
    cursor.execute(status_sql)
    status_rows = cursor.fetchall()
    
    db_open_count = next((item['value'] for item in status_rows if item.get('Status') == 'Open'), 0)
    db_closed_count = next((item['value'] for item in status_rows if item.get('Status') == 'Closed'), 0)
    
    # Correct the counts based on real-time closing dates
    correction_sql = "SELECT COUNT(*) as stale_count FROM dbo.BaseTender WHERE Status = 'Open' AND closingDate < GETDATE();"
    cursor.execute(correction_sql)
    stale_count = cursor.fetchone()['stale_count']
    
    print(f"Found {stale_count} stale 'Open' tenders that are now closed.")
    
    final_open_tenders = db_open_count - stale_count
    final_closed_tenders = db_closed_count + stale_count

    return {
        "openTenders": final_open_tenders,
        "closedTenders": final_closed_tenders,
        "totalTenders": final_open_tenders + final_closed_tenders,
        "statusBreakdown": [
            {'name': 'Open', 'value': final_open_tenders},
            {'name': 'Closed', 'value': final_closed_tenders}
        ]
    }

def fetch_public_location_breakdown(cursor):
    """
    Resiliently fetches the breakdown of tenders by province/location from child tables.
    """
    print("Fetching location breakdown from DB...")
    all_locations = []
    location_queries = {
        "Eskom": ("SELECT province FROM dbo.EskomTender WHERE province IS NOT NULL AND province <> '';", 'province'),
        "Transnet": ("SELECT location FROM dbo.TransnetTender WHERE location IS NOT NULL AND location <> '';", 'location'),
        "Sanral": ("SELECT region FROM dbo.SanralTender WHERE region IS NOT NULL AND region <> '';", 'region')
    }

    for source, (sql, col_name) in location_queries.items():
        try:
            cursor.execute(sql)
            all_locations.extend([row[col_name] for row in cursor.fetchall()])
            print(f"Successfully queried {source} tenders for location.")
        except Exception as e:
            # If a query fails (e.g., table doesn't exist yet, column name wrong), log and continue
            print(f"WARNING: Could not query {source} tenders for location. Reason: {e}")

    location_counts = Counter(all_locations)
    tenders_by_province = [{'name': loc, 'value': count} for loc, count in location_counts.items()]
    tenders_by_province.sort(key=lambda x: x['value'], reverse=True)
    return tenders_by_province

def fetch_source_breakdown(cursor):
    """
    Fetches the breakdown of tenders by their source from the BaseTender table.
    """
    print("Fetching source breakdown from DB...")
    source_sql = "SELECT Source, COUNT(*) as value FROM dbo.BaseTender GROUP BY Source ORDER BY value DESC;"
    cursor.execute(source_sql)
    return [{'name': row['Source'], 'value': row['value']} for row in cursor.fetchall()]