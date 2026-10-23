from importlib import import_module
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_expected_foundation_files_exist():
    expected = [
        "app.py",
        "ui/components.py",
        "ui/demo_service.py",
        "ui/styles.py",
        "common/schemas.py",
        "ai/image_processing.py",
        "ai/config.py",
        "ai/errors.py",
        "ai/extraction_schema.py",
        "ai/vision_provider.py",
        "ai/medicine_extractor.py",
        "verification/database.py",
        "verification/data_loader.py",
        "verification/alert_matcher.py",
        "docs/architecture.md",
        "docs/data_flow.md",
        "docs/database_design.md",
        "docs/api_contracts.md",
        "docs/collaboration_workflow.md",
        "docs/implementation_roadmap.md",
    ]
    assert all((ROOT / item).is_file() for item in expected)


def test_packages_import_without_circular_dependencies():
    for module in (
        "common.schemas",
        "ai.image_processing",
        "ai.vision_provider",
        "ai.medicine_extractor",
        "verification.database",
        "verification.data_loader",
        "verification.alert_matcher",
    ):
        assert import_module(module) is not None


def test_test_configuration_is_present():
    assert (ROOT / "requirements.txt").is_file()
    assert (ROOT / ".gitignore").is_file()
