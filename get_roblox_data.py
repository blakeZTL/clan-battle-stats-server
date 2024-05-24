from typing import List
from data_classes import (
    ClanBattleApiResponse,
    ClanBattleData,
    ClansData,
    ConfigData,
    ClanData,
    DiamondContributions,
    DiamondContribution,
    AllTimeDiamondContributions,
    Member,
    Battle,
    PointContribution,
    ClanApiResponse,
    Goal,
    ClansApiResponse,
    Rewards,
    Reward,
    UserProfile
)
import requests

def get_clan_data(clan_name: str) -> ClanApiResponse:
    url = f"https://biggamesapi.io/api/clan/{clan_name}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    if data["data"] is None:
        return None

    return ClanApiResponse(
        status=data["status"],
        data=ClanData(
            Created=data["data"]["Created"],
            Owner=data["data"]["Owner"],
            Name=data["data"]["Name"],
            Icon=data["data"]["Icon"],
            Desc=data["data"]["Desc"],
            MemberCapacity=data["data"]["MemberCapacity"],
            OfficerCapacity=data["data"]["OfficerCapacity"],
            GuildLevel=data["data"]["GuildLevel"],
            Members=[Member(**member) for member in data["data"]["Members"]],
            DepositedDiamonds=data["data"]["DepositedDiamonds"],
            DiamondContributions=DiamondContributions(
                AllTime=AllTimeDiamondContributions(
                    Sum=data["data"]["DiamondContributions"]["AllTime"]["Sum"],
                    Data=[
                        DiamondContribution(**contribution)
                        for contribution in data["data"]["DiamondContributions"][
                            "AllTime"
                        ]["Data"]
                    ],
                )
            ),
            Status=data["data"]["Status"],
            StatusTimestamp=data["data"]["StatusTimestamp"],
            StatusUsername=data["data"]["StatusUsername"],
            Battles={
                k: Battle(
                    **{
                        key: value
                        for key, value in v.items()
                        if key != "Goals" and key != "PointContributions"
                    },
                    PointContributions=[
                        PointContribution(**pc) for pc in v["PointContributions"]
                    ],
                    Goals=[Goal(**goal) for goal in v["Goals"]]
                    if "Goals" in v
                    else None,
                )
                for k, v in data["data"]["Battles"].items()
            },
            LastKickTimestamp=data["data"]["LastKickTimestamp"],
            BronzeMedals=data["data"].get("BronzeMedals"),
            SilverMedals=data["data"].get("SilverMedals"),
            GoldMedals=data["data"].get("GoldMedals"),
            CountryCode=data["data"].get("CountryCode"),
        ),
    )

def get_clans(page_size:int=25) -> ClansApiResponse:
    if page_size > 100:
        page_size = 100
    url = f"https://biggamesapi.io/api/clans?page=1&pageSize={page_size}&sort=Points&sortOrder=desc"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    if data["data"] is None:
        return None
    
    clan_data = []
    for clan in data["data"]:
        clan_data.append(ClansData(
            Created = clan["Created"],
            Name = clan["Name"],
            MemberCapacity = clan["MemberCapacity"],
            DepositedDiamonds = clan["DepositedDiamonds"],
            CountryCode = clan["CountryCode"],
            Members = clan["Members"],
            Points = clan["Points"]))

    return ClansApiResponse(data=clan_data,status=data["status"])

def get_active_clan_battle()->ClanBattleApiResponse:
    url = "https://biggamesapi.io/api/activeClanBattle"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    if data["data"] is None:
        return None
    
    clan_battle= ClanBattleData(
        _id=data["data"]["_id"],
        configName=data["data"]["configName"],
        category=data["data"]["category"],
        configData=ConfigData(
            _script=data["data"]["configData"]["_script"],
            FinishTime=data["data"]["configData"]["FinishTime"],
            Title=data["data"]["configData"]["Title"],
            _id=data["data"]["configData"]["_id"],
            StartTime=data["data"]["configData"]["StartTime"],
            Rewards=Rewards(
                Bronze=[Reward(**reward) for reward in data["data"]["configData"]["Rewards"]["Bronze"]],
                Silver=[Reward(**reward) for reward in data["data"]["configData"]["Rewards"]["Silver"]],
                Gold=[Reward(**reward) for reward in data["data"]["configData"]["Rewards"]["Gold"]]
            )
        ))
        
    return ClanBattleApiResponse(data=clan_battle,status=data["status"])
    
def get_roblox_users(userIds:List[int])->List[UserProfile]:
    url = "https://users.roblox.com/v1/users"
    body = {
        "userIds":userIds,
        "excludeBannedUsers": False
    }
    response = requests.post(url,json=body)
    if response.status_code != 200:
        return None
    data = response.json()
    if data["data"] is None:
        return None
    user_data = []
    for user in data["data"]:
        user_data.append(UserProfile(
            id=user["id"],
            name=user["name"],
            displayName=user["displayName"],
            hasVerifiedBadge=user["hasVerifiedBadge"],
        ))

    return user_data
    
if __name__ == "__main__":
    data = get_roblox_users([5347907548])
    for user in data:
        print(user.displayName)
    
    
