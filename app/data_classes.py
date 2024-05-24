from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class UserProfile:
    hasVerifiedBadge: bool
    id: int
    name: str
    displayName: str
    externalAppDisplayName: Optional[str] = None
    description: Optional[str]= None
    created: Optional[str]= None
    isBanned: Optional[bool]= None  
    

@dataclass
class Member:
    UserID: int
    PermissionLevel: int
    JoinTime: int

@dataclass
class DiamondContribution:
    UserID: int
    Diamonds: int

@dataclass
class PointContribution:
    UserID: int
    Points: int
    
@dataclass
class Goal:
    Type: int
    Amount: int
    Stars: int
    Progress: int
    Tier: int
    Contributions: Dict[str, int]

@dataclass
class Battle:
    ProcessedAwards: bool
    AwardUserIDs: List[int]
    BattleID: str
    Points: int
    PointContributions: List[PointContribution]
    EarnedMedal: str
    Goals: Optional[List[Goal]] = None
    Place: Optional[int] = None
    EarnedMedal: Optional[str] = None

@dataclass
class AllTimeDiamondContributions:
    Sum: int
    Data: List[DiamondContribution]

@dataclass
class DiamondContributions:
    AllTime : AllTimeDiamondContributions

@dataclass
class ClanData:
    Created: int
    Owner: int
    Name: str
    Icon: str
    Desc: str
    MemberCapacity: int
    OfficerCapacity: int
    GuildLevel: int
    Members: List[Member]
    DepositedDiamonds: int
    DiamondContributions: DiamondContributions
    Status: str
    StatusTimestamp: int
    StatusUsername: str
    Battles: Dict[str, Battle]    
    LastKickTimestamp: int
    BronzeMedals: Optional[int] = None
    SilverMedals: Optional[int] = None
    GoldMedals: Optional[int] = None
    CountryCode: Optional[str] = None

@dataclass
class ClanApiResponse:
    status: str
    data: ClanData

@dataclass
class Reward:
    _data: Dict[str, str]

@dataclass
class Rewards:
    Bronze: List[Reward]
    Silver: List[Reward]
    Gold: List[Reward]

@dataclass
class ConfigData:
    _script: Optional[str]
    FinishTime: int
    Title: str
    _id: str
    StartTime: int
    Rewards: Rewards

@dataclass
class ClanBattleData:
    _id: str
    configName: str
    category: str
    configData: ConfigData

@dataclass
class ClanBattleApiResponse:
    status: str
    data: ClanBattleData

# @dataclass
# class MemberData(PointContribution, UserProfile):
#     id: int
#     name: str
#     Points: int
#     PermissionLevel: Optional[int]
#     JoinTime: Optional[int]

@dataclass
class ClansData:
    Created: int
    Name: str
    MemberCapacity: int
    DepositedDiamonds: int
    CountryCode: Optional[str]
    Members: int
    Points: int

@dataclass
class ClansApiResponse:
    status: str
    data: List[ClansData]