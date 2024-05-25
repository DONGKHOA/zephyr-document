Workqueue Thread
===============================================================================


.. contents::
    :local:
    :depth: 2


Tổng quan
*******************************************************************************

-   *Workqueue* là một đối tượng trong kernel mà được sử dụng một thread thực 
    thi các công việc *(work items)* theo cơ chế FIFO. Mỗi một công việc được thực 
    thi bằng cách gọi hàm đó. *Workqueue* thường được sử dụng bởi các ngắt và các thread 
    có mức độ ưu tiên cao để xử lý các công việc không khẩn cấp sang các thread có mức 
    ưu tiên thấp hơn để không ảnh hướng đến thời gian chạy của hệ thống. Ngoài ra nó còn 
    được dùng để các hàm init (khởi tạo cho các module khác, do các hàm này thường được 
    gọi trong main làm cho ``CONFIG_MAIN_STACK_SIZE`` phải đủ lớn nhưng điều này không còn 
    cần thiết sau khi init xong dẫn đến một vấn đề RAM sẽ bị bỏ phí).

-   Số lượng workqueue chỉ bị giới hạn bởi ram.

Lifecycle
*******************************************************************************

-   Mỗi work item đều đươc định nghĩa và được chỉ định bới một địa chỉ trong 
    vùng nhớ.

-   Một work item được gán cho một **handler function** *(là một function được thực thi trong 
    work queue thread)*.

-   Một delayable work item có đươc lập lịch sau một khoảng thời gian nhất định:

    -   Delayable work item bao gồm một work item tiêu chuẩn và thêm thời gian lập lịch.

    -   Sau khi hết thời gian chờ thì kernel sẽ submit work item và thực hiện như bình 
        thường.

-   Một work item ở trạng thái **running** khi nó được chạy trong workqueue, 
    và nó có ở trạng thái **canceling** nếu được yêu cầu cancel trước khi nó
    chạy.

-   Một work item có thể ở nhiều trạng thái:

    -   Chạy trong workqueue.

    -   Đã đánh dấu cancelling (bởi vì có thread gọi ``k_work_cancel_sync()``, 
        và đợi cho đến khi work item được thực hiện xong).

    -   Queue chạy trên môt queue khác.

    -   Được lập lịch submitted cho một queue (có thể là một queue khác).

Cách sử dụng Workqueues
*******************************************************************************

.. note::

    Dưới đây là cách sử dụng một vài API để sử dung workqueue, tham khảo thêm API 
    khác `tại đây <https://docs.zephyrproject.org/latest/kernel/services/threads/workqueue.html#how-to-use-workqueues>`_.


Cách sử dụng work item
-------------------------------------------------------------------------------

Submit một work item:

.. code-block:: c

    static uint16_t count = 0;

    struct device_info {
        struct k_work work;
        char name[10];
    };

    struct device_info device_user;

    void print_mess(struct k_work *item)
    {
        struct device_info *device = 
                CONTAINER_OF(item, struct device_info, work);
        printf("%s, %d\n", device->name, count);
        count++;
    }

    int main()
    {
        /* initialize name info for a device */
        strcpy(device_user.name, "Dong Khoa");

        /* initialize work item for print name of device*/
        k_work_init(&device_user.work, print_mess);
        while (1)
        {
            /* submit work item every after 100ms */
            k_work_submit(&device_user.work);
            k_busy_wait(100000);
        }
        

        return 0;
    }

Các thư viện được ``#include`` vào project:

.. code-block:: c

    #include "zephyr/kernel.h"
    #include "zephyr/sys/printk.h"
    #include "string.h"

Build và chạy mô phỏng đoạn code trên:

.. code-block:: c

    west build -b qemu_x86
    west build -t run


.. important:: 

    Nếu sử dụng ``k_work_submit()`` thì sẽ được chạy trên *system queue*.

Định nghĩa và điều khiển Workqueues
-------------------------------------------------------------------------------

Thư viện được ``#inlcude`` giống ở phần trên:

Khởi tạo và bắt đầu cho Workqueue:

.. code-block:: c

    #define STACK_SIZE 500
    #define PRIORITY 5

    K_THREAD_STACK_DEFINE(my_stack_area, STACK_SIZE);

    struct k_work_q my_work_q;

    int main()
    {
        k_work_queue_init(&my_work_q);

        k_work_queue_start(&my_work_q, my_stack_area,
                            K_THREAD_STACK_SIZEOF(my_stack_area),
                            PRIORITY, NULL);

        return 0;
    }

Submit work item vào workqueue:

