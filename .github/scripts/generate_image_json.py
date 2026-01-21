import os
import json

def generate_json():
    # 1. 配置文件夹路径
    # 注意：GitHub Actions 默认在仓库根目录运行，这里直接写文件夹名即可
    image_folder = 'leviicons'
    output_filename = 'levi.icons.json'

    # 2. 获取 GitHub 环境变量
    # 只有在 GitHub Actions 环境下才有这个变量 (格式: 用户名/仓库名)
    repo = os.environ.get('GITHUB_REPOSITORY')
    
    if not repo:
        print("❌ 错误: 未检测到 GITHUB_REPOSITORY 环境变量，请确保在 GitHub Actions 中运行。")
        return

    # 3. 初始化 JSON 数据结构
    json_data = {
        "name": "Levi图标订阅",
        "description": "收集一些自己常用的图标,欢迎大家引用,如您有新的软件图标可以在issue中说明.",
        "icons": []
    }

    # 4. 检查图片文件夹是否存在
    if not os.path.exists(image_folder):
        print(f"❌ 错误: 找不到文件夹 '{image_folder}'，请检查仓库结构。")
        return

    # 5. 文件名排序 保证 JSON 顺序稳定，避免 Git 提交历史混乱
    files = sorted(os.listdir(image_folder))

    count = 0
    for filename in files:
        if filename.endswith(".png"):
            # 拼接路径
            image_path = f"{image_folder}/{filename}"
            # 生成 GitHub Raw 链接
            raw_url = f"https://raw.githubusercontent.com/{repo}/main/{image_path}"
            
            icon_data = {
                "name": filename, 
                "url": raw_url
            }
            json_data["icons"].append(icon_data)
            count += 1

    # 6. 输出 JSON 文件到根目录
    with open(output_filename, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=2)

    print(f"✅ 成功生成配置！")
    print(f"📂 仓库: {repo}")
    print(f"🖼️ 图标数量: {count}")
    print(f"💾 输出文件: {output_filename}")

if __name__ == "__main__":
    generate_json()
