from datetime import datetime, timezone

def convert_unix_timestamp_to_date(unix_timestamp: int) -> datetime:
    return datetime.fromtimestamp(unix_timestamp, timezone.utc)
