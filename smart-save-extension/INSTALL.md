# 🚀 HƯỚNG DẪN CÀI ĐẶT NHANH

## Bước 1: Mở Chrome Extensions

1. Mở Chrome
2. Gõ vào address bar: `chrome://extensions/`
3. Nhấn Enter

## Bước 2: Bật Developer Mode

1. Tìm toggle **Developer mode** ở góc trên bên phải
2. Bật nó lên (màu xanh)

## Bước 3: Load Extension

1. Nhấn nút **Load unpacked** (góc trên bên trái)
2. Duyệt đến thư mục: `e:\ubuntu\Docker\mdx-vietnamese\smart-save-extension`
3. Nhấn **Select Folder**

## Bước 4: Kiểm tra

Extension sẽ xuất hiện với:

- Icon 💾
- Tên: "Smart Save Location"
- Trạng thái: Enabled

## Bước 5: Ghim Extension (Tùy chọn)

1. Nhấn vào icon puzzle 🧩 trên thanh công cụ Chrome
2. Tìm "Smart Save Location"
3. Nhấn vào icon ghim 📌

## ✅ Hoàn thành

Bây giờ bạn có thể:

1. Mở file local bất kỳ
2. Nhấn vào icon extension để xem thông tin
3. Khi Save As, extension sẽ hiển thị thông báo gợi ý thư mục gốc

---

## 🎯 Test Extension

### Test 1: Mở file local

```
1. Mở file: e:\ubuntu\Docker\mdx-vietnamese\docs\index.mdx
2. Nhấn vào icon extension
3. Kiểm tra popup hiển thị đúng thư mục
```

### Test 2: Save As

```
1. Mở file như trên
2. Nhấn Ctrl+S hoặc Ctrl+Shift+S
3. Xem thông báo hiện lên góc phải màn hình
4. Đường dẫn được copy tự động
```

### Test 3: Copy path

```
1. Mở popup extension
2. Nhấn "📋 Copy đường dẫn thư mục"
3. Dán (Ctrl+V) để kiểm tra
```

---

## ⚠️ Lưu ý

- Extension chỉ hoạt động với file local (`file://`)
- Không hoạt động với file trên web
- Chrome không cho phép tự động thay đổi vị trí Save As
- Bạn cần copy + dán thủ công (rất nhanh!)

---

## 🐛 Nếu có lỗi

1. **Extension không load:**
   - Kiểm tra Developer mode đã bật
   - Kiểm tra đường dẫn thư mục đúng

2. **Không hiển thị thông tin:**
   - Reload extension
   - Mở lại file
   - Kiểm tra console (F12)

3. **Thông báo không hiện:**
   - Reload trang
   - Kiểm tra quyền extension

---

**Cần trợ giúp?** Xem file README.md để biết chi tiết!
