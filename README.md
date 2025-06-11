*  Giới thiệu
Ứng dụng "Ký số Đỉnh Cao" là một website đơn giản nhưng mạnh mẽ được phát triển bằng Flask và RSA 
để thực hiện việc tạo chữ ký số và xác minh tính toàn vẹn của tệp tin. Ứng dụng phù hợp với mục đích học tập, minh họa cho các nguyên lý bảo mật dữ liệu bằng mã hóa bất đối xứng.
*Chức năng cơ bản
 Ký số tệp tin:
Người dùng tải lên một tệp bất kỳ và hệ thống sẽ tạo ra một chữ ký số sử dụng thuật toán RSA với SHA-256.

 Xác minh chữ ký:
Tải lên tệp gốc và chữ ký số để kiểm tra xem chữ ký đó có hợp lệ không (đảm bảo tệp không bị thay đổi).

 Tự động sinh khóa RSA (2048-bit) nếu chưa có khóa tồn tại trong thư mục.

 Giao diện đẹp, hiện đại, thân thiện với người dùng, sử dụng Bootstrap 5 và biểu tượng từ Bootstrap Icons.
 *Kỹ thuật & công nghệ sử dụng
Công nghệ	Vai trò
Python 3	Ngôn ngữ lập trình chính
Flask	Web Framework nhẹ
cryptography	Thư viện thực hiện RSA và SHA-256
Bootstrap 5	Tạo giao diện đẹp, responsive
HTML + CSS	Hiển thị giao diện người dùng
*Một số hình ảnh
![image](https://github.com/user-attachments/assets/b6d75d0a-d2f9-45c4-bd27-e25b1db69a6f)
