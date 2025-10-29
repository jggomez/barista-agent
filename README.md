# Barista Agent ☕

A sophisticated AI-powered virtual barista system built with Google ADK (Agent Development Kit), Gemini AI, and Firebase Firestore. This multi-component system provides intelligent coffee menu assistance through natural language interactions, vector-based semantic search, and image generation capabilities.

## 🧑🏽‍💻 Design Overview

###  Context Diagram
<img width="761" height="691" alt="Barista Agent System drawio" src="https://github.com/user-attachments/assets/41c8fb3a-ae36-439b-a3be-33d34a4c0f11" />

### Container Diagram
<img width="1136" height="1201" alt="Barista Agent System - Container Diagram drawio" src="https://github.com/user-attachments/assets/14c166c1-6b9c-49ad-9a12-613a52ad45f5" />

### Component Diagram
<img width="1351" height="1021" alt="Barista Agent System - Component Diagram drawio" src="https://github.com/user-attachments/assets/6f526e65-66a1-4d82-bf04-ab99468dae49" />


## 🏗️ Architecture Overview

This project consists of three main components:

1. **Pipeline Data Ingestion Menu** - Processes and embeds menu data
2. **Barista Agent System** - Core AI agent with specialized tools
3. **UI** - Interactive Gradio-based chat interface

## 📁 Project Structure

```
Barista-Agent/
├── pipeline-data-ingestion-menu/  # Menu data processing pipeline
│   ├── src/
│   │   └── ingestion_menu.py      # Embedding creation and Firestore ingestion
│   ├── resources/
│   │   └── menu.md                # Coffee menu source data
│   ├── pyproject.toml             # Dependencies (langchain, google-cloud-firestore)
│   └── .env                       # Environment configuration
│
├── barista-agent-system/          # Main AI agent application
│   ├── agents/
│   │   ├── barista_agent/
│   │   │   ├── agent.py           # Agent configuration and initialization
│   │   │   ├── prompts/
│   │   │   │   ├── prompts.yaml   # Agent instructions and behavior
│   │   │   │   └── load_prompts.py
│   │   │   └── tools/             # Agent capabilities
│   │   │       ├── menu_tools.py          # Vector search for menu items
│   │   │       ├── promotions_tools.py    # Daily promotions logic
│   │   │       ├── image_coffee_tools.py  # Image generation with Imagen
│   │   │       ├── availability_check_tools.py  # Stock verification
│   │   │       └── common_tools.py        # Utility functions
│   │   └── images/                # Generated/stored images
│   ├── main.py                    # FastAPI application entry point
│   ├── start.sh                   # Startup script
│   ├── Dockerfile                 # Container configuration
│   ├── deploy-agent.sh            # Google Cloud Run deployment
│   └── pyproject.toml             # Dependencies (google-adk, firestore)
│
├── UI/                            # User interface
│   ├── src/
│   │   └── ui_main.py             # Gradio chat interface
│   ├── Dockerfile                 # UI container configuration
│   ├── deploy-ui.sh               # UI deployment script
│   └── pyproject.toml             # Dependencies (gradio, requests)
│
├── .gitignore                     # Git exclusions
├── .pre-commit-config.yaml        # Code quality hooks
└── README.md                      # This file
```

## 🧩 Components

### 1. Pipeline Data Ingestion Menu

**Purpose:** Prepares the coffee menu for semantic search by creating vector embeddings.

**Key Features:**
- **Chunking:** Uses LangChain's `MarkdownHeaderTextSplitter` to parse menu items by category (`##` headers)
- **Embedding Generation:** Creates 768-dimensional embeddings using Gemini's `gemini-embedding-001` model
- **Storage:** Saves embeddings to Firestore with vector support for similarity search

**Technologies:**
- LangChain Community & Text Splitters
- Google Cloud Firestore
- Google Generative AI (Gemini)
- Python 3.10+

**Usage:**
```bash
cd pipeline-data-ingestion-menu
poetry install
poetry run python src/ingestion_menu.py
```

**Configuration:**
- Database: `embeddings` (Firestore)
- Collection: `menu`
- Embedding Model: `gemini-embedding-001`
- Output Dimensionality: 768

### 2. Barista Agent System

**Purpose:** The intelligent core that handles customer interactions using specialized tools.

**Key Features:**

#### Agent Configuration (`agent.py`)
- Built with Google ADK's `LlmAgent`
- Uses configurable LLM (default: `gemini-2.5-flash`)
- Instructions loaded from YAML for easy customization

#### Specialized Tools

1. **`menu_tools.py`** - Vector-based menu search
   - Performs semantic similarity search in Firestore
   - Returns top 2 most relevant menu items using cosine distance
   - Queries embeddings collection for natural language understanding

2. **`promotions_tools.py`** - Daily deals management
   - Mock promotion system based on day of week
   - Returns special offers and loyalty bonuses

3. **`image_coffee_tools.py`** - Coffee visualization
   - Generates images using Google Imagen (`imagen-4.0-generate-001`)
   - Uploads to Google Cloud Storage
   - Returns public URLs to generated images

4. **`availability_check_tools.py`** - Stock verification
   - Real-time inventory checks (implementation specific)

5. **`common_tools.py`** - Utility functions
   - Date/time helpers for context-aware responses

#### API Server (`main.py`)
- FastAPI application using ADK's `get_fast_api_app`
- Session management with SQLite
- CORS-enabled for web interface
- Serves both API and web interface

