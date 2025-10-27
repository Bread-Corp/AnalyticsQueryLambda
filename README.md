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

## 🔧 Setup & Deployment

Ready to deploy your analytics powerhouse? Let's build something amazing! 🚀

### 📋 Prerequisites
- AWS Account with Lambda, RDS, and API Gateway permissions 🔑
- RDS SQL Server with comprehensive tender schema 🗄️
- Analytics database user (`AnalyticsAppUser`) with SELECT permissions 👤
- External User & Watchlist APIs deployed and accessible 🌐
- Docker Desktop for Linux-compatible layer building 🐳

### 🚀 Deployment Steps

#### 1. **🏗️ Build the Data Layer**
```bash
# Navigate to the layer build directory
cd pymssql-layer-build

# Execute the Docker build script
./build.bat

# Upload the resulting pymssql-layer.zip to AWS Lambda Layers
```

#### 2. **⚡ Create the Analytics Lambda**
- **Function Name**: `AnalyticsQueryHandler` 
- **Runtime**: Python 3.9 🐍
- **Architecture**: x86_64
- **Execution Role**: Lambda + VPC + CloudWatch permissions

#### 3. **🔧 Configure Intelligence Variables**
Set up your analytics environment in the Lambda configuration:

| Variable | Purpose | Example |
|----------|---------|---------|
| `DB_ENDPOINT` | Database connection point | `analytics-db.cluster-xxx.rds.amazonaws.com` |
| `DB_NAME` | Target database | `tendertool_production` |
| `DB_USER` | Analytics user account | `AnalyticsAppUser` |
| `DB_PASSWORD` | Secure access credentials | `[YourSecurePassword]` |

#### 4. **📦 Deploy the Intelligence Code**
```bash
# Package your analytics engine
zip analytics-function.zip lambda_function.py db_handler.py

# Upload via AWS Console or CLI
aws lambda update-function-code --function-name AnalyticsQueryHandler --zip-file fileb://analytics-function.zip
```

#### 5. **🔗 Attach Intelligence Layers**
- Add your `pymssql-layer` for database connectivity
- Attach your `requests-layer` for API integrations

#### 6. **🌐 Configure API Gateway**
```bash
# Create HTTP API endpoint
aws apigatewayv2 create-api --name TenderAnalyticsAPI --protocol-type HTTP

# Configure GET /analytics route
aws apigatewayv2 create-route --api-id [your-api-id] --route-key "GET /analytics"
```

## ⚙️ Configuration (Environment Variables)

| Variable | Required | Description | Example Value |
|----------|----------|-------------|---------------|
| `DB_ENDPOINT` | ✅ Yes | RDS SQL Server hostname | `tender-analytics.cluster-xxx.rds.amazonaws.com` |
| `DB_NAME` | ✅ Yes | Target database name | `tendertool_production` |
| `DB_USER` | ✅ Yes | Analytics database user | `AnalyticsAppUser` |
| `DB_PASSWORD` | ✅ Yes | Database access password | `[SecurePassword123!]` |
| `USER_FETCH_API_URL` | 🔶 Optional | User management API template | `https://api.example.com/dev/tenderuser/fetch/{}` |
| `WATCHLIST_API_URL` | 🔶 Optional | Watchlist service API template | `https://api.example.com/dev/watchlist/{}` |

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
