// Content Script - Chạy trên mọi trang
console.log('Smart Save Location content script loaded');

// Lắng nghe message từ background
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'showSaveDialog') {
        // Hiển thị thông báo về thư mục gốc
        showNotification(request.directory);
        sendResponse({ received: true });
    }
});

// Hiển thị notification trên trang
function showNotification(directory) {
    // Tạo notification element
    const notification = document.createElement('div');
    notification.id = 'smart-save-notification';
    notification.innerHTML = `
    <div style="
      position: fixed;
      top: 20px;
      right: 20px;
      background: #4CAF50;
      color: white;
      padding: 15px 20px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      z-index: 999999;
      font-family: Arial, sans-serif;
      font-size: 14px;
      max-width: 400px;
      animation: slideIn 0.3s ease-out;
    ">
      <strong>💾 Smart Save Location</strong><br>
      <span style="font-size: 12px; opacity: 0.9;">
        Thư mục gốc: <code style="background: rgba(255,255,255,0.2); padding: 2px 6px; border-radius: 3px;">${directory}</code>
      </span>
    </div>
  `;

    // Thêm CSS animation
    const style = document.createElement('style');
    style.textContent = `
    @keyframes slideIn {
      from {
        transform: translateX(400px);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
  `;
    document.head.appendChild(style);

    document.body.appendChild(notification);

    // Tự động ẩn sau 5 giây
    setTimeout(() => {
        notification.style.animation = 'slideIn 0.3s ease-out reverse';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// Theo dõi Ctrl+S / Cmd+S
document.addEventListener('keydown', async (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        // Lấy thông tin file từ background
        chrome.runtime.sendMessage({ action: 'getFileInfo' }, (response) => {
            if (response && response.fileInfo) {
                console.log('File info:', response.fileInfo);
                showNotification(response.fileInfo.directory);
            }
        });
    }
});

// Theo dõi khi người dùng mở Save As dialog
// Lưu ý: Không thể trực tiếp can thiệp vào native dialog
// Chỉ có thể hiển thị gợi ý
window.addEventListener('beforeunload', () => {
    chrome.runtime.sendMessage({ action: 'getFileInfo' }, (response) => {
        if (response && response.fileInfo) {
            console.log('Page unloading, original directory:', response.fileInfo.directory);
        }
    });
});
