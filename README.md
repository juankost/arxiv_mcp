# ArXiv MCP Server

A Model Context Protocol (MCP) server that provides seamless access to ArXiv papers through intelligent PDF download and markdown conversion capabilities. This server enables AI assistants and other MCP clients to easily retrieve and process academic papers from ArXiv.

## 🚀 Features

- **ArXiv Integration**: Download papers directly from ArXiv using paper IDs or URLs
- **Smart OCR Conversion**: Convert PDF papers to clean markdown using Mistral's OCR API
- **Intelligent Caching**: Automatically cache downloaded PDFs and converted markdown files
- **Robust Error Handling**: Built-in retry logic with exponential backoff for API reliability
- **Easy Deployment**: Simple setup for both local development and remote deployment
- **MCP Compatible**: Works seamlessly with Cursor, Claude Desktop, and other MCP clients

## 📋 Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Mistral API key (get one at [console.mistral.ai](https://console.mistral.ai/))

## 🛠️ Installation

### Local Development Setup

1. **Clone the repository**:

   ```bash
   git clone <your-repo-url>
   cd arxiv_mcp
   ```

2. **Install dependencies**:

   ```bash
   uv sync
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory:

   ```bash
   MISTRAL_API_KEY=your_mistral_api_key_here
   PAPER_DIR=papers  # Optional: default is "papers"
   PORT=8001         # Optional: default is 8001
   TRANSPORT=stdio   # Optional: default is "stdio"
   ```

4. **Create required directories**:
   ```bash
   mkdir -p papers/pdf papers/md
   ```

## 🚀 Usage

### Running Locally

**Option 1: Direct execution**

```bash
uv run python main.py
```

**Option 2: Using the installed script**

```bash
uv run arxiv-mcp
```

**Option 3: Testing with MCP Inspector**

```bash
npm run inspect
```

### Connecting to Cursor

Add the following to your Cursor MCP configuration:

**For local development (stdio transport)**:

```json
{
  "mcpServers": {
    "arxiv-mcp": {
      "command": "uv",
      "args": ["run", "python", "/path/to/arxiv_mcp/main.py"],
      "env": {
        "MISTRAL_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**For remote deployment (HTTP transport)**:

```json
{
  "mcpServers": {
    "arxiv-mcp": {
      "command": "uv",
      "args": ["run", "python", "/path/to/arxiv_mcp/main.py"],
      "env": {
        "MISTRAL_API_KEY": "your_api_key_here",
        "TRANSPORT": "http",
        "PORT": "8001"
      }
    }
  }
}
```

## 🔧 Available Tools

### `get_url_from_arxiv_paper_id`

Get the PDF URL for an ArXiv paper using its ID.

**Parameters**:

- `paper_id` (str): The ArXiv paper ID (e.g., "2302.14691")

**Returns**: The PDF URL of the paper

### `get_markdown_text_from_paper_URL`

Download a paper from URL and convert it to clean markdown format.

**Parameters**:

- `url_path` (str): The URL of the ArXiv paper PDF

**Returns**: The paper content as formatted markdown text

**Features**:

- Automatic caching (won't re-download/convert existing papers)
- Handles large PDFs with intelligent page splitting
- Robust error handling with retry logic

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Add tests** if applicable
5. **Commit your changes**:
   ```bash
   git commit -m 'Add amazing feature'
   ```
6. **Push to the branch**:
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Running Tests

```bash
# Run the built-in tests
uv run python arxiv_mcp/server.py
```

## 📁 Project Structure

```
arxiv_mcp/
├── arxiv_mcp/           # Main package
│   ├── __init__.py      # Package initialization
│   ├── server.py        # MCP server implementation
│   ├── mistral_ocr.py   # PDF to markdown conversion
│   └── utils.py         # Utility functions
├── main.py              # Entry point
├── pyproject.toml       # Python project configuration
├── package.json         # Node.js dependencies (for MCP inspector)
├── papers/              # Cache directory for downloaded papers
│   ├── pdf/            # Cached PDF files
│   └── md/             # Cached markdown files
└── README.md           # This file
```

## ⚙️ Configuration

### Environment Variables

| Variable          | Description                       | Default  | Required |
| ----------------- | --------------------------------- | -------- | -------- |
| `MISTRAL_API_KEY` | Your Mistral API key              | -        | ✅       |
| `PAPER_DIR`       | Directory to store papers         | `papers` | ❌       |
| `PORT`            | Server port                       | `8001`   | ❌       |
| `TRANSPORT`       | Transport method (`stdio`/`http`) | `stdio`  | ❌       |

### Paper Storage

Papers are automatically organized in the following structure:

```
papers/
├── pdf/    # Original PDF files (cached by ArXiv ID)
└── md/     # Converted markdown files (cached by ArXiv ID)
```

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [ArXiv](https://arxiv.org/) for providing free access to academic papers
- [Mistral AI](https://mistral.ai/) for their excellent OCR API
- [Model Context Protocol](https://modelcontextprotocol.io/) for the MCP framework
