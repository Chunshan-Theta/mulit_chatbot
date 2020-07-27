from typing import Optional


class ContinueCommand(dict):
    def add_command(self, user_id, command):
        try:
            self.__getitem__(user_id)
        except KeyError:
            self.__setitem__(user_id, None)

        self.__setitem__(user_id, command)

    def find_user(self, user_id) -> Optional[str]:
        try:
            self.__getitem__(user_id)
        except KeyError:
            return None

        user_command = self.__getitem__(user_id)
        self.__setitem__(user_id, None)
        return user_command

command_tmp_record = ContinueCommand()
