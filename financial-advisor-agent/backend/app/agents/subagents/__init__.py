"""
Subagent definitions for Financial Advisor AI Agent
"""
from .email_researcher import email_researcher_agent
from .calendar_scheduler import calendar_scheduler_agent
from .hubspot_manager import hubspot_manager_agent

__all__ = [
    'email_researcher_agent',
    'calendar_scheduler_agent',
    'hubspot_manager_agent'
]
