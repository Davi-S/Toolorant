import enum
import requests
import logging

logger = logging.getLogger(__name__)

def fetch_dynamic_enum(enum_name, url, process_items):
    """Fetch data from API and create an Enum dynamically with deduplication"""
    try:
        logger.info(f"Fetching {enum_name} data from {url}")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        items = process_items(data['data'])
        
        # Deduplicate items by name
        unique_items = {}
        for name, value in items:
            if name not in unique_items:
                unique_items[name] = value
            else:
                print(f"Warning: Duplicate map name detected and skipped - {name}")
        
        logger.info("Processed %s items: %s", enum_name, ', '.join(f"{k}: {v}" for k, v in unique_items.items()))
        
        return enum.Enum(enum_name, unique_items.items())
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch {enum_name}: {e}")
        raise RuntimeError(f"Failed to fetch {enum_name}: {e}")

def process_agents(agents_data):
    logger.info("Processing agents data")
    agents = [
        a for a in agents_data 
        if a.get('isPlayableCharacter', False)
    ]
    sorted_agents = sorted(agents, key=lambda x: x['displayName'])
    logger.info(f"Found {len(sorted_agents)} playable agents")
    return [
        (a['displayName'].upper().replace(' ', '_'), a['uuid']) 
        for a in sorted_agents
    ]

def process_maps(maps_data):
    logger.info("Processing maps data")
    map_items = []
    for m in maps_data:
        # Skip The Range map
        if m['displayName'] in ['The Range', 'Basic Training']:
            logger.info(f"Skipping map: {m['displayName']}")
            continue
            
        parts = m['mapUrl'].split('/')

        # Find the index of "Maps" in the URL path
        try:
            maps_index = parts.index("Maps")
        except ValueError:
            logger.warning(f"Invalid map URL format: {m['mapUrl']}")
            continue

        # Extract the map ID based on the "Maps" segment
        if maps_index + 1 < len(parts):
            # Handle special case for HURM maps
            if parts[maps_index + 1] == "HURM":
                # For URLs like /Game/Maps/HURM/HURM_Alley/HURM_Alley
                map_id = parts[maps_index + 2]  # Get "HURM_Alley"
            else:
                map_id = parts[maps_index + 1]  # Normal case (e.g., Ascent -> Ascen
        else:
            logger.warning(f"Invalid map URL format: {m['mapUrl']}")
            continue

        map_name = m['displayName'].upper().replace(' ', '_')
        map_items.append((map_name, map_id))
        logger.info(f"Added map: {map_name} -> {map_id}")

    logger.info(f"Found {len(map_items)} playable maps")
    return sorted(map_items, key=lambda x: x[0])

# Dynamically create enums
logger.info("Creating Agent enum")
Agent = fetch_dynamic_enum('Agent', 'https://valorant-api.com/v1/agents', process_agents)

logger.info("Creating Map enum")
Map = fetch_dynamic_enum('Map', 'https://valorant-api.com/v1/maps', process_maps)

logger.info("Finished creating enums")

class GameMode(enum.Enum):
    # check for "QueueID" on the match info to find if the "Bomb" game mode is competitive or unrated
    COMPETITIVE = "Bomb" + "Competitive"
    REPLICATION = "OneForAll"
    SPIKE_RUSH = "QuickBomb"
    SWIFTPLAY = "Swiftplay_EndOfRoundCredits"
    UNRATED = "Bomb"

class Rank(enum.Enum):
    UNRANKED_1 = 0
    UNRANKED_2 = enum.auto()
    UNRANKED_3 = enum.auto()
    IRON_1 = enum.auto()
    IRON_2 = enum.auto()
    IRON_3 = enum.auto()
    BRONZE_1 = enum.auto()
    BRONZE_2 = enum.auto()
    BRONZE_3 = enum.auto()
    SILVER_1 = enum.auto()
    SILVER_2 = enum.auto()
    SILVER_3 = enum.auto()
    GOLD_1 = enum.auto()
    GOLD_2 = enum.auto()
    GOLD_3 = enum.auto()
    PLATINUM_1 = enum.auto()
    PLATINUM_2 = enum.auto()
    PLATINUM_3 = enum.auto()
    DIAMOND_1 = enum.auto()
    DIAMOND_2 = enum.auto()
    DIAMOND_3 = enum.auto()
    ASCENDANT_1 = enum.auto()
    ASCENDANT_2 = enum.auto()
    ASCENDANT_3 = enum.auto()
    IMMORTAL_1 = enum.auto()
    IMMORTAL_2 = enum.auto()
    IMMORTAL_3 = enum.auto()
    RADIANT = enum.auto()
