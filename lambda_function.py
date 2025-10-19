import json
import os
import pymssql

# --- Global Scope ---
db_endpoint = os.environ.get('DB_ENDPOINT')
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_port = 1433

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
    db_connection = pymssql.connect(
        server=db_endpoint,
        user=db_user,
        password=db_password,
        database=db_name,
        port=db_port,
        autocommit=True
    )
    print("Database connection established successfully.")
    return db_connection

def lambda_handler(event, context):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(as_dict=True)
        
        print("Executing analytics queries...")
        
        # Query 1: Get the status breakdown directly from the 'Status' column.
        status_sql = "SELECT Status, COUNT(*) as value FROM dbo.BaseTender GROUP BY Status;"
        cursor.execute(status_sql)
        status_rows = cursor.fetchall()
        
        # Initial counts from the database
        db_open_count = next((item['value'] for item in status_rows if item.get('Status') == 'Open'), 0)
        db_closed_count = next((item['value'] for item in status_rows if item.get('Status') == 'Closed'), 0)
        
        # Query 2: The "Final Precaution" - Find 'Open' tenders that are now closed.
        correction_sql = "SELECT COUNT(*) as stale_count FROM dbo.BaseTender WHERE Status = 'Open' AND closingDate < GETDATE();"
        cursor.execute(correction_sql)
        stale_count = cursor.fetchone()['stale_count']
        
        print(f"Found {stale_count} stale 'Open' tenders that are now closed.")

        # --- Real-time correction of the numbers ---
        final_open_tenders = db_open_count - stale_count
        final_closed_tenders = db_closed_count + stale_count
        total_tenders = final_open_tenders + final_closed_tenders

        status_breakdown = [
            {'name': 'Open', 'value': final_open_tenders},
            {'name': 'Closed', 'value': final_closed_tenders}
        ]

        # --- Resilient Location Querying (with corrected column names) ---
        all_locations = []

        try:
            cursor.execute("SELECT province FROM dbo.EskomTender WHERE province IS NOT NULL AND province <> '';")
            for row in cursor.fetchall():
                all_locations.append(row['province'])
            print("Successfully queried Eskom tenders.")
        except Exception as e:
            print(f"WARNING: Could not query Eskom tenders. Reason: {e}")

        try:
            cursor.execute("SELECT location FROM dbo.TransnetTender WHERE location IS NOT NULL AND location <> '';")
            for row in cursor.fetchall():
                all_locations.append(row['location'])
            print("Successfully queried Transnet tenders.")
        except Exception as e:
            print(f"WARNING: Could not query Transnet tenders. Reason: {e}")

        try:
            cursor.execute("SELECT region FROM dbo.SanralTender WHERE region IS NOT NULL AND region <> '';")
            for row in cursor.fetchall():
                all_locations.append(row['region'])
            print("Successfully queried Sanral tenders.")
        except Exception as e:
            print(f"WARNING: Could not query Sanral tenders. Reason: {e}")

        cursor.close()
        print("Queries completed successfully.")
        
        # Process location data
        from collections import Counter
        location_counts = Counter(all_locations)
        tenders_by_province = [{'name': loc, 'value': count} for loc, count in location_counts.items()]
        tenders_by_province.sort(key=lambda x: x['value'], reverse=True)

        # Calculate final open ratio
        open_ratio = (final_open_tenders / total_tenders) * 100 if total_tenders > 0 else 0

        analytics_payload = {
            "totalTenders": total_tenders, 
            "openTenders": final_open_tenders, 
            "closedTenders": final_closed_tenders,
            "openRatio": round(open_ratio, 2), 
            "statusBreakdown": status_breakdown, 
            "tendersByProvince": tenders_by_province
        }
        
        return {
            'statusCode': 200, 
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps(analytics_payload)
        }

    except Exception as e:
        print(f"FATAL ERROR: An exception occurred in the handler: {e}")
        return {'statusCode': 500, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'error': 'An internal server error occurred.'})}