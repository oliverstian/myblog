from io import BytesIO

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image, ImageDraw, ImageFont


class WatermarkStorage(FileSystemStorage):  # FileSystemStorage实现了基本的本地文件存储
    def save(self, name, content, max_length=None):
        """
        上传文件的时候执行，比如CKeditor中需要用到某张图片时，需要先选中本地图片，
        然后上传到django服务器，再能插入文中使用。这个上传图片的过程就需要执行save。
        content指的就是上传的那个文件，content_type就是文件类型加后缀
        """
        # 处理逻辑
        if hasattr(content, "content_type"):  # 上传头像时没有content_type属性
            if 'image' in content.content_type:
                # 加水印
                image = self.watermark_with_text(content, 'olivertian.com', 'red')
                content = self.convert_image_to_file(image, name)

        return super().save(name, content, max_length=max_length)

    def convert_image_to_file(self, image, name):
        temp = BytesIO()
        image.save(temp, format='PNG')
        file_size = temp.tell()
        return InMemoryUploadedFile(temp, None, name, 'image/png', file_size, None)

    def watermark_with_text(self, file_obj, text, color, fontfamily=None):
        image = Image.open(file_obj).convert('RGBA')
        draw = ImageDraw.Draw(image)
        width, height = image.size
        margin = 10
        if fontfamily:
            font = ImageFont.truetype(fontfamily, int(height / 20))
        else:
            font = None
        textWidth, textHeight = draw.textsize(text, font)
        x = (width - textWidth - margin) / 2  # 计算横轴位置
        y = height - textHeight - margin  # 计算纵轴位置
        draw.text((x, y), text, color, font)

        return image
