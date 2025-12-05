// Popup Script
document.addEventListener('DOMContentLoaded', async () => {
    // Lấy thông tin file hiện tại
    await loadFileInfo();

    // Load settings
    await loadSettings();

    // Event listeners
    document.getElementById('saveSettings').addEventListener('click', saveSettings);
    document.getElementById('copyPath').addEventListener('click', copyPath);
    document.getElementById('openFolder').addEventListener('click', openFolder);
});

// Lấy thông tin file hiện tại
async function loadFileInfo() {
    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        if (tab) {
            // Lấy từ storage
            const result = await chrome.storage.local.get(`tab_${tab.id}`);
            const fileInfo = result[`tab_${tab.id}`];

            if (fileInfo) {
                document.getElementById('originalPath').textContent = fileInfo.originalPath;
                document.getElementById('directory').textContent = fileInfo.directory;
                updateStatus('Đã tìm thấy thông tin file', 'success');
            } else if (tab.url && tab.url.startsWith('file://')) {
                const filePath = decodeURIComponent(tab.url.replace('file:///', ''));
                const directory = filePath.substring(0, filePath.lastIndexOf('/'));

                document.getElementById('originalPath').textContent = filePath;
                document.getElementById('directory').textContent = directory;
                updateStatus('Đã phát hiện file local', 'success');
            } else {
                updateStatus('Không phải file local', 'error');
            }
        }
    } catch (error) {
        console.error('Error loading file info:', error);
        updateStatus('Lỗi: ' + error.message, 'error');
    }
}

// Load settings
async function loadSettings() {
    try {
        const result = await chrome.storage.local.get('defaultSavePath');
        if (result.defaultSavePath) {
            document.getElementById('defaultPath').value = result.defaultSavePath;
        }
    } catch (error) {
        console.error('Error loading settings:', error);
    }
}

// Save settings
async function saveSettings() {
    try {
        const path = document.getElementById('defaultPath').value;

        await chrome.storage.local.set({
            defaultSavePath: path
        });

        updateStatus('✅ Đã lưu cài đặt', 'success');

        setTimeout(() => {
            updateStatus('Sẵn sàng', '');
        }, 2000);
    } catch (error) {
        console.error('Error saving settings:', error);
        updateStatus('❌ Lỗi: ' + error.message, 'error');
    }
}

// Copy path to clipboard
async function copyPath() {
    try {
        const directory = document.getElementById('directory').textContent;

        if (directory && directory !== '-') {
            await navigator.clipboard.writeText(directory);
            updateStatus('✅ Đã copy đường dẫn', 'success');

            setTimeout(() => {
                updateStatus('Sẵn sàng', '');
            }, 2000);
        } else {
            updateStatus('❌ Không có đường dẫn để copy', 'error');
        }
    } catch (error) {
        console.error('Error copying path:', error);
        updateStatus('❌ Lỗi: ' + error.message, 'error');
    }
}

// Open folder in Explorer
async function openFolder() {
    try {
        const directory = document.getElementById('directory').textContent;

        if (directory && directory !== '-') {
            // Tạo link để mở folder
            // Lưu ý: Chrome không cho phép mở file:// trực tiếp từ extension
            // Cần sử dụng workaround

            updateStatus('💡 Mở File Explorer và dán đường dẫn', 'success');

            // Copy path tự động
            await navigator.clipboard.writeText(directory);

            // Hiển thị hướng dẫn
            setTimeout(() => {
                updateStatus('Đã copy! Dán vào Explorer (Ctrl+L, Ctrl+V)', 'success');
            }, 1000);
        } else {
            updateStatus('❌ Không có thư mục để mở', 'error');
        }
    } catch (error) {
        console.error('Error opening folder:', error);
        updateStatus('❌ Lỗi: ' + error.message, 'error');
    }
}

// Update status message
function updateStatus(message, type = '') {
    const statusEl = document.getElementById('status');
    statusEl.textContent = message;
    statusEl.className = 'status ' + type;
}

// Refresh info every 2 seconds
setInterval(loadFileInfo, 2000);
