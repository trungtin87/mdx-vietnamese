---
description: Deploy project lên GitHub Pages
---

# Workflow: Deploy lên GitHub Pages

Workflow này sẽ hướng dẫn bạn cách deploy project MDX Vietnamese lên GitHub Pages.

## Bước 1: Cài đặt dependencies

```bash
npm install
```

## Bước 2: Build documentation

```bash
npm run docs
```

## Bước 3: Kiểm tra thư mục public đã được tạo

Sau khi build, thư mục `public` sẽ chứa các file tĩnh để deploy.

```bash
ls public
```

## Bước 4: Commit và push code lên GitHub

```bash
git add .
git commit -m "Update documentation"
git push origin main
```

## Bước 5: Cấu hình GitHub Pages

1. Vào repository trên GitHub
2. Vào **Settings** → **Pages**
3. Trong phần **Source**, chọn **GitHub Actions**
4. Workflow GitHub Actions đã được cấu hình tại `.github/workflows/website.yml` sẽ tự động chạy

## Bước 6: Kiểm tra deployment

Sau khi workflow chạy xong, website sẽ được deploy tại:

```text
https://<username>.github.io/<repository-name>/
```

## Lưu ý

- **Cấu hình URL**: Đảm bảo file `docs/_config.js` có URL đúng:

  ```javascript
  const site = new URL('https://<username>.github.io/<repository-name>/')
  ```

  Nếu URL sai, CSS và assets sẽ không load được.

- Đảm bảo file `.github/workflows/website.yml` đã được cấu hình đúng
- Kiểm tra GitHub Actions tab để xem trạng thái deployment
- Nếu có lỗi, kiểm tra logs trong GitHub Actions để debug
- Sau khi push code, đợi khoảng 2-3 phút để GitHub Actions build và deploy
