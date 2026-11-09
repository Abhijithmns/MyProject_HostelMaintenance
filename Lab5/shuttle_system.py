"""Campus Shuttle Timetable & Fleet Tracker.

Logs passenger counts per trip, computes average loads,
flags under-used routes, and syncs fleet data to fleet.json.
"""

import json
import random
from datetime import datetime

# Global state
routes = {
    "R1": {"name": "Main Gate - Library", "trips": []},
    "R2": {"name": "Hostel - Sports Complex", "trips": []},
    "R3": {"name": "Admin Block - Metro", "trips": []},
}
MIN_CAPACITY = 10


def add_trip_log(route_id, passenger_count, logs=None):
    """Log a passenger count for a trip on the given route.

    Uses None as the default for logs to avoid the mutable-default-argument
    bug; a fresh list is created on each call when no list is provided.
    Also validates that passenger_count is a non-negative integer.
    """
    if logs is None:
        logs = []
    if not isinstance(passenger_count, int) or passenger_count < 0:
        print(
            f"Warning: invalid passenger count '{passenger_count}' "
            f"for route {route_id} – trip not recorded."
        )
        return logs
    routes[route_id]["trips"].append(passenger_count)
    logs.append(
        f"{datetime.now()}: {route_id} carried {passenger_count}"
    )
    return logs


def remove_route(route_id):
    """Remove a route by ID, ignoring unknown route IDs."""
    routes.pop(route_id, None)


def average_load(route_id):
    """Return the average passenger load for a route.

    Returns None if the route does not exist or has no trips recorded.
    """
    if route_id not in routes:
        return None
    trips = routes[route_id]["trips"]
    if not trips:
        return None
    return sum(trips) / len(trips)


def underused_routes():
    """Return a list of route IDs whose average load is below MIN_CAPACITY."""
    flagged = []
    for route_id in routes:
        avg = average_load(route_id)
        if avg is not None and avg < MIN_CAPACITY:
            flagged.append(route_id)
    return flagged


def assign_driver(route_id):  # pylint: disable=unused-argument
    """Randomly assign a driver to the given route.

    route_id is accepted for API consistency but not used yet;
    future versions may use it for route-specific driver pools.
    """
    drivers = ["Prakash", "Leela", "Imran", "Tom"]
    return random.choice(drivers)  # nosec B311


def sync_fleet_data(file="fleet.json"):
    """Write the current routes dict to a JSON file and reload it."""
    with open(file, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(routes))
    with open(file, encoding="utf-8") as fh:
        loaded = json.loads(fh.read())
    # Merge loaded data back without replacing the global reference
    routes.clear()
    routes.update(loaded)


def main():
    """Run the shuttle system demo."""
    add_trip_log("R1", 32)
    add_trip_log("R1", 28)
    add_trip_log("R2", 4)
    add_trip_log("R2", -6)   # negative count – will be rejected
    add_trip_log("R3", "full")  # non-integer – will be rejected
    print("Driver for R1:", assign_driver("R1"))
    print("Underused:", underused_routes())
    print("R1 average:", average_load("R1"))
    sync_fleet_data()
    remove_route("R3")
    choice = input("Route to look up (Enter for R2): ") or "R2"
    if choice in routes:
        print("Trips on", choice, ":", routes[choice]["trips"])
    else:
        print(f"Route '{choice}' not found.")
    r3_avg = average_load("R3")
    if r3_avg is not None:
        print("R3 average:", r3_avg)
    else:
        print("R3 average: N/A (route removed or no trips)")


main()
