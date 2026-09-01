"""
Script sinh file Icon (.ico & .png) chất lượng cao đa kích thước cho ứng dụng Visual AlgoStudio.
"""
import os
from PIL import Image, ImageDraw

def create_app_icon():
    os.makedirs("assets", exist_ok=True)
    size = (512, 512)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Vẽ nền tròn bo góc / Gradient nền tối chuyên nghiệp
    bg_margin = 16
    draw.rounded_rectangle(
        [bg_margin, bg_margin, size[0] - bg_margin, size[1] - bg_margin],
        radius=110,
        fill="#0f172a",
        outline="#38bdf8",
        width=10
    )

    # 2. Vẽ biểu tượng Cây Nhị Phân (Binary Tree) ở nửa trên
    # Cạnh nối (Edges)
    root_pt = (256, 120)
    left_pt = (140, 230)
    right_pt = (372, 230)
    
    draw.line([root_pt, left_pt], fill="#38bdf8", width=12)
    draw.line([root_pt, right_pt], fill="#0284c7", width=12)

    # Nút cây (Tree Nodes)
    r = 42
    # Nút Root (Cyan)
    draw.ellipse([root_pt[0]-r, root_pt[1]-r, root_pt[0]+r, root_pt[1]+r], fill="#38bdf8", outline="#ffffff", width=6)
    # Nút Left (Amber)
    draw.ellipse([left_pt[0]-r, left_pt[1]-r, left_pt[0]+r, left_pt[1]+r], fill="#fbbf24", outline="#ffffff", width=6)
    # Nút Right (Emerald)
    draw.ellipse([right_pt[0]-r, right_pt[1]-r, right_pt[0]+r, right_pt[1]+r], fill="#34d399", outline="#ffffff", width=6)

    # 3. Vẽ biểu tượng Cột Sắp Xếp (Sorting Bars) ở nửa dưới
    bars = [
        (80, 430, 48, 110, "#0284c7"),
        (148, 430, 48, 170, "#38bdf8"),
        (216, 430, 48, 80,  "#fbbf24"),
        (284, 430, 48, 150, "#f87171"),
        (352, 430, 48, 200, "#34d399"),
        (420, 430, 48, 230, "#a855f7")
    ]
    for x, base_y, bw, bh, color in bars:
        draw.rounded_rectangle([x, base_y - bh, x + bw, base_y], radius=8, fill=color, outline="#ffffff", width=3)

    # 4. Lưu ra file PNG và file ICO đầy đủ các kích thước (16, 32, 48, 64, 128, 256)
    png_path = os.path.join("assets", "app_icon.png")
    ico_path = os.path.join("assets", "app_icon.ico")
    
    img.save(png_path, format="PNG")
    img.save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    
    print(f"✅ Đã tạo thành công Icon ứng dụng tại:\n   - {ico_path}\n   - {png_path}")

if __name__ == "__main__":
    create_app_icon()