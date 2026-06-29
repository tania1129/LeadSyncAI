from fastapi import APIRouter

router = APIRouter()


@router.get("/dashboard")
def get_dashboard_stats():
    """
    TODO: Return top-level KPIs for the dashboard:
    total_leads, qualified_leads, closed_won, total_revenue,
    conversion_rate, avg_ai_score, avg_sales_cycle_days.
    Supports date range filtering.
    """
    return {"message": "dashboard stats stub — not yet implemented"}


@router.get("/sales-reps")
def get_sales_rep_performance():
    """
    TODO: Return per-rep breakdown:
    leads_assigned, leads_closed, revenue_generated, conversion_rate.
    Powers the salesperson leaderboard on the dashboard.
    """
    return {"message": "sales rep performance stub — not yet implemented"}


@router.get("/lead-sources")
def get_lead_source_breakdown():
    """
    TODO: Return conversion rate and revenue grouped by lead source
    (wolfpack, website, referral, manual, other).
    """
    return {"message": "lead source breakdown stub — not yet implemented"}


@router.get("/conversion-funnel")
def get_conversion_funnel():
    """
    TODO: Return count of leads at each pipeline stage so the
    frontend can render a funnel chart.
    e.g. new → qualified → contacted → appointment_set → closed_won
    """
    return {"message": "conversion funnel stub — not yet implemented"}


@router.get("/ai-insights")
def get_ai_insights():
    """
    TODO: Return AI-generated insights about the sales data.
    e.g. 'High-scoring leads in Miami convert 25% better than average.'
    Calls the Anthropic API with aggregated stats and returns bullet insights.
    """
    return {"message": "ai insights stub — not yet implemented"}


@router.get("/revenue-over-time")
def get_revenue_over_time():
    """
    TODO: Return revenue grouped by day/week/month for a line chart.
    Supports granularity param: ?granularity=week
    """
    return {"message": "revenue over time stub — not yet implemented"}
