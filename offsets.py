import json
from typing import Dict, Any

with open('hazedumper/csgo.json', 'r') as f_:
    CSGO_OFFSETS: Dict[str, Any] = json.load(f_)

SIGNATURES: Dict[str, int] = CSGO_OFFSETS['signatures']
NETVARS: Dict[str, int] = CSGO_OFFSETS['netvars']


m_iHealth = NETVARS['m_iHealth']
dwEntityList = SIGNATURES['dwEntityList']
dwViewMatrix = SIGNATURES['dwViewMatrix']
m_iTeamNum = NETVARS['m_iTeamNum']
m_vecOrigin = NETVARS['m_vecOrigin']
m_lifeState = NETVARS['m_lifeState']
dwLocalPlayer = SIGNATURES['dwLocalPlayer']
m_Collision = NETVARS['m_Collision']
m_iGlowIndex = NETVARS['m_iGlowIndex']
is_c4_owner = SIGNATURES['is_c4_owner']
m_iCrosshairId = NETVARS['m_iCrosshairId']
dwForceAttack = SIGNATURES['dwForceAttack']
dwClientState = SIGNATURES['dwClientState']
dwClientState_MaxPlayer = SIGNATURES['dwClientState_MaxPlayer']
dwClientState_State = SIGNATURES['dwClientState_State']
dwGlowObjectManager = SIGNATURES['dwGlowObjectManager']
