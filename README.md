# RadioBioCalc — Seminar Hypofractionation (Sinh học Bức xạ)

Website giáo dục của **Nhóm 4 — Trường Đại học Khoa học Tự nhiên, ĐHQG-HCM — Khoa Vật lý / Vật lý Kỹ thuật**. Dự án dựa trên hai bản HTML nhóm đã cung cấp, bổ sung hai logo nguyên bản do nhóm gửi, cải thiện module BED có xét tái sinh cho từng loại mô, và có poster tổng hợp một trang khổ **A2**.

> **LƯU Ý AN TOÀN:** Đây là mô hình minh họa dùng cho học tập và seminar, **không phải phần mềm lập kế hoạch xạ trị** và không được sử dụng để chỉ định hoặc sửa đổi liệu trình của bệnh nhân. Tham số trên trang là dữ liệu ví dụ, không phải quy chuẩn lâm sàng.

## Các mục

- **Trang chủ:** giới thiệu RadioBioCalc, logo Trường ĐH KHTN (bên trái) và logo bộ môn/khoa được cung cấp (bên phải), thông tin giảng viên và nhóm.
- **Module 1:** BED và EQD2 chưa xét tái sinh theo mô hình LQ; có biểu đồ so sánh và đường cong sống sót mang tính minh họa.
- **Module 2:** BED **có xét tái sinh** của mô bướu và mô lành theo các giá trị nhập riêng. Mặc định mô lành muộn có K_n = 0; có ví dụ mô lành sớm giả định. Trả về BED trước và sau hiệu chỉnh cùng phần BED suy giảm.
- **Module 3:** chuyển đổi phác đồ bảo toàn BED lý thuyết cho một loại mô; nhắc người dùng khi số buổi tính ra không nguyên.
- **Module 4:** minh họa tình huống sai phân liều hoặc gián đoạn lịch chiếu; các phép làm tròn và giả định không thay thế quyết định chuyên môn.

**Công thức lõi Module 2:**

`BED = n × d × (1 + d / (α/β)) − K × max(0, T − Tk)`

Trong đó d là liều tại **mô đang xét** (không mặc định liều mô lành bằng liều kê cho bướu), T và Tk tính bằng ngày, K tính bằng Gy/ngày. Đối với mô lành muộn trong phạm vi công cụ, thường chọn `K = 0`. Trường hợp mô lành sớm dùng K riêng và là ví dụ giả định.

**Bài kiểm tra Module 2:** bướu `n=30`, `d=2 Gy`, `α/β=10 Gy`, `T=42`, `Tk=28`, `K=0.9` -> `BED0=72 Gy_10`, `BED loss=12.6 Gy_10`, `BED=59.4 Gy_10`.

## Mở website trên máy tính

Chỉ cần mở `index.html` bằng Chrome/Edge/Firefox. Có thể dùng VS Code + Live Server nhưng không bắt buộc. Toàn bộ CSS và JavaScript quan trọng đã được lưu trong `assets/`, không phụ thuộc CDN để tính toán.

## Xuất bản trên GitHub Pages (khuyến nghị: tự động tạo QR trong poster)

1. Đăng nhập GitHub và tạo **repository Public** tên gợi ý: `radiobiocalc-hypofractionation`.
2. Tải **toàn bộ nội dung bên trong thư mục dự án**, bao gồm cả thư mục ẩn `.github`, lên nhánh `main` của repository. Đảm bảo `index.html` nằm ở gốc repository, không phải trong một thư mục con khác. Nếu sử dụng GitHub Desktop hoặc dòng lệnh, các thư mục con được giữ nguyên.
3. Tại repository, vào **Settings → Pages → Build and deployment → Source → GitHub Actions**.
4. Trong tab **Actions**, chạy workflow tên **Publish RadioBioCalc + poster QR** nếu nó chưa tự chạy; workflow cũng chạy khi đẩy commit mới lên `main`.
5. Workflow tự dựng poster PDF/PNG và hai QR thật từ URL GitHub Pages, rồi xuất bản toàn bộ website. Trên GitHub, vào **Settings → Pages → Visit site** để lấy URL đã xuất bản và kiểm tra bằng trình duyệt khác.

**Địa chỉ mặc định** của một project Pages (không dùng tên miền riêng) sẽ có dạng `https://TEN_TAI_KHOAN.github.io/TEN_REPO/`. Không xem đây là URL của bạn cho đến khi GitHub xác nhận site đã triển khai thành công.

