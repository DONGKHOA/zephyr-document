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

-   Một delayable work item có đươc lên lịch sau một khoảng thời gian nhất định:

    -   Delayable work item bao gồm một work item tiêu chuẩn và thêm thời gian lên lịch.

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

Định nghĩa và điều khiển Workqueues
-------------------------------------------------------------------------------

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