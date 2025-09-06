import pandas as pd
import streamlit as st

from ark_nova_setup_randomizer.utils.ark_nova_picks import (
    pick_bonus_tiles,
    pick_maps,
    pick_project_cards,
    pick_starting_player,
)

st.set_page_config(
    page_title="Ark Nova - Setup Randomizer",
    page_icon=":rhinoceros:",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        "Get Help": None,
        "Report a bug": "https://www.google.com",
        "About": None,
    },
)

st.title("Ark Nova - Setup Randomizer")

# --- constants ---
PLAYER_COUNT_ARRAY = [2, 3, 4]
SELECT_BOX_WIDTH_PLAYER_COUNT = 100

# --- state initializations ---
if "replace_alternative" not in st.session_state:
    st.session_state.replace_alternative = True
if "add_alternative" not in st.session_state:
    st.session_state.add_alternative = False
if "add_map_pack_1" not in st.session_state:
    st.session_state.add_map_pack_1 = True
if "add_map_pack_2" not in st.session_state:
    st.session_state.add_map_pack_2 = True
if "include_bonus_tiles" not in st.session_state:
    st.session_state.include_bonus_tiles = True
if "include_projects" not in st.session_state:
    st.session_state.include_projects = True
if "include_marine" not in st.session_state:
    st.session_state.include_marine = True


# --- on_change functions ---
def check_deactivate_marine_world() -> None:
    if (
        not st.session_state.include_bonus_tiles
        and not st.session_state.include_projects
    ):
        st.session_state.include_marine = False


player_count = st.selectbox(
    label="Playercount",
    options=PLAYER_COUNT_ARRAY,
    width=SELECT_BOX_WIDTH_PLAYER_COUNT,
    key="player_count",
)

player_options = [
    "🔵 🐟",
    "⚫ 🐧",
    "🔴 🐅",
    "🟡 🐒",
]

player_row = st.columns(player_count)

players = []

for idx, player_column in enumerate(player_row):
    with player_column:
        players.append(
            st.selectbox(
                label=f"Player {idx + 1}",
                options=player_options,
                index=idx,
                key=f"player_{idx+1}_choice",
            )
        )

with st.popover("Settings"):
    st.checkbox(
        "Replace Default Maps with Alternative Versions",
        key="replace_alternative",
        disabled=st.session_state.add_alternative,
    )
    st.checkbox(
        "Add Alternative Map Versions on Top",
        key="add_alternative",
        disabled=st.session_state.replace_alternative,
    )
    st.checkbox(
        "Add Map Pack 1",
        key="add_map_pack_1",
    )
    st.checkbox(
        "Add Map Pack 2",
        key="add_map_pack_2",
    )
    st.checkbox(
        "Include Bonus Tiles",
        key="include_bonus_tiles",
        on_change=check_deactivate_marine_world,
    )
    st.checkbox(
        "Include Base Conservation Project Cards",
        key="include_projects",
        on_change=check_deactivate_marine_world,
    )
    st.checkbox(
        "Include Marine World (Bonus Tiles & Projects)",
        key="include_marine",
        disabled=not st.session_state.include_bonus_tiles
        and not st.session_state.include_projects,
    )
    st.number_input(
        "Number of Maps per Player",
        min_value=1,
        value=2,
        key="maps_per_player",
    )

generate_col, randomness_col = st.columns([0.3, 0.7])

with generate_col:
    generate_button = st.button("Generate Setup")
with randomness_col:
    randomness_button = st.button("Randomness Experiment")

if generate_button:
    st.divider()
    starting_player = pick_starting_player(players=players)
    st.subheader("Starting Player")
    st.write(starting_player)

    st.subheader("Picked Maps")
    try:
        picked_maps = pick_maps(
            player_count=st.session_state.player_count,
            replace_alternative=st.session_state.replace_alternative,
            add_alternative=st.session_state.add_alternative,
            add_map_pack_1=st.session_state.add_map_pack_1,
            add_map_pack_2=st.session_state.add_map_pack_2,
            maps_per_player=st.session_state.maps_per_player,
        )
        map_df = pd.DataFrame(
            {
                "Player": players,
            },
        )
        for idx in range(st.session_state.maps_per_player):
            map_df[f"Map {idx + 1}"] = picked_maps[
                idx * len(players) : idx * len(players) + len(players)
            ]

        st.dataframe(map_df, hide_index=True)
    except Exception as e:
        st.error(e)

    if st.session_state.include_bonus_tiles:
        st.subheader("Picked Bonus Tiles")
        bonus_tiles = pick_bonus_tiles(include_marine=st.session_state.include_marine)
        positions = ["5", "5", "8", "8"]
        if st.session_state.include_marine:
            positions += ["Rep."]
        bonus_df = pd.DataFrame({"Position": positions, "Bonus Tile": bonus_tiles})
        st.dataframe(bonus_df, hide_index=True)
    if st.session_state.include_projects:
        st.subheader("Picked Projects")
        projects = pick_project_cards(
            include_marine=st.session_state.include_marine,
            player_count=len(players),
        )
        st.write("\n".join([f"- {project}" for project in projects]))

if randomness_button:
    st.divider()
    st.subheader("Starting Player - Law of Large Numbers")
    with st.spinner("Generating results..."):
        results_dict = {}
        for _ in range(10000):
            starting_player = pick_starting_player(players=players)
            results_dict[starting_player] = results_dict.get(starting_player, 0) + 1
        for key, val in results_dict.items():
            st.write(f"{key} {val}")
