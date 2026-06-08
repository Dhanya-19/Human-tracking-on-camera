import time
import math

# Memory Registries
threat_memory = {}       # track_id -> float (current score)
loiter_start_times = {}  # track_id -> timestamp
last_seen = {}           # track_id -> timestamp
trajectory_history = {}  # track_id -> list of (x, y) coordinates

# DEFINING OUR RESTRICTED ZONE (ROI)
RESTRICTED_ZONE = [800, 200, 1200, 600] 

def is_inside_roi(bbox, roi):
    """
    Checks if the center point of the person's bounding box falls inside the ROI.
    bbox format: [x1, y1, x2, y2]
    """
    if not bbox or len(bbox) < 4:
        return False
    # Calculate center of the person
    cx = (bbox[0] + bbox[2]) / 2
    cy = (bbox[1] + bbox[3]) / 2
    
    rx_min, ry_min, rx_max, ry_max = roi
    return rx_min <= cx <= rx_max and ry_min <= cy <= ry_max

def calculate_pacing_factor(track_id, cx, cy):
    """
    Calculates if the person is pacing around a small area.
    Returns a multiplier based on chaotic/tightly localized movement.
    """
    if track_id not in trajectory_history:
        trajectory_history[track_id] = []
        
    # Append current position and keep only the last 30 positions
    trajectory_history[track_id].append((cx, cy))
    if len(trajectory_history[track_id]) > 30:
        trajectory_history[track_id].pop(0)
        
    if len(trajectory_history[track_id]) < 10:
        return 1.0 # Not enough history yet
        
    # Calculate the max distance spread of their movement
    x_coords = [p[0] for p in trajectory_history[track_id]]
    y_coords = [p[1] for p in trajectory_history[track_id]]
    
    spread_x = max(x_coords) - min(x_coords)
    spread_y = max(y_coords) - min(y_coords)
    
    if spread_x < 80 and spread_y < 80:
        return 1.5  # Boost multiplier for suspicious localized pacing
    return 1.0

def calculate_threat_score(track_id, bbox=None):
    """
    Upgraded Threat Assessment Core (Deterministic & Spatial)
    Accepts track_id and optional current bbox coordinates [x1, y1, x2, y2]
    """
    current_time = time.time()
    last_seen[track_id] = current_time
    
    if track_id not in loiter_start_times:
        loiter_start_times[track_id] = current_time
        threat_memory[track_id] = 10.0  # Safe initial base threat score
        
    loiter_duration = current_time - loiter_start_times[track_id]
    
    # Calculate baseline time-increment score
    base_increment = loiter_duration * 2.0
    
    # Dynamic Multipliers based on behavior
    roi_multiplier = 1.0
    pacing_multiplier = 1.0
    
    if bbox is not None:
        cx = (bbox[0] + bbox[2]) / 2
        cy = (bbox[1] + bbox[3]) / 2
        
        # 1. Evaluate Zonal Breach Feature
        if is_inside_roi(bbox, RESTRICTED_ZONE):
            roi_multiplier = 2.0  
            
        # 2. Evaluate Trajectory Pacing Feature
        pacing_multiplier = calculate_pacing_factor(track_id, cx, cy)
        
    # Calculate final algorithmic score
    calculated_score = 10.0 + (base_increment * roi_multiplier * pacing_multiplier)
    new_score = max(0.0, min(100.0, calculated_score))
    threat_memory[track_id] = new_score
    
    # Map out operational states based on concrete multipliers
    if roi_multiplier > 1.0 and loiter_duration > 5:
        activity = "RESTRICTED ZONE BREACH"
    elif pacing_multiplier > 1.0 and loiter_duration > 10:
        activity = "PACING / LOITERING"
    elif loiter_duration > 15:
        activity = "EXTENDED LOITERING"
    else:
        activity = "NORMAL"
        
    # Severity assignment
    if new_score >= 75 or activity == "RESTRICTED ZONE BREACH":
        level = "HIGH"
        color = (0, 0, 255)      # Red
    elif new_score >= 45:
        level = "MEDIUM"
        color = (0, 255, 255)    # Yellow
    else:
        level = "LOW"
        color = (0, 255, 0)      # Green
        
    return int(new_score), level, color, activity

def cleanup_old_tracks():
    current_time = time.time()
    remove_ids = []
    
    for track_id, seen_time in last_seen.items():
        if current_time - seen_time > 5.0:
            remove_ids.append(track_id)
            
    for track_id in remove_ids:
        last_seen.pop(track_id, None)
        threat_memory.pop(track_id, None)
        loiter_start_times.pop(track_id, None)
        trajectory_history.pop(track_id, None)