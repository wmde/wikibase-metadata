import json, requests

from src.user_data.user_data_url import usersURL


def fetchUserData(api_url: str) -> list[dict]:
    data = []

    shouldQuery = True
    next = None

    while shouldQuery:
        users_url = usersURL(api_url, continue_from=next)
        print(f"Querying {users_url}")
        result = requests.get(users_url, timeout=10)
        query_data = json.loads(result.content)
        data.extend(query_data["query"]["allusers"])
        print(f"\tData Length: {len(data)}")
        if "continue" in query_data:
            next = query_data["continue"]["aufrom"]
        else:
            shouldQuery = False

    return data
