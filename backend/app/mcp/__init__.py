"""MCP clients registry.

Import this module to obtain MCP client stubs. In production this file should
instantiate real MCP client wrappers that communicate with MCP servers.
"""
from .email_mcp import EmailMCP
from .tavily_server import TavilyMCP
from .youtube_server import YouTubeMCP
from .document_server import DocumentMCP
from .calendar_server import CalendarMCP
from .notification_server import NotificationMCP
from .analytics_server import AnalyticsMCP


def get_email_mcp() -> EmailMCP:
    return EmailMCP()


def get_tavily_mcp() -> TavilyMCP:
    return TavilyMCP()


def get_youtube_mcp() -> YouTubeMCP:
    return YouTubeMCP()


def get_document_mcp() -> DocumentMCP:
    return DocumentMCP()


def get_calendar_mcp() -> CalendarMCP:
    return CalendarMCP()


def get_notification_mcp() -> NotificationMCP:
    return NotificationMCP()


def get_analytics_mcp() -> AnalyticsMCP:
    return AnalyticsMCP()
# MCP servers will live here (stubs/clients)
