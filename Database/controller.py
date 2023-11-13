import discord, settings
from Database.models import UserActivity
from Users.models import User
from .models import UserActivity, PointType
from Base_Classes.controller import Controller

class Ranks(Controller):
    async def process_message(self, message: discord.Message):
        if isinstance(message.channel, discord.TextChannel) and int(message.channel.id) in settings.XP_DISABLED_CHANNELS:
            return
        await self.add_points(message.id, message.author.id, PointType.MESSAGE)

    async def process_reaction(self, payload: discord.RawReactionActionEvent):
        if payload.event_type == 'REACTION_ADD':
            await self.add_points(payload.message_id, payload.user_id, PointType.REACTION)
        else:
            await self.reduce_points(payload.message_id, payload.user_id, PointType.REACTION, UserActivity.MODE_REDUCE)
    
    async def announcement(self, message):
        await self.messenger.send_message(message)

    async def _save_to_db(
        self, 
        message_id: int, 
        user_id: int, 
        point_type: PointType, 
        manual_points: int = 0,
        mode: str = UserActivity.MODE_ADD
        ):
        # private function only for controller
        user = User.fetch_user_by_id(user_id)
        member = await self.bot_handler.fetch_member(user_id)
        user_activity = UserActivity(message_id = message_id, user = user)
        changed, number_levels, current_level = user_activity.record_new_points(point_type, mode, manual_points)

        if changed:
            new_level = current_level + number_levels
            message = message = f'Congratulations <@{user_id}> you\'ve hit `level {new_level}`! :wolf:\n'
            if new_level == 5:
                message += f'Type `!lvl member` to receive your new rank. Thank you for participating in the server! :tada:'
            elif new_level == 10:
                message += f'Type `!lvl expert` to receive your new rank. Thank you for participating in the server! :tada:'
            elif new_level == 20:
                message += f'Type `!lvl veteran` to receive your new rank. Thank you for participating in the server! :tada:'
            elif new_level == 30:
                message += f'Type `!lvl champion` to receive your new rank. Thank you for participating in the server! :tada:'
            await self.announcement(message)

    async def add_points(self, message_id, user_id, point_type, manual_points = 0):
        await self._save_to_db(message_id, user_id, point_type, manual_points = manual_points)
    
    async def reduce_points(self, message_id, user_id, point_type, mode: str):
        await self._save_to_db(message_id, user_id, point_type, mode = mode)