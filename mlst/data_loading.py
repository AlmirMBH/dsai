from ingest import load_data

_bookings, _events, _weather, _web_analytics = None, None, None, None

def get_data():
    global _bookings, _events, _weather, _web_analytics
    if _bookings is None:
        _bookings, _events, _weather, _web_analytics = load_data()
    return _bookings, _events, _weather, _web_analytics

