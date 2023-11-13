import enum, math, peewee
from Users.models import User
from Base_Classes.models import BaseModel

class PointType(enum.Enum):
    MESSAGE = 3
    REACTION = 0
    MANUAL = 0

class LevelSystem:
    @staticmethod
    def get_rank(points: float):
        level = 1
        xp_required = 12

        while points >= xp_required:
            points -= xp_required
            level += 1
            xp_required += 2
        return level
    
    @staticmethod
    def get_level_xp(level: int):
        return 12 + 2 * (level - 1)

    @staticmethod
    def level_changed(current_points, new_points):
        changed = False
        current_level = LevelSystem.get_rank(current_points)
        new_level = LevelSystem.get_rank(new_points)
        if current_level != new_level:
            changed = True
        number_levels = new_level - current_level

        return changed, number_levels, current_level
    

class UserActivity(BaseModel):
    MODE_ADD = 'ADD'
    MODE_REDUCE = 'REDUCE'
    MODE_CHOICES = ((MODE_ADD, MODE_ADD), (MODE_REDUCE, MODE_REDUCE))

    user = peewee.ForeignKeyField(model = User)
    message_id = peewee.CharField(max_length = 255)
    reaction = peewee.BooleanField(default = False)
    points = peewee.FloatField()
    mode = peewee.CharField(choices = MODE_CHOICES, default = MODE_ADD)

    def record_new_points(self, point_type: PointType, mode: str, manual_points = 0):
        points = point_type.value
        if point_type == PointType.REACTION:
            self.reaction = True
        if point_type == PointType.MANUAL:
            points = manual_points
        
        current_total_points = UserActivity.get_points(self.user.user_id)
        if mode == UserActivity.MODE_ADD:
            new_total_points = current_total_points + points
        else:
            new_total_points = current_total_points - points

        self.user.total_points = new_total_points
        self.user.save()

        self.points = points
        self.mode = mode
        self.save()

        return LevelSystem.level_changed(current_total_points, new_total_points)

    @staticmethod
    def get_points(user_id):

        added_points_sum = UserActivity.select(
            UserActivity.points, peewee.fn.SUM(UserActivity.points).alias('total')).join(User).where(User.user_id == user_id, UserActivity.mode == UserActivity.MODE_ADD)
    
        reduced_points_sum = UserActivity.select(
            UserActivity.points, peewee.fn.SUM(UserActivity.points).alias('total')).join(User).where(User.user_id == user_id, UserActivity.mode == UserActivity.MODE_REDUCE)
        
        added_total = 0
        if added_points_sum[0].total:
            added_total = added_points_sum[0].total
        reduced_total = 0
        if reduced_points_sum[0].total:
            reduced_total = reduced_points_sum[0].total

        return added_total - reduced_total

    @staticmethod
    def count_messages(user_id):
        return UserActivity.select(UserActivity, User).join(User).where(User.user_id == user_id, UserActivity.reaction == False).count()

    @staticmethod
    def count_reactions(user_id):
        added_reactions = (
        UserActivity.select(UserActivity, User)
        .join(User)
        .where(
            (User.user_id == user_id) & (UserActivity.reaction == True) & (UserActivity.mode == UserActivity.MODE_ADD))
        .count()
        )

        reduced_reactions = (
        UserActivity.select(UserActivity, User)
        .join(User)
        .where(
            (User.user_id == user_id) & (UserActivity.reaction == True) & (UserActivity.mode == UserActivity.MODE_REDUCE))
        .count()
        )
        return added_reactions - reduced_reactions