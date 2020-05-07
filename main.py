import time

from client_control import ClientControl, CLIENT_MODULE_NAME
from engine_control import EngineControl, ENGINE_MODULE_NAME
from glow_object_manager import GlowObjectManager
from player import Player
from process import get_process_handle, get_process_id
from trigger_bot import TriggerBot

CSGO_PROCESS_NAME = 'csgo.exe'


def main():
    pid = get_process_id(CSGO_PROCESS_NAME)
    if pid is None:
        print(f"Процесс {CSGO_PROCESS_NAME} не найден")
        return

    with get_process_handle(pid) as process_handle:
        client_control = ClientControl(process_handle.handle)
        engine_control = EngineControl(process_handle.handle)

        glow_object_manager = GlowObjectManager(client_control.address, process_handle.handle)

        print(
            f"{CSGO_PROCESS_NAME} pid: {pid}\n"
            f"handle: {process_handle.handle}\n"
            f"engine_address ({ENGINE_MODULE_NAME}): {engine_control.client_state_pointer}\n"
            f"client_address ({CLIENT_MODULE_NAME}): {client_control.address}\n"
            f"client_state: {engine_control.client_state_pointer}"
        )

        local_player = Player(process_handle.handle, 0)
        trigger_bot = TriggerBot(local_player, process_handle.handle, client_control.address)
        # trigger_bot.enable()
        while True:
            max_players_count = engine_control.get_max_players()
            local_player_pointer = client_control.get_local_player_pointer()
            local_player.change_pointer_if_needed(local_player_pointer)
            local_player.read_all_variables()

            for i in range(max_players_count):
                player_pointer = client_control.get_player_pointer(i)
                other_player = Player(process_handle.handle, player_pointer)
                if not other_player.is_alive() or other_player.get_team() == local_player.team:
                    continue

                trigger_bot.shoot_if_needed(i)
                other_player.read_all_variables()
                glow_object_manager.draw_player(other_player.glow_index, other_player.health)

            trigger_bot.clear_shoot_state()
            time.sleep(0.01)


if __name__ == "__main__":
    main()
