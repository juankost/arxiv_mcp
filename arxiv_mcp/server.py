import arxiv
import os
import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from arxiv_mcp.mistral_ocr import convert_pdf_to_markdown, cleanup_markdown_text


load_dotenv()
PAPER_DIR = os.getenv("PAPER_DIR", "papers")
# os.makedirs(f"{PAPER_DIR}/pdf", exist_ok=True)
# os.makedirs(f"{PAPER_DIR}/md", exist_ok=True)

mcp = FastMCP("arxiv_mcp")


@mcp.tool()
def get_url_from_arxiv_paper_id(paper_id: str) -> str:
    """
    Get the URL of a paper from its arxiv ID, by querying the arXiv API

    Args:
        paper_id (str): The ID of the paper to get the URL for

    Returns:
        str: The URL of the paper, or None if the paper is not found
    """

    client = arxiv.Client()
    search = arxiv.Search(
        id_list=[paper_id], max_results=1, sort_by=arxiv.SortCriterion.LastUpdatedDate
    )

    papers = list(client.results(search))

    if len(papers) == 0:
        return None
    else:
        paper = papers[0]
        return paper.pdf_url


def get_paper_id_from_url(url_path: str) -> str:
    """
    Get the paper ID from the URL
    """
    paper_id = url_path.split("/")[-1]
    if "pdf" in paper_id:
        return paper_id.split(".")[0]
    else:
        return paper_id


def download_paper_pdf(url_path: str):
    """
    Download the PDF of a paper from its URL, and saves it to the PAPER_DIR.
    Returns the output path of the downloaded PDF.

    Args:
        url_path (str): The URL of the paper to download

    Returns:
        str: The path to the downloaded PDF
    """

    paper_id = get_paper_id_from_url(url_path)
    output_path = f"{PAPER_DIR}/pdf/{paper_id}.pdf"
    response = requests.get(url_path)
    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path


@mcp.tool()
def get_markdown_text_from_paper_URL(url_path: str):
    """
    Extracts nicely formatted markdown text from a paper URL and returns the markdown text
    Args:
        pdf_path (str): The path to the PDF file to convert.

    Returns:
        str: The path to the markdown file.
    """
    # Check if the markdown file exists in cache:
    paper_id = get_paper_id_from_url(url_path)
    output_path = f"{PAPER_DIR}/md/{paper_id}.md"
    if os.path.isfile(output_path):
        with open(output_path, "r") as f:
            return f.read()
    else:
        # It doesn't exist, download the PDF and convert it to markdown
        pdf_path = download_paper_pdf(url_path)
        markdown_path = f"{PAPER_DIR}/md/{paper_id}.md"
        markdown_text = convert_pdf_to_markdown(pdf_path, markdown_path)
        cleaned_markdown_text = cleanup_markdown_text(markdown_text)
        return cleaned_markdown_text


def test_get_url_from_arxiv_paper_id():
    paper_id = "2302.14691"
    expected_url = "arxiv.org/pdf/2302.14691"
    url = get_url_from_arxiv_paper_id(paper_id)
    print("Extracted URL: ", url)
    print("Expected URL: ", expected_url)
    assert expected_url in url


def test_download_paper_pdf():
    url_path = "https://arxiv.org/pdf/2302.14691"
    output_path = download_paper_pdf(url_path)
    print("Downloaded PDF to: ", output_path)
    assert os.path.isfile(output_path)


def test_get_markdown_text_from_paper_URL():
    url_path = "https://arxiv.org/pdf/2302.14691"
    markdown_text = get_markdown_text_from_paper_URL(url_path)
    print("Markdown text: ", markdown_text)
    assert markdown_text is not None


def test_get_paper_id_from_url():
    url_path = "https://arxiv.org/pdf/2302.14691"
    paper_id = get_paper_id_from_url(url_path)
    print("Paper ID: ", paper_id)
    assert paper_id == "2302.14691"


if __name__ == "__main__":
    test_get_url_from_arxiv_paper_id()
    test_download_paper_pdf()
    test_get_markdown_text_from_paper_URL()
    test_get_paper_id_from_url()
