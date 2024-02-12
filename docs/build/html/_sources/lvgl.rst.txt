LVGL
===========================================================================


---------------------------------------------------------------------------
Yêu cầu về phần cứng
---------------------------------------------------------------------------
- Hướng dẫn này được chạy trên board STM32F746G_Disco.
- Máy tính được sử dụng Ubuntu 22.04 (dual boot).

---------------------------------------------------------------------------
Cài đặt phần mềm SquareLine Studio
---------------------------------------------------------------------------

- Truy cập `Link <https://squareline.io/downloads>`_.

- **Các bước cài đặt:**

Bước 1: Giải nén tệp vừa tải

Bước 2: Chạy file setup.sh

    - Mở terminal truy cập vào thư mục có chứa file setup.sh
    - Chạy các lệnh sau.

.. code-block:: console
    
    chmod +x setup.sh
    ./setup.sh

**Lưu ý: Nếu xảy ra lỗi thiếu thư viện thì các bạn cài thêm cho máy.**

---------------------------------------------------------------------------
Sử dụng phần mềm SquareLine Studio
---------------------------------------------------------------------------

- Mở phần mềm SquareLine Studio.
- Đăng nhập (hoặc đăng ký) tài khoản.

.. image:: ../img/img_11.png
   :alt: alternate text

- Tạo Project mới.

.. image:: ../img/img_12.png
   :alt: alternate text

- Export source code sau khi design trên SquareLine Studio

.. image:: ../img/img_13.png
   :alt: alternate text

.. image:: ../img/img_14.png
   :alt: alternate text

---------------------------------------------------------------------------
Thêm source code mới vào project
---------------------------------------------------------------------------

**Lưu ý: Đổi đường dẫn trong file** ``ui.h`` **thành** ``#include "lvgl.h"``.

.. image:: ../img/img_15.png
   :alt: alternate text

- Thêm các thư viện trong file ``main.c``

.. image:: ../img/img_16.png
   :alt: alternate text

- Chỉnh sửa file ``CMakeLists.txt`` cùng cấp với folder ``src`` như sau.

.. image:: ../img/img_18.png
   :alt: alternate text

.. image:: ../img/img_17.png
   :alt: alternate text