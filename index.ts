// ─── Enums ────────────────────────────────────────────────────────────────────

export type UserRole = "admin" | "manager" | "sales_rep";

export type LeadStatus =
  | "new"
  | "ai_qualifying"
  | "qualified"
  | "sent_to_crm"
  | "contacted"
  | "appointment_set"
  | "proposal_sent"
  | "closed_won"
  | "closed_lost"
  | "disqualified";

export type LeadTemperature = "hot" | "warm" | "cold";
export type LeadSource = "wolfpack" | "website" | "referral" | "manual" | "other";
export type SyncStatus = "pending" | "success" | "failed" | "retrying";

export type EventType =
  | "lead_created"
  | "ai_qualification_started"
  | "ai_qualification_completed"
  | "sent_to_crm"
  | "assigned"
  | "status_changed"
  | "note_added"
  | "contacted"
  | "appointment_set"
  | "proposal_sent"
  | "closed_won"
  | "closed_lost";

// ─── Core Models ──────────────────────────────────────────────────────────────

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
}

export interface Lead {
  id: string;
  first_name: string;
  last_name: string;
  email?: string;
  phone?: string;
  address?: string;
  city?: string;
  state?: string;
  zip_code?: string;
  source: LeadSource;
  status: LeadStatus;
  temperature?: LeadTemperature;
  service_interest?: string;

  // AI outputs
  ai_score?: number;
  ai_summary?: string;
  ai_recommended_action?: string;

  // Business data
  estimated_budget?: number;
  actual_revenue?: number;
  timeline?: string;
  is_decision_maker?: boolean;
  notes?: string;

  // CRM
  gorilla_lead_id?: string;
  gorilla_synced_at?: string;

  // Relations
  assigned_to?: string;
  assigned_to_user?: User;
  events?: LeadEvent[];

  closed_at?: string;
  created_at: string;
  updated_at: string;
}

export interface LeadEvent {
  id: string;
  lead_id: string;
  event_type: EventType;
  title: string;
  description?: string;
  metadata?: Record<string, unknown>;
  created_at: string;
  created_by_user?: User;
}

// ─── Analytics ────────────────────────────────────────────────────────────────

export interface DashboardStats {
  total_leads: number;
  qualified_leads: number;
  closed_won: number;
  total_revenue: number;
  conversion_rate: number;
  avg_ai_score: number;
  avg_sales_cycle_days: number;
}

export interface SalesRepPerformance {
  user_id: string;
  full_name: string;
  leads_assigned: number;
  leads_closed: number;
  revenue_generated: number;
  conversion_rate: number;
}

export interface LeadSourceBreakdown {
  source: LeadSource;
  count: number;
  conversion_rate: number;
  revenue: number;
}

// ─── Auth ─────────────────────────────────────────────────────────────────────

export interface AuthTokens {
  access_token: string;
  token_type: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}
