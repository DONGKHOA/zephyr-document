

MỘT SỐ HƯỞNG DẪN VỀ ZEPHYR PROJECT - ZEPHYR OS
===========================================================================

---------------------------------------------------------------------------
Yêu cầu về phần cứng
---------------------------------------------------------------------------

- Ubuntu version từ 20 trở lên (khuyến nghị cài dual boot nếu sài máy áo có thể bị lỗi khi flash vào chip).
- Ổ cứng cấp phát cho ubuntu trên 20GB.

---------------------------------------------------------------------------
Các bước cài đặt
---------------------------------------------------------------------------
**Lưu ý trước khi cài đặt là đảm bảo mạng kết nối luôn ổn định và máy tính không được mất điện giữa lúc cài 
(đây là ubuntu nên cái gì cũng có thể đi luôn cái ubuntu)**

Bước 1: Cài đặt các tool phụ thuộc (CMake, Python, Devicetree compiler)
---------------------------------------------------------------------------

- Sử dụng ``apt`` để cài đặt các tool:

.. code-block:: console

    sudo apt install --no-install-recommends git cmake ninja-build gperf \
    ccache dfu-util device-tree-compiler wget \
    python3-dev python3-pip python3-setuptools python3-tk python3-wheel xz-utils file \
    make gcc gcc-multilib g++-multilib libsdl2-dev libmagic1


- Check lại xem đã cài được chưa:

.. code-block:: console

    cmake --version
    python3 --version
    dtc --version

- **Kết quả:**

.. image:: ../img/img_1.png
   :alt: alternate text

Bước 2: Cài môi trường ảo và zephyr project
---------------------------------------------------------------------------

- Sử dụng ``apt`` để cài gói ``venv`` của Python:

.. code-block:: console

    sudo apt install python3-venv

- Tạo môi trường ảo: 

.. code-block:: console

    python3 -m venv ~/zephyrproject/.venv


- Activate môi trường ảo:

.. code-block:: console

    source ~/zephyrproject/.venv/bin/activate

**Lưu ý: mỗi khi muốn build hoặc flash zephyr project đều phải sử dụng lệnh này.**

- Cài đặt ``west``:

.. code-block:: console
    
    pip install west

- Get source code của Zephyr:

.. code-block:: console
    
    west init ~/zephyrproject
    cd ~/zephyrproject
    west update

**Lưu ý: đây là nguồn để học về các hàm sử dụng trong zephyr rất hiệu quả nên hãy cố gắng khai thác hết mức có thể.**

- Export Zephyr CMake package:

.. code-block:: console
    
    west zephyr-export

- Cài đặt các requirement:

.. code-block:: console
    
    pip install -r ~/zephyrproject/zephyr/scripts/requirements.txt


Bước 3: Cài Zephyr SDK
---------------------------------------------------------------------------

- Tải và verify Zephyr SDK:

.. code-block:: console

    cd ~
    wget https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.16.4/zephyr-sdk-0.16.4_linux-x86_64.tar.xz
    wget -O - https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.16.4/sha256.sum | shasum --check --ignore-missing

- Giải nén tệp vừa tải:

.. code-block:: console

    tar xvf zephyr-sdk-0.16.4_linux-x86_64.tar.xz

- Cài đặt Zephyr SDK:

.. code-block:: console

    cd zephyr-sdk-0.16.4
    ./setup.sh

Bước 4: Build một project sample
---------------------------------------------------------------------------

- Chọn một project sample:

.. code-block:: console

    cd ~
    cd ./zephyrproject/zephyr/samples/basic/blinky

- Chọn Board để build:

**Các board mà zephyr hổ trở:** `Supported Boards <https://docs.zephyrproject.org/latest/boards/index.html#boards>`_.

.. code-block:: console

    west build -p always -b <your-board-name>

**Nếu bạn thêm lệnh** ``set(BOARD <your-board-name>)`` **trong file CMakeLists.txt trong project thì chỉ cần ghi:** ``west build``

.. image:: ../img/img_2.png
   :alt: alternate text

**Nếu như bạn gặp lỗi:**

.. image:: ../img/img_3.png
   :alt: alternate text

**Hãy truy cập vào thư mục đó rồi chỉnh sửa file main.c như sau:** *(Lưu ý sau khi thay đổi file main.c
hãy xóa thư mục build trong project đó hãy build lại)*

