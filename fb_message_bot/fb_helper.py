from typing import Optional
import requests
from pymessenger import Bot

from fb_message_bot.fb_attachment import AttachmentGeneric
from fb_message_bot.fb_quickreply import FbQuickReply


class FbHelperBot(Bot):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_domains_whitelist = ["https://www.silkrode.com.tw/", "https://instagram.ftpe8-2.fna.fbcdn.net", "https://peterssendreceiveapp.ngrok.io"]

    def add_whitelist_website(self, whitelisted_domains:[str], access_token: Optional[str]):
        url = "https://graph.facebook.com/v2.6/me/thread_settings?"
        response = requests.post(
            url,
            params={
                "access_token": access_token
            },
            json={
              "setting_type" : "domain_whitelisting",
              "whitelisted_domains" : whitelisted_domains,
              "domain_action_type": "add"
            }
        )
        return {"code":response, "body":response.json()}

    def add_default_domain_to_whitelisting(self):
        return self.add_whitelist_website(access_token=self.access_token,whitelisted_domains=self.default_domains_whitelist)

    def send_templete_message(self,recipient_id, message_obj: AttachmentGeneric):
        payload = {
            'recipient': {
                'id': recipient_id
            },
            'message': message_obj
        }
        return self.send_raw(payload)

    def send_quickreplay_message(self,recipient_id, message_obj: FbQuickReply):
        payload = {
            'recipient': {
                'id': recipient_id
            },
            'message': message_obj
        }
        return self.send_raw(payload)
