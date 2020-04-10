from unittest.mock import patch, mock_open

import pytest

from frequency import NGram, Language, NGramType

LANGUAGE = Language.ENGLISH
TYPE_BIGRAM = NGramType.BIGRAM
FAILING_LANGUAGE = "py"
FAILING_N_GRAM_TYPE = -5


class TestNGram:
    def test_init__language_validation(self):
        with pytest.raises(Exception) as exception:
            NGram(language=FAILING_LANGUAGE)
        assert "Unsupported language" in str(exception.value)

    def test_init__n_gram_type_validation(self):
        with pytest.raises(Exception) as exception:
            NGram(n=FAILING_N_GRAM_TYPE)
        assert "Unsupported n-gram type" in str(exception.value)

    def test_filename(self):
        ngram_loader = NGram(language=LANGUAGE, n=TYPE_BIGRAM)
        assert './en/bigrams' == ngram_loader._filename

        ngram_loader = NGram(language=LANGUAGE, n=NGramType.QUADRAGRAM)
        assert './en/quadragrams' == ngram_loader._filename

    def test_filename__with_default_values(self):
        ngram_loader = NGram()
        assert './en/monograms' == ngram_loader._filename

    @patch("builtins.open", new_callable=mock_open, read_data="AB 12\nDF 1\n")
    def test_get_first_n(self, _mock_file):
        ngram_loader = NGram(language=LANGUAGE, n=TYPE_BIGRAM)

        records = ngram_loader.get_first_n(1)
        assert {'AB': 12} == records

        records = ngram_loader.get_first_n(2)
        assert {'AB': 12, 'DF': 1} == records

    @patch("builtins.open", new_callable=mock_open, read_data="AB 12\nDF 1\n")
    def test_get_first_n__limit_larger_than_file(self, _mock_file):
        ngram_loader = NGram(language=LANGUAGE, n=TYPE_BIGRAM)

        records = ngram_loader.get_first_n(5)
        assert {'AB': 12, 'DF': 1} == records

    @patch("builtins.open", new_callable=mock_open, read_data="AB 12\nDF 1\n")
    def test_get_first_n__negative_limit(self, _mock_file):
        ngram_loader = NGram(language=LANGUAGE, n=TYPE_BIGRAM)

        records = ngram_loader.get_first_n(-1)
        assert {} == records

    @patch("builtins.open", new_callable=mock_open, read_data="AB 12\nDF 1\n")
    def test_get_first_n__zero_limit(self, _mock_file):
        ngram_loader = NGram(language=LANGUAGE, n=TYPE_BIGRAM)

        records = ngram_loader.get_first_n(0)
        assert {} == records

    # TODO: test limit function