.. code-block:: c

    #include "zephyr/kernel.h"
    #include "zephyr/sys/printk.h"
    #include "string.h"

    #define STACK_SIZE 1024
    #define PRIORITY 5

    K_THREAD_STACK_DEFINE(my_stack_area, STACK_SIZE);

    struct k_work_q my_work_q;

    static uint16_t count = 0;

    struct device_info {
        struct k_work work;
        char name[10];
    };

    struct device_info device_user;

    void print_mess(struct k_work *item)
    {
        struct device_info *device = 
            CONTAINER_OF(item, struct device_info, work);
        printk("%s, %d\n", device->name, count); // Use printk instead of printf
        count++;
    }

    int main()
    {
        printk("Workqueue example\n");
        
        /* initialize name info for a device */
        strcpy(device_user.name, "Dong Khoa");

        /* initialize work item for print name of device*/
        k_work_init(&device_user.work, print_mess);

        k_work_queue_init(&my_work_q);

        k_work_queue_start(&my_work_q, my_stack_area,
                            K_THREAD_STACK_SIZEOF(my_stack_area),
                            PRIORITY, NULL);

        while (1)
        {
            /* submit work item every after 100ms */
            k_work_submit_to_queue(&my_work_q ,&device_user.work);
            k_busy_wait(100000);

            /* Delay to ensure work item execution */
            k_sleep(K_MSEC(1));
        }

        return 0;
    }

Lập lịch cho Delayable Work Item
-------------------------------------------------------------------------------

.. code-block:: c

    #include <zephyr/kernel.h>
    #include <zephyr/sys/printk.h>
    #include <string.h>

    #define STACK_SIZE 1024
    #define PRIORITY 5

    K_THREAD_STACK_DEFINE(my_stack_area, STACK_SIZE);


    static uint16_t count = 0;

    struct device_info {
        struct k_work_delayable my_delayed_work;
        char name[10];
    };

    struct device_info device_user;

    void delayed_work_handler(struct k_work *item)
    {
        struct device_info *device = 
                CONTAINER_OF(item, struct device_info, my_delayed_work.work);
        printk("%s, %d\n", device->name, count++);
        k_busy_wait(100000);
        k_work_reschedule(&device->my_delayed_work, K_NO_WAIT); // Resubmit the workqueue
    }

    int main(void)
    {
        printk("Delayable Work Item example\n");

        /* Initialize name info for a device */
        strcpy(device_user.name, "Dong Khoa");

        /* Initialize delayed work item */
        k_work_init_delayable(&device_user.my_delayed_work, &delayed_work_handler);

        /* Submit the delayed work item to start */
        k_work_schedule(&device_user.my_delayed_work, K_NO_WAIT);

        /* Infinite loop */
        while (1) {
            k_sleep(K_FOREVER);
        }
        return 0;
    }


Có hai trường hợp sử dụng delayable work item, tùy thuộc vào có gia hạn khi có sự kiến mới 
xảy ra. Ví dụ như là nhận kí từ từ *UART*:

-   ``k_work_schedule()`` (hoặc ``k_work_schedule_for_queue()``) lập lịch work thực hiện tại 
    một thời điểm nhất định (sau thời gian ``delay``). Sử dụng để lấy data sau một khoảng thời gian delay 
    kể từ lúc nhận được data chưa xử lý đầu tiên.

-   ``k_work_reschedule()`` (hoặc ``k_work_reschedule_for_queue()``). Sử dụng để lấy data sau một khoảng 
    thời gian delay kể từ khi nhân được data chưa xử lý cuối cùng.

.. note:: 

    ``k_work_schedule()`` và ``k_work_reschedule()`` đều có tham số  ``delay``. 
    Nếu ``delay`` được truyền vào là ``K_NO_WAIT`` thì nó sẽ tương tự với 
    ``k_work_submit_to_queue()``.

Một số trường hợp cần sử dụng Workqueue
*******************************************************************************

-   Tránh *race condition*

-   Kiểm tra giá trị trả về.

-   Tối ưu hóa.

.. note::

    Xem thêm `best practices <https://docs.zephyrproject.org/latest/kernel/services/threads/workqueue.html#workqueue-best-practices>`_.


.. important::

    Sử dụng workqueue để trì hoãn quá trình xử lý ngắt phức tạp để ISR có thể chia sẽ dử liệu với thread. 
    Điều này cho phép quá trình xử lý liên quan đến ngắt được thực hiện kịp thời mà không ảnh hưởng đến 
    khả năng phản hồi của hệ thống với các lần ngắt tiếp theo.