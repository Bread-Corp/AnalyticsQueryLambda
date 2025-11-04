# 📊 Tender Analytics Lambda Function — Business Intelligence Powerhouse

[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange.svg)](https://aws.amazon.com/lambda/)
[![Python 3.9](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/)
[![Amazon RDS](https://img.shields.io/badge/AWS-RDS-9d68c4.svg)](https://aws.amazon.com/rds/)
[![SQL Server](https://img.shields.io/badge/SQL%20Server-CC2727.svg)](https://www.microsoft.com/sql-server/)
[![API Gateway](https://img.shields.io/badge/AWS-API%20Gateway-FF9900.svg)](https://aws.amazon.com/api-gateway/)

**Transforming tender data into actionable business intelligence!** 📈 This AWS Lambda function serves as the analytical brain behind the Tender Tool's dynamic dashboard, delivering real-time insights and personalized analytics that power data-driven procurement decisions across South Africa's business landscape.

## 📚 Table of Contents

- [📜 Overview](#-overview)
- [✨ Features](#-features)
- [⚙️ Architecture & Workflow](#️-architecture--workflow)
- [🔧 Setup & Deployment](#-setup--deployment)
- [⚙️ Configuration](#️-configuration-environment-variables)
- [🚀 Usage](#-usage)
- [🧰 Troubleshooting](#-troubleshooting)
- [📊 API Response Examples](#-api-response-examples)

## 📜 Overview

Welcome to the data science command center! 🎯 This serverless analytics engine transforms raw tender information from our comprehensive database into intelligent, actionable insights. Whether you're a public user exploring market trends or a power user managing complex watchlists, this function delivers personalized analytics that drive smart procurement decisions! 🚀

**What makes it analytically awesome?** 💡
- 🎭 **Multi-Persona Intelligence**: Adapts analytics based on user roles and permissions
- ⚡ **Real-Time Processing**: Live calculations from massive tender databases
- 🔗 **API Integration**: Seamlessly combines database analytics with external user services
- 🎯 **Smart Fallbacks**: Graceful degradation ensures users always get valuable insights

## ✨ Features

Our analytics engine delivers three distinct intelligence levels, each tailored to specific user needs:

### 🌍 **Public Analytics (Default View)**
Perfect for market researchers and newcomers exploring the procurement landscape:
- 📊 **Total Tender Count**: Real-time calculation of all opportunities in the system
- 🟢 **Live Opportunity Tracker**: Current count of open tenders ready for bidding
- 🔴 **Historical Analysis**: Count of closed tenders for trend analysis
- ⚖️ **Market Ratio Intelligence**: Open-to-closed ratio for market health assessment
- 📈 **Status Breakdown**: Visual representation of opportunity distribution
- 🗺️ **Geographic Intelligence**: Provincial breakdown across South Africa's procurement landscape

### 👤 **Standard User Analytics**
Enhanced insights for registered users managing their procurement portfolios:
- ✅ **All Public Analytics** (comprehensive market view)
- 📋 **Personal Watchlist Intelligence**:
  - 👀 Total tenders under surveillance
  - 🎯 Open opportunities in your portfolio
  - 📊 Personal opportunity ratio analysis
  - ⏰ Deadline proximity alerts (closing soon vs. future opportunities)

### 🦸 **Super User Analytics**
Executive-level intelligence for platform administrators and power users:
- ✅ **All Public Analytics** (complete market overview)
- 🏭 **Source Distribution Analysis**: Tender counts by provider (Eskom, Transnet, SANRAL, SARS, eTenders)
- 👥 **Platform Administration Intelligence**:
  - 📊 Total platform user count
  - 👤 Standard user demographics
  - 🦸 Super user population
  - 📈 Monthly registration growth metrics

## ⚙️ Architecture & Workflow

Our analytics engine follows an intelligent, adaptive processing flow:

### 🔄 The Intelligence Pipeline:

1. **🌐 API Gateway Trigger**: HTTP requests hit our `/analytics` endpoint with lightning-fast response times

2. **🔍 User Intelligence Detection**: Smart header analysis to determine user context and permissions level

3. **🧠 Adaptive Processing Logic**:
   ```
   📥 Request Analysis
   ├─ 🚫 No User ID → Public Analytics Pipeline
   ├─ 👤 User ID Present
   │   ├─ 🔍 Super User Check → External API Call
   │   ├─ 🦸 Super User Confirmed → Full Intelligence Suite
   │   ├─ 👤 Standard User → Watchlist Intelligence
   │   └─ ❌ Fallback → Public Analytics
   └─ 📊 Response Generation
   ```

4. **🗄️ Database Intelligence**: Lightning-fast SQL queries against our comprehensive RDS database using optimized `pymssql` connections

5. **🔗 External API Orchestration**: Seamless integration with user management and watchlist services for personalized insights

6. **📊 Response Optimization**: JSON payload optimization for maximum dashboard performance

## 📦 Deployment

This section covers three deployment methods for the Analytics Query Handler Lambda Function. Choose the method that best fits your workflow and infrastructure preferences.

### 🛠️ Prerequisites

Before deploying, ensure you have:
- AWS CLI configured with appropriate credentials 🔑
- AWS SAM CLI installed (`pip install aws-sam-cli`)
- Python 3.9 runtime support in your target region
- Access to AWS Lambda, RDS, API Gateway, and CloudWatch Logs services ☁️
- Analytics layer dependencies for database connectivity
- VPC configuration for RDS access (if applicable)

### 🎯 Method 1: AWS Toolkit Deployment

Deploy directly through your IDE using the AWS Toolkit extension.

#### Setup Steps:
1. **Install AWS Toolkit** in your IDE (VS Code, IntelliJ, etc.)
2. **Configure AWS Profile** with your credentials
3. **Open Project** containing `lambda_function.py` and `db_handler.py`

#### Deploy Process:
1. **Right-click** on `lambda_function.py` in your IDE
2. **Select** "Deploy Lambda Function" from AWS Toolkit menu
3. **Configure Deployment**:
   - Function Name: `AnalyticsQueryHandler`
   - Runtime: `python3.9`
   - Handler: `lambda_function.lambda_handler`
   - Memory: `128 MB`
   - Timeout: `60 seconds`
4. **Add Layers** manually after deployment:
   - analytics-layer (for database connectivity)
5. **Set Environment Variables**:
   ```
   DB_ENDPOINT=tender-tool-db.c2hq4seoidxc.us-east-1.rds.amazonaws.com
   DB_NAME=tendertool_db
   DB_USER=AnalyticsAppUser
   DB_PASSWORD=T3nder$Tool_DB_2025!
   USER_FETCH_API_URL=https://api.example.com/dev/tenderuser/fetch/{}
   WATCHLIST_API_URL=https://api.example.com/dev/watchlist/{}
   ```
6. **Configure IAM Permissions** for RDS, VPC, and CloudWatch Logs
7. **Set up API Gateway** manually and connect to the Lambda function

#### Post-Deployment:
- Test the function using the AWS Toolkit test feature
- Monitor logs through CloudWatch integration
- Verify database connectivity and API Gateway integration
- Test analytics endpoints with different user roles

### 🚀 Method 2: SAM Deployment

Use AWS SAM for infrastructure-as-code deployment with the provided template.

#### Initial Setup:
```bash
# Install AWS SAM CLI
pip install aws-sam-cli

# Verify installation
sam --version
```

#### Create Required Layer Directory:
Since the template references an analytics layer not included in the repository, create it:

```bash
# Create analytics layer directory
mkdir -p analytics-layer/python

# Install required database and HTTP connectivity packages
pip install pymssql -t analytics-layer/python/
pip install sqlalchemy -t analytics-layer/python/
pip install requests -t analytics-layer/python/
pip install urllib3 -t analytics-layer/python/
```

#### Build and Deploy:
```bash
# Build the SAM application
sam build

# Deploy with guided configuration (first time)
sam deploy --guided

# Follow the prompts:
# Stack Name: analytics-query-handler-stack
# AWS Region: us-east-1 (or your preferred region)
# Confirm changes before deploy: Y
# Allow SAM to create IAM roles: Y
# Save parameters to samconfig.toml: Y
```

#### Environment Variables Setup:
The template already includes the required database environment variables:

```yaml
# Already configured in template.yml
Environment:
  Variables:
    DB_ENDPOINT: tender-tool-db.c2hq4seoidxc.us-east-1.rds.amazonaws.com
    DB_NAME: tendertool_db
    DB_PASSWORD: T3nder$Tool_DB_2025!
    DB_USER: AnalyticsAppUser
```

#### Add Optional API Environment Variables:
```bash
# Add external API URLs after initial deployment
aws lambda update-function-configuration \
    --function-name AnalyticsQueryHandler \
    --environment Variables='{
        "DB_ENDPOINT":"tender-tool-db.c2hq4seoidxc.us-east-1.rds.amazonaws.com",
        "DB_NAME":"tendertool_db",
        "DB_USER":"AnalyticsAppUser",
        "DB_PASSWORD":"T3nder$Tool_DB_2025!",
        "USER_FETCH_API_URL":"https://api.example.com/dev/tenderuser/fetch/{}",
        "WATCHLIST_API_URL":"https://api.example.com/dev/watchlist/{}"
    }'
```

#### Subsequent Deployments:
```bash
# Quick deployment after initial setup
sam build && sam deploy
```

#### Local Testing with SAM:
```bash
# Test function locally with API Gateway simulation
sam local start-api

# Test specific analytics endpoint
curl http://localhost:3000/analytics

# Test with user headers
curl -H "X-User-ID: user-12345" http://localhost:3000/analytics
```

#### SAM Deployment Advantages:
- ✅ Complete infrastructure management
- ✅ Automatic layer creation and management
- ✅ API Gateway integration included
- ✅ Environment variables defined in template
- ✅ IAM permissions and VPC configuration
- ✅ Easy rollback capabilities
- ✅ CloudFormation integration

### 🔄 Method 3: Workflow Deployment (CI/CD)

Automated deployment using GitHub Actions workflow for production environments.

#### Setup Requirements:
1. **GitHub Repository Secrets**:
   ```
   AWS_ACCESS_KEY_ID: Your AWS access key
   AWS_SECRET_ACCESS_KEY: Your AWS secret key
   AWS_REGION: us-east-1 (or your target region)
   ```

2. **Pre-existing Lambda Function**: The workflow updates an existing function, so deploy initially using Method 1 or 2.

#### Deployment Process:
1. **Create Release Branch**:
   ```bash
   # Create and switch to release branch
   git checkout -b release
   
   # Make your changes to lambda_function.py or db_handler.py
   # Commit changes
   git add .
   git commit -m "feat: update analytics query processing logic"
   
   # Push to trigger deployment
   git push origin release
   ```

2. **Automatic Deployment**: The workflow will:
   - Checkout the code
   - Configure AWS credentials
   - Create deployment zip with `lambda_function.py` and `db_handler.py`
   - Update the existing Lambda function code
   - Maintain existing configuration (layers, environment variables, API Gateway, etc.)

#### Manual Trigger:
You can also trigger deployment manually:
1. Go to **Actions** tab in your GitHub repository
2. Select **"Deploy Python Lambda to AWS"** workflow
3. Click **"Run workflow"**
4. Choose the `release` branch
5. Click **"Run workflow"** button

#### Workflow Deployment Advantages:
- ✅ Automated CI/CD pipeline
- ✅ Consistent deployment process
- ✅ Audit trail of deployments
- ✅ Easy rollback to previous commits
- ✅ No local environment dependencies

### 🔧 Post-Deployment Configuration

Regardless of deployment method, verify the following:

#### Environment Variables Verification:
Ensure these environment variables are properly set:

```bash
# Verify environment variables via AWS CLI
aws lambda get-function-configuration \
    --function-name AnalyticsQueryHandler \
    --query 'Environment.Variables'
```

Expected output:
```json
{
    "DB_ENDPOINT": "tender-tool-db.c2hq4seoidxc.us-east-1.rds.amazonaws.com",
    "DB_NAME": "tendertool_db",
    "DB_USER": "AnalyticsAppUser",
    "DB_PASSWORD": "T3nder$Tool_DB_2025!",
    "USER_FETCH_API_URL": "https://api.example.com/dev/tenderuser/fetch/{}",
    "WATCHLIST_API_URL": "https://api.example.com/dev/watchlist/{}"
}
```

#### Database User Setup:
Ensure the analytics database user exists and has proper permissions:

```sql
-- Connect to your SQL Server RDS instance
-- Create the analytics user if not exists
CREATE LOGIN AnalyticsAppUser WITH PASSWORD = 'T3nder$Tool_DB_2025!';
USE tendertool_db;
CREATE USER AnalyticsAppUser FOR LOGIN AnalyticsAppUser;

-- Grant required permissions for analytics queries
GRANT SELECT ON dbo.BaseTender TO AnalyticsAppUser;
GRANT SELECT ON dbo.TenderSource TO AnalyticsAppUser;
GRANT SELECT ON dbo.Province TO AnalyticsAppUser;
GRANT SELECT ON dbo.TenderStatus TO AnalyticsAppUser;
-- Add other necessary table permissions as needed
```

#### API Gateway Configuration Verification:
Check that API Gateway is properly configured:

```bash
# List API Gateway APIs
aws apigatewayv2 get-apis

# Get specific API configuration
aws apigatewayv2 get-api --api-id [your-api-id]

# Test the analytics endpoint
curl https://[api-id].execute-api.[region].amazonaws.com/analytics
```

### 🧪 Testing Your Deployment

After deployment, test the function thoroughly:

#### Test Analytics Endpoints:
```bash
# Test public analytics (no headers)
curl https://[api-id].execute-api.[region].amazonaws.com/analytics

# Test standard user analytics
curl -H "X-User-ID: user-12345" \
     https://[api-id].execute-api.[region].amazonaws.com/analytics

# Test super user analytics
curl -H "X-User-ID: superuser-67890" \
     https://[api-id].execute-api.[region].amazonaws.com/analytics

# Test direct Lambda invocation
aws lambda invoke \
    --function-name AnalyticsQueryHandler \
    --payload '{"httpMethod":"GET","path":"/analytics","headers":{}}' \
    response.json
```

#### Expected Success Response (Public Analytics):
```json
{
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
    },
    "body": "{\"totalTenders\":15847,\"openTenders\":342,\"closedTenders\":15505,\"openToClosedRatio\":0.022}"
}
```

#### Expected Success Indicators:
- ✅ Function executes without errors
- ✅ CloudWatch logs show successful database connections
- ✅ API Gateway returns 200 status codes
- ✅ Analytics data is properly formatted JSON
- ✅ Different user types receive appropriate data levels
- ✅ External API integrations work (when configured)

### 🔍 Monitoring and Maintenance

#### CloudWatch Metrics to Monitor:
- **Duration**: Function execution time for analytics queries
- **Error Rate**: Failed analytics requests
- **Memory Utilization**: RAM usage during complex queries
- **API Gateway Metrics**: Request counts and latency
- **Database Connection Health**: RDS connection metrics

#### Log Analysis:
```bash
# View recent logs
aws logs tail /aws/lambda/AnalyticsQueryHandler --follow

# Search for successful analytics queries
aws logs filter-log-events \
    --log-group-name /aws/lambda/AnalyticsQueryHandler \
    --filter-pattern "Analytics query completed"

# Search for database connection issues
aws logs filter-log-events \
    --log-group-name /aws/lambda/AnalyticsQueryHandler \
    --filter-pattern "Database connection"

# Monitor API Gateway access logs
aws logs filter-log-events \
    --log-group-name /aws/apigateway/[api-id] \
    --filter-pattern "/analytics"
```

### 🚨 Troubleshooting Deployments

<details>
<summary><strong>Analytics Layer Dependencies Missing</strong></summary>

**Issue**: Database connectivity or HTTP request packages not available

**Solution**: Ensure analytics layer is properly created and attached:
```bash
# For SAM: Verify layer directory exists and contains packages
ls -la analytics-layer/python/
ls -la analytics-layer/python/pymssql/
ls -la analytics-layer/python/requests/

# For manual deployment: Create and upload layer separately
```
</details>

<details>
<summary><strong>Database Connection Failures</strong></summary>

**Issue**: Cannot connect to RDS SQL Server for analytics

**Solution**: Verify database configuration and network access:
- Check DB_ENDPOINT points to correct RDS instance
- Verify AnalyticsAppUser exists and has correct password
- Ensure Lambda is in same VPC as RDS or configure VPC peering
- Check RDS security groups allow Lambda subnet access
- Verify database is accessible and not in maintenance mode
</details>

<details>
<summary><strong>API Gateway Integration Issues</strong></summary>

**Issue**: API Gateway not properly connected to Lambda

**Solution**: Verify API Gateway configuration:
- Check API Gateway has correct Lambda integration
- Verify Lambda permissions allow API Gateway invocation
- Test API Gateway deployment and stage configuration
- Check CORS settings if accessing from web applications
</details>

<details>
<summary><strong>VPC and Security Group Configuration</strong></summary>

**Issue**: Lambda cannot access RDS due to VPC restrictions

**Solution**: Configure VPC properly:
- Ensure Lambda and RDS are in same VPC
- Configure security group rules for database port (1433 for SQL Server)
- Verify subnet routing and NAT gateway configuration
- Check network ACLs allow database traffic
</details>

<details>
<summary><strong>External API Integration Failures</strong></summary>

**Issue**: User fetch or watchlist APIs not responding

**Solution**: Implement robust error handling:
- Verify external API endpoints are accessible
- Check authentication tokens and API keys
- Implement graceful fallback to public analytics
- Monitor external API rate limits and quotas
</details>

<details>
<summary><strong>Environment Variables Not Set</strong></summary>

**Issue**: Missing database or API configuration

**Solution**: Set environment variables using AWS CLI:
```bash
aws lambda update-function-configuration \
    --function-name AnalyticsQueryHandler \
    --environment Variables='{
        "DB_ENDPOINT":"tender-tool-db.c2hq4seoidxc.us-east-1.rds.amazonaws.com",
        "DB_NAME":"tendertool_db",
        "DB_USER":"AnalyticsAppUser",
        "DB_PASSWORD":"T3nder$Tool_DB_2025!",
        "USER_FETCH_API_URL":"https://api.example.com/dev/tenderuser/fetch/{}",
        "WATCHLIST_API_URL":"https://api.example.com/dev/watchlist/{}"
    }'
```
</details>

<details>
<summary><strong>Workflow Deployment Fails</strong></summary>

**Issue**: GitHub Actions workflow errors

**Solution**: 
- Check repository secrets are correctly configured
- Verify the target Lambda function exists in AWS
- Ensure workflow has correct function ARN
- Check that both lambda_function.py and db_handler.py exist in repository
</details>

Choose the deployment method that best fits your development workflow and infrastructure requirements. SAM deployment is recommended for development environments, while workflow deployment excels for production analytics services requiring high availability and consistent updates.

## 🚀 Usage

### 🌍 Public Analytics Request
```bash
curl https://your-api-id.execute-api.region.amazonaws.com/analytics
```

### 👤 User-Specific Analytics Request
```bash
curl -H "X-User-ID: user-12345" \
     https://your-api-id.execute-api.region.amazonaws.com/analytics
```

### 🦸 Super User Analytics Request
```bash
curl -H "X-User-ID: superuser-67890" \
     https://your-api-id.execute-api.region.amazonaws.com/analytics
```

## 🧰 Troubleshooting

### 🚨 Common Analytics Challenges

<details>
<summary><strong>Database Connection Timeouts</strong></summary>

**Issue**: Lambda timing out on database connections.

**Solution**: Ensure your Lambda is in the same VPC as your RDS instance, or configure appropriate security groups. Database analytics requires reliable connectivity! 🗄️

</details>

<details>
<summary><strong>External API Integration Failures</strong></summary>

**Issue**: User fetch or watchlist APIs returning errors.

**Solution**: Implement robust fallback logic - users should always receive at least public analytics. Check API endpoints and authentication tokens! 🔗

</details>

<details>
<summary><strong>Performance Optimization</strong></summary>

**Issue**: Slow response times for complex analytics queries.

**Solution**: Optimize your SQL queries, consider database indexing, and implement connection pooling. Analytics should be lightning-fast! ⚡

</details>

<details>
<summary><strong>Layer Compatibility Issues</strong></summary>

**Issue**: pymssql layer not working with Lambda runtime.

**Solution**: Ensure your layer was built on Linux x86_64 architecture matching your Lambda runtime. Use Docker for consistent builds! 🐳

</details>

## 📊 API Response Examples

### 🌍 Public Analytics Response
```json
{
  "statusCode": 200,
  "body": {
    "totalTenders": 15847,
    "openTenders": 342,
    "closedTenders": 15505,
    "openToClosedRatio": 0.022,
    "statusBreakdown": {
      "Open": 342,
      "Closed": 15505
    },
    "provinceBreakdown": {
      "Gauteng": 4521,
      "Western Cape": 3102,
      "KwaZulu-Natal": 2876
    }
  }
}
```

### 👤 Standard User Analytics Response
```json
{
  "statusCode": 200,
  "body": {
    "totalTenders": 15847,
    "openTenders": 342,
    "standardUserAnalytics": {
      "totalWatchedTenders": 23,
      "openWatchedTenders": 8,
      "watchedOpenRatio": 0.348,
      "tendersClosingSoon": 3,
      "tendersClosingLater": 5
    }
  }
}
```

---

> Built with love, bread, and code by **Bread Corporation** 🦆❤️💻
