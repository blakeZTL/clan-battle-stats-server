from agg_roblox_data import calculate_points_per_unit,get_active_clan_battle,get_clan_data,agg_clan_member_profiles
from fastapi import APIRouter

router = APIRouter()

@router.get("/ppu/{clanName}")
def get_ppu(clanName: str):
    current_battle = get_active_clan_battle()
    clan_data = get_clan_data(clanName)
    ppu = calculate_points_per_unit(clan_data, current_battle)
    return ppu

@router.get("/get-clan-members/{clanName}")
def get_clan_members(clanName: str):
    clan_data = get_clan_data(clanName)
    clan_profiles = agg_clan_member_profiles(clan_data)
    print(clan_profiles)
    return clan_profiles
