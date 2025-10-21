# Tender Analytics Lambda Function

## 📜 Overview

This AWS Lambda function serves as the backend API endpoint for the Tender Tool's analytics dashboard. It provides aggregated data about tenders stored in an RDS SQL Server database and incorporates user-specific information by calling external APIs. The function adapts its response based on the presence and type of user ID provided in the request header.

## ✨ Features

The function provides three distinct views of analytics data:

1. **Public Analytics (Default):**
    * Total number of tenders (calculated real-time).
    * Count of open tenders (real-time).
    * Count of closed tenders (real-time).
    * Open-to-closed ratio.
    * Breakdown of tenders by current status (Open/Closed).
    * Breakdown of tenders by province/location (aggregated from relevant source tables like Eskom, Transnet, Sanral).

2. **Standard User Analytics:**
    * Includes **all** Public Analytics data.
    * Adds a `standardUserAnalytics` section containing statistics about the user's personal watchlist (fetched from an external API), such as:
        * Total tenders watched.
        * Open tenders watched.
        * Ratio of open watched tenders.
        * Count of tenders closing soon/later.

3. **Super User Analytics:**
    * Includes **all** Public Analytics data.
    * Adds a `tendersBySource` section showing the count of tenders from each provider (Eskom, Transnet, etc.).
    * Adds a `superUserAnalytics` section containing platform-wide user statistics (fetched from an external API), such as:
        * Total user count.
        * Standard user count.
        * Super user count.
        * Number of new registrations this month.

## ⚙️ Architecture & Workflow

1. **Trigger:** The function is triggered by an AWS API Gateway HTTP API endpoint (typically `GET /analytics`).
2. **User Identification:** It checks for an `X-User-ID` header in the incoming request.
3. **Branching Logic:**
    * **No User ID:** Proceeds directly to fetch public analytics from the database.
    * **User ID Present:**
        * Attempts to call an external API (`/tenderuser/fetch/{userID}`) to check if the user is a Super User.
        * **If Super User:** Fetches public analytics, source breakdown from the database, and formats admin stats from the API response.
        * **If Not Super User (or fetch fails):** Attempts to call an external API (`/watchlist/{userID}`) to get standard user data.
        * **If Standard User:** Fetches public analytics from the database and formats watchlist stats from the API response.
        * **If Watchlist Fails (or ID invalid):** Falls back to fetching only public analytics from the database.
4. **Database Interaction:** Uses the `db_handler.py` module to manage connections (`pymssql`) and execute SQL queries against the RDS database. Connection credentials are read from environment variables.
5. **Response:** Returns a JSON payload (`statusCode: 200`) containing the relevant analytics data or an error response (`statusCode: 500`).

## 🔧 Setup & Deployment

### Prerequisites

* AWS Account with permissions to create Lambda, Layers, API Gateway, and IAM Roles.
* RDS SQL Server database instance with the required schema (`dbo.BaseTender`, `dbo.EskomTender`, etc.).
* A dedicated database user (`AnalyticsAppUser`) with `SELECT` permissions on the necessary tables.
* The external User Fetch API and Watchlist API must be deployed and accessible.
* Docker Desktop installed locally (for building the layer).

### Steps

1. **Build Lambda Layer:**
    * Create a layer containing the `pymssql` library. It **must** be built in a Linux environment compatible with the chosen Lambda runtime (Python 3.9). Use the provided `build.bat` script in the `pymssql-layer-build` directory with Docker.
    * Upload the resulting `pymssql-layer.zip` file to AWS Lambda Layers. Name it appropriately (e.g., `pymssql-layer`) and set the compatible runtime to **Python 3.9**.
    * Ensure you have your separate `requests-layer` available, also compatible with Python 3.9.
2. **Create Lambda Function:**
    * Create a new Lambda function in the AWS console.
    * **Name:** `AnalyticsQueryHandler` (or your preferred name).
    * **Runtime:** Select **Python 3.9**.
    * **Architecture:** `x86_64`.
    * **Execution Role:** Create or use an existing role with permissions for:
        * Basic Lambda execution (`AWSLambdaBasicExecutionRole`).
        * Database access (typically via VPC permissions if Lambda is in VPC, although the final version runs outside VPC).
        * *(Optional but Recommended):* CloudWatch Logs access.
3. **Configure Environment Variables:**
    * Navigate to Configuration > Environment variables.
    * Add the following variables:
        * `DB_ENDPOINT`: The hostname of your RDS SQL Server instance.
        * `DB_NAME`: The specific database name (e.g., `tendertool_db`).
        * `DB_USER`: The database username created (e.g., `AnalyticsAppUser`).
        * `DB_PASSWORD`: The password for the database user.
        * *(Optional):* `USER_FETCH_API_URL`, `WATCHLIST_API_URL` if you want to override the defaults.
4. **Deploy Code:**
    * Create a zip file containing `lambda_function.py` and `db_handler.py`.
    * Upload this zip file as the **Code source** for the Lambda function.
5. **Attach Layers:**
    * Attach the `pymssql-layer` you created.
    * Attach your existing `requests-layer`.
6. **Configure Handler & Timeout:**
    * Ensure the **Handler** in Runtime settings is `lambda_function.lambda_handler`.
    * Increase the **Timeout** (General configuration) to at least 20-30 seconds to allow for database and API call latency.
7. **Set Up API Gateway Trigger:**
    * Create an HTTP API in API Gateway.
    * Create a `GET` route for `/analytics`.
    * Configure an integration to trigger your `AnalyticsQueryHandler` Lambda function.
    * Deploy the API stage.

## ⚙️ Configuration (Environment Variables)

| Variable          | Description                                                    | Example Value                                          |
| :---------------- | :------------------------------------------------------------- | :----------------------------------------------------- |
| `DB_ENDPOINT`     | Hostname of the RDS SQL Server instance.                       | `your-db.xxxx.us-east-1.rds.amazonaws.com`             |
| `DB_NAME`         | Name of the specific database to connect to.                   | `tendertool_db`                                        |
| `DB_USER`         | Database username with read permissions.                       | `AnalyticsAppUser`                                     |
| `DB_PASSWORD`     | Password for the database user.                                | `YourSecurePassword`                                   |
| `USER_FETCH_API_URL` | *(Optional)* URL template for the user fetch API.            | `https://.../dev/tenderuser/fetch/{}`                  |
| `WATCHLIST_API_URL`| *(Optional)* URL template for the user watchlist API.        | `https://.../dev/watchlist/{}`                         |

## 🚀 Usage

Invoke the API Gateway endpoint associated with the Lambda function using a `GET` request to the `/analytics` path.

* **Public Analytics:** Send the request with no specific headers.
* **User-Specific Analytics:** Include the custom header `X-User-ID` with the appropriate user's ID string.

Example (using curl):

```bash
# Public Analytics
curl https://{your-api-id}[.execute-api.us-east-1.amazonaws.com/analytics](https://.execute-api.us-east-1.amazonaws.com/analytics)

# Standard or Super User Analytics
curl -H "X-User-ID: {user-id-string}" https://{your-api-id}[.execute-api.us-east-1.amazonaws.com/analytics](https://.execute-api.us-east-1.amazonaws.com/analytics)
