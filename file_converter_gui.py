"""
Script chuyển đổi hàng loạt giữa MD, MDX và HTML với giao diện đồ họa
Hỗ trợ: MD ↔ MDX ↔ HTML
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
from typing import List, Tuple
import re
import markdown
from datetime import datetime

class FileConverter:
    """Class xử lý chuyển đổi file"""
    
    @staticmethod
    def md_to_mdx(content: str, filename: str) -> str:
        """Chuyển đổi MD sang MDX"""
        # Thêm metadata MDX nếu chưa có
        if not content.startswith('export'):
            metadata = f"""export const info = {{
  modified: new Date('{datetime.now().strftime('%Y-%m-%d')}'),
  published: new Date('{datetime.now().strftime('%Y-%m-%d')}')
}}

"""
            content = metadata + content
        
        return content
    
    @staticmethod
    def mdx_to_md(content: str) -> str:
        """Chuyển đổi MDX sang MD - loại bỏ JSX và exports"""
        # Loại bỏ export statements
        content = re.sub(r'^export\s+.*$', '', content, flags=re.MULTILINE)
        
        # Loại bỏ import statements
        content = re.sub(r'^import\s+.*$', '', content, flags=re.MULTILINE)
        
        # Loại bỏ JSX components (cơ bản)
        content = re.sub(r'<[A-Z][^>]*>.*?</[A-Z][^>]*>', '', content, flags=re.DOTALL)
        content = re.sub(r'<[A-Z][^/>]*\s*/>', '', content)
        
        # Loại bỏ JSX comments
        content = re.sub(r'\{/\*.*?\*/\}', '', content, flags=re.DOTALL)
        
        # Loại bỏ dòng trống thừa
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        return content.strip()
    
    @staticmethod
    def md_to_html(content: str, filename: str) -> str:
        """Chuyển đổi MD sang HTML"""
        # Chuyển đổi markdown sang HTML
        html_content = markdown.markdown(
            content,
            extensions=['extra', 'codehilite', 'toc']
        )
        
        # Tạo HTML hoàn chỉnh
        html_template = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{filename}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        pre code {{
            background: none;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #ddd;
            margin: 0;
            padding-left: 20px;
            color: #666;
        }}
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        img {{
            max-width: 100%;
            height: auto;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #f4f4f4;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
        
        return html_template
    
    @staticmethod
    def html_to_md(content: str) -> str:
        """Chuyển đổi HTML sang MD (cơ bản)"""
        # Loại bỏ HTML tags (cơ bản)
        # Chuyển đổi headings
        content = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', content, flags=re.DOTALL)
        content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', content, flags=re.DOTALL)
        content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', content, flags=re.DOTALL)
        content = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1', content, flags=re.DOTALL)
        content = re.sub(r'<h5[^>]*>(.*?)</h5>', r'##### \1', content, flags=re.DOTALL)
        content = re.sub(r'<h6[^>]*>(.*?)</h6>', r'###### \1', content, flags=re.DOTALL)
        
        # Chuyển đổi paragraphs
        content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', content, flags=re.DOTALL)
        
        # Chuyển đổi links
        content = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', content, flags=re.DOTALL)
        
        # Chuyển đổi code
        content = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', content, flags=re.DOTALL)
        content = re.sub(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', r'```\n\1\n```', content, flags=re.DOTALL)
        
        # Chuyển đổi emphasis
        content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', content, flags=re.DOTALL)
        content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', content, flags=re.DOTALL)
        
        # Loại bỏ các tags còn lại
        content = re.sub(r'<[^>]+>', '', content)
        
        # Loại bỏ dòng trống thừa
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        return content.strip()


class ConverterGUI:
    """Giao diện chuyển đổi file"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Chuyển đổi MD/MDX/HTML - Hàng loạt")
        self.root.geometry("900x700")
        
        # Biến
        self.source_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.conversion_type = tk.StringVar(value="md_to_mdx")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Thiết lập giao diện"""
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Tiêu đề
        title = ttk.Label(main_frame, text="CHUYỂN ĐỔI FILE HÀNG LOẠT", 
                         font=('Arial', 16, 'bold'))
        title.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Thư mục nguồn
        ttk.Label(main_frame, text="Thư mục nguồn:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.source_dir, width=50).grid(row=1, column=1, pady=5)
        ttk.Button(main_frame, text="Chọn", command=self.browse_source).grid(row=1, column=2, padx=5)
        
        # Thư mục đích
        ttk.Label(main_frame, text="Thư mục đích:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_dir, width=50).grid(row=2, column=1, pady=5)
        ttk.Button(main_frame, text="Chọn", command=self.browse_output).grid(row=2, column=2, padx=5)
        
        # Loại chuyển đổi
        ttk.Label(main_frame, text="Loại chuyển đổi:").grid(row=3, column=0, sticky=tk.W, pady=5)
        
        conversion_frame = ttk.Frame(main_frame)
        conversion_frame.grid(row=3, column=1, columnspan=2, sticky=tk.W, pady=5)
        
        conversions = [
            ("MD → MDX", "md_to_mdx"),
            ("MDX → MD", "mdx_to_md"),
            ("MD → HTML", "md_to_html"),
            ("MDX → HTML", "mdx_to_html"),
            ("HTML → MD", "html_to_md"),
            ("HTML → MDX", "html_to_mdx"),
        ]
        
        for i, (text, value) in enumerate(conversions):
            ttk.Radiobutton(conversion_frame, text=text, variable=self.conversion_type, 
                           value=value).grid(row=i//3, column=i%3, sticky=tk.W, padx=10)
        
        # Nút chuyển đổi
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="🔄 Chuyển đổi", command=self.convert_files,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Xóa log", command=self.clear_log).pack(side=tk.LEFT, padx=5)
        
        # Log
        ttk.Label(main_frame, text="Nhật ký:").grid(row=5, column=0, sticky=tk.W, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(main_frame, width=100, height=25, 
                                                  font=('Consolas', 9))
        self.log_text.grid(row=6, column=0, columnspan=3, pady=5)
        
        # Thanh trạng thái
        self.status_var = tk.StringVar(value="Sẵn sàng")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
    def browse_source(self):
        """Chọn thư mục nguồn"""
        directory = filedialog.askdirectory(title="Chọn thư mục nguồn")
        if directory:
            self.source_dir.set(directory)
            self.log(f"📁 Đã chọn thư mục nguồn: {directory}")
            
    def browse_output(self):
        """Chọn thư mục đích"""
        directory = filedialog.askdirectory(title="Chọn thư mục đích")
        if directory:
            self.output_dir.set(directory)
            self.log(f"📁 Đã chọn thư mục đích: {directory}")
    
    def log(self, message: str):
        """Ghi log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def clear_log(self):
        """Xóa log"""
        self.log_text.delete(1.0, tk.END)
        self.log("🗑️ Đã xóa nhật ký")
    
    def convert_files(self):
        """Chuyển đổi các file"""
        source = self.source_dir.get()
        output = self.output_dir.get()
        conversion = self.conversion_type.get()
        
        if not source or not output:
            messagebox.showerror("Lỗi", "Vui lòng chọn thư mục nguồn và đích!")
            return
        
        # Xác định extension
        conversions_map = {
            "md_to_mdx": (".md", ".mdx", FileConverter.md_to_mdx),
            "mdx_to_md": (".mdx", ".md", FileConverter.mdx_to_md),
            "md_to_html": (".md", ".html", FileConverter.md_to_html),
            "mdx_to_html": (".mdx", ".html", lambda c, f: FileConverter.md_to_html(FileConverter.mdx_to_md(c), f)),
            "html_to_md": (".html", ".md", FileConverter.html_to_md),
            "html_to_mdx": (".html", ".mdx", lambda c, f: FileConverter.md_to_mdx(FileConverter.html_to_md(c), f)),
        }
        
        source_ext, target_ext, converter_func = conversions_map[conversion]
        
        # Tìm tất cả file (bao gồm thư mục con)
        source_path = Path(source)
        files = list(source_path.rglob(f"*{source_ext}"))
        
        if not files:
            messagebox.showwarning("Cảnh báo", f"Không tìm thấy file {source_ext} nào!")
            return
        
        # Đếm số thư mục con
        unique_dirs = set(f.parent.relative_to(source_path) for f in files)
        num_dirs = len(unique_dirs)
        
        self.log(f"\n{'='*80}")
        self.log(f"🚀 Bắt đầu chuyển đổi: {conversion.replace('_', ' ').upper()}")
        self.log(f"📂 Nguồn: {source}")
        self.log(f"📂 Đích: {output}")
        self.log(f"📄 Tìm thấy {len(files)} file trong {num_dirs} thư mục")
        self.log(f"🔄 Sẽ giữ nguyên cấu trúc thư mục gốc")
        self.log(f"{'='*80}\n")
        
        success_count = 0
        error_count = 0
        
        for file_path in files:
            try:
                # Đọc file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Chuyển đổi
                filename = file_path.stem
                converted_content = converter_func(content, filename)
                
                # Tạo đường dẫn output
                relative_path = file_path.relative_to(source_path)
                output_path = Path(output) / relative_path.parent / f"{filename}{target_ext}"
                
                # Tạo thư mục nếu chưa có
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Ghi file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(converted_content)
                
                self.log(f"✅ {relative_path} → {output_path.name}")
                success_count += 1
                
            except Exception as e:
                self.log(f"❌ Lỗi {file_path.name}: {str(e)}")
                error_count += 1
        
        # Tổng kết
        self.log(f"\n{'='*80}")
        self.log(f"✨ Hoàn thành!")
        self.log(f"   ✅ Thành công: {success_count} file")
        self.log(f"   ❌ Lỗi: {error_count} file")
        self.log(f"{'='*80}\n")
        
        self.status_var.set(f"Đã chuyển đổi {success_count}/{len(files)} file")
        
        messagebox.showinfo("Hoàn thành", 
                          f"Đã chuyển đổi thành công {success_count}/{len(files)} file!")


def main():
    """Hàm chính"""
    root = tk.Tk()
    
    # Cấu hình style
    style = ttk.Style()
    style.theme_use('clam')
    
    app = ConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    # Kiểm tra thư viện
    try:
        import markdown
    except ImportError:
        print("⚠️  Cần cài đặt thư viện markdown:")
        print("   pip install markdown")
        input("Nhấn Enter để thoát...")
        exit(1)
    
    main()
