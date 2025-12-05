// Background Service Worker
console.log('Smart Save Location Extension loaded');

// Lưu trữ thông tin file đã mở
let fileOrigins = new Map();

// Lắng nghe khi tab được tạo hoặc cập nhật
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.url) {
        // Kiểm tra nếu là file:// URL
        if (changeInfo.url.startsWith('file://')) {
            const filePath = decodeURIComponent(changeInfo.url.replace('file:///', ''));
            const directory = filePath.substring(0, filePath.lastIndexOf('/'));

            // Lưu thông tin thư mục gốc
            fileOrigins.set(tabId, {
                originalPath: filePath,
                directory: directory,
                timestamp: Date.now()
            });

            console.log('Detected file opened:', filePath);
            console.log('Directory:', directory);

            // Lưu vào storage để popup có thể truy cập
            chrome.storage.local.set({
                [`tab_${tabId}`]: {
                    originalPath: filePath,
                    directory: directory,
                    timestamp: Date.now()
                }
            });
        }
    }
});

// Lắng nghe khi tab bị đóng
chrome.tabs.onRemoved.addListener((tabId) => {
    fileOrigins.delete(tabId);
    chrome.storage.local.remove(`tab_${tabId}`);
});

// Lắng nghe download events
chrome.downloads.onCreated.addListener((downloadItem) => {
    console.log('Download started:', downloadItem);

    // Lấy tab hiện tại
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs[0]) {
            const tabId = tabs[0].id;
            const fileInfo = fileOrigins.get(tabId);

            if (fileInfo) {
                console.log('Found original directory:', fileInfo.directory);

                // Thử thay đổi đường dẫn download (Chrome có giới hạn)
                // Chỉ có thể gợi ý filename, không thể force directory
                const filename = downloadItem.filename;
                const suggestedPath = `${fileInfo.directory}/${filename}`;

                // Hiển thị notification
                chrome.notifications.create({
                    type: 'basic',
                    iconUrl: 'icons/icon48.png',
                    title: 'Smart Save Location',
                    message: `Gợi ý lưu tại: ${fileInfo.directory}`,
                    priority: 2
                });
            }
        }
    });
});

// API để content script gọi
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'getFileInfo') {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            if (tabs[0]) {
                const fileInfo = fileOrigins.get(tabs[0].id);
                sendResponse({ fileInfo: fileInfo });
            }
        });
        return true; // Giữ message channel mở
    }

    if (request.action === 'setDefaultPath') {
        chrome.storage.local.set({
            defaultSavePath: request.path
        });
        sendResponse({ success: true });
    }
});

// Lắng nghe keyboard shortcuts
chrome.commands.onCommand.addListener((command) => {
    if (command === 'save-to-origin') {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            if (tabs[0]) {
                const fileInfo = fileOrigins.get(tabs[0].id);
                if (fileInfo) {
                    // Gửi message đến content script
                    chrome.tabs.sendMessage(tabs[0].id, {
                        action: 'showSaveDialog',
                        directory: fileInfo.directory
                    });
                }
            }
        });
    }
});
