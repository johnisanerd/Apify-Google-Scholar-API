# 🎓 Google Scholar API: Papers, Citations, and Author Profiles in Clean JSON

> The efficient, reliable, and developer-friendly way to use the Google Scholar API.

**Actor page:** [apify.com/johnvc/google-scholar-api](https://apify.com/johnvc/google-scholar-api?fpr=9n7kx3)
**Input schema:** [apify.com/johnvc/google-scholar-api/input-schema](https://apify.com/johnvc/google-scholar-api/input-schema?fpr=9n7kx3)

The Google Scholar API returns academic search results, citation formats, and author profiles as clean, structured JSON. A single `mode` parameter dispatches to six endpoints: search papers, get citation formats for a paper, or pull an author's profile, articles, citations, and co-authors. Each search result carries the title, authors, publication summary, cited-by count, versions, and links. Built for literature reviews, citation analysis, research dashboards, and AI agent workflows.

## Video Walkthrough

[![Watch the walkthrough](https://img.youtube.com/vi/jREWahDGhJM/maxresdefault.jpg)](https://www.youtube.com/watch?v=jREWahDGhJM)

## Quick Start

### Prerequisites
- Python 3.11 or higher
- An Apify account and API key ([get a free key here](https://apify.com?fpr=9n7kx3))

1. **Clone the repository**
   ```bash
   git clone https://github.com/johnisanerd/Apify-Google-Scholar-API.git
   cd Apify-Google-Scholar-API
   ```

2. **Install dependencies with UV**
   ```bash
   # Install UV if you do not have it:
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install project dependencies:
   uv sync
   ```

3. **Configure your API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your Apify API key
   # Get your free API key at: https://apify.com?fpr=9n7kx3
   ```

4. **Run the example**
   ```bash
   uv run python google-scholar-api-example.py
   ```

### Alternative: set the API key directly
```bash
export APIFY_API_TOKEN="your_api_key_here"
uv run python google-scholar-api-example.py
```

## Modes

| Mode | What it returns | Key input |
|------|-----------------|-----------|
| `search` | Papers for a query, one row per paper | `q` (or `cites`, `cluster`) |
| `cite` | Citation formats (MLA, APA, and more) for a paper | `result_id` |
| `author_profile` | An author's profile and metrics | `author_id` |
| `author_articles` | An author's article list | `author_id` |
| `author_citation` | One article from an author's profile | `author_id`, `citation_id` |
| `author_co_authors` | An author's co-authors | `author_id` |

## Why Use This Google Scholar API?

**Six endpoints, one Actor.** Search, citation formats, and four author endpoints, all selected with a single `mode`.

**Rich search results.** Each paper comes back with title, authors (with author IDs), publication summary, cited-by total, versions, and links to citing and related pages.

**Author graphs.** Resolve an `author_id` to a profile, the full article list, a single citation, or the co-author network.

**Precise filtering.** Restrict by year range (`as_ylo`, `as_yhi`), language, review-articles-only, and result type (articles, case law, or include patents).

**Predictable, pay-per-use pricing.** Billing is per query (per page on paginated modes), with a small per-run fee.

**Easy to automate.** Call it from Python in a few lines, or load it as an MCP tool so assistants like Claude and Cursor can run literature searches for you on demand.

## Features

### Core Capabilities
- Paper search with year, language, and type filters
- Citation-format lookup for any result
- Author profile, articles, citation, and co-author endpoints
- Pagination on search and author-articles modes
- Optional patents and case-law results via `as_sdt`

### Data Quality
- One row per paper in search mode, with a stable `result_id`
- Authors as structured entries with `author_id` for chaining
- Cited-by and versions counts on every result
- Search parameters echoed on every row

## Usage Examples

### Search papers
```json
{
  "mode": "search",
  "q": "machine learning",
  "as_ylo": 2020,
  "num": 10
}
```

### Citation formats for a paper
```json
{
  "mode": "cite",
  "result_id": "EQ8shYj8Ai8J"
}
```

### An author's articles
```json
{
  "mode": "author_articles",
  "author_id": "rSVIHasAAAAJ",
  "sort": "pubdate"
}
```

## Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `mode` | `str` | Yes | `search` | `search`, `cite`, `author_profile`, `author_articles`, `author_citation`, `author_co_authors`. |
| `q` | `str` | for search | - | Query; supports operators like `author:smith`, `source:nature`. |
| `cites` / `cluster` | `str` | no | - | Article ID for citing papers / all versions (search mode). |
| `result_id` | `str` | for cite | - | Paper cluster ID (from a search result). |
| `author_id` | `str` | for author modes | - | Google Scholar author ID, e.g. `rSVIHasAAAAJ`. |
| `citation_id` | `str` | for author_citation | - | Specific article ID in an author's profile. |
| `hl` | `str` | no | `en` | Interface language. |
| `as_ylo` / `as_yhi` | `int` | no | - | Earliest / latest publication year (search mode). |
| `as_sdt` | `str` | no | `0` | `0` exclude patents, `7` include patents, `4` case law. |
| `num` | `int` | no | `10` | Results per page (search 1-20, author_articles 1-100). |
| `max_pages` | `int` | no | `1` | Pages to fetch (search and author_articles). |

## Output Format

A real `search` for `machine learning` returns one row per paper (the `snippet` is present but trimmed here).

```json
{
  "_mode": "search",
  "search_parameters": { "mode": "search", "q": "machine learning", "num": 5, "max_pages": 1 },
  "position": 1,
  "result_id": "EQ8shYj8Ai8J",
  "paper_title": "Machine learning",
  "link": "https://books.google.com/books?id=ctM-EAAAQBAJ",
  "publication_info": {
    "summary": "ZH Zhou - 2021 - books.google.com",
    "authors": [
      { "name": "ZH Zhou", "author_id": "rSVIHasAAAAJ", "link": "https://scholar.google.com/citations?user=rSVIHasAAAAJ" }
    ]
  },
  "inline_links": {
    "cited_by_total": 3793,
    "versions_total": 7,
    "cited_by_link": "https://scholar.google.com/scholar?cites=...",
    "versions_link": "https://scholar.google.com/scholar?cluster=..."
  }
}
```

Each paper row carries the `paper_title`, a `snippet`, structured `publication_info` (summary plus authors with their `author_id`), `resources` (PDF links when available), and `inline_links` with cited-by and versions counts and links. The `author_id` values chain into the author modes.

---

## Use as an MCP tool

You can load the Google Scholar API as an MCP tool so assistants call it for you. The MCP server URL preloads just this one Actor:

```
https://mcp.apify.com/?tools=actors,docs,johnvc/google-scholar-api
```

Authenticate with OAuth in the browser when offered, or with your Apify API token (the same `APIFY_API_TOKEN` used by the Python example). Get a token at https://console.apify.com/settings/integrations and a free Apify account at https://apify.com?fpr=9n7kx3 .

## Install in Claude Cowork Desktop

![Install in Claude Cowork Desktop](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_desktop.png)

Cowork is the desktop app's automation mode. To give it the Google Scholar API as a tool, add the Apify MCP server as a connector.

1. Open the Claude desktop app and go to **Settings → Connectors** (or **Settings → Developer → Edit Config** to edit `claude_desktop_config.json` directly).
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the Apify MCP server, preloaded with only this Actor:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=actors,docs,johnvc/google-scholar-api"
      ]
    }
  }
}
```

3. Restart the app. When Cowork first calls the tool, complete the OAuth prompt in your browser, or add your Apify API token in the connector settings to skip OAuth.
4. In a Cowork chat, confirm the tool is available and ask it to run the Google Scholar API.

Download the desktop app and start a free trial: https://claude.ai/referral/uIlpa7nPLg
More help: https://docs.apify.com/platform/integrations/claude-desktop

## Install in Claude Code

![Install in Claude Code](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_code.png)

Claude Code is the command-line tool. Add the Actor's MCP server with one command:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/google-scholar-api"
```

To use a token instead of browser OAuth:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/google-scholar-api" \
  --header "Authorization: Bearer YOUR_APIFY_TOKEN"
```

Then verify with `claude mcp list`, or run `/mcp` inside a session. Ask Claude Code to call the Google Scholar API.

Try Claude Code free: https://claude.ai/referral/uIlpa7nPLg
Claude Code MCP docs: https://code.claude.com/docs/en/mcp

## Install in Claude (website)

![Install in Claude (website)](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_ai.png)

On claude.ai you add Apify as a connector, then enable just this Actor's tool.

1. Go to **Settings → Connectors → Browse connectors** and search for **Apify MCP server**. Install it (enable or update if prompted).
2. When connecting, authenticate with your Apify API token, and enable the tool `johnvc/google-scholar-api`.
3. In any chat, open **+ → Connectors** and turn on **Apify**.
4. Alternatively, choose **Add custom connector** and paste the full MCP URL `https://mcp.apify.com/?tools=actors,docs,johnvc/google-scholar-api`, using OAuth when prompted.
5. Ask Claude to run the Google Scholar API.

Open Claude on the web: https://claude.ai

## Install in Cursor

![Install in Cursor](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_cursor.png)

Cursor reads MCP servers from a project file at `.cursor/mcp.json`.

1. In your project, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/google-scholar-api"
    }
  }
}
```

2. If you prefer token auth over browser OAuth, add a header:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/google-scholar-api",
      "headers": { "Authorization": "Bearer YOUR_APIFY_TOKEN" }
    }
  }
}
```

3. Open **Cursor → Settings → MCP** and confirm the **apify** server is connected (green dot).
4. In Composer or Chat, ask Cursor to call the Google Scholar API.

New to Cursor? Get it here: https://cursor.com/referral?code=XQP4VBLI3NNX

## Install in ChatGPT

![Install in ChatGPT](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_ChatGPT.png)

ChatGPT connects to the Apify MCP server through Developer mode (available on ChatGPT Pro, Plus, Business, Enterprise, and Education plans).

1. Click your profile icon, then go to **Settings > Apps**. If you do not see a **Create app** button, open **Advanced settings** and enable **Developer mode**.
2. Click **Create app** and fill out the form:
   - **Name:** Apify
   - **MCP Server URL:** `https://mcp.apify.com/?tools=actors,docs,johnvc/google-scholar-api`
   - **Authentication:** OAuth
3. Click **Create** and authorize the connection with Apify.
4. To use the app in a conversation, click **+** in the chat, choose **Developer mode**, and select **Apify**.

More help: https://docs.apify.com/platform/integrations/mcp

---

[**Made with care**](https://apify.com/johnvc?fpr=9n7kx3)

*Use the Google Scholar API to power literature reviews, citation analysis, and research dashboards with reliable, structured results.*

## Featured Tasks

Ready-to-run examples on the Apify Store.

- [Export Google Scholar Results to CSV](https://apify.com/johnvc/google-scholar-api/examples/export-google-scholar-results-to-csv?fpr=9n7kx3)

Last Updated: 2026.06.21
