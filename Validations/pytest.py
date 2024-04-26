import pytest
from io import StringIO
import pandas as pd

###Pass Test Cases


def test_valid_article():
    # Example of a valid article
    article = MedicalArticle(title="Valid Title", content="Valid Content" + "a" * 490)
    assert article.title == "Valid Title"
    assert len(article.content) >= 500

def test_strip_whitespace_title():
    # Title with surrounding whitespaces that should be stripped and validated
    article = MedicalArticle(title="  Valid Title  ", content="Valid Content" + "a" * 490)
    assert article.title == "Valid Title"

def test_minimum_length_content():
    # Content is exactly 500 characters long
    article = MedicalArticle(title="Good Title", content="a" * 500)
    assert len(article.content) == 500

def test_file_with_valid_data():
    data = StringIO("""Title,Content\nValid Title,{}""".format("a" * 500))
    df = pd.read_csv(data)
    validated_data, errors = validate_medical_data(data)
    assert len(validated_data) == 1 and len(errors) == 0

def test_multiple_valid_entries():
    data = StringIO("Title,Content\nValid1,{}\nValid2,{}".format("a" * 500, "b" * 500))
    df = pd.read_csv(data)
    validated_data, errors = validate_medical_data(data)
    assert len(validated_data) == 2 and len(errors) == 0

### Fail Test Cases


def test_empty_title():
    # Title is empty, should fail
    with pytest.raises(ValueError) as excinfo:
        MedicalArticle(title="", content="Valid Content" + "a" * 490)
    assert "title must not be empty or just whitespace" in str(excinfo.value)

def test_title_too_short():
    # Title is too short, should fail
    with pytest.raises(ValueError) as excinfo:
        MedicalArticle(title="No", content="Valid Content" + "a" * 490)
    assert "ensure this value has at least 3 characters" in str(excinfo.value)

def test_content_too_short():
    # Content is too short, should fail
    with pytest.raises(ValueError) as excinfo:
        MedicalArticle(title="Valid Title", content="Short")
    assert "ensure this value has at least 500 characters" in str(excinfo.value)

def test_invalid_csv_format():
    # CSV data is malformed or has incorrect headers
    data = StringIO("IncorrectHeader1,IncorrectHeader2\nValue1,Value2")
    df = pd.read_csv(data)
    validated_data, errors = validate_medical_data(data)
    assert len(errors) == 1  # Expecting an error due to missing required fields

def test_missing_content_column():
    # Missing 'Content' column in the data
    data = StringIO("Title\nOnly Title")
    df = pd.read_csv(data)
    validated_data, errors = validate_medical_data(data)
    assert len(errors) == 1  # Errors due to missing 'Content' column
