"""
Data Sync API Endpoints

Handles initial and incremental data synchronization from Gmail and HubSpot.
"""
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from app.database import get_db
from app.api.dependencies import get_current_user
from app.models import User
from app.services.ingestion_service import IngestionService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class SyncRequest(BaseModel):
    """Request model for data sync"""
    max_emails: Optional[int] = 100
    max_contacts: Optional[int] = 100
    email_query: Optional[str] = None
    sync_gmail: bool = True
    sync_hubspot: bool = True


class SyncResponse(BaseModel):
    """Response model for data sync"""
    status: str
    message: str
    task_id: Optional[str] = None


@router.post("/initial", response_model=SyncResponse)
async def initial_sync(
    request: SyncRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Trigger initial data sync for user

    This endpoint ingests data from Gmail and HubSpot and creates embeddings
    for semantic search. The sync runs in the background.

    Args:
        request: Sync configuration
        background_tasks: FastAPI background tasks
        current_user: Authenticated user
        db: Database session

    Returns:
        SyncResponse with status and message

    Example:
        POST /api/sync/initial
        {
            "max_emails": 100,
            "max_contacts": 100,
            "email_query": "newer_than:90d",
            "sync_gmail": true,
            "sync_hubspot": true
        }
    """
    try:
        # Validate user has required OAuth tokens
        if request.sync_gmail and not current_user.google_token:
            raise HTTPException(
                status_code=400,
                detail="Google OAuth not configured. Please authenticate with Google first."
            )

        if request.sync_hubspot and not current_user.hubspot_token:
            raise HTTPException(
                status_code=400,
                detail="HubSpot OAuth not configured. Please authenticate with HubSpot first."
            )

        # Add sync task to background
        background_tasks.add_task(
            _perform_sync,
            user_id=current_user.id,
            max_emails=request.max_emails,
            max_contacts=request.max_contacts,
            email_query=request.email_query,
            sync_gmail=request.sync_gmail,
            sync_hubspot=request.sync_hubspot
        )

        logger.info(f"Initial sync triggered for user {current_user.email}")

        return SyncResponse(
            status="success",
            message="Initial sync started in background. This may take a few minutes.",
            task_id=None  # TODO: Add proper task tracking
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error triggering initial sync: {e}")
        raise HTTPException(status_code=500, detail=f"Error starting sync: {str(e)}")


@router.post("/incremental", response_model=SyncResponse)
async def incremental_sync(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Trigger incremental data sync for user

    This endpoint syncs only new data since the last sync.
    Uses last_gmail_sync and last_hubspot_sync timestamps from user model.

    Args:
        background_tasks: FastAPI background tasks
        current_user: Authenticated user
        db: Database session

    Returns:
        SyncResponse with status and message
    """
    try:
        # Check if initial sync has been done
        if not current_user.last_gmail_sync and not current_user.last_hubspot_sync:
            raise HTTPException(
                status_code=400,
                detail="No initial sync found. Please run initial sync first."
            )

        # Determine query based on last sync
        email_query = None
        if current_user.last_gmail_sync:
            # Format date for Gmail query
            date_str = current_user.last_gmail_sync.strftime("%Y/%m/%d")
            email_query = f"after:{date_str}"

        # Add sync task to background
        background_tasks.add_task(
            _perform_sync,
            user_id=current_user.id,
            max_emails=50,  # Smaller limit for incremental
            max_contacts=50,
            email_query=email_query,
            sync_gmail=bool(current_user.google_token),
            sync_hubspot=bool(current_user.hubspot_token)
        )

        logger.info(f"Incremental sync triggered for user {current_user.email}")

        return SyncResponse(
            status="success",
            message="Incremental sync started in background.",
            task_id=None
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error triggering incremental sync: {e}")
        raise HTTPException(status_code=500, detail=f"Error starting sync: {str(e)}")


@router.get("/status")
async def sync_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get sync status for user

    Returns:
        Dict with last sync timestamps and data counts
    """
    try:
        from app.services.retrieval_service import RetrievalService

        # Get document stats
        retrieval_service = RetrievalService(db)
        stats = retrieval_service.get_stats(current_user)

        return {
            "last_gmail_sync": current_user.last_gmail_sync.isoformat() if current_user.last_gmail_sync else None,
            "last_hubspot_sync": current_user.last_hubspot_sync.isoformat() if current_user.last_hubspot_sync else None,
            "gmail_configured": bool(current_user.google_token),
            "hubspot_configured": bool(current_user.hubspot_token),
            "document_counts": stats
        }

    except Exception as e:
        logger.error(f"Error getting sync status: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting status: {str(e)}")


def _perform_sync(
    user_id: str,
    max_emails: int,
    max_contacts: int,
    email_query: Optional[str],
    sync_gmail: bool,
    sync_hubspot: bool
):
    """
    Background task to perform actual sync

    Args:
        user_id: User ID to sync for
        max_emails: Maximum emails to sync
        max_contacts: Maximum contacts to sync
        email_query: Optional Gmail query filter
        sync_gmail: Whether to sync Gmail
        sync_hubspot: Whether to sync HubSpot
    """
    from app.database import SessionLocal

    db = SessionLocal()

    try:
        # Get user
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            logger.error(f"User {user_id} not found for sync")
            return

        # Create ingestion service
        ingestion_service = IngestionService(db)

        # Perform sync
        if sync_gmail and sync_hubspot:
            results = ingestion_service.ingest_all(
                user=user,
                max_emails=max_emails,
                max_contacts=max_contacts,
                email_query=email_query
            )
            logger.info(f"Full sync complete for user {user.email}: {results}")

        elif sync_gmail:
            results = ingestion_service.ingest_gmail_emails(
                user=user,
                max_emails=max_emails,
                query=email_query
            )
            logger.info(f"Gmail sync complete for user {user.email}: {results}")

        elif sync_hubspot:
            results = ingestion_service.ingest_hubspot_data(
                user=user,
                max_contacts=max_contacts
            )
            logger.info(f"HubSpot sync complete for user {user.email}: {results}")

    except Exception as e:
        logger.error(f"Error in background sync task: {e}")

    finally:
        db.close()
