"""
Script để dịch tất cả các file MDX từ tiếng Anh sang tiếng Việt
"""

import os
import re
from pathlib import Path

# Từ điển dịch các cụm từ thường gặp
TRANSLATIONS = {
    # Headings và titles
    "What is MDX?": "MDX là gì?",
    "Getting started": "Bắt đầu",
    "Get started": "Bắt đầu",
    "Using MDX": "Sử dụng MDX",
    "Extending MDX": "Mở rộng MDX",
    "Troubleshooting MDX": "Khắc phục sự cố MDX",
    "Docs": "Tài liệu",
    "Guides": "Hướng dẫn",
    "Blog": "Blog",
    "Community": "Cộng đồng",
    "Packages": "Gói",
    "Migrating": "Di chuyển",
    "Playground": "Sân chơi",
    
    # Common phrases
    "Continue reading": "Đọc tiếp",
    "Read more": "Đọc thêm",
    "Learn more": "Tìm hiểu thêm",
    "Get started": "Bắt đầu",
    "Further reading": "Đọc thêm",
    "Prerequisites": "Điều kiện tiên quyết",
    "Contents": "Nội dung",
    "Table of contents": "Mục lục",
    
    # MDX specific
    "Markdown for the component era": "Markdown cho kỷ nguyên component",
    "component era": "kỷ nguyên component",
    "What does MDX do?": "MDX làm gì?",
    "MDX in short": "MDX tóm tắt",
    "New: MDX 3!": "Mới: MDX 3!",
    
    # Technical terms (keep some in English with Vietnamese explanation)
    "Components & plugins": "Components & plugins",
    "List of components": "Danh sách components",
    "List of plugins": "Danh sách plugins",
    "Using plugins": "Sử dụng plugins",
    "Creating plugins": "Tạo plugins",
    
    # Common sentences
    "This article explains": "Bài viết này giải thích",
    "These docs explain": "Tài liệu này giải thích",
    "See also": "Xem thêm",
    "Note": "Lưu ý",
    "Warning": "Cảnh báo",
    "Example": "Ví dụ",
    "Examples": "Ví dụ",
}

def translate_mdx_content(content):
    """
    Dịch nội dung MDX từ tiếng Anh sang tiếng Việt
    Giữ nguyên code blocks, JSX, imports, exports
    """
    # Áp dụng các bản dịch
    for en, vi in TRANSLATIONS.items():
        # Dịch trong headings
        content = re.sub(rf'^(#{1,6})\s+{re.escape(en)}\s*$', rf'\1 {vi}', content, flags=re.MULTILINE)
        # Dịch trong text thường
        content = content.replace(en, vi)
    
    return content

def process_mdx_file(file_path):
    """Xử lý một file MDX"""
    print(f"Đang xử lý: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Dịch nội dung
        translated = translate_mdx_content(content)
        
        # Ghi đè file gốc
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(translated)
        
        print(f"✓ Đã dịch: {file_path}")
        return True
    except Exception as e:
        print(f"✗ Lỗi khi xử lý {file_path}: {e}")
        return False

def main():
    """Hàm chính"""
    docs_dir = Path(r"e:\ubuntu\Docker\mdx-vietnamese\docs")
    
    # Tìm tất cả file MDX
    mdx_files = list(docs_dir.rglob("*.mdx"))
    
    print(f"Tìm thấy {len(mdx_files)} file MDX")
    print("=" * 60)
    
    success_count = 0
    for mdx_file in mdx_files:
        if process_mdx_file(mdx_file):
            success_count += 1
    
    print("=" * 60)
    print(f"Hoàn thành: {success_count}/{len(mdx_files)} file")

if __name__ == "__main__":
    main()
