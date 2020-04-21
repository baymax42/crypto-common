from typing import Optional, List, Any, Tuple, overload

from .types import Language, NGramType, NGramCountMap, NGramFrequencyMap


def get_n_gram_frequency(n_gram_type: NGramType, text: str):
    return n_gram_count_from_text(n_gram_type.value, text)


def get_n_gram_frequency(n_gram_type: NGramType, language: Language = Language.ENGLISH, limit: int = 30):
    n_gram_loader = NGramFileLoader(language=language, n=n_gram_type)
    counts = n_gram_loader.get_first_n(limit)
    return n_gram_loader.to_frequencies(counts)


def n_gram_count_to_frequency(counts: NGramCountMap) -> NGramFrequencyMap:
    all_count = sum(counts.values())
    return NGramFrequencyMap({key: count / all_count for key, count in counts})


def n_gram_count_from_text(n: int, base_text: str) -> NGramCountMap:
    text = ''.join(base_text.upper().split())
    n_gram_counts = dict()

    for frame_end in range(n, len(text) - n):
        frame_start = frame_end - n
        extracted_n_gram = text[frame_start:frame_end]
        if extracted_n_gram in n_gram_counts:
            n_gram_counts[extracted_n_gram] += 1
        else:
            n_gram_counts[extracted_n_gram] = 1

    return NGramCountMap({n_gram: count for n_gram, count in sorted(n_gram_counts.items(),
                                                                    key=lambda item: item[1],
                                                                    reverse=True)})


class NGramFileLoader:
    _gram_type_name_list = ['monograms', 'bigrams', 'trigrams', 'quadgrams']

    def __init__(self, **kwargs) -> None:
        """
        n-gram loader which returns count for specified n-grams for given language.

        :key language: Language - language to use when loading file with specified ngram
        :key n: NGramType - number which specify which ngram to choose (e.g 2 = bigram)

        Defaults to ``Language.ENGLISH`` and ``NGramType.MONOGRAM``.

        Examples::

            ngram = NGram(language=Language.ENGLISH, n=NGramType.MONOGRAM)

        """
        super().__init__()
        self._language = kwargs.get('language', Language.ENGLISH)
        self._n = kwargs.get('n', NGramType.MONOGRAM)
        _validate(self._language, self._n)

        self._all_count: Optional[int] = None

    @property
    def _filename(self) -> str:
        return './{}/{}'.format(self._language.value, self._gram_type_name_list[self._n.value - 1])

    @property
    def _counts_filename(self) -> str:
        return './{}/{}_counts'.format(self._language.value, self._gram_type_name_list[self._n.value - 1])

    def _load_all_count(self):
        with open(self._counts_filename, 'r') as count_file:
            count = count_file.readline().strip()
        self._all_count = count

    def get_first_n(self, limit: int) -> NGramCountMap:
        with open(self._filename, 'r') as n_gram_file:
            records = _get_n_from_file(n_gram_file, limit)
        return records

    def limit(self, skip: int, limit: int) -> NGramCountMap:
        with open(self._filename, 'r') as n_gram_file:
            [next(n_gram_file) for _ in range(skip)]
            records = _get_n_from_file(n_gram_file, limit)
        return records

    def to_frequencies(self, ngram_count: NGramCountMap) -> NGramFrequencyMap:
        if self._all_count is None:
            self._load_all_count()
        return NGramFrequencyMap({key: count / self._all_count for key, count in ngram_count})


def _format_record(record: str) -> Tuple[str, int]:
    key, count = record.strip().split(' ')
    return key, int(count)


def _validate(language: Any, n: Any):
    if not isinstance(language, Language):
        raise Exception('Unsupported language: {}'.format(language))
    if not isinstance(n, NGramType):
        raise Exception('Unsupported n-gram type: {}'.format(n))


def _convert_file_content(file_content: List[str]) -> NGramCountMap:
    record_tuples = map(_format_record, file_content)
    records = {key: count for key, count in record_tuples}
    return NGramCountMap(records)


def _get_n_from_file(file, limit) -> NGramCountMap:
    file_content = []
    for _ in range(limit):
        try:
            file_content.append(next(file))
        except StopIteration:
            pass
    return _convert_file_content(file_content)
