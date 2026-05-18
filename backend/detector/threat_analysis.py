import random
import time


threat_memory = {}

loiter_start_times = {}

last_seen = {}


def calculate_threat_score(track_id):

    current_time = time.time()

    last_seen[track_id] = current_time

    if track_id not in loiter_start_times:

        loiter_start_times[track_id] = current_time

    loiter_duration = (
        current_time -
        loiter_start_times[track_id]
    )

    if track_id not in threat_memory:

        base_score = random.randint(15, 30)

        threat_memory[track_id] = base_score

    current_score = threat_memory[track_id]

    change = random.randint(-1, 2)

    new_score = current_score + change

    if loiter_duration > 5:

        new_score += 4

    if loiter_duration > 10:

        new_score += 8

    if loiter_duration > 15:

        new_score += 12

    new_score = max(0, min(100, new_score))

    threat_memory[track_id] = new_score

    if loiter_duration > 15:

        activity = "SUSPICIOUS"

    elif loiter_duration > 8:

        activity = "LOITERING"

    else:

        activity = "NORMAL"

    if new_score >= 75:

        level = "HIGH"

        color = (0, 0, 255)

    elif new_score >= 45:

        level = "MEDIUM"

        color = (0, 255, 255)

    else:

        level = "LOW"

        color = (0, 255, 0)

    return int(new_score), level, color, activity


def cleanup_old_tracks():

    current_time = time.time()

    remove_ids = []

    for track_id, seen_time in last_seen.items():

        if current_time - seen_time > 3:

            remove_ids.append(track_id)

    for track_id in remove_ids:

        last_seen.pop(track_id, None)

        threat_memory.pop(track_id, None)

        loiter_start_times.pop(track_id, None)