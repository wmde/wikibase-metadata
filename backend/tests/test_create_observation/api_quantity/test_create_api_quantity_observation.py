import re

DATA_DIRECTORY = "tests/test_create_observation/api_quantity/data"
ALL_PAGES_API_URL = re.compile(
    r"^https://example\.com/w/api\.php\?action=query&list=allpages&apnamespace=(\d+)&aplimit=max&format=json(|&apcontinue=Q\d+)$"
)
