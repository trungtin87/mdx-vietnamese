"""
Script tự động dịch tất cả các file MDX từ tiếng Anh sang tiếng Việt
Giữ nguyên cấu trúc MDX, code blocks, JSX, imports, exports
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Từ điển dịch toàn diện
TRANSLATIONS = {
    # === TIÊU ĐỀ CHÍNH ===
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
    "Projects": "Dự án",
    "Support": "Hỗ trợ",
    "About": "Giới thiệu",
    "Contribute": "Đóng góp",
    "Sponsor": "Tài trợ",
    
    # === CÁC PHẦN TRONG TÀI LIỆU ===
    "Contents": "Nội dung",
    "Table of contents": "Mục lục",
    "Prerequisites": "Điều kiện tiên quyết",
    "Further reading": "Đọc thêm",
    "Introduction": "Giới thiệu",
    "Overview": "Tổng quan",
    "Examples": "Ví dụ",
    "Example": "Ví dụ",
    "Usage": "Sử dụng",
    "Installation": "Cài đặt",
    "Configuration": "Cấu hình",
    
    # === CỤM TỪ PHỔ BIẾN ===
    "This article explains": "Bài viết này giải thích",
    "This guide shows": "Hướng dẫn này cho thấy",
    "This page explains": "Trang này giải thích",
    "This page lists": "Trang này liệt kê",
    "These docs explain": "Tài liệu này giải thích",
    "These pages explain": "Các trang này giải thích",
    "See also": "Xem thêm",
    "For example": "Ví dụ",
    "For instance": "Chẳng hạn",
    "In other words": "Nói cách khác",
    "That is": "Tức là",
    "Note": "Lưu ý",
    "Warning": "Cảnh báo",
    "Important": "Quan trọng",
    "Tip": "Mẹo",
    
    # === HÀNH ĐỘNG ===
    "Continue reading": "Đọc tiếp",
    "Read more": "Đọc thêm",
    "Learn more": "Tìm hiểu thêm",
    "See more": "Xem thêm",
    "Click here": "Nhấp vào đây",
    "Try it": "Thử ngay",
    "Play": "Chơi thử",
    
    # === MDX SPECIFIC ===
    "Markdown for the component era": "Markdown cho kỷ nguyên component",
    "component era": "kỷ nguyên component",
    "What does MDX do?": "MDX làm gì?",
    "MDX in short": "MDX tóm tắt",
    "How MDX works": "MDX hoạt động như thế nào",
    "MDX content": "Nội dung MDX",
    "MDX provider": "MDX provider",
    "MDX syntax": "Cú pháp MDX",
    "MDX format": "Định dạng MDX",
    
    # === COMPONENTS & TECHNICAL ===
    "Components": "Components",
    "Props": "Props",
    "Layout": "Layout",
    "Expressions": "Biểu thức",
    "Interleaving": "Xen kẽ",
    "List of components": "Danh sách components",
    "List of plugins": "Danh sách plugins",
    "Using plugins": "Sử dụng plugins",
    "Creating plugins": "Tạo plugins",
    
    # === CÂU THÔNG DỤNG ===
    "Here you can": "Tại đây bạn có thể",
    "You can": "Bạn có thể",
    "We recommend": "Chúng tôi khuyên bạn nên",
    "It is recommended": "Nên",
    "Please read": "Vui lòng đọc",
    "Please note": "Vui lòng lưu ý",
    "Make sure": "Đảm bảo",
    "Don't forget": "Đừng quên",
    
    # === COMMUNITY ===
    "community projects": "các dự án cộng đồng",
    "where to get help": "nơi nhận trợ giúp",
    "how to contribute": "cách đóng góp",
    "code of conduct": "quy tắc ứng xử",
    "Asking quality questions": "Đặt câu hỏi chất lượng",
    
    # === COMMON PHRASES ===
    "by default": "theo mặc định",
    "for more information": "để biết thêm thông tin",
    "as follows": "như sau",
    "in this case": "trong trường hợp này",
    "for now": "hiện tại",
    "at the moment": "tại thời điểm này",
    "in the future": "trong tương lai",
    "as well": "cũng như",
    "such as": "chẳng hạn như",
    "like so": "như sau",
    
    # === VERBS ===
    "explains": "giải thích",
    "shows": "cho thấy",
    "demonstrates": "minh họa",
    "describes": "mô tả",
    "provides": "cung cấp",
    "allows": "cho phép",
    "enables": "cho phép",
    "supports": "hỗ trợ",
    "requires": "yêu cầu",
    "expects": "mong đợi",
}

# Các pattern cần bỏ qua khi dịch
SKIP_PATTERNS = [
    r'^```',  # Code fence
    r'^~~~',  # Alternative code fence
    r'^import\s',  # Import statements
    r'^export\s',  # Export statements
    r'^\s*<[A-Z]',  # JSX components
    r'^\s*</[A-Z]',  # JSX closing tags
    r'^\[.+\]:',  # Link definitions
    r'^\s*\*\s*\[',  # List items with links (usually references)
    r'^\s*{/\*',  # JSX comments
    r'^\s*\*/}',  # JSX comment end
]

def should_skip_translation(line: str) -> bool:
    """Kiểm tra xem dòng có nên bỏ qua dịch không"""
    stripped = line.strip()
    
    # Bỏ qua dòng trống
    if not stripped:
        return True
    
    # Kiểm tra các pattern
    for pattern in SKIP_PATTERNS:
        if re.match(pattern, stripped):
            return True
    
    return False

def translate_text(text: str) -> str:
    """Dịch văn bản sử dụng từ điển"""
    result = text
    
    # Sắp xếp theo độ dài giảm dần để dịch cụm từ dài trước
    sorted_translations = sorted(TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)
    
    for english, vietnamese in sorted_translations:
        # Dịch whole word/phrase
        # Case sensitive cho các từ viết hoa
        if english[0].isupper():
            result = re.sub(r'\b' + re.escape(english) + r'\b', vietnamese, result)
        else:
            # Case insensitive cho các từ thường
            result = re.sub(r'\b' + re.escape(english) + r'\b', vietnamese, result, flags=re.IGNORECASE)
    
    return result

def translate_mdx_file(file_path: Path, dry_run: bool = False) -> Tuple[bool, int]:
    """
    Dịch một file MDX
    
    Returns:
        (success, lines_translated)
    """
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Đang xử lý: {file_path.relative_to(file_path.parents[2])}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        translated_lines = []
        in_code_block = False
        code_fence = None
        lines_translated = 0
        
        for i, line in enumerate(lines, 1):
            # Theo dõi code blocks
            stripped = line.strip()
            if stripped.startswith('```') or stripped.startswith('~~~'):
                if not in_code_block:
                    in_code_block = True
                    code_fence = stripped[:3]
                elif stripped.startswith(code_fence):
                    in_code_block = False
                    code_fence = None
                translated_lines.append(line)
                continue
            
            # Bỏ qua nếu trong code block hoặc là dòng đặc biệt
            if in_code_block or should_skip_translation(line):
                translated_lines.append(line)
                continue
            
            # Dịch dòng
            original_line = line
            translated_line = translate_text(line)
            
            if translated_line != original_line:
                lines_translated += 1
                if dry_run:
                    print(f"  Line {i}: {original_line.strip()[:60]}...")
                    print(f"       → {translated_line.strip()[:60]}...")
            
            translated_lines.append(translated_line)
        
        # Ghi file nếu không phải dry run
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
                f.writelines(translated_lines)
            print(f"  ✓ Đã dịch {lines_translated} dòng")
        else:
            print(f"  → Sẽ dịch {lines_translated} dòng")
        
        return True, lines_translated
        
    except Exception as e:
        print(f"  ✗ Lỗi: {e}")
        return False, 0

def main():
    """Hàm chính"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Dịch các file MDX sang tiếng Việt')
    parser.add_argument('--dry-run', action='store_true', help='Chỉ xem trước, không ghi file')
    parser.add_argument('--file', type=str, help='Dịch một file cụ thể')
    parser.add_argument('--skip-translated', action='store_true', default=True, 
                       help='Bỏ qua các file đã dịch')
    args = parser.parse_args()
    
    docs_dir = Path(r"e:\ubuntu\Docker\mdx-vietnamese\docs")
    
    # Danh sách file đã dịch (bỏ qua)
    skip_files = {
        'extending-mdx.mdx',
        'what-is-mdx.mdx',
        '404.mdx',
        'playground.mdx',
    } if args.skip_translated else set()
    
    # Nếu chỉ định file cụ thể
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            file_path = docs_dir / args.file
        
        if file_path.exists():
            translate_mdx_file(file_path, args.dry_run)
        else:
            print(f"Không tìm thấy file: {args.file}")
        return
    
    # Tìm tất cả file MDX
    mdx_files = sorted(docs_dir.rglob("*.mdx"))
    
    print(f"\n{'='*80}")
    print(f"{'[CHẾ ĐỘ XEM TRƯỚC] ' if args.dry_run else ''}DỊCH CÁC FILE MDX")
    print(f"{'='*80}")
    print(f"Tìm thấy {len(mdx_files)} file MDX")
    print(f"Bỏ qua {len(skip_files)} file đã dịch")
    print(f"{'='*80}\n")
    
    success_count = 0
    skipped_count = 0
    total_lines_translated = 0
    
    for mdx_file in mdx_files:
        # Bỏ qua file đã dịch
        if mdx_file.name in skip_files:
            print(f"⊘ Bỏ qua (đã dịch): {mdx_file.relative_to(docs_dir)}")
            skipped_count += 1
            continue
        
        success, lines_translated = translate_mdx_file(mdx_file, args.dry_run)
        if success:
            success_count += 1
            total_lines_translated += lines_translated
    
    print(f"\n{'='*80}")
    print(f"KẾT QUẢ:")
    print(f"  - Đã xử lý: {success_count} file")
    print(f"  - Đã bỏ qua: {skipped_count} file")
    print(f"  - Tổng số dòng đã dịch: {total_lines_translated}")
    print(f"  - Tổng cộng: {len(mdx_files)} file")
    if args.dry_run:
        print(f"\n  ⚠️  Đây là chế độ xem trước. Chạy lại không có --dry-run để thực sự dịch.")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