**Technologies:**
- Google Agent Development Kit (ADK)
- Google Generative AI (Gemini)
- Google Cloud Firestore
- Google Cloud Storage
- FastAPI & Uvicorn
- PIL (image processing)
- Python-dotenv

**Deployment:**
```bash
cd barista-agent-system
./deploy-agent.sh  # Deploys to Google Cloud Run
```

**Environment Variables:**
- `LLM_AGENT`: LLM model name (e.g., `gemini-2.5-flash`)
- `PROJECT_ID`: Google Cloud project ID
- `GCS_BUCKET_NAME`: Storage bucket for images
- `MODEL_IMAGEN`: Imagen model version
- `GOOGLE_API_KEY`: API key (stored in Secret Manager)

### 3. UI (User Interface)

**Purpose:** Provides an intuitive chat interface for interacting with the barista agent.

**Key Features:**
- **Gradio-based chat interface** with message history
- **Session management** with unique user/session IDs
- **Streaming responses** for real-time interaction
- **Error handling** with retry capability
- **Session reset** for troubleshooting

**Technologies:**
- Gradio 5.x (Soft theme)
- Python Requests
- Python-dotenv

**How It Works:**
1. Creates unique user and session IDs on initialization
2. Sends messages to the agent's `/run` endpoint
3. Displays responses in a conversational format
4. Supports multiple content parts in responses

**Usage:**
```bash
cd UI
poetry install
poetry run python src/ui_main.py
```

**Deployment:**
```bash
./deploy-ui.sh  # Deploys to Google Cloud Run
```

**Environment Variables:**
- `AGENT_URL_BASE`: URL of the deployed barista agent API

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Poetry package manager
- Google Cloud account with:
  - Firestore database named `embeddings`
  - Cloud Storage bucket
  - API keys for Gemini AI
  - Cloud Run (for deployment)

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Barista-Agent
   ```

2. **Set up Firestore index:**
   ```bash
   gcloud firestore indexes composite create \
   --collection-group=menu \
   --query-scope=COLLECTION \
   --field-config field-path=embedding,vector-config='{"dimension":"768", "flat": "{}"}' \
   --database=embeddings
   ```

3. **Configure environment variables:**
   Create `.env` files in each component directory with appropriate credentials.

4. **Ingest menu data:**
   ```bash
   cd pipeline-data-ingestion-menu
   poetry install
   poetry run python src/ingestion_menu.py
   ```

5. **Run the agent locally:**
   ```bash
   cd barista-agent-system
   poetry install
   poetry run python main.py
   ```

6. **Launch the UI:**
   ```bash
   cd UI
   poetry install
   poetry run python src/ui_main.py
   ```

## 🛠️ Development

### Code Quality
This project uses pre-commit hooks with:
- Ruff (linting & formatting)
- MyPy (type checking)
- Import reordering
- YAML/TOML validation

Install hooks:
```bash
pre-commit install
```

## 🌐 Deployment

Both the agent and UI are containerized and deploy to Google Cloud Run:

1. **Agent Deployment:**
   ```bash
   cd barista-agent-system
   ./deploy-agent.sh
   ```

2. **UI Deployment:**
   ```bash
   cd UI
   ./deploy-ui.sh
   ```

## 📝 Agent Capabilities

The Virtual Barista Agent can:
- ✅ Answer questions about coffee menu items
- ✅ Check product availability in real-time
- ✅ Provide current promotions based on the day
- ✅ Generate visual representations of coffee drinks
- ✅ Guide customers through the purchase process
- ❌ Answer questions outside of coffee-related topics (politely declines)

## 🔧 Configuration

### Agent Behavior (`prompts.yaml`)
The agent's personality and capabilities are defined in the prompts configuration:
- Strict expertise boundary (coffee only)
- Tool usage instructions
- Response formatting guidelines

### Menu Data (`menu.md`)
Menu items are organized by categories:
- Hand-Crafted Drinks
- Classic Brews

Each item includes name, description, and price.

## 📦 Dependencies

### Pipeline
- `langchain-community` - Document loading
- `langchain-text-splitters` - Text chunking
- `google-cloud-firestore` - Vector storage
- `google-genai` - Embeddings

### Agent
- `google-adk` - Agent framework
- `google-cloud-firestore` - Database
- `pillow` - Image processing
- `pyyaml` - Configuration

### UI
- `gradio` - Web interface
- `requests` - HTTP client

## Testing

### Try out!
https://barista-agent-ui-823002731253.us-central1.run.app

### Web UI 1
<img width="1906" height="938" alt="Screenshot 2025-10-28 at 1 51 24 a m" src="https://github.com/user-attachments/assets/53182285-a77e-44b6-8807-89f7614907ce" />

### Web UI 2
<img width="1900" height="937" alt="Screenshot 2025-10-28 at 1 51 34 a m" src="https://github.com/user-attachments/assets/200e53ce-37ea-402f-8293-020b25dbc963" />


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with proper commit messages
4. Run pre-commit hooks
5. Submit a pull request

## 👤 Author

Juan Guillermo Gómez (juan.gomez01@gmail.com)
Linkedin: [@jggomezt](https://www.linkedin.com/in/jggomezt

## 🙏 Acknowledgments

- Google ADK team for the agent framework
- Google Generative AI for Gemini and Imagen models
- LangChain for document processing utilities
