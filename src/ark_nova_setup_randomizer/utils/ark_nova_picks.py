import random
import re


def parse_exclude_maps(value: str) -> list[str]:
    if not value.strip():
        return []
    token_pattern = re.compile(r"^(?:[1-9]|1[0-4]|[1-8]a)$")

    parts = [p.strip() for p in value.split(",")]
    result = []

    for p in parts:
        if not p:
            continue
        if not token_pattern.match(p):
            raise ValueError(
                f"This map does not exist or the string was not entered correctly (comma-separated!): {p}"
            )
        result.append(p)

    return result


def pick_maps(
    player_count: int,
    replace_alternative: bool,
    add_alternative: bool,
    add_map_pack_1: bool,
    add_map_pack_2: bool,
    maps_per_player: int = 2,
    exclude_maps: list[str] | None = None,
) -> list[str]:
    if replace_alternative and add_alternative:
        raise ValueError("replace alternative and add_alternative cannot both be True.")

    default_maps = [
        "1: Observation Tower",
        "2: Outdoor Areas",
        "3: Silver Lake",
        "4: Commercial Harbor",
        "5: Park Restaurant",
        "6: Research Institute",
        "7: Ice Cream Parlors",
        "8: Hollywood Hills",
    ]
    alternative_maps = [
        re.sub(r"^(\d+):\s*(.*)$", r"\1a: \2 (Alt.)", m) for m in default_maps
    ]

    map_pack_1 = [
        "9: Geographical Zoo",
        "10: Rescue Station",
    ]

    map_pack_2 = [
        "11: Caves",
        "12: Artificial Intelligence",
        "13: Drawing Board",
        "14: Lagoon",
    ]

    map_pool = default_maps[:]  # copy

    if replace_alternative:
        map_pool = [
            re.sub(r"^(\d+):\s*(.*)$", r"\1a: \2 (Alt.)", m) for m in default_maps
        ]
    if add_alternative:
        map_pool = default_maps + alternative_maps
    if add_map_pack_1:
        map_pool += map_pack_1
    if add_map_pack_2:
        map_pool += map_pack_2

    if len(map_pool) < player_count * maps_per_player:
        raise ValueError(
            "Not enough maps available for the selected player count and maps per player."
        )

    needed = player_count * maps_per_player
    if len(map_pool) < needed:
        raise ValueError(
            "Not enough maps available for the selected player count and maps per player."
        )

    def map_id(label: str) -> str:
        m = re.match(r"^(\d{1,2}a?):", label, flags=re.IGNORECASE)
        if not m:
            raise ValueError(f"Unexpected map label format: {label!r}")
        return m.group(1).lower()

    exclude_set = {e.lower() for e in (exclude_maps or [])}
    map_pool = [m for m in map_pool if map_id(m) not in exclude_set]

    if len(map_pool) < needed:
        raise ValueError(
            "Not enough maps left after exclusions for the selected player count and maps per player."
        )

    return random.sample(map_pool, needed)


def pick_starting_player(players: list[str]) -> str:
    return random.sample(players, 1)[0]


def pick_bonus_tiles(include_marine: bool) -> list[str]:
    default_tiles = [
        "10 Money",
        "Size 3 Enclosure",
        "2 Reputation",
        "3 X-Tokens",
        "3 Cards (Rep. Range)",
        "Partner Zoo",
        "University",
        "2x Multiplier",
        "Marketing",
    ]
    marine_tiles = [
        "Ignore 3 Animal Req.",
        "Extra Shift",
        "Joker for Base Project",
        "3x Posturing",
        "3x Adapt",
        "Snap + Handsize",
    ]

    if include_marine:
        default_tiles += marine_tiles

    return random.sample(default_tiles, 5 if include_marine else 4)


def pick_project_cards(include_marine: bool, player_count: int) -> list[str]:
    default_projects = [
        "Species Diversity",
        "Habitat Diversity",
        "Africa",
        "Americas",
        "Australia",
        "Asia",
        "Europe",
        "Primates",
        "Reptiles",
        "Predators",
        "Herbivores",
        "Birds",
    ]
    marine_projects = [
        "Sea Animals",
    ]

    if include_marine:
        default_projects += marine_projects

    return random.sample(default_projects, 4 if player_count > 3 else 3)
