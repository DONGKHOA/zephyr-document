Message queue
===============================================================================


.. contents::
    :local:
    :depth: 2

Tổng quan
*******************************************************************************

Các hoạt động (Implementation) có trong messeage queue
*******************************************************************************

Định nghĩa message queue
-------------------------------------------------------------------------------

.. code-block:: c

    struct data_item_type {
        uint32_t field1;
        uint32_t field2;
        uint32_t field3;
    };

    char my_msgq_buffer[10 * sizeof(struct data_item_type)];
    struct k_msgq my_msgq;

    k_msgq_init(&my_msgq, my_msgq_buffer, sizeof(struct data_item_type), 10);

Có thể thay thế ``k_msgq_init`` bằng ``K_MSGQ_DEFINE``.

.. code-block:: c

    K_MSGQ_DEFINE(my_msgq, sizeof(struct data_item_type), 10, 1);

Ghi dữ liệu vào message queue
-------------------------------------------------------------------------------

Lấy dữ liệu từ message queue
-------------------------------------------------------------------------------

Đọc dữ liệu từ message queue
-------------------------------------------------------------------------------