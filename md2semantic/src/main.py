import sys

import structlog

from src.config import settings
from src.etl.extract import GitHubExtractor
from src.etl.load import load_to_postgres
from src.etl.transform import parse_markdown
from src.utils.logger import configure_logger

configure_logger()
log = structlog.get_logger()

def main():
    try:
        log.info("🚀 Starting ETL Pipeline",
                 owner=settings.GITHUB_OWNER,
                 repo=settings.GITHUB_REPO,
                 branch=settings.GITHUB_BRANCH)

        # 1. Extract
        extractor = GitHubExtractor()
        raw_files = extractor.get_md_files()

        if not raw_files:
            log.warning("⚠️ No Markdown files found. Exiting.")
            return

        log.info("✅ Extraction complete", files_found=len(raw_files))

        # 2. Transform
        transformed_data = []
        for f in raw_files:
            result = parse_markdown(f)
            if result:
                transformed_data.append(result)

        log.info("✅ Transformation complete", docs_parsed=len(transformed_data))

        # 3. Load
        if transformed_data:
            load_to_postgres(transformed_data)
        else:
            log.warning("⚠️ No data available to load after transformation.")

        log.info("🏁 Pipeline Finished Successfully")

    except Exception as e:
        log.error("❌ Pipeline Failed", error=str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
