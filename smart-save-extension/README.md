# 💾 Smart Save Location - Chrome Extension

## 📋 Mô tả

Extension Chrome giúp bạn tự động nhớ và gợi ý thư mục gốc khi Save As file.

**Lưu ý quan trọng:** Do giới hạn bảo mật của Chrome, extension **KHÔNG THỂ** tự động thay đổi vị trí lưu file trong dialog Save As. Tuy nhiên, extension sẽ:

- ✅ Nhớ thư mục gốc của file bạn đang mở
- ✅ Hiển thị thông báo gợi ý thư mục
- ✅ Copy tự động đường dẫn để bạn dán nhanh
- ✅ Hiển thị thông tin trong popup

## 🚀 Cài đặt

### Bước 1: Chuẩn bị icons

Tạo 3 file icon trong thư mục `icons/`:

- `icon16.png` (16x16px)
- `icon48.png` (48x48px)
- `icon128.png` (128x128px)

Bạn có thể tạo icon đơn giản bằng cách:

1. Mở Paint/Photoshop
2. Tạo hình vuông với màu xanh lá
3. Thêm biểu tượng 💾 hoặc 📁
4. Lưu với các kích thước trên

### Bước 2: Load extension vào Chrome

1. Mở Chrome và truy cập: `chrome://extensions/`
2. Bật **Developer mode** (góc trên bên phải)
3. Nhấn **Load unpacked**
4. Chọn thư mục `smart-save-extension`
5. Extension sẽ xuất hiện trong danh sách

### Bước 3: Cấp quyền

Khi cài đặt, Chrome sẽ yêu cầu các quyền:

- ✅ **Downloads**: Theo dõi download
- ✅ **Storage**: Lưu thông tin thư mục
- ✅ **Tabs**: Theo dõi tab đang mở
- ✅ **All URLs**: Chạy trên mọi trang

## 💻 Sử dụng

### Cách 1: Mở file local

1. Mở file từ thư mục local (File → Open File hoặc kéo thả)
2. Extension tự động nhận diện thư mục gốc
3. Khi bạn Save As, sẽ có thông báo hiển thị đường dẫn gốc

### Cách 2: Sử dụng popup

1. Nhấn vào icon extension trên thanh công cụ
2. Xem thông tin file hiện tại
3. Sử dụng các nút:
   - **📋 Copy đường dẫn**: Copy thư mục để dán vào Save As dialog
   - **📁 Mở thư mục**: Hướng dẫn mở thư mục trong Explorer
   - **💾 Lưu cài đặt**: Lưu thư mục mặc định

### Cách 3: Keyboard shortcut

Nhấn `Ctrl+S` (hoặc `Cmd+S` trên Mac):

- Thông báo sẽ hiển thị đường dẫn thư mục gốc
- Đường dẫn được copy tự động

## ✨ Tính năng

### 🎯 Chính

- **Tự động nhận diện thư mục gốc** khi mở file local
- **Hiển thị thông báo** khi Save As
- **Copy tự động** đường dẫn thư mục
- **Popup thông tin** chi tiết về file
- **Lưu cài đặt** thư mục mặc định

### 🔧 Phụ

- Giao diện đẹp với gradient
- Animation mượt mà
- Tự động refresh thông tin
- Hỗ trợ cả Windows và Mac

## 📖 Hướng dẫn chi tiết

### Khi Save As file

1. **Mở file** từ `e:\ubuntu\Docker\mdx-vietnamese\docs\index.mdx`
2. Extension nhận diện thư mục: `e:\ubuntu\Docker\mdx-vietnamese\docs`
3. Khi bạn **Save As** (Ctrl+Shift+S):
   - Thông báo hiện lên: "Thư mục gốc: e:\ubuntu\Docker\mdx-vietnamese\docs"
   - Đường dẫn được copy tự động
4. Trong Save As dialog:
   - Nhấn `Ctrl+L` để focus vào address bar
   - Nhấn `Ctrl+V` để dán đường dẫn
   - Nhấn Enter
5. Bạn đã ở đúng thư mục gốc!

### Sử dụng popup

```
┌─────────────────────────────────────┐
│  💾 Smart Save Location             │
│  Tự động nhảy đến thư mục gốc       │
├─────────────────────────────────────┤
│  📂 Thông tin file hiện tại         │
│  Đường dẫn gốc:                     │
│  e:\ubuntu\Docker\...\index.mdx     │
│  Thư mục:                           │
│  e:\ubuntu\Docker\...\docs          │
├─────────────────────────────────────┤
│  ⚙️ Cài đặt                         │
│  Thư mục mặc định:                  │
│  [e:\ubuntu\Docker\mdx-vietnamese]  │
│  [💾 Lưu cài đặt]                   │
├─────────────────────────────────────┤
│  [📋 Copy đường dẫn thư mục]        │
│  [📁 Mở thư mục trong Explorer]     │
├─────────────────────────────────────┤
│  ✅ Đã copy đường dẫn               │
└─────────────────────────────────────┘
```

## ⚠️ Giới hạn

Do bảo mật của Chrome:

1. **Không thể tự động thay đổi vị trí Save As**
   - Chrome không cho phép extension can thiệp vào native dialog
   - Giải pháp: Copy + dán thủ công (rất nhanh!)

2. **Chỉ hoạt động với file local**
   - File phải được mở từ `file://` protocol
   - Không hoạt động với file trên web

3. **Cần quyền truy cập**
   - Cần cấp quyền downloads, storage, tabs

## 🔧 Tùy chỉnh

### Thay đổi thời gian hiển thị thông báo

Mở `content.js`, tìm dòng:

```javascript
setTimeout(() => {
  notification.style.animation = 'slideIn 0.3s ease-out reverse';
  setTimeout(() => notification.remove(), 300);
}, 5000); // ← Thay đổi 5000 (5 giây)
```

### Thay đổi màu sắc

Mở `popup.html`, tìm:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

Thay bằng màu bạn thích!

## 🐛 Xử lý lỗi

### Extension không hoạt động

1. Kiểm tra Developer mode đã bật
2. Reload extension: `chrome://extensions/` → Reload
3. Kiểm tra console: Right-click icon → Inspect popup

### Không nhận diện file

1. Đảm bảo file được mở bằng `file://` protocol
2. Kiểm tra quyền truy cập
3. Xem console log: F12 → Console

### Thông báo không hiện

1. Kiểm tra content script đã load
2. Xem console: F12 → Console
3. Reload trang

## 📝 Changelog

### v1.0.0 (2025-12-05)

- ✨ Phát hành phiên bản đầu tiên
- ✅ Nhận diện thư mục gốc
- ✅ Hiển thị thông báo
- ✅ Copy tự động
- ✅ Popup với giao diện đẹp

## 🤝 Đóng góp

Nếu bạn muốn cải thiện extension:

1. Fork repository
2. Tạo branch mới
3. Commit changes
4. Push và tạo Pull Request

## 📄 License

MIT License - Tự do sử dụng và chỉnh sửa

---

**Tạo bởi:** MDX Vietnamese Project  
**Phiên bản:** 1.0.0  
**Ngày:** 2025-12-05

**Lưu ý:** Extension này là workaround cho giới hạn của Chrome. Để có trải nghiệm tốt nhất, hãy sử dụng kết hợp với keyboard shortcuts!
