import json
from channels.generic.websocket import AsyncWebsocketConsumer
from helpers.allmodels import Tickets,Ticketattachments
from channels.db import database_sync_to_async


class ChatRoomConsumer(AsyncWebsocketConsumer):
    
    @database_sync_to_async
    def createticket_message(self,message,sender,message_id,uid,attachments):
        check_message_exist=Tickets.objects.check_message_exist(uid,sender)
        if(check_message_exist):
            message=check_message_exist
        else:
            message=Tickets.objects.createticketmessage(message,sender,message_id,uid)
        if(attachments):
            atachments_list=json.loads(attachments)
            for atachment in atachments_list:
                Ticketattachments.objects.updateticket_id(atachment['id'],message.id)
        return message

    async def connect(self):
        self.chat_box_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.group_name = "ticket_%s" % self.chat_box_name

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    # This function receive messages from WebSocket.
   
    async def receive(self, text_data):
        message_data_json = json.loads(text_data)
        message_data=message_data_json['message']
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "sendMessage",
                "message": message_data["message"],
                "sender": message_data["sender"],
                "message_id": message_data["message_id"],
                "recipient": message_data["recipient"],
                "uid": message_data["uid"],
                'attachments':message_data['attachments']

            },
        )
    # Receive message from room group.
    async def sendMessage(self, event):
        message_details= event
        print(f"message_details {message_details}")
        createmessage=await self.createticket_message(event["message"],event["sender"],event["message_id"],event["uid"],message_details['attachments'])
        await self.send(
            text_data=json.dumps(
                {
                    "message": message_details["message"],
                    "sender": message_details["sender"],
                    "message_id": message_details["message_id"],
                    "recipient": message_details["recipient"],
                    "uid": message_details["uid"],
                    'attachments':message_details['attachments']

                }
            )
        )

    pass
