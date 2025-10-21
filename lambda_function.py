import json
import requests # Provided by layer
import db_handler # Our custom module
import os

# --- API Endpoints ---
USER_FETCH_API_URL = os.environ.get("USER_FETCH_API_URL", "https://4owkixd548.execute-api.us-east-1.amazonaws.com/dev/tenderuser/fetch/{}")
WATCHLIST_API_URL = os.environ.get("WATCHLIST_API_URL", "https://4owkixd548.execute-api.us-east-1.amazonaws.com/dev/watchlist/{}")
API_TIMEOUT_SECONDS = 10

def format_error_response(message="An internal server error occurred.", status_code=500):
    """ Creates a standardized error response for API Gateway """
    return {
        'statusCode': status_code,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'error': message})
    }

def get_public_analytics(cursor):
    """ Gathers all public analytics data using the db_handler """
    print("Getting public analytics...")
    status_data = db_handler.fetch_public_status_breakdown(cursor)
    location_data = db_handler.fetch_public_location_breakdown(cursor)

    total_tenders = status_data.get("totalTenders", 0)
    open_tenders = status_data.get("openTenders", 0)
    open_ratio = (open_tenders / total_tenders) * 100 if total_tenders > 0 else 0

    return {
        "totalTenders": total_tenders,
        "openTenders": open_tenders,
        "closedTenders": status_data.get("closedTenders", 0),
        "openRatio": round(open_ratio, 2),
        "statusBreakdown": status_data.get("statusBreakdown", []),
        "tendersByProvince": location_data
    }

def format_standard_user_analytics(api_response, cursor):
    """
    Formats the Standard User payload.
    Includes all public analytics PLUS user-specific watchlist stats.
    """
    print("Formatting standard user analytics...")
    # 1. Get the base public analytics data
    analytics_payload = get_public_analytics(cursor)

    # 2. Extract watchlist stats from the API response
    watchlist_analytics = api_response.get('analytics', {})
    total_watched = watchlist_analytics.get('count', 0)
    closed_watched = watchlist_analytics.get('closed', 0)
    open_watched = total_watched - closed_watched

    # 3. Add the user-specific section with the new name
    analytics_payload["standardUserAnalytics"] = { # Renamed from quickInsights
        "totalUserTenders": total_watched,
        "openUserTenders": open_watched,
        "userOpenRatio": round((open_watched / total_watched) * 100, 2) if total_watched > 0 else 0,
        "closingSoon": watchlist_analytics.get('closingSoon', 0),
        "closingLater": watchlist_analytics.get('closingLater', 0)
    }
    return analytics_payload

def format_super_user_analytics(api_response, cursor):
    """
    Formats the Super User payload.
    Includes all public analytics, source breakdown, PLUS admin stats.
    """
    print("Formatting super user analytics...")
    # 1. Get all public analytics data
    analytics_payload = get_public_analytics(cursor)
    
    # 2. Get the source breakdown from the database
    source_data = db_handler.fetch_source_breakdown(cursor)
    analytics_payload["tendersBySource"] = source_data
    
    # 3. Add admin stats from the /fetch API response with the new name
    analytics_payload["superUserAnalytics"] = { # Renamed from adminStats
        "totalUsers": api_response.get("userCount", 0),
        "standardUsers": api_response.get("standardUserCount", 0),
        "superUsers": api_response.get("superUserCount", 0),
        "newRegistrationsThisMonth": api_response.get("registeredRecently", 0)
    }
    
    return analytics_payload

def lambda_handler(event, context):
    print(f"Received event: {event}")
    user_id = None
    cursor = None # Ensure cursor is defined for finally block
    conn = None # Ensure conn is defined for finally block

    try:
        # Check for the User ID in headers (case-insensitive)
        headers = event.get('headers', {})
        user_id = headers.get('x-user-id') or headers.get('X-User-ID')
        print(f"Extracted UserID: {user_id}")

        conn = db_handler.get_db_connection()
        cursor = conn.cursor(as_dict=True)
        
        analytics_payload = {}

        if not user_id:
            # --- Scenario 1: Public Analytics ---
            print("No UserID provided, fetching public analytics.")
            analytics_payload = get_public_analytics(cursor)
        else:
            # --- Scenario 2 or 3: User-Specific Analytics ---
            is_super_user = False
            super_user_data = None
            
            # Attempt to fetch Super User data
            try:
                print(f"Attempting Super User fetch for UserID: {user_id}")
                response = requests.get(USER_FETCH_API_URL.format(user_id), timeout=API_TIMEOUT_SECONDS)
                print(f"Super User API response status: {response.status_code}")
                
                if response.status_code == 200:
                    super_user_data = response.json()
                    is_super_user = True
                else:
                    print(f"Super User fetch failed or user is not admin (Status: {response.status_code}). Proceeding to Standard User check.")
                    
            except requests.exceptions.RequestException as e:
                print(f"WARNING: Request to Super User API failed: {e}. Proceeding to Standard User check.")
            except json.JSONDecodeError as e:
                 print(f"WARNING: Failed to decode Super User API response: {e}. Proceeding to Standard User check.")

            if is_super_user and super_user_data:
                # --- Scenario 3: Super User Analytics ---
                print("User is Super User, formatting Super User analytics.")
                analytics_payload = format_super_user_analytics(super_user_data, cursor)
            else:
                # Attempt to fetch Standard User data (Watchlist)
                try:
                    print(f"Attempting Standard User watchlist fetch for UserID: {user_id}")
                    response = requests.get(WATCHLIST_API_URL.format(user_id), timeout=API_TIMEOUT_SECONDS)
                    print(f"Standard User API response status: {response.status_code}")

                    if response.status_code == 200:
                        # --- Scenario 2: Standard User Analytics ---
                        print("User is Standard User, formatting Standard User analytics.")
                        standard_user_data = response.json()
                        # Pass cursor here to fetch public data
                        analytics_payload = format_standard_user_analytics(standard_user_data, cursor)
                    else:
                        # If watchlist also fails, assume invalid ID and show public
                        print(f"Standard User watchlist fetch failed (Status: {response.status_code}). Falling back to public analytics.")
                        analytics_payload = get_public_analytics(cursor)
                        
                except requests.exceptions.RequestException as e:
                    print(f"WARNING: Request to Standard User API failed: {e}. Falling back to public analytics.")
                    analytics_payload = get_public_analytics(cursor)
                except json.JSONDecodeError as e:
                     print(f"WARNING: Failed to decode Standard User API response: {e}. Falling back to public analytics.")
                     analytics_payload = get_public_analytics(cursor)

        # --- Return Success Response ---
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps(analytics_payload)
        }

    except pymssql.Error as db_err: # Catch specific database errors
        print(f"FATAL DATABASE ERROR: {db_err}")
        return format_error_response("Database error occurred.")
    except Exception as e: # Catch any other unexpected errors
        print(f"FATAL UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return format_error_response()
    finally:
        # Ensure the cursor is always closed if it was opened
        if cursor:
            try:
                cursor.close()
                print("Database cursor closed.")
            except Exception as e:
                print(f"Error closing cursor: {e}")