.. code-block:: console

    #include <stdio.h>
    #include <zephyr/kernel.h>
    #include <zephyr/drivers/gpio.h>

    /* 1000 msec = 1 sec */
    #define SLEEP_TIME_MS   1000

    /* The devicetree node identifier for the "led0" alias. */
    #define LED0_NODE DT_ALIAS(led0)
    static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(LED0_NODE, gpios);

    int main(void)
    {
        int ret;
        bool led_state = true;

        if (!gpio_is_ready_dt(&led)) {
            return 0;
        }

        ret = gpio_pin_configure_dt(&led, GPIO_OUTPUT_ACTIVE);
        if (ret < 0) {
            return 0;
        }

        while (1) {
            ret = gpio_pin_toggle_dt(&led);
            if (ret < 0) {
                return 0;
            }

            led_state = !led_state;
            printf("LED state: %s\n", led_state ? "ON" : "OFF");
            k_msleep(SLEEP_TIME_MS);
        }
        return 0;
    }

.. image:: ../img/img_4.png
   :alt: alternate text


---------------------------------------------------------------------------
Cấu trúc về Zephyr Project
---------------------------------------------------------------------------

**Về phần này các bạn coi theo** `Slides <https://docs.google.com/presentation/d/12dFrL5vy-qN5w3uh-lv_V1EL9MIDEYXP/edit#slide=id.g2b313a0e26e_0_132>`_ **của mình làm.**

---------------------------------------------------------------------------
Guiconfig
---------------------------------------------------------------------------

- Thay vì bạn sử dụng file `pri.conf` để config các ngoại vi, chức năng trên zephyr thì bạn có thể dùng gui.

- Sử dụng lệnh:

.. code-block:: console

    west build -t guiconfig

.. image:: ../img/img_5.png
   :alt: alternate text


---------------------------------------------------------------------------
Debug cho ARM [STM32]sử dụng OpenOCD + VSCODE
---------------------------------------------------------------------------

Bước 1: Cài đặt openocd
---------------------------------------------------------------------------

- Đầu tiên hãy kiểm tra xem máy tính đã có openOCD hay chưa: mở termial và gõ lệnh sau:

.. code-block:: console

    openocd


- Nếu màn hình terminal như sau thì máy bạn đã có (bỏ qua bước cài đặt):

.. image:: ../img/img_6.png
   :alt: alternate text

- Nếu không xuất hiện màn hình như trên thì cài openOCD:

.. code-block:: console

    sudo apt update
    sudo apt upgrade
    git clone https://github.com/openocd-org/openocd.git
    cd openocd
    ./bootstrap
    ./configure -–prefix=/usr/local –enable-ftdi –enable-stlink
    make
    sudo make install


- Tìm đường dẫn đến openocde lưu trong máy:

.. code-block:: console

    which openocd

**Tham khảo cách cài đặt:** `OPENOCD <https://www.youtube.com/watch?v=FNDp1G0bYoU>`_.

Bước 2: Cài đặt các extension trong vscode
---------------------------------------------------------------------------

.. image:: ../img/img_7.png
   :alt: alternate text

.. image:: ../img/img_8.png
   :alt: alternate text

.. image:: ../img/img_9.png
   :alt: alternate text

Bước 3: Thêm các file json để debug được trên vscode
---------------------------------------------------------------------------

- Thêm một thư mục .vscode gồm có hai file setting.json và launch.json

- *Lưu ý đổi thành đúng tên user mà máy tính các bạn đã cài đặt trên máy.*

**Nội dung file setting.json**

.. code-block:: console

    {
        "terminal.integrated.env.windows": 
        {
            "PATH": "/home/dongkhoa/zephyrproject/zephyr/scripts;${env:PATH}",
            "ZEPHYR_BASE": "/home/dongkhoa/zephyrprojec/zephyr"
        }
    }


**Nội dung file launch.json**

.. code-block:: console

    {
        "version": "0.2.0",
        "configurations": 
        [
            {
                "name": "STM32Debug",
                "device": "STM32F746G_Disco",
                "gdbPath": "/home/dongkhoa/zephyr-sdk-0.16.4/arm-zephyr-eabi/bin/arm-zephyr-eabi-gdb",
                "cwd": "${workspaceFolder}",
                "executable": "${workspaceFolder}/build/zephyr/zephyr.elf",
                "request": "launch",
                "type": "cortex-debug",
                "servertype": "openocd",
                "interface": "swd",
                "configFiles":["/home/dongkhoa/zephyrproject/zephyr/boards/arm/stm32f746g_disco/support/openocd.cfg"],
                "runToEntryPoint": "main",
                "postRestartCommands": [
                    "break main",
                    "continune"
                ]
            }
        ]
    }



Bước 4: Debug
---------------------------------------------------------------------------

**Chọn vào nút màu xanh để bắt đầu debug**

.. image:: ../img/img_10.png
   :alt: alternate text