from __future__ import annotations


class CMSClient:
    """Represent a future integration with a content management system."""

    def fetch_context(self, context_id: str) -> dict[str, str]:
        """Retrieve context data from the CMS."""

        raise NotImplementedError
