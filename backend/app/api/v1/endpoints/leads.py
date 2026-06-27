from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def list_leads():
    """
    TODO: Return paginated leads.
    Supports filtering by status, temperature, assigned_to, source, date range.
    Sales reps only see their own leads; managers/admins see all.
    """
    return {"message": "list leads stub — not yet implemented"}


@router.post("/")
def create_lead():
    """
    TODO: Create a new lead (manual intake or Wolfpack webhook).
    Automatically creates a lead_created LeadEvent.
    Optionally triggers AI qualification immediately.
    """
    return {"message": "create lead stub — not yet implemented"}


@router.get("/{lead_id}")
def get_lead(lead_id: str):
    """
    TODO: Return a single lead with full details:
    contact info, AI score, all LeadEvents (timeline), GorillaSync status.
    """
    return {"message": f"get lead {lead_id} stub — not yet implemented"}


@router.patch("/{lead_id}")
def update_lead(lead_id: str):
    """
    TODO: Update status, notes, assigned_to, actual_revenue, etc.
    Automatically writes a status_changed or note_added LeadEvent.
    """
    return {"message": f"update lead {lead_id} stub — not yet implemented"}


@router.delete("/{lead_id}")
def delete_lead(lead_id: str):
    """
    TODO: Soft-delete or disqualify — set status = disqualified.
    Hard deletes are intentionally not supported to preserve audit trail.
    """
    return {"message": f"delete lead {lead_id} stub — not yet implemented"}


@router.post("/{lead_id}/qualify")
def trigger_ai_qualification(lead_id: str):
    """
    TODO: Start an AI qualification session for this lead.
    Creates an AIQualification row, sets status = ai_qualifying,
    calls the Anthropic API with the qualification questions,
    stores the conversation + extracted data + score.
    """
    return {"message": f"qualify lead {lead_id} stub — not yet implemented"}


@router.get("/{lead_id}/events")
def get_lead_events(lead_id: str):
    """
    TODO: Return the full LeadEvent timeline for a lead, ordered by created_at.
    This is what powers the Lead Journey UI component.
    """
    return {"message": f"lead {lead_id} events stub — not yet implemented"}


@router.post("/{lead_id}/notes")
def add_note(lead_id: str):
    """
    TODO: Add a note to a lead.
    Creates a note_added LeadEvent with the note text in metadata.
    """
    return {"message": f"add note to lead {lead_id} stub — not yet implemented"}
