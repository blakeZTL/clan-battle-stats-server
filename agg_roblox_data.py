from datetime import datetime, timezone
from data_classes import ClanApiResponse, ClanBattleApiResponse
from get_roblox_data import get_clan_data, get_roblox_users, get_active_clan_battle
from helpers import convert_unix_timestamp_to_date


def agg_clan_member_profiles(clan_data: ClanApiResponse):
    member_ids = [member.UserID for member in clan_data.data.Members]
    if clan_data.data.Owner not in member_ids:
        member_ids.append(clan_data.data.Owner)
    user_profiles = get_roblox_users(member_ids)
    member_data = []
    for profile in user_profiles:
        join_time = [
            member.JoinTime
            for member in clan_data.data.Members
            if member.UserID == profile.id
        ]
        if join_time:
            join_time = join_time[0]
        else:
            join_time = None
        member_data.append(
            {
                "id": profile.id,
                "name": profile.name,
                "displayName": profile.displayName,
                "JoinTime": join_time,
            }
        )
    return member_data


def assign_clan_member_points(clan_data: ClanApiResponse, current_battle: str):
    member_profiles = agg_clan_member_profiles(clan_data)
    clan_data_point_contributions = clan_data.data.Battles[
        current_battle
    ].PointContributions

    for member in member_profiles:
        points = [
            point.Points
            for point in clan_data_point_contributions
            if point.UserID == member["id"]
        ]
        member["Points"] = points[0] if points else 0

    return member_profiles


def assign_member_effective_start_time(
    clan_data: ClanApiResponse, current_battle: ClanBattleApiResponse
):
    current_battle_name = current_battle.data.configName
    members_with_points = assign_clan_member_points(clan_data, current_battle_name)
    start_time = convert_unix_timestamp_to_date(
        current_battle.data.configData.StartTime
    )
    for member in members_with_points:
        if member["JoinTime"] is None or member["JoinTime"] < current_battle.data.configData.StartTime:            
            member["EffectiveStartTime"] = start_time
        else:
            member["EffectiveStartTime"] = convert_unix_timestamp_to_date(member["JoinTime"])

    return members_with_points


def calculate_points_per_unit(
    clan_data: ClanApiResponse, current_battle: ClanBattleApiResponse
):
    members_with_points_and_time = assign_member_effective_start_time(
        clan_data, current_battle
    )
    utc_now = datetime.now(timezone.utc)
    battle_start_time = convert_unix_timestamp_to_date(
        current_battle.data.configData.StartTime
    )
    for member in members_with_points_and_time:
        effective_start_time = member["EffectiveStartTime"]
        if effective_start_time > battle_start_time:
            time_difference = utc_now - effective_start_time
        else:
            time_difference = utc_now - battle_start_time

        time_difference_hours = time_difference.total_seconds() / 3600
        time_difference_days = time_difference.total_seconds() / 86400

        member["PointsPerHour"] = (
            member["Points"] / time_difference_hours if time_difference_hours > 0 else 0
        )
        member["PointsPerDay"] = (
            member["Points"] / time_difference_days if time_difference_days > 0 else 0
        )

    return members_with_points_and_time


if __name__ == "__main__":
    current_battle = get_active_clan_battle()
    member_data = calculate_points_per_unit(get_clan_data("SOUP"), current_battle)
    print(member_data)
