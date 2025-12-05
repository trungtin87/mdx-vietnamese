"""
Script tự động dịch các file MDX từ tiếng Anh sang tiếng Việt
Sử dụng từ điển dịch và giữ nguyên cấu trúc MDX, code blocks, JSX
"""

import os
import re
from pathlib import Path
from typing import Dict, List

# Từ điển dịch chi tiết
TRANSLATIONS: Dict[str, str] = {
    # Tiêu đề chính
    "What is MDX?": "MDX là gì?",
    "Getting started": "Bắt đầu",
    "Using MDX": "Sử dụng MDX",
    "Extending MDX": "Mở rộng MDX",
    "Troubleshooting MDX": "Khắc phục sự cố MDX",
    
    # Các phần trong tài liệu
    "Contents": "Nội dung",
    "Prerequisites": "Điều kiện tiên quyết",
    "Further reading": "Đọc thêm",
    "Table of contents": "Mục lục",
    
    # Cụm từ phổ biến
    "This article explains": "Bài viết này giải thích",
    "This guide shows": "Hướng dẫn này cho thấy",
    "See also": "Xem thêm",
    "For example": "Ví dụ",
    "Note": "Lưu ý",
    "Warning": "Cảnh báo",
    
    # MDX specific
    "Markdown for the component era": "Markdown cho kỷ nguyên component",
    "MDX syntax": "Cú pháp MDX",
    "How MDX works": "MDX hoạt động như thế nào",
    "MDX content": "Nội dung MDX",
    "MDX provider": "MDX provider",
    
    # Components & Props
    "Components": "Components",
    "Props": "Props",
    "Layout": "Layout",
    "Expressions": "Biểu thức",
    "Interleaving": "Xen kẽ",
    
    # Actions
    "Continue reading": "Đọc tiếp",
    "Read more": "Đọc thêm",
    "Learn more": "Tìm hiểu thêm",
    "Get started": "Bắt đầu",
    "Play": "Chơi thử",
}

def translate_heading(line: str) -> str:
    """Dịch các heading markdown"""
    match = re.match(r'^(#{1,6})\s+(.+)$', line) 
    if match:
        hashes, text = match.groups()
        for en, vi in TRANSLATIONS.items():
            if text.strip() == en:
                return f"{hashes} {vi}"
    return line

def should_skip_line(line: str) -> bool:
    """Kiểm tra xem dòng có nên bỏ qua dịch không"""
    # Bỏ qua code blocks
    if line.strip().startswith('```') or line.strip().startswith('~~~'):
        return True
    # Bỏ qua imports/exports
    if line.strip().startswith(('import ', 'export ')):
        return True
    # Bỏ qua JSX tags
    if re.match(r'^\s*<[^>]+>\s*$', line):
        return True
    # Bỏ qua links
    if line.strip().startswith('[') and ']:' in line:
        return True
    return False

def translate_line(line: str, in_code_block: bool) -> str:
    """Dịch một dòng văn bản"""
    if in_code_block or should_skip_line(line):
        return line
    
    # Dịch heading
    if line.strip().startswith('#'):
        return translate_heading(line)
    
    # Dịch các cụm từ trong văn bản
    result = line
    for en, vi in TRANSLATIONS.items():
        # Chỉ dịch nếu là whole word
        result = re.sub(r'\b' + re.escape(en) + r'\b', vi, result)
    
    return result

def translate_mdx_file(file_path: Path) -> bool:
    """Dịch một file MDX"""
    print(f"Đang dịch: {file_path.relative_to(file_path.parents[1])}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        translated_lines = []
        in_code_block = False
        code_fence = None
        
        for line in lines:
            # Theo dõi code blocks
            stripped = line.strip()
            if stripped.startswith('```') or stripped.startswith('~~~'):
                if not in_code_block:
                    in_code_block = True
                    code_fence = stripped[:3]
                elif stripped.startswith(code_fence):
                    in_code_block = False
                    code_fence = None
            
            # Dịch dòng
            translated_line = translate_line(line, in_code_block)
            translated_lines.append(translated_line)
        
        # Ghi file
        with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
            f.writelines(translated_lines)
        
        print(f"  ✓ Hoàn thành")
        return True
        
    except Exception as e:
        print(f"  ✗ Lỗi: {e}")
        return False

def main():
    """Hàm chính"""
    docs_dir = Path(r"e:\ubuntu\Docker\mdx-vietnamese\docs")
    
    # Tìm tất cả file MDX
    mdx_files = sorted(docs_dir.rglob("*.mdx"))
    
    print(f"\n{'='*70}")
    print(f"Tìm thấy {len(mdx_files)} file MDX")
    print(f"{'='*70}\n")
    
    # Danh sách file đã dịch (bỏ qua)
    skip_files = {
        'extending-mdx.mdx',
        'index.mdx',  # trong docs/docs
        '404.mdx',
        'playground.mdx',
    }
    
    success_count = 0
    skipped_count = 0
    
    for mdx_file in mdx_files:
        # Bỏ qua file đã dịch
        if mdx_file.name in skip_files:
            print(f"Bỏ qua (đã dịch): {mdx_file.relative_to(docs_dir)}")
            skipped_count += 1
            continue
        
        if translate_mdx_file(mdx_file):
            success_count += 1
    
    print(f"\n{'='*70}")
    print(f"Kết quả:")
    print(f"  - Đã dịch: {success_count} file")
    print(f"  - Đã bỏ qua: {skipped_count} file")
    print(f"  - Tổng cộng: {len(mdx_files)} file")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
