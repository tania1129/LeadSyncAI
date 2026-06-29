from fastapi import APIRouter

router = APIRouter()


@router.post("/sync/{lead_id}")
def sync_lead_to_gorilla(lead_id: str):
    """
    TODO: Push a qualified lead to Gorilla CRM.
    1. Build the payload from the lead + AI qualification data.
    2. POST to GORILLA_API_URL with GORILLA_API_KEY auth.
    3. Store the response in GorillaSync (gorilla_lead_id, status).
    4. Write a sent_to_crm LeadEvent.
    5. On failure, set status = failed and store the error message.
    """
    return {"message": f"sync lead {lead_id} to Gorilla stub — not yet implemented"}


@router.get("/sync/{lead_id}/status")
def get_sync_status(lead_id: str):
    """
    TODO: Return the current GorillaSync record for this lead.
    Shows status (pending / success / failed / retrying),
    last_synced_at, and any error messages.
    """
    return {"message": f"sync status for lead {lead_id} stub — not yet implemented"}


@router.post("/sync/{lead_id}/retry")
def retry_sync(lead_id: str):
    """
    TODO: Re-attempt a failed Gorilla sync.
    Increments retry_count, resets status to pending, re-runs the push.
    Should be rate-limited (max 3 retries before flagging for manual review).
    """
    return {"message": f"retry sync for lead {lead_id} stub — not yet implemented"}


@router.post("/webhook")
def gorilla_webhook():
    """
    TODO: Receive status updates pushed FROM Gorilla back to LeadPulse.
    e.g. when a rep updates a lead in Gorilla, it notifies us here.
    Verifies a webhook secret, then updates the lead status and writes a LeadEvent.
    """
    return {"message": "Gorilla webhook stub — not yet implemented"}
