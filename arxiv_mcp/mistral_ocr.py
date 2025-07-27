from mistralai import Mistral
import PyPDF2
from typing import Optional, List
import os
from arxiv_mcp.utils import retry_with_exponential_backoff

MIN_PAGES = 10


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


def get_pdf_page_count(pdf_path: str) -> int:
    """Get the total number of pages in a PDF file."""
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        return len(pdf_reader.pages)


@retry_with_exponential_backoff(max_retries=3, base_delay=2.0, max_delay=300.0)
def convert_pdf_to_markdown(
    pdf_path: str,
    markdown_path: str,
    uploaded_pdf: Optional[str] = None,
    pages: Optional[List[int]] = None,
):
    """Converts a PDF file to a Markdown file using the Mistral OCR API.

    Args:
        pdf_path (str): The file path to the input PDF document.
        markdown_path (str): The file path where the output Markdown text will be saved.
        uploaded_pdf (str, optional): The uploaded PDF file.
        pages (List[int], optional): The pages to process. If None, all pages will be processed.
    """

    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

    # Upload PDF if not already uploaded
    if uploaded_pdf is None:
        uploaded_pdf = client.files.upload(
            file={
                "file_name": pdf_path,
                "content": open(pdf_path, "rb"),
            },
            purpose="ocr",
        )

    # Get total page count if pages not specified
    if pages is None:
        total_pages = get_pdf_page_count(pdf_path)
        pages = list(range(total_pages))

    # Try processing the whole PDF or divide and conquer it
    try:
        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": client.files.get_signed_url(file_id=uploaded_pdf.id).url,
            },
            pages=pages,
            timeout_ms=60000,  # Increased timeout for large files
        )

        # Are we processing the whole PDF?
        is_top_level = len(pages) == get_pdf_page_count(pdf_path)
        if is_top_level:
            markdown_text = ""
            for page in ocr_response.pages:
                markdown_text += page.markdown

            with open(markdown_path, "w") as f:
                f.write(markdown_text)
            return markdown_text
        else:
            # We will simply return the markdown text, and the list of page info chunks
            markdown_text = ""
            for page in ocr_response.pages:
                markdown_text += page.markdown
            return markdown_text

    except Exception as e:
        print(f"Error processing pages {pages[0]}-{pages[-1]}: {e}")

        # If we have too few pages to divide further, raise the error
        if len(pages) <= MIN_PAGES:
            raise Exception(
                f"Failed to process PDF pages {pages[0]}-{pages[-1]} and cannot divide further "
                f"(minimum {MIN_PAGES} pages)"
            )

        # Divide and conquer: split pages in half
        mid_point = len(pages) // 2
        first_half = pages[:mid_point]
        second_half = pages[mid_point:]

        print(f"Dividing pages {pages[0]}-{pages[-1]} into two halves:")
        print(f"  First half: {first_half[0]}-{first_half[-1]} ({len(first_half)} pages)")
        print(f"  Second half: {second_half[0]}-{second_half[-1]} ({len(second_half)} pages)")

        # Recursively process each half
        first_half_text = convert_pdf_to_markdown(pdf_path, markdown_path, uploaded_pdf, first_half)
        second_half_text = convert_pdf_to_markdown(
            pdf_path, markdown_path, uploaded_pdf, second_half
        )

        # Combine results
        combined_text = first_half_text + second_half_text

        # Save combined result if this is the top-level call
        if len(pages) == get_pdf_page_count(pdf_path):
            with open(markdown_path, "w") as f:
                f.write(combined_text)

        else:
            # just return the combined text and page info to the parent call
            return combined_text
    return
