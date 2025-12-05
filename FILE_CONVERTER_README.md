# Hướng dẫn sử dụng File Converter GUI

## 📋 Mô tả

Script Python với giao diện đồ họa để chuyển đổi hàng loạt giữa các định dạng:
- **MD** (Markdown)
- **MDX** (Markdown + JSX)
- **HTML**

## 🚀 Cài đặt

### 1. Cài đặt Python
Đảm bảo bạn đã cài Python 3.7 trở lên.

### 2. Cài đặt thư viện cần thiết

```bash
pip install markdown
```

**Lưu ý:** `tkinter` thường đi kèm với Python, không cần cài thêm.

## 💻 Sử dụng

### Chạy script

```bash
python file_converter_gui.py
```

### Các bước sử dụng

1. **Chọn thư mục nguồn**: Nhấn nút "Chọn" bên cạnh "Thư mục nguồn" và chọn thư mục chứa file cần chuyển đổi

2. **Chọn thư mục đích**: Nhấn nút "Chọn" bên cạnh "Thư mục đích" và chọn nơi lưu file đã chuyển đổi

3. **Chọn loại chuyển đổi**:
   - **MD → MDX**: Chuyển Markdown sang MDX (thêm metadata)
   - **MDX → MD**: Chuyển MDX sang Markdown (loại bỏ JSX, exports)
   - **MD → HTML**: Chuyển Markdown sang HTML hoàn chỉnh
   - **MDX → HTML**: Chuyển MDX sang HTML
   - **HTML → MD**: Chuyển HTML sang Markdown
   - **HTML → MDX**: Chuyển HTML sang MDX

4. **Nhấn "🔄 Chuyển đổi"**: Bắt đầu quá trình chuyển đổi

5. **Xem kết quả**: Theo dõi tiến trình trong phần "Nhật ký"

## ✨ Tính năng

### 🎯 Chuyển đổi hỗ trợ

#### MD → MDX
- Tự động thêm metadata (export info)
- Giữ nguyên toàn bộ nội dung Markdown
- Thêm timestamp tự động

#### MDX → MD
- Loại bỏ tất cả export statements
- Loại bỏ import statements
- Loại bỏ JSX components
- Loại bỏ JSX comments `{/* */}`
- Làm sạch dòng trống thừa

#### MD/MDX → HTML
- Chuyển đổi Markdown sang HTML
- Tạo file HTML hoàn chỉnh với CSS đẹp
- Hỗ trợ:
  - Code highlighting
  - Tables
  - Blockquotes
  - Images
  - Links
  - Typography tối ưu

#### HTML → MD/MDX
- Chuyển đổi headings (h1-h6)
- Chuyển đổi paragraphs
- Chuyển đổi links
- Chuyển đổi code blocks
- Chuyển đổi emphasis (*italic*, **bold**)
- Loại bỏ HTML tags

### 🔧 Tính năng khác

- **Xử lý hàng loạt**: Chuyển đổi tất cả file trong thư mục và thư mục con
- **Giữ cấu trúc thư mục**: File output giữ nguyên cấu trúc thư mục nguồn
- **Giữ tên file gốc**: Chỉ thay đổi extension
- **Log chi tiết**: Theo dõi từng file được chuyển đổi
- **Thống kê**: Hiển thị số file thành công/lỗi
- **Giao diện thân thiện**: Dễ sử dụng, không cần dòng lệnh

## 📁 Ví dụ

### Cấu trúc thư mục nguồn
```
docs/
├── getting-started.md
├── guides/
│   ├── installation.md
│   └── configuration.md
└── api/
    └── reference.md
```

### Sau khi chuyển đổi MD → MDX
```
output/
├── getting-started.mdx
├── guides/
│   ├── installation.mdx
│   └── configuration.mdx
└── api/
    └── reference.mdx
```

## ⚙️ Cấu hình nâng cao

### Tùy chỉnh HTML template

Mở file `file_converter_gui.py` và chỉnh sửa hàm `md_to_html()` để thay đổi:
- CSS styling
- HTML structure
- Meta tags

### Tùy chỉnh MDX metadata

Chỉnh sửa hàm `md_to_mdx()` để thay đổi:
- Metadata fields
- Date format
- Author information

## 🐛 Xử lý lỗi

### Lỗi "No module named 'markdown'"
```bash
pip install markdown
```

### Lỗi encoding
Script tự động sử dụng UTF-8. Nếu gặp lỗi, kiểm tra encoding của file nguồn.

### File không được chuyển đổi
- Kiểm tra extension file (phải đúng với loại chuyển đổi)
- Xem log để biết lỗi cụ thể
- Đảm bảo có quyền ghi vào thư mục đích

## 📝 Lưu ý

1. **Backup dữ liệu**: Luôn backup trước khi chuyển đổi hàng loạt
2. **Kiểm tra kết quả**: Xem lại một vài file sau khi chuyển đổi
3. **HTML → MD**: Chuyển đổi cơ bản, có thể cần chỉnh sửa thủ công
4. **MDX → MD**: Một số JSX phức tạp có thể không được loại bỏ hoàn toàn

## 🎨 Giao diện

```
┌─────────────────────────────────────────────────────────┐
│         CHUYỂN ĐỔI FILE HÀNG LOẠT                      │
├─────────────────────────────────────────────────────────┤
│ Thư mục nguồn:  [_______________] [Chọn]               │
│ Thư mục đích:   [_______________] [Chọn]               │
│                                                         │
│ Loại chuyển đổi:                                       │
│  ○ MD → MDX    ○ MDX → MD     ○ MD → HTML             │
│  ○ MDX → HTML  ○ HTML → MD    ○ HTML → MDX            │
│                                                         │
│          [🔄 Chuyển đổi]  [🗑️ Xóa log]                │
├─────────────────────────────────────────────────────────┤
│ Nhật ký:                                               │
│ ┌─────────────────────────────────────────────────┐   │
│ │ [12:00:00] 📁 Đã chọn thư mục nguồn...         │   │
│ │ [12:00:05] 🚀 Bắt đầu chuyển đổi...            │   │
│ │ [12:00:06] ✅ file1.md → file1.mdx             │   │
│ │ [12:00:07] ✅ file2.md → file2.mdx             │   │
│ │ [12:00:08] ✨ Hoàn thành!                       │   │
│ └─────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│ Sẵn sàng                                               │
└─────────────────────────────────────────────────────────┘
```

## 🤝 Hỗ trợ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra log trong giao diện
2. Đảm bảo đã cài đúng thư viện
3. Kiểm tra quyền truy cập thư mục

## 📄 License

MIT License - Tự do sử dụng và chỉnh sửa

---

**Tạo bởi:** MDX Vietnamese Translation Project
**Phiên bản:** 1.0.0
**Ngày:** 2025-12-05
