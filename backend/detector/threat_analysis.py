import time
import math

# Memory Registries
threat_memory = {}       
loiter_start_times = {}  
last_seen = {}           
trajectory_history = {}  

# Registry for tracking zone residency time
zone_entry_times = {}    

# Fallback boundaries (Will be continually updated dynamically by inference.py parameters)
RESTRICTED_ZONE = [800, 200, 1150, 600] 

def is_inside_roi(bbox, roi):
    """
    Checks if the center point of the person's bounding box falls inside the ROI.
    """
    if not bbox or len(bbox) < 4:
        return False
    cx = (bbox[0] + bbox[2]) / 2
    cy = (bbox[1] + bbox[3]) / 2
    
    rx_min, ry_min, rx_max, ry_max = roi
    return rx_min <= cx <= rx_max and ry_min <= cy <= ry_max

def calculate_pacing_factor(track_id, cx, cy):
    if track_id not in trajectory_history:
        trajectory_history[track_id] = []
        
    trajectory_history[track_id].append((cx, cy))
    if len(trajectory_history[track_id]) > 30:
        trajectory_history[track_id].pop(0)
        
    if len(trajectory_history[track_id]) < 10:
        return 1.0
        
    x_coords = [p[0] for p in trajectory_history[track_id]]
    y_coords = [p[1] for p in trajectory_history[track_id]]
    
    spread_x = max(x_coords) - min(x_coords)
    spread_y = max(y_coords) - min(y_coords)
    
    if spread_x < 80 and spread_y < 80:
        return 1.5
    return 1.0

def calculate_threat_score(track_id, bbox=None):
    current_time = time.time()
    last_seen[track_id] = current_time
    
    if track_id not in loiter_start_times:
        loiter_start_times[track_id] = current_time
        threat_memory[track_id] = 10.0
        
    loiter_duration = current_time - loiter_start_times[track_id]
    base_increment = loiter_duration * 2.0
    
    roi_multiplier = 1.0
    pacing_multiplier = 1.0
    is_breaching_confirmed = False
    
    if bbox is not None:
        cx = (bbox[0] + bbox[2]) / 2
        cy = (bbox[1] + bbox[3]) / 2
        
        # Strict time-constrained area validation
        if is_inside_roi(bbox, RESTRICTED_ZONE):
            roi_multiplier = 2.0  
            
            if track_id not in zone_entry_times:
                zone_entry_times[track_id] = current_time
                
            time_spent_in_zone = current_time - zone_entry_times[track_id]
            
            # Target must persist inside the area bounds for more than 3 full seconds
            if time_spent_in_zone >= 3.0:
                is_breaching_confirmed = True
        else:
            zone_entry_times.pop(track_id, None)
            
        pacing_multiplier = calculate_pacing_factor(track_id, cx, cy)
        
    calculated_score = 10.0 + (base_increment * roi_multiplier * pacing_multiplier)
    new_score = max(0.0, min(100.0, calculated_score))
    threat_memory[track_id] = new_score
    
    # --- UPGRADED TIMING MILESTONE MATCHING ENGINE ---
    if is_breaching_confirmed:
        activity = "RESTRICTED ZONE BREACH"
    elif pacing_multiplier > 1.0 and loiter_duration > 7.0:    # Tightened from 10 to 7 seconds
        activity = "PACING / LOITERING"
    elif loiter_duration > 8.0:                               # Tightened from 15 to 8 seconds
        activity = "EXTENDED LOITERING"
    else:
        activity = "NORMAL"
        
    if new_score >= 75 or is_breaching_confirmed:
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
        if current_time - seen_time > 5.0:
            remove_ids.append(track_id)
            
    for track_id in remove_ids:
        last_seen.pop(track_id, None)
        threat_memory.pop(track_id, None)
        loiter_start_times.pop(track_id, None)
        trajectory_history.pop(track_id, None)
        zone_entry_times.pop(track_id, None)