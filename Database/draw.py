from PIL import Image, ImageDraw, ImageFont
import uuid, settings 

class RankImage:
    def draw_basic_information(self, display_name, total_points, current_rank, count_messages, count_reactions):
        uuid4 = str(uuid.uuid4())
        img = Image.open(settings.IMAGES_DIR / 'rank_bg.png')
        font_big = ImageFont.truetype('Ubuntu-M.ttf', 30)
        font_small = ImageFont.truetype('Ubuntu-M.ttf', 20)

        d = ImageDraw.Draw(img)
        d.text(
            (180, 38), 
            f'{display_name}', 
            fill = 'black', 
            font = font_big, 
            anchor = 'ls')

        d.text(
            (630, 38), 
            f'Level {str(current_rank).rjust(2, "0")}', 
            fill = 'black', 
            font = font_big, 
            anchor = 'rs')

        d.text(
            (180, 70), 
            f'XP: {int(total_points)}', 
            fill = 'black', 
            font = font_small, 
            anchor = 'ls')

        d.text(
            (180, 100), 
            f'RP Messages: {count_messages}', 
            fill = 'black', 
            font = font_small, 
            anchor = 'ls')

        # d.text(
        #     (180, 130), 
        #     f'Total Reactions: {count_reactions}', 
        #     fill = 'black', 
        #     font = font_small, 
        #     anchor = 'ls')

        full_image_path = settings.IMAGES_TEMP_DIR / f'{uuid4}.png'
        img.save(full_image_path)
        return full_image_path

    def draw_progress_bar(self, full_image_path, next_level_xp_diff, level_progress):
        progress = level_progress / next_level_xp_diff + 1
        if progress == 1:
            progress = 0
        img = Image.open(full_image_path)
        d = ImageDraw.Draw(img)
        full_width = 643

        if progress > 0 and progress <= 100:
            width = full_width * progress
            shape = ((12.0, 244.0), (width, 290.0))
            d.rectangle(xy = shape, fill = '#0f0')

        font_small = ImageFont.truetype('Ubuntu-M.ttf', 20)
        required_points = next_level_xp_diff - level_progress

        progress_percentage = round(progress * 100)

        d.text((full_width / 2, 270), 
        f'{progress_percentage}% (Required: {required_points})',
        fill = 'black',
        anchor = 'ms',
        font = font_small)
        img.save(full_image_path)

    def draw_member_avatar(self, full_image_path, member_avatar_path):
        img = Image.open(full_image_path)
        avatar_img = Image.open(member_avatar_path)
        avatar_img.thumbnail((144, 144), Image.Resampling.LANCZOS)
        img.paste(avatar_img, (8, 8))
        img.save(full_image_path)

        if member_avatar_path.exists():
            self.delete_image(member_avatar_path)
    
    def delete_image(self, full_image_path):
        full_image_path.unlink()
