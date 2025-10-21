# Video Topic Generator - Hướng dẫn sử dụng

Script Python để gọi API generate-topic cho nhiều video từ file Excel, xử lý 5 video đồng thời.

## Cài đặt

```bash
pip install -r requirements.txt
```

## Chuẩn bị file Excel

File Excel của bạn cần có ít nhất 1 cột:
- **Video Name** (bắt buộc): Tên file video, tương ứng với `object_key` trong API
- **ID Video** (tùy chọn): ID của video, tương ứng với `id_video` trong API. Nếu không có, script sẽ dùng Video Name

### Ví dụ cấu trúc Excel:

| Video Name   | ID Video |
|--------------|----------|
| video1.mp4   | vid001   |
| video2.mp4   | vid002   |
| video3.mp4   | vid003   |

Hoặc chỉ cần 1 cột:

| Video Name   |
|--------------|
| video1.mp4   |
| video2.mp4   |
| video3.mp4   |

## Sử dụng

```bash
python generate_video_topics.py <đường_dẫn_file_excel>
```

### Ví dụ:

```bash
# Với file Excel
python generate_video_topics.py videos.xlsx

# Với file CSV (file mẫu đã có sẵn)
python generate_video_topics.py example_videos.csv
```

## Tính năng

- Đọc file Excel/CSV chứa danh sách video
- Gọi API generate-topic cho mỗi video
- Xử lý **5 video đồng thời** để tăng tốc độ
- **Lưu response của mỗi video vào file JSON riêng** trong thư mục `responses/`
- Logging chi tiết quá trình xử lý
- Báo cáo tổng kết khi hoàn thành

## Lưu trữ Responses

Mỗi response từ API sẽ được lưu vào file JSON riêng trong thư mục `responses/` với tên file dựa trên tên video.

### Ví dụ:
- Video: `video1.mp4` → File: `responses/video1.json`
- Video: `my video 2.mp4` → File: `responses/my_video_2.json`

### Cấu trúc file JSON:

```json
{
  "video_name": "video1.mp4",
  "status": "success",
  "data": {
    // Response data from API
  }
}
```

## Cấu hình

Bạn có thể thay đổi các thông số trong file `generate_video_topics.py`:

- `API_URL`: URL của API
- `BEARER_TOKEN`: Token xác thực
- `MAX_WORKERS`: Số lượng video xử lý đồng thời (mặc định: 5)
- `REQUEST_TIMEOUT`: Thời gian timeout cho mỗi request (mặc định: 300 giây = 5 phút)
- `OUTPUT_DIR`: Thư mục lưu responses (mặc định: `responses`)

### Lưu ý về Timeout:
- Nếu video xử lý lâu, bạn có thể tăng `REQUEST_TIMEOUT` lên cao hơn (ví dụ: 600 = 10 phút)
- Timeout mặc định đã tăng từ 60 giây lên 300 giây để tránh lỗi ReadTimeout

## Output mẫu

```
2024-01-20 10:00:00 - INFO - Reading Excel file: videos.xlsx
2024-01-20 10:00:00 - INFO - Found 10 videos to process
2024-01-20 10:00:00 - INFO - Starting processing with 5 concurrent workers...
2024-01-20 10:00:01 - INFO - [Row 1] Processing: video1.mp4
2024-01-20 10:00:01 - INFO - [Row 2] Processing: video2.mp4
2024-01-20 10:00:01 - INFO - [Row 3] Processing: video3.mp4
2024-01-20 10:00:01 - INFO - [Row 4] Processing: video4.mp4
2024-01-20 10:00:01 - INFO - [Row 5] Processing: video5.mp4
2024-01-20 10:00:02 - INFO - [Row 1] SUCCESS: video1.mp4
2024-01-20 10:00:02 - INFO - [Row 6] Processing: video6.mp4
...
==================================================
PROCESSING SUMMARY
==================================================
Total videos: 10
Successful: 10
Failed: 0
Errors: 0
Responses saved to: ./responses/
==================================================
```

## Cấu trúc thư mục sau khi chạy

```
.
├── generate_video_topics.py
├── requirements.txt
├── videos.xlsx
└── responses/
    ├── video1.json
    ├── video2.json
    ├── video3.json
    └── ...
```
