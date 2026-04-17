"""
GA4 Google Ads Campaign Report for oi.tax
Property ID: 273918863

Requirements:
    pip install google-analytics-data google-auth

Usage:
    python ga4_ads_report.py --key service_account.json
"""

import argparse
import json
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    OrderBy,
)
from google.oauth2 import service_account

PROPERTY_ID = "273918863"

DIMENSIONS = [
    "sessionGoogleAdsCampaignName",
    "sessionGoogleAdsMedium",
    "sessionDefaultChannelGroup",
    "month",
]

METRICS = [
    "sessions",
    "totalUsers",
    "newUsers",
    "bounceRate",
    "averageSessionDuration",
    "conversions",
    "totalRevenue",
]


def build_client(key_path: str) -> BetaAnalyticsDataClient:
    creds = service_account.Credentials.from_service_account_file(
        key_path,
        scopes=["https://www.googleapis.com/auth/analytics.readonly"],
    )
    return BetaAnalyticsDataClient(credentials=creds)


def run_report(client: BetaAnalyticsDataClient, start: str, end: str) -> dict:
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        dimensions=[Dimension(name=d) for d in DIMENSIONS],
        metrics=[Metric(name=m) for m in METRICS],
        date_ranges=[DateRange(start_date=start, end_date=end)],
        order_bys=[
            OrderBy(
                metric=OrderBy.MetricOrderBy(metric_name="sessions"),
                desc=True,
            )
        ],
    )
    return client.run_report(request)


def format_report(response) -> None:
    headers = [d.name for d in response.dimension_headers] + [
        m.name for m in response.metric_headers
    ]
    print("\t".join(headers))
    print("-" * 120)
    for row in response.rows:
        dims = [v.value for v in row.dimension_values]
        mets = [v.value for v in row.metric_values]
        print("\t".join(dims + mets))
    print(f"\nTotal rows: {response.row_count}")


def main():
    parser = argparse.ArgumentParser(description="GA4 Google Ads report for oi.tax")
    parser.add_argument("--key", required=True, help="Path to service account JSON key")
    parser.add_argument("--start", default="2025-01-01", help="Start date YYYY-MM-DD")
    parser.add_argument("--end", default="today", help="End date YYYY-MM-DD or 'today'")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    client = build_client(args.key)
    response = run_report(client, args.start, args.end)

    if args.json:
        rows = []
        for row in response.rows:
            record = {}
            for i, d in enumerate(response.dimension_headers):
                record[d.name] = row.dimension_values[i].value
            for i, m in enumerate(response.metric_headers):
                record[m.name] = row.metric_values[i].value
            rows.append(record)
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        format_report(response)


if __name__ == "__main__":
    main()
