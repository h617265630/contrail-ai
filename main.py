import argparse
import json
from pathlib import Path

from learnpathly_langchain.service import generate_learning_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate learning path with user input")
    parser.add_argument(
        "--query",
        type=str,
        default="我想系统学习 LLM，并能做项目",
        help="真实用户学习目标输入",
    )
    parser.add_argument(
        "--out",
        type=str,
        default="",
        help="可选：将生成结果保存为本地 JSON 文件路径（例如 outputs/result.json）",
    )
    args = parser.parse_args()

    response = generate_learning_path(args.query)
    output_json = response.model_dump_json(indent=2, ensure_ascii=False)
    print(output_json)

    if args.out:
        out_path = Path(args.out)
        if out_path.parent:
            out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output_json, encoding="utf-8")