### Cách đẩy lên bằng Git (nếu đã cài Git)

Từ thư mục dự án đã giải nén:

```bash
git init
git add .
git commit -m "Publish RadioBioCalc seminar website and poster"
git branch -M main
git remote add origin https://github.com/TEN_TAI_KHOAN/TEN_REPO.git
git push -u origin main
```

Thay `TEN_TAI_KHOAN` và `TEN_REPO` theo tài khoản của bạn. Trên GitHub.com cũng có mục **Add file → Upload files** để tải nội dung theo cấu trúc tương tự.

### Nếu muốn dùng Pages “Deploy from a branch” thay cho workflow

Website vẫn hoạt động nếu chọn **Settings → Pages → Deploy from a branch → main / (root)**. Nhưng poster đóng gói sẵn chỉ chứa ô QR dự phòng, vì lúc tạo chưa có URL công khai. Sau khi nhận được URL live, chạy script tạo QR bên dưới rồi commit lại thư mục `poster/`.

## Poster A2 và QR

- `poster/RadioBioCalc_Poster.pdf`: poster A2, phù hợp in ấn.
- `poster/RadioBioCalc_Poster.png`: ảnh poster xem nhanh.
- `poster/QR_Website.png`: QR truy cập **website** — được tạo tự động khi chạy workflow thành công.
- `poster/QR_Poster.png`: QR truy cập **poster PDF trên GitHub Pages** — được tạo tự động khi chạy workflow thành công.

**Vì URL chưa có ở bản offline, hai ô QR trong poster offline có ghi rõ “CHƯA CÓ LINK”. Đây không phải QR hỏng; đây là bản chờ xuất bản.** Workflow tự thay thế hai ô đó bằng QR thật trước khi đăng site.

Nếu muốn tạo tay sau khi website đã live:

```bash
python -m pip install reportlab Pillow qrcode PyMuPDF
python tools/finalize_poster.py --site-url https://TEN_TAI_KHOAN.github.io/TEN_REPO/
```

`--poster-url` tùy chọn dùng khi poster được lưu trên một URL HTTPS công khai khác. Công cụ tạo lại poster cả PDF và PNG cùng hai ảnh QR.

## Cấu trúc

```text
index.html
.nojekyll
.github/workflows/deploy.yml
assets/
  radiobio.css
  chart-lite.js
  logo_truong.jpg
  logo_khoa.jpg
  previews/      (5 ảnh chụp trang chủ và 4 module để dựng poster)
poster/
  RadioBioCalc_Poster.pdf
  RadioBioCalc_Poster.png
tools/
  finalize_poster.py
```

Có thể kiểm tra bốn module bằng Node.js trước khi upload: `node tests/calculation-smoke.cjs`.

## Kiểm tra nhanh trước khi nộp seminar

- Nhấp vào mỗi module trên thanh điều hướng và thử thay dữ liệu.
- Với Module 2, nhập mẫu đầu cổ phía trên phải ra **59,40 Gy** cho bướu.
- Chuyển Module 2 sang tình huống mô lành muộn K_n=0: BED mô lành trước và sau hiệu chỉnh bằng nhau.
- Trên GitHub Pages, cả hai logo và biểu đồ hiển thị đủ, link `poster/RadioBioCalc_Poster.pdf` mở được.
- Dùng điện thoại quét **QR website** và **QR poster** từ bản đã triển khai; mỗi QR phải mở đúng trang.

## Ghi chú khoa học

Phương trình BED dùng LQ thông thường và một mô hình tái sinh tuyến tính sau thời điểm khởi phát Tk, không mô phỏng đầy đủ tất cả quá trình sửa chữa, tuần hoàn tế bào, tái oxy hóa, dị biệt liều trong thể tích mô hoặc lịch chiếu thực tế. Tốc độ K, thời điểm Tk và α/β phải có nguồn phù hợp đối tượng mô/loại bệnh trong báo cáo chính thức. BED và EQD2 mô lành với α/β khác BED bướu **không nên đem so trực tiếp** như cùng một đại lượng sinh học. Các phép toán điều chỉnh số buổi/phân liều trong module 3–4 là toán học giả định, không phải khuyến nghị điều trị.

## Ghi công

Tài liệu seminar Nhóm 4, môn Sinh học Bức xạ. Nhận diện trường và bộ môn lấy từ hình người dùng cung cấp. Các ảnh minh họa trang là ảnh chụp của website RadioBioCalc này.
