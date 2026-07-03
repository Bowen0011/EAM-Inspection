"""
图片水印工具
使用 Pillow 库在图片右下角叠加水印文字
格式：设备编号_提交时间
"""
from PIL import Image, ImageDraw, ImageFont
import os


def add_watermark(input_path: str, output_path: str, watermark_text: str) -> str:
    """
    在图片右下角叠加水印文字
    :param input_path: 输入图片路径
    :param output_path: 输出图片路径
    :param watermark_text: 水印文字内容（格式：设备编号_提交时间）
    :return: 输出图片路径
    """
    try:
        # 打开图片
        img = Image.open(input_path).convert("RGBA")
    except Exception as e:
        raise RuntimeError(f"无法打开图片: {e}")

    # 创建水印图层
    watermark_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark_layer)

    # 尝试加载字体，如果系统没有指定字体则使用默认
    font_size = max(int(img.width * 0.035), 20)  # 根据图片宽度动态调整字体大小
    try:
        # Windows 常见中文字体路径
        font_paths = [
            "C:/Windows/Fonts/simhei.ttf",       # SimHei
            "C:/Windows/Fonts/msyh.ttc",          # Microsoft YaHei
            "C:/Windows/Fonts/simsun.ttc",        # SimSun
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",  # Linux CJK
        ]
        font = None
        for fp in font_paths:
            if os.path.exists(fp):
                font = ImageFont.truetype(fp, font_size)
                break
        if font is None:
            font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()

    # 计算水印位置（右下角，留出边距）
    margin = int(font_size * 0.5)
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = img.width - text_width - margin
    y = img.height - text_height - margin

    # 绘制半透明白色文字背景（提高可读性）
    background_bbox = (x - 5, y - 5, x + text_width + 10, y + text_height + 10)
    draw.rectangle(background_bbox, fill=(0, 0, 0, 80))

    # 绘制水印文字（白色，半透明）
    draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 200))

    # 合并图层
    watermarked_img = Image.alpha_composite(img, watermark_layer)

    # 转换为 RGB 保存（去除Alpha通道以兼容JPEG）
    if watermarked_img.mode == "RGBA":
        watermarked_img = watermarked_img.convert("RGB")

    # 保存图片
    watermarked_img.save(output_path, quality=95)

    return output_path