from typing import Optional, List, Union
from semaphore import Attachment

from bot_commands import AdminCommandStrings, PublicCommandStrings


class MessageHandler():
    def __init__(self) -> None:
        pass

    @staticmethod
    def prepare_broadcast_message(message: str) -> str:
        if message == '':
            return None
        else:
            message = message[len("!broadcast"):].strip()
            if message == '':
                return None
            else:
                return message

    def prepare_attachments(self, attachments: Optional[List[Attachment]]) -> List:
        if attachments == []:
            return None

        attachments_to_send = []
        for attachment in attachments:
            attachment_to_send = {"filename": attachment.stored_filename,
                                  "width": attachment.width,
                                  "height": attachment.height,
                                  "contentType": attachment.content_type,
                                  }
            attachments_to_send.append(attachment_to_send)

        return attachments_to_send

    @staticmethod
    def compose_help_message(add_admin_commands: bool = False) -> str:
        def _add_commands(message, command_strings):
            for command_str in command_strings:
                message += "\t" + command_str.value + "\n"
            return message

        message = "I'm sorry, I didn't understand you but I understand the following commands:\n\n"
        message = _add_commands(message, PublicCommandStrings)
        if add_admin_commands:
            message = _add_commands(message, AdminCommandStrings)
        message += "\nPlease try again"
        return message

    @staticmethod
    def compose_must_subscribe_message() -> str:
        message = "To be able to send messages you must be a subscriber too.\n"
        message += "Please subscribe by sending:\n"
        message += f"\t{PublicCommandStrings.subscribe.value}\n"
        message += "and try again after that."
        return message

    @staticmethod
    def compose_message_to_admin(message: str, user: Optional[str]) -> str:
        header = "***Admin***\n"
        if user is not None:
            header += user + "\n"
        return header + message
