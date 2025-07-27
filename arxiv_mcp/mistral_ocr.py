from mistralai import Mistral
import os
from arxiv_mcp.utils import retry_with_exponential_backoff


def cleanup_markdown_text(markdown_text: str) -> str:
    """
    Cleanup the markdown text by removing the references, acknowledgments, and Appendix sections
    (unless specified to keep the appendix)

    Args:
        markdown_text (str): The markdown text to cleanup

    Returns:
        str: The cleaned up markdown text
    """

    # TODO: Not implemented yet, returning original markdown text
    return markdown_text


@retry_with_exponential_backoff(max_retries=3, base_delay=2.0, max_delay=300.0)
def convert_pdf_to_markdown(
    url_path: str,
    markdown_path: str,
):
    """Converts a PDF file from a URL to a Markdown file using the Mistral OCR API.

    Args:
        url_path (str): The URL of the input PDF document.
        markdown_path (str): The file path where the output Markdown text will be saved.
    """
    use_cache = os.environ.get("USE_CACHE") == "1"

    if use_cache and markdown_path and os.path.exists(markdown_path):
        print(f"Loading cached markdown file from {markdown_path}")
        with open(markdown_path, "r") as f:
            return f.read()

    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

    try:
        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": url_path,
            },
            include_image_base64=True,
            timeout_ms=180000,  # Increased timeout for large files from URL
        )

        markdown_text = ""
        for page in ocr_response.pages:
            markdown_text += page.markdown

        if use_cache and markdown_path:
            # Create directory for markdown file if it doesn't exist
            os.makedirs(os.path.dirname(markdown_path), exist_ok=True)
            with open(markdown_path, "w") as f:
                f.write(markdown_text)

        return markdown_text

    except Exception as e:
        print(f"Error processing PDF from URL {url_path}: {e}")
        raise
