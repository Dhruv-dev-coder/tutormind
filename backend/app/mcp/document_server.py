"""Document Processing MCP server stub.

Handles PDF/DOCX/TXT extraction, chunking and basic parsing. Production must
forward to a specialized MCP document processor that returns chunks and metadata.
"""
from typing import Dict, Any, List
import re
from datetime import datetime, timedelta


class DocumentMCP:
    async def extract_text(self, document_bytes: bytes, content_type: str) -> str:
        """Extract text from document bytes."""
        try:
            if isinstance(document_bytes, bytes):
                return document_bytes.decode('utf-8')
            return str(document_bytes)
        except Exception as e:
            print(f"Text extraction failed: {e}")
            return ""

    async def parse_syllabus(self, text: str) -> Dict[str, Any]:
        """Parse syllabus text into structured chapters."""
        chapters = []
        lines = text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line and len(line) > 3:
                # Skip very short lines or empty lines
                chapters.append({
                    "name": line[:100],
                    "topics": [f"Topic {i+1}" for i in range(3)],
                    "estimated_hours": 5 + (len(chapters) % 10),
                    "difficulty": ["beginner", "intermediate", "advanced"][len(chapters) % 3]
                })
        
        return {"chapters": chapters, "total_topics": len(chapters)}

    async def parse_datesheet(self, text: str) -> Dict[str, Any]:
        """Parse datesheet text to extract exam dates."""
        # Try to extract dates using regex
        date_patterns = [
            r'(\d{4}-\d{2}-\d{2})',
            r'(\d{1,2}/\d{1,2}/\d{4})',
            r'(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})',
        ]
        
        today = datetime.now()
        exam_date = today + timedelta(days=90)
        days_remaining = 90
        
        # Try to find dates in the text
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                try:
                    # Parse the first found date
                    if '-' in matches[0]:
                        exam_date = datetime.strptime(matches[0], '%Y-%m-%d')
                    elif '/' in matches[0]:
                        exam_date = datetime.strptime(matches[0], '%m/%d/%Y')
                    days_remaining = max(1, (exam_date - today).days)
                    break
                except:
                    continue
        
        return {
            "exam_date": exam_date.isoformat(),
            "days_remaining": days_remaining,
            "subjects": ["Mathematics", "Science", "English"]
        }

    async def chunk_content(self, text: str, chunk_size: int = 1000) -> List[Dict[str, Any]]:
        """Chunk text into smaller pieces for processing."""
        chunks = []
        for i, start in enumerate(range(0, len(text), chunk_size)):
            chunks.append({
                "chunk_id": f"c{i+1}",
                "text": text[start:start + chunk_size]
            })
        return chunks
