import requests
import structlog

from src.config import settings

log = structlog.get_logger()

class GitHubExtractor:
    def __init__(self):
        self.headers = {"Authorization": f"token {settings.GITHUB_TOKEN}"} if settings.GITHUB_TOKEN else {}

    def fetch_file_content(self, download_url: str) -> str:
        """
        Fetch raw content from a GitHub file URL.

        Args:
            download_url: Direct download URL for the file from GitHub API

        Returns:
            Raw text content of the file

        Raises:
            Exception: If the HTTP request fails or times out
        """
        try:
            response = requests.get(download_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            log.error("Failed to fetch file", url=download_url, error=str(e))
            raise

    def get_md_files(self, path: str = "", collected_count: int = 0) -> list[dict]:
        """
        Recursively crawl repo for .md files up to MAX_FILES limit.

        Args:
            path: Directory path within the repository
            collected_count: Current number of files collected (for recursion)

        Returns:
            List of dictionaries containing file metadata and content
        """
        # Early return if we've already hit the limit
        if collected_count >= settings.MAX_FILES:
            return []

        url = f"https://api.github.com/repos/{settings.GITHUB_OWNER}/{settings.GITHUB_REPO}/contents/{path}"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            items = response.json()
        except Exception as e:
            log.error("Failed to list repo contents", path=path, error=str(e))
            return []

        md_files = []
        for item in items:
            # Check if we've reached the limit
            if collected_count + len(md_files) >= settings.MAX_FILES:
                break

            if item["type"] == "file" and item["name"].endswith(".md"):
                content = self.fetch_file_content(item["download_url"])
                md_files.append({
                    "file_name": item["name"],
                    "source_url": item["html_url"],
                    "content": content
                })

            elif item["type"] == "dir":
                # Only recurse if we haven't hit the limit
                remaining = settings.MAX_FILES - (collected_count + len(md_files))
                if remaining > 0:
                    md_files.extend(
                        self.get_md_files(item["path"], collected_count + len(md_files))
                    )

        return md_files
