from pathlib import Path
import pandas as pd
from pandas.testing import assert_frame_equal
import nbformat

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "trees.csv"
NOTEBOOK_PATH = ROOT / "notebooks" / "01_forest_analysis.ipynb"
RESULT_PATH = ROOT / "results" / "species_summary.csv"


def test_source_data_exists():
    assert DATA_PATH.exists(), "Файл data/trees.csv не найден."


def test_source_data_has_expected_columns():
    df = pd.read_csv(DATA_PATH)
    expected_columns = ["plot_id", "species", "diameter_cm", "height_m", "age_years", "status"]
    assert list(df.columns) == expected_columns, "Структура исходных данных была изменена."


def _get_cell_sources():
    nb = nbformat.read(NOTEBOOK_PATH, as_version=4)
    return [cell.get("source", "") for cell in nb.cells]


def test_notebook_exists():
    assert NOTEBOOK_PATH.exists(), "Ноутбук notebooks/01_forest_analysis.ipynb не найден."


def test_source_code_added():
    sources = _get_cell_sources()
    cell_4 = list(filter(lambda s: "Шаг 4." in s, sources))
    assert len(cell_4) == 1, "Найдена более одной ячейки с 'Шаг 4.'. Убедитесь, что код добавлен в правильную ячейку."
    cell_4_index = sources.index(cell_4[0])
    assert cell_4_index < len(sources) - 1, "Код для 'Шаг 4.' должен быть добавлен до ячейки 'Шаг 5.'."
    assert not "Шаг 5." in sources[cell_4_index + 1], "Код для 'Шаг 4.' должен быть добавлен в ячейку перед 'Шаг 5.'."

def test_markdown_conclusion_filled():
    sources = _get_cell_sources()
    cell_5 = list(filter(lambda s: "Шаг 5." in s, sources))
    assert len(cell_5) == 1, "Найдена более одной ячейки с 'Шаг 5.'. Убедитесь, что код добавлен в правильную ячейку."
    cell_5_index = sources.index(cell_5[0])
    assert cell_5_index < len(sources) - 1, "Текст для 'Шаг 5.' должен быть добавлен до ячейки 'Шаг 6.'."
    assert not "Шаг 6." in sources[cell_5_index + 1], "Текст для 'Шаг 5.' должен быть добавлен в ячейку перед 'Шаг 6.'."


def test_results_file_exists():
    assert RESULT_PATH.exists(), "Файл results/species_summary.csv не найден."


def test_results_content():
    test_results_file_exists()

    result = pd.read_csv(RESULT_PATH)

    expected = pd.DataFrame(
        [
            {
                "species": "birch",
                "tree_count": 3,
                "mean_diameter_cm": 20.00,
                "mean_height_m": 16.00,
                "mean_age_years": 24.00,
            },
            {
                "species": "pine",
                "tree_count": 4,
                "mean_diameter_cm": 29.75,
                "mean_height_m": 19.75,
                "mean_age_years": 44.00,
            },
            {
                "species": "spruce",
                "tree_count": 3,
                "mean_diameter_cm": 29.00,
                "mean_height_m": 22.67,
                "mean_age_years": 42.00,
            },
        ]
    )

    assert list(result.columns) == list(expected.columns), (
        "Колонки в results/species_summary.csv не совпадают с ожидаемыми."
    )

    result = result.sort_values("species").reset_index(drop=True)
    expected = expected.sort_values("species").reset_index(drop=True)

    for column in ["mean_diameter_cm", "mean_height_m", "mean_age_years"]:
        result[column] = result[column].round(2)

    assert_frame_equal(result, expected, check_dtype=False)
