import os
import shutil

# ==========配置区==========
BASE_DIR = r"D:\BC101\Examples"
# 模板章节
TEMPLATE_CHAPTER = "L08"
# 模板项目名称
TEMPLATE_PROJECT = "L08_02_DRAW_LINE"
# 模板完整路径
SRC_TEMPLATE = os.path.join(BASE_DIR, TEMPLATE_CHAPTER, TEMPLATE_PROJECT)
PLACEHOLDER = TEMPLATE_PROJECT

def main():
    new_proj = input("输入新项目名称(例:L09_01_DRAW_LINE): ").strip()
    if not new_proj:
        print("项目名不能为空")
        return

    # 按下划线分割，取第一段作为外层目录，兼容 L100_01_XXX
    parts = new_proj.split("_", 1)
    if len(parts) < 2:
        print("项目名称格式错误，示例：L09_01_DRAW_LINE，需要包含下划线")
        return
    outer_dir = parts[0]

    src = SRC_TEMPLATE
    outer_path = os.path.join(BASE_DIR, outer_dir)
    dst = os.path.join(outer_path, new_proj)

    if not os.path.isdir(src):
        print(f"模板目录不存在: {src}")
        return
    if os.path.exists(dst):
        print(f"目标项目已存在: {dst}")
        return

    # 创建外层Lxx目录（不存在则新建）
    os.makedirs(outer_path, exist_ok=True)

    # 复制整个模板目录
    shutil.copytree(src, dst)
    
    # 章节字符处理
    old_chapter_part = f"\\\\{TEMPLATE_CHAPTER}\\\\"
    new_chapter_part = f"\\\\{outer_dir}\\\\"

    # 遍历全部json/cpp文件，替换占位符
    for root, dirs, files in os.walk(dst):
        for filename in files:
            filepath = os.path.join(root, filename)
            if filename.lower().endswith((".json", ".cpp")):
                with open(filepath, "r", encoding="utf-8") as f:
                    text = f.read()
                text = text.replace(PLACEHOLDER, new_proj).replace(old_chapter_part, new_chapter_part )
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(text)

    # 重命名cpp文件
    old_cpp = os.path.join(dst, f"{PLACEHOLDER}.cpp")
    new_cpp = os.path.join(dst, f"{new_proj}.cpp")
    if os.path.exists(old_cpp):
        os.rename(old_cpp, new_cpp)

    print("创建完成")
    print(f"源模板: {src}")
    print(f"外层目录: {outer_path}")
    print(f"新项目: {dst}")
    print(f"源码文件: {new_cpp}")

if __name__ == "__main__":
    main()
