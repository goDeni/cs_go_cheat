from typing import Dict, Any

CSGO_OFFSETS: Dict[str, Any] = {
    "timestamp": 1588780897,
    "signatures": {
        "anim_overlays": 10624,
        "clientstate_choked_commands": 19752,
        "clientstate_delta_ticks": 372,
        "clientstate_last_outgoing_command": 19748,
        "clientstate_net_channel": 156,
        "convar_name_hash_table": 192760,
        "dwClientState": 5807564,
        "dwClientState_GetLocalPlayer": 384,
        "dwClientState_IsHLTV": 19776,
        "dwClientState_Map": 652,
        "dwClientState_MapDirectory": 392,
        "dwClientState_MaxPlayer": 904,
        "dwClientState_PlayerInfo": 21176,
        "dwClientState_State": 264,
        "dwClientState_ViewAngles": 19848,
        "dwEntityList": 81017572,
        "dwForceAttack": 51859580,
        "dwForceAttack2": 51859592,
        "dwForceBackward": 51859652,
        "dwForceForward": 51859664,
        "dwForceJump": 85907328,
        "dwForceLeft": 51859688,
        "dwForceRight": 51859676,
        "dwGameDir": 6456824,
        "dwGameRulesProxy": 86379100,
        "dwGetAllClasses": 13983532,
        "dwGlobalVars": 5806800,
        "dwGlowObjectManager": 86554808,
        "dwInput": 85545104,
        "dwInterfaceLinkList": 9412324,
        "dwLocalPlayer": 13826964,
        "dwMouseEnable": 13850424,
        "dwMouseEnablePtr": 13850376,
        "dwPlayerResource": 51852332,
        "dwRadarBase": 85428308,
        "dwSensitivity": 13850068,
        "dwSensitivityPtr": 13850024,
        "dwSetClanTag": 564816,
        "dwViewMatrix": 80958500,
        "dwWeaponTable": 85547860,
        "dwWeaponTableIndex": 12892,
        "dwYawPtr": 13849496,
        "dwZoomSensitivityRatioPtr": 13870560,
        "dwbSendPackets": 867674,
        "dwppDirect3DDevice9": 684080,
        "find_hud_element": 754434624,
        "force_update_spectator_glow": 3772626,
        "interface_engine_cvar": 256492,
        "is_c4_owner": 3823760,
        "m_bDormant": 237,
        "m_flSpawnTime": 41824,
        "m_pStudioHdr": 10572,
        "m_pitchClassPtr": 85428984,
        "m_yawClassPtr": 13849496,
        "model_ambient_min": 5819884,
        "set_abs_angles": 1896672,
        "set_abs_origin": 1896224
    },
    "netvars": {
        "cs_gamerules_data": 0,
        "m_ArmorValue": 45928,
        "m_Collision": 800,
        "m_CollisionGroup": 1140,
        "m_Local": 12220,
        "m_MoveType": 604,
        "m_OriginalOwnerXuidHigh": 12740,
        "m_OriginalOwnerXuidLow": 12736,
        "m_SurvivalGameRuleDecisionTypes": 4896,
        "m_SurvivalRules": 3320,
        "m_aimPunchAngle": 12332,
        "m_aimPunchAngleVel": 12344,
        "m_angEyeAnglesX": 45932,
        "m_angEyeAnglesY": 45936,
        "m_bBombPlanted": 2461,
        "m_bFreezePeriod": 32,
        "m_bGunGameImmunity": 14640,
        "m_bHasDefuser": 45944,
        "m_bHasHelmet": 45916,
        "m_bInReload": 12965,
        "m_bIsDefusing": 14620,
        "m_bIsQueuedMatchmaking": 116,
        "m_bIsScoped": 14612,
        "m_bIsValveDS": 117,
        "m_bSpotted": 2365,
        "m_bSpottedByMask": 2432,
        "m_bStartedArming": 13296,
        "m_bUseCustomAutoExposureMax": 2521,
        "m_bUseCustomAutoExposureMin": 2520,
        "m_bUseCustomBloomScale": 2522,
        "m_clrRender": 112,
        "m_dwBoneMatrix": 9896,
        "m_fAccuracyPenalty": 13104,
        "m_fFlags": 260,
        "m_flC4Blow": 10640,
        "m_flCustomAutoExposureMax": 2528,
        "m_flCustomAutoExposureMin": 2524,
        "m_flCustomBloomScale": 2532,
        "m_flDefuseCountDown": 10668,
        "m_flDefuseLength": 10664,
        "m_flFallbackWear": 12752,
        "m_flFlashDuration": 42000,
        "m_flFlashMaxAlpha": 41996,
        "m_flLastBoneSetupTime": 10532,
        "m_flLowerBodyYawTarget": 14972,
        "m_flNextAttack": 11632,
        "m_flNextPrimaryAttack": 12856,
        "m_flSimulationTime": 616,
        "m_flTimerLength": 10644,
        "m_hActiveWeapon": 12024,
        "m_hMyWeapons": 11768,
        "m_hObserverTarget": 13196,
        "m_hOwner": 10700,
        "m_hOwnerEntity": 332,
        "m_iAccountID": 12232,
        "m_iClip1": 12900,
        "m_iCompetitiveRanking": 6788,
        "m_iCompetitiveWins": 7048,
        "m_iCrosshairId": 46036,
        "m_iEntityQuality": 12204,
        "m_iFOV": 12772,
        "m_iFOVStart": 12776,
        "m_iGlowIndex": 42024,
        "m_iHealth": 256,
        "m_iItemDefinitionIndex": 12202,
        "m_iItemIDHigh": 12224,
        "m_iMostRecentModelBoneCounter": 9872,
        "m_iObserverMode": 13176,
        "m_iShotsFired": 41856,
        "m_iState": 12888,
        "m_iTeamNum": 244,
        "m_lifeState": 607,
        "m_nFallbackPaintKit": 12744,
        "m_nFallbackSeed": 12748,
        "m_nFallbackStatTrak": 12756,
        "m_nForceBone": 9868,
        "m_nTickBase": 13360,
        "m_rgflCoordinateFrame": 1092,
        "m_szCustomName": 12348,
        "m_szLastPlaceName": 13748,
        "m_thirdPersonViewAngles": 12760,
        "m_vecOrigin": 312,
        "m_vecVelocity": 276,
        "m_vecViewOffset": 264,
        "m_viewPunchAngle": 12320
    }
}

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
