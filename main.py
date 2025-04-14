from tqdm import tqdm
import argparse

# 检查URL是否以extensions中的后缀结尾（不区分大小写）
def is_ext_url(url, extensions):
    """精确检测净化后的URL是否以指定扩展名结尾"""
    purified_url = clean_params(url).lower()
    return any(purified_url.endswith(f".{ext.lower()}") for ext in extensions)

# 去除URL中?及之后的参数
def clean_params(url):
    """净化URL：移除?后的参数并去除首尾空格"""
    return url.split('?', 1)[0].strip()

def main():

    #解析命令行参数
    parser = argparse.ArgumentParser(description="URL处理工具")
    parser.add_argument("--ext_delete", nargs="+", type=str, help="需要过滤的拓展名列表(如 js css php)")
    parser.add_argument("--duplicate", help="去除重复项", action="store_true")
    args = parser.parse_args()

    #读文件urls.txt
    with open('urls.txt','r') as file:
        lines = file.readlines()

    # 定义一个set(),用来去重
    seen = set() if args.duplicate else None
    # 用来存储url
    unique_lines = []
    # 用来记录空行,重复项,特定后缀的url行数
    stats = {
        'empty': 0,
        'duplicate': 0,
        'ext': 0
    }

    with tqdm(total=len(lines), desc="处理进度", unit="行") as pbar:
        for line in lines:
            # 过滤空行
            if not line:
                stats['empty'] += 1
                pbar.update(1)
                continue

            # 去除特定后缀url
            if args.ext_delete and is_ext_url(line, args.ext_delete):
                stats['ext'] += 1
                pbar.update(1)
                continue

            # 检测是否之前出现过这个url(仅当启用--duplicate时)
            if args.duplicate:
                # 如果之前出现过,则continue
                if line in seen:
                    stats['duplicate'] += 1 #用来记录出现过的url
                    pbar.update(1)
                    continue
                # 如果没有出现过,则加到seen这个set()里面
                seen.add(line)

            # 存到最终的列表里面
            unique_lines.append(line)
            pbar.update(1)

    with open('urls.txt','w') as file:
        file.writelines(unique_lines)

    # print(f"去重完成, 原数量:{len(lines)}, 现有数量:{len(unique_lines)}, 删除了{skiped}个")
    # 打印结果
    print(f"\n=== 处理结果 ===")
    print(f"原始行数: {len(lines)}")
    print(f"保留行数: {len(unique_lines)}")
    print(f"移除空行: {stats['empty']}")
    if args.ext_delete:
        exts = ",".join(args.ext_delete)
        print(f"移除 {exts} 后缀url行数: {stats['ext']}")
    if args.duplicate:
        print(f"移除重复url行数: {stats['duplicate']}")
    print(f"总计处理: {sum(stats.values())}")


if __name__ == '__main__':
    main()