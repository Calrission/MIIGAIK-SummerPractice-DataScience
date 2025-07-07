import os
import pandas as pd
from requests import RequestException

import html_datasource
import parser
import saver
import cache
from homework_1 import utils
from homework_1.constants import SAVE_DIR, OUTPUT_DIR
from homework_1.csv_builder import DataFrameCsvBuilder


def test_get_index_html():
    print("test_get_index_html")
    result = html_datasource.get_index_html()
    assert result is not None
    print("test_get_index_html - good")


def test_get_html():
    print("test_get_html")
    url = "https://ratcatcher.ru/media/summer_prac/parcing/21/0ab20eccc35b.html"
    result = html_datasource.get_html(url)
    assert result is not None
    try:
        html_datasource.get_html("https://ratcatcher.ru/test_bad_url")
        print("test_get_html - bad url")
    except RequestException as _:
        print("test_get_html - good")


def test_parse_index_to_urls():
    print("test_parse_index_to_urls")
    index_html = utils.mock("mock_index.html")
    result = parser.parse_index_to_urls(index_html)
    assert isinstance(result, list)
    assert len(result) > 0
    print(f"len index html = {len(result)}")
    print("test_parse_index_to_urls - good")


def test_save():
    print("test_save_url")
    name = "ratcatcher.html"
    html = "test"
    cache.save(name, html)
    path = os.path.join(SAVE_DIR, name)
    assert os.path.exists(path)
    with open(path, "r") as f:
        content = f.read()
        assert content == html
    os.remove(path)
    print("test_save_url - good")


def test_check_is_saved():
    print("test_check_is_saved")
    name = "ratcatcher.html"
    cache.save(name, "test")
    assert cache.check_is_saved(name)
    os.remove(os.path.join(SAVE_DIR, name))
    print("test_check_is_saved - good")


def test_read():
    print("test_read")
    name = "ratcatcher.html"
    origin_content = "test"
    cache.save(name, origin_content)
    content = cache.read(name)
    assert content == origin_content
    os.remove(os.path.join(SAVE_DIR, name))
    print("test_read - good")


def test_url2name():
    print("test_url2name")
    url = "https://ratcatcher.ru/media/summer_prac/parcing/21/0ab20eccc35b.html"
    name = utils.url2name(url)
    assert name == "0ab20eccc35b.html"
    print("test_url2name - good")


def test_parse_page():
    print("test_parse_page")
    html_page = utils.mock("mock_page.html")
    headers, rows = parser.parse_page(html_page)
    assert isinstance(rows, list)
    assert isinstance(rows[0], list)
    assert isinstance(headers, list)
    assert len(rows) == 1
    mock_headers_table = [
        "checking_status", "duration", "credit_history", "purpose", "credit_amount", "savings_status", "employment",
        "installment_commitment", "personal_status", "other_parties", "residence_since", "property_magnitude", "age",
        "other_payment_plans", "housing", "existing_credits", "job", "num_dependents", "own_telephone",
        "foreign_worker",
        "class"
    ]
    mock_content_table = [
        "<0", "6.0", "critical/other existing credit", "radio/tv", "1169.0", "no known savings", ">=7", "4.0",
        "male single", "none", "4.0", "real estate", "67.0", "none", "own", "2.0", "skilled", "1.0", "yes", "yes",
        "good"
    ]
    assert headers == mock_headers_table
    assert rows == [mock_content_table]
    print("test_parse_page - good")


def test_build_with_row_only():
    print("test_build_with_row_only")
    builder = DataFrameCsvBuilder()
    row = ["Alice", "30"]
    builder.add_row(row)
    df = builder.build()
    expected = pd.DataFrame([row])
    assert df.equals(expected)
    print("test_build_with_row_only - good")


def test_build_with_header_only():
    print("test_build_with_header_only")
    builder = DataFrameCsvBuilder()
    header = ["Name", "Age"]
    builder.add_header(header)
    df = builder.build()
    expected = pd.DataFrame(columns=header)
    assert df.equals(expected)
    print("test_build_with_header_only - good")


def test_build_with_header_and_rows():
    print("test_build_with_header_and_rows")
    builder = DataFrameCsvBuilder()
    header = ["Name", "Age"]
    rows = [
        ["Alice", "30"],
        ["Bob", "25"]
    ]
    builder.add_header(header)
    for row in rows:
        builder.add_row(row)
    df = builder.build()
    expected = pd.DataFrame(rows, columns=header)
    assert df.equals(expected)
    print("test_build_with_header_and_rows - good")


def test_save_builder():
    print("test_save_builder")
    df = DataFrameCsvBuilder().add_header(["Name", "Age"]).add_row(["Alice", "12"]).build()
    name = "test.csv"
    saver.save(name, df)
    path = os.path.join(OUTPUT_DIR, name)
    assert os.path.exists(path)
    text = utils.read(path)
    assert not text.endswith("\n")
    os.remove(path)
    print("test_save_builder - good")


if __name__ == '__main__':
    saver.prepare()
    cache.prepare()
    test_get_index_html()
    test_get_html()
    test_parse_index_to_urls()
    test_parse_page()
    test_save()
    test_check_is_saved()
    test_build_with_row_only()
    test_build_with_header_only()
    test_build_with_header_and_rows()
    test_save_builder()
    test_url2name()
    test_read()
