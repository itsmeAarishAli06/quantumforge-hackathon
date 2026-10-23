# 💊 Dawa-Muhafiz
### AI-Powered Medicine Packaging Review Prototype

<p align="center">
  <strong>Making medicine packaging review more accessible through AI-assisted text extraction.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Project-Academic%20Prototype-0F766E?style=for-the-badge" alt="Academic Prototype" />
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/AI-Google%20Gemini-4285F4?style=for-the-badge&logo=googlegemini&logoColor=white" alt="Google Gemini" />
</p>

<p align="center">
  <em>An academic prototype exploring how AI-assisted extraction can support the review of visible medicine packaging details against official medicine alert information.</em>
</p>

---

> [!IMPORTANT]
> **Prototype status:** The current implementation provides a Streamlit interface, editable medicine details, optional Gemini-powered image extraction, and a synthetic demonstration mode. **Real DRAP alert retrieval and medicine-alert matching are not implemented.** This project does not authenticate medicines, certify their safety, or provide medical advice.

## 📑 Table of Contents

- [Overview](#-overview)
- [Current Features](#-current-features)
- [How It Works](#-how-it-works)
- [Technology Stack](#-technology-stack)
- [Getting Started](#-getting-started)
- [Gemini API Configuration](#-gemini-api-configuration)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Current Limitations](#-current-limitations)
- [Safety and Privacy](#-safety-and-privacy)
- [Roadmap](#-roadmap)
- [Official References](#-official-references)

## 🔍 Overview

**Dawa-Muhafiz** is an academic project focused on AI-assisted medicine packaging review in Pakistan.

Medicine packaging contains important information such as product names, manufacturers, batch numbers, manufacturing dates, and expiry dates. Reading this information can be challenging when packaging text is small, blurred, curved, or difficult to interpret.

Dawa-Muhafiz explores a workflow in which users can upload a packaging image, extract visible details with an AI vision model, review and correct the extracted fields, and explore a clearly labelled synthetic demonstration of the intended alert-review interface.

The long-term direction is to explore integration with reviewed, authoritative medicine-alert data. That integration is future work, not a capability of the current phase.

## ✨ Current Features

| Feature | Description |
|---|---|
| 🖼️ Image Upload | Upload JPG, JPEG, or PNG medicine packaging images. |
| 🔎 Input Validation | Enforces a default 10 MB upload limit and validates the decoded image format. |
| 🤖 AI-Assisted Extraction | Uses Google Gemini vision when an API key is configured and the user explicitly requests extraction. |
| ✏️ Editable Fields | Review and correct extracted medicine details before proceeding. |
| 🧪 Synthetic Demo Mode | Explore sample details and four synthetic interface scenarios without requiring a Gemini API key. |
| 🛡️ Safety Messaging | Displays limitations and guidance to review extracted information carefully. |
| 🎨 User Interface | Provides a navy-and-teal theme, grouped fields, clear workflow steps, and labelled result states. |
| 🧩 Structured Data | Uses shared Pydantic schemas to validate extracted information. |
| 🧪 Automated Tests | Includes tests for project setup and data schemas. |

## 🔄 How It Works

The current application separates AI-assisted extraction from the synthetic demonstration workflow.

```text
                 Dawa-Muhafiz
                       |
             +---------+---------+
             |                   |
        Upload Image        Synthetic Demo
             |                   |
       Validate File       Load Fixed Fixture
             |
     User Requests Extraction
             |
       Gemini API Configured?
             |
        Yes  |  No
         |       |
    Send Image   Explain Setup
    to Gemini    Requirements
         |
    Extract Visible Details
         |
    Validate Structured Output
         |
    Review and Edit Fields
         |
    Review Safety Notice
```

**Important distinction:** The synthetic demonstration uses predefined sample data unrelated to the uploaded image. Neither workflow performs real DRAP alert retrieval or matching in the current implementation.

## 🛠️ Technology Stack

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Google_Gemini-4285F4?style=flat-square&logo=googlegemini&logoColor=white" alt="Google Gemini" />
  <img src="https://img.shields.io/badge/Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white" alt="Pydantic" />
  <img src="https://img.shields.io/badge/Pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white" alt="Pytest" />
  <img src="https://img.shields.io/badge/Git%20%26%20GitHub-181717?style=flat-square&logo=github&logoColor=white" alt="Git and GitHub" />
</p>

- **Language:** Python 3.11 or newer
- **Frontend:** Streamlit
- **AI integration:** Google Gen AI Python SDK (`google-genai`)
- **Data validation:** Pydantic
- **Testing:** Pytest
- **Configuration:** Environment variables via a local `.env` file
- **Version control:** Git and GitHub

## 🚀 Getting Started

### Prerequisites

Before running the project, install:

- Python 3.11 or newer
- Git
- A code editor such as Visual Studio Code

### 1. Clone the Repository

```powershell
git clone https://github.com/itsmeAarishAli06/quantumforge-hackathon.git
cd quantumforge-hackathon
```

### 2. Create a Virtual Environment

```powershell
py -3.11 -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a local environment file from the example:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and add your own Gemini API key if you want to use live image extraction.

```dotenv
GEMINI_API_KEY=your_gemini_api_key_here
```

Optionally, configure the model and timeout using `GEMINI_MODEL` and `GEMINI_TIMEOUT_MS`, as supported by the application.

**Never commit your real API key to GitHub.** The `.env` file should remain excluded by `.gitignore`.

### 5. Run the Application

```powershell
streamlit run app.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser to use the application.

Without a Gemini API key, live extraction remains disabled, but the synthetic demonstration mode is available.

## 🤖 Gemini API Configuration

Dawa-Muhafiz uses Google's maintained `google-genai` Python SDK to request structured output from a configurable Gemini vision model.

To enable live extraction:

1. Visit [Google AI Studio](https://aistudio.google.com/).
2. Obtain an API key using Google's available account and usage requirements.
3. Store the key in your local `.env` file.
4. Restart the Streamlit application.
5. Upload an appropriate packaging image and explicitly select **Extract with Gemini**.
6. Review every extracted field against the original package.

The application transmits uploaded image bytes to Google Gemini only after the user explicitly requests live extraction.

AI extraction is fallible. Small text, poor image quality, curved surfaces, and obscured details can lead to missing or incorrect values. Unknown or ambiguous information must be reviewed rather than assumed correct.

## 🧪 Testing

Run the automated test suite from the project root with the virtual environment activated:

```powershell
python -m pytest -q
```

The current tests cover project setup and shared schema validation.

Tests do not require a Gemini API key or make external network calls. Passing these tests does not establish the accuracy of medicine identification or the reliability of any real-world safety assessment.

## 📁 Project Structure

```text
quantumforge-hackathon/
│
├── ai/
│   ├── __init__.py
│   ├── image_processing.py
│   ├── medicine_extractor.py
│   └── vision_provider.py
│
├── common/
│   ├── __init__.py
│   └── schemas.py
│
├── data/
│   ├── .gitkeep
│   └── README.md
│
├── docs/
│   ├── architecture.md
│   ├── api_contracts.md
│   ├── collaboration_workflow.md
│   ├── data_flow.md
│   ├── database_design.md
│   └── implementation_roadmap.md
│
├── tests/
│   ├── __init__.py
│   ├── test_project_setup.py
│   └── test_schemas.py
│
├── ui/
│   ├── components.py
│   └── demo_service.py
│
├── verification/
│   ├── __init__.py
│   ├── alert_matcher.py
│   ├── data_loader.py
│   └── database.py
│
├── .env.example
├── .gitignore
├── app.py
├── requirements.txt
└── README.md
```

### Key Modules

- **`app.py`** — Streamlit interface, upload validation, session state, editable fields, and demonstration workflow.
- **`ai/`** — Image processing, Gemini integration, and structured extraction.
- **`common/schemas.py`** — Shared Pydantic data contracts.
- **`ui/components.py`** — Reusable interface components, result panels, and safety notices.
- **`ui/demo_service.py`** — Fixed synthetic sample details and demonstration scenarios.
- **`verification/`** — Foundations for future reviewed-data imports and deterministic alert matching; real verification is not implemented.
- **`docs/`** — Architecture, API contracts, data flow, database design, collaboration workflow, and implementation roadmap.
- **`tests/`** — Automated project setup and schema tests.

## ⚠️ Current Limitations

The current phase is a prototype, not a production medicine-verification system.

- No live DRAP connection or official alert database is queried.
- No real alert matching is performed.
- Synthetic demonstration results are not generated from the uploaded image.
- AI-extracted details may be incomplete or incorrect.
- A displayed `NO_MATCH_FOUND` status does not mean that a medicine is genuine, approved, or safe.
- The prototype does not replace pharmacists, healthcare professionals, or official regulatory information.

## 🔐 Safety and Privacy

Dawa-Muhafiz is designed to encourage careful review rather than automatic trust in AI output.

- Uploaded images are processed in memory and are not saved to disk by the current upload workflow.
- Image bytes are transmitted to Google only when live Gemini extraction is explicitly requested.
- Avoid uploading images containing personal or otherwise sensitive information.
- Review extracted details against the original packaging.
- Do not treat an AI result or synthetic demonstration as proof of authenticity or safety.
- Never commit API keys, personal information, uploaded images, or local databases to version control.

For medicine-related concerns, consult a qualified pharmacist and check relevant official information from the [Drug Regulatory Authority of Pakistan (DRAP)](https://www.dra.gov.pk/).

## 🗺️ Roadmap

The following are potential future improvements, not claims about existing functionality.

- [ ] Improve extraction accuracy and field-level review.
- [ ] Add stronger validation and error-handling tests.
- [ ] Design a reliable ingestion process for reviewed, authoritative medicine-alert data.
- [ ] Implement deterministic matching against an approved alert dataset.
- [ ] Display traceable evidence and source references for any future matches.
- [ ] Add integration tests using controlled fixtures.
- [ ] Evaluate security, privacy, accessibility, and deployment requirements before production use.

Any future alert-matching functionality should clearly distinguish confirmed matches, uncertain results, and cases where no reliable conclusion can be reached.

## 📚 Official References

- [Google Gen AI Python SDK](https://github.com/googleapis/python-genai)
- [Gemini Image Understanding](https://ai.google.dev/gemini-api/docs/image-understanding)
- [Gemini Structured Output](https://ai.google.dev/gemini-api/docs/structured-output)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [DRAP — Official Website](https://www.dra.gov.pk/)

---

<p align="center">
  <strong>Dawa-Muhafiz</strong>
  <br />
  <em>An academic exploration of AI-assisted medicine packaging review.</em>
  <br /><br />
  Built for learning, experimentation, and responsible AI development.
</p>
