from django.urls import path
from .views import AddPurchaseInvoiceAPIView, AddPurchaseItemAPIView, BhishiAttachmentListAPI, BhishiAttachmentUploadAPI, BhishiCreateAPI, BhishiDashboardAPI, BhishiGetUpdateAPI, BhishiListAPI, BhishiPaymentAPI, BhishiPaymentDetailsAPIView, CustomerAllTransactionDetailAPIView, InstallmentAttachmentCreateAPIView, InstallmentAttachmentListAPIView, ItemPaymentDetailAPIView,BhishiPaymentHistoryAPI, LoanAttachmentCreateAPIView, LoanAttachmentListAPIView, LoanCompletionAttachmentUploadAPIView, LoanCompletionAttachmentListAPIView, LoanCompletionAttachmentDetailAPIView, LoanCompletionAttachmentByLoanAPIView, OrderAttachmentRetrieveAPIView, BhishiReportPDFView, BillingDetailAPIView, CraftsmanAttachmentDeleteAPIView, DeleteBhishiAPIView,DiamondBillingDeleteAPIView, CraftsmanAttachmentListAPIView, CraftsmanAttachmentUploadAPIView, OrderMarkCompletedAPIView, OrderAttachmentUploadAPIView, SupplierAttachmentDeleteAPIView,SupplierAttachmentUploadAPIView, SupplierAttachmentListAPIView,CustomerListCreateAPIView, CustomerDetailAPIView,SaleInvoiceBatchDetailAPIView, CustomerPaymentSummaryAPIView, InventoryValueAPIView, ItemPaymentHistoryAPIView, JobWorkDeleteAPIView,JobWorkListAPIView,JobWorkDetailAPIView,ItemPaymentGetAPIView, DiamondBillingCreateAPIView, InstallmentDetailAPIView, InstallmentListByPaymentAPIView, ItemPaymentCreateAPIView, ItemPaymentListAPIView, InstallmentEntryListAPIView,DeleteOrderAPIView, JobWorkCreateAPIView, LoanCreateAPIView, LoanDeleteAPIView, LoanDetailAPIView, LoanListAPIView,SaleItemBulkUpdateAPIView, LoanPaymentAPIView, LoanPaymentAddAPIView, LoanPaymentCreateAPIView, LoanPaymentDetailsAPIView, LoanSoftDeleteAPIView, LoanUpdateAPIView,MetalListCreateAPIView, MetalDetailAPIView,CaratListCreateAPIView, CaratDetailAPIView,AddJewelryAPIView,JewelryListAPIView,JewelryDetailAPIView,JewelryUpdateAPIView,JewelryDeleteAPIView, MetalRateAPIView, MetalRateCreateAPIView, MetalRateListAPIView, MetalRateUpdateAPIView, NotificationListAPIView, OrderManagementCreateView, OrderStatusListView, OrderStatusUpdateView, OrderUpdateAPIView, PurchaseInvoiceDetailAPIView, PurchaseInvoiceListAPIView, PurchaseItemDeleteAPIView, PurchaseItemListAPIView, PurchaseVoucherCreateAPIView, PurchaseVoucherDetailAPIView, PurchaseVoucherListAPIView, SaleInvoiceDetailAPIView,SaleItemCreateAPIView, SaleItemDeleteAPIView, SaleItemDetailAPIView, SaleItemListCreateAPIView, BulkSaleItemDeleteAPIView, OrderCreateAPIView,OrderListAPIView,OrderDetailAPIView, SalesSummaryAPIView, TotalStockAPIView,TransactionListAPIView, URDAdjustmentCreateAPIView, URDAdjustmentListView, UpdateInstallmentStatusAPIView, UpdatePurchaseItemAPIView
from .reportView import AllTransactionHistoryAPIView, GSTReportAPIView, KaragirReportAPIView, SaleItemDetailRawSQL, SalesReportAPIView, SupplierBalanceReportAPIView, TransactionHistoryAPIView, WhatsAppSendAPIView


urlpatterns = [
    path('customers/', CustomerListCreateAPIView.as_view(), name='customer-list-create'),
    path('customers/<int:customer_id>/', CustomerDetailAPIView.as_view(), name='customer-detail'),
    path(
        "customer-full-details/<int:customer_id>/",
        CustomerAllTransactionDetailAPIView.as_view(),
        name="customer-full-details"
    ),

    path('metals/', MetalListCreateAPIView.as_view(), name='metal-list-create'),
    path('metals/<int:id>/', MetalDetailAPIView.as_view(), name='metal-detail'),
    path('precious-metal/inventory/', TotalStockAPIView.as_view(), name='metal-inventory'),
    path("inventory-value/", InventoryValueAPIView.as_view(), name='metal-value'),

    # Carat CRUD
    path('carats/', CaratListCreateAPIView.as_view(), name='carat-list-create'),
    path('carats/<int:id>/', CaratDetailAPIView.as_view(), name='carat-detail'),

    path('add-jewelry/', AddJewelryAPIView.as_view(), name='add-jewelry'),
    path('jewelry/add/', AddJewelryAPIView.as_view(), name='add-jewelry'),
    path('jewelry/list/', JewelryListAPIView.as_view(), name='list-jewelry'),
    path('jewelry/<int:pk>/', JewelryDetailAPIView.as_view(), name='detail-jewelry'),
    path('jewelry/update/<int:pk>/', JewelryUpdateAPIView.as_view(), name='update-jewelry'),
    path('jewelry/delete/<int:pk>/', JewelryDeleteAPIView.as_view(), name='delete-jewelry'),


    path('sale-item/add/', SaleItemCreateAPIView.as_view(), name='add-sale-item'),
    path("sale-item/", SaleItemListCreateAPIView.as_view(), name="saleitem-list-create"),
    path("sale-item/<int:pk>/", SaleItemDetailAPIView.as_view(), name="saleitem-detail"),
    path('saleitems/<int:id>/delete/', SaleItemDeleteAPIView.as_view(), name='saleitem-delete'),
    path('saleitems/bulk-delete/', BulkSaleItemDeleteAPIView.as_view(), name='saleitem-bulk-delete'),
    path("sale-invoice-details/", SaleInvoiceDetailAPIView.as_view()),
    path("saleitems-invoice-details/", SaleInvoiceBatchDetailAPIView.as_view()),

    path('sale-item/bulk-update/', SaleItemBulkUpdateAPIView.as_view(), name='sale-item-bulk-update'),

    path('urd-adjustments/', URDAdjustmentCreateAPIView.as_view(), name='urd-adjustment-create'),
    path('item-payment-history/', ItemPaymentHistoryAPIView.as_view(), name='payment-history'),

    path('add-item-payment/', ItemPaymentCreateAPIView.as_view(), name='add-item-payment'),
    
    path('payments-installments/', ItemPaymentListAPIView.as_view(), name='item-payment-list'),
    path('payments-installments/<int:master_id>/', InstallmentDetailAPIView.as_view(), name='installment-detail'),

    path('add-order/', OrderCreateAPIView.as_view(), name='add-order'),
    path('order/attachment/upload/', OrderAttachmentUploadAPIView.as_view(), name='order-attachment-upload'),
    path('order/attachment/get/', OrderAttachmentRetrieveAPIView.as_view(), name='order-attachment-get'),
    path("orders/", OrderListAPIView.as_view(), name="order-list"),
    path("orders/<int:order_id>/", OrderDetailAPIView.as_view(), name="order-detail"),
    path('order/delete/<int:order_id>/', DeleteOrderAPIView.as_view(), name='delete-order'),
    path('order/update/<int:order_id>/', OrderUpdateAPIView.as_view(), name='order-update'),


    path("create-diamond-billing/", DiamondBillingCreateAPIView.as_view(), name="order-list"),
    path('diamond-billing/list/', TransactionListAPIView.as_view(), name='transaction-list'),
    path('billing/<int:billing_id>/', BillingDetailAPIView.as_view(), name='billing-detail'),
    path('diamond-billing/delete/<int:billing_id>/', DiamondBillingDeleteAPIView.as_view(), name='diamond-billing-delete'),

    #path('loans/add/', LoanCreateAPIView.as_view(), name='loan-add'),
# urls.py

    path('loan/attachment/add/', LoanAttachmentCreateAPIView.as_view(), name='loan-attachment-add'),
    path('loan/attachment/list/', LoanAttachmentListAPIView.as_view(), name='loan-attachment-list'),
    
    # ✅ Loan Completion Attachment APIs
    path('loan/completion/attachment/upload/', LoanCompletionAttachmentUploadAPIView.as_view(), name='loan-completion-attachment-upload'),
    path('loan/completion/attachments/', LoanCompletionAttachmentListAPIView.as_view(), name='loan-completion-attachment-list'),
    path('loan/completion/attachments/<int:attachment_id>/', LoanCompletionAttachmentDetailAPIView.as_view(), name='loan-completion-attachment-detail'),
    path('loan/<int:loan_id>/completion/attachments/', LoanCompletionAttachmentByLoanAPIView.as_view(), name='loan-completion-attachments-by-loan'),
    
    path('loans/add/', LoanCreateAPIView.as_view(), name='loan-create'),
    path('loan/list/', LoanListAPIView.as_view(), name='loan-list'),
    path('loan/<int:id>/', LoanDetailAPIView.as_view(), name='loan-detail'),
    path('loan/update/<int:id>/', LoanUpdateAPIView.as_view(), name='loan-update'),
    path("loan/delete/<int:loan_id>/", LoanSoftDeleteAPIView.as_view(), name="loan-soft-delete"),
    path('loan/paymentcreate/', LoanPaymentAddAPIView.as_view(), name='loan-add payment'),
    path('loan-delete/<int:loan_id>/', LoanDeleteAPIView.as_view(), name='loan-delete'),
    path('loanpayment-details/', LoanPaymentDetailsAPIView.as_view(), name='loanpayment-details'),

    path('loan/payment/', LoanPaymentAPIView.as_view(), name='loan-payment'),
    path("make/loan-payment/", LoanPaymentCreateAPIView.as_view(), name="loan-payment-create"),


    path('add-ordermanagement/', OrderManagementCreateView.as_view(), name='add-order'),

    path('all-orders/', OrderStatusListView.as_view(), name='order-status-list'),
    path('orders/<int:pk>/update-status/', OrderStatusUpdateView.as_view(), name='order-status-update'),

    path("jobwork/add/", JobWorkCreateAPIView.as_view(), name="jobwork-add"),
    path("orders/mark-completed/",
            OrderMarkCompletedAPIView.as_view(),
            name="order-mark-completed"
        ),
    path(
            "itempayment-list/",
            ItemPaymentGetAPIView.as_view(),
            name="itempayment-get"
        ),
    path("item-payment/details/",
        ItemPaymentDetailAPIView.as_view(),
        name="item-payment-details"
    ),
    path('job-works/', JobWorkListAPIView.as_view(), name='jobwork-list'),
    path('job-works/<int:id>/', JobWorkDetailAPIView.as_view(), name='jobwork-detail'),
    path("metalrate/add/", MetalRateCreateAPIView.as_view(), name="metalrate-add"),
    path('update-metal-rate/<int:pk>/', MetalRateUpdateAPIView.as_view(), name='update-metal-rate'),
    path('order-management/delete/<int:jobwork_id>/', JobWorkDeleteAPIView.as_view(), name="jobwork-delete"),
    #path("delete-jobwork/<int:id>/", JobWorkDeleteAPIView.as_view(), name="delete-jobwork"),

    path("metalrate/list/", MetalRateListAPIView.as_view(), name="metalrate-list"),
    path('todays-sale/', SalesSummaryAPIView.as_view(), name='urd-adjustment-create'),
    path('todays-metal-rate/', MetalRateAPIView.as_view(), name='metal-rate'),



    path('purchase-voucher/create/', PurchaseVoucherCreateAPIView.as_view(), name='purchase-voucher-create'),
    path('purchase-voucher/list/', PurchaseVoucherListAPIView.as_view(), name='purchase-voucher-list'),
    path('purchase-voucher/detail/<int:pk>/', PurchaseVoucherDetailAPIView.as_view(), name='purchase-voucher-detail'),


    path('add-purchase-item/', AddPurchaseItemAPIView.as_view(), name='purchase-item-detail'),
    path('purchase-items/update/<int:pk>/', UpdatePurchaseItemAPIView.as_view(), name='update-purchase-item'),
    path('purchase-items/', PurchaseItemListAPIView.as_view(), name='list-purchase-items'),
    path('purchase-items/<int:pk>/delete/', PurchaseItemDeleteAPIView.as_view(), name="purchase-item-delete"),

    path('purchase-invoice/add/', AddPurchaseInvoiceAPIView.as_view(), name='add-purchase-invoice'),
    path('purchase-invoices/', PurchaseInvoiceListAPIView.as_view(), name="purchase-invoice-list"),
    path("purchase-invoice-details/", PurchaseInvoiceDetailAPIView.as_view()),

    path('installment-entry-list/', CustomerPaymentSummaryAPIView.as_view(), name='installment-entry-list'),
    path('all-installment/<int:item_payment_id>/', InstallmentListByPaymentAPIView.as_view(), name='all-installment'),
    path('installments/update-payment/', UpdateInstallmentStatusAPIView.as_view(), name='update-installment-status'),
    path('installment-attachment/add/', InstallmentAttachmentCreateAPIView.as_view(), name='installment-attachment-add'),
    path('installment-attachment/<int:installment_id>/', InstallmentAttachmentListAPIView.as_view(), name='installment-attachment-list'),

    path('customer-balance-report/', SaleItemDetailRawSQL.as_view(), name='all-sale-items-raw-sql'),
    path('transaction-history/', TransactionHistoryAPIView.as_view(), name='transaction-history'),

    path('karagir-report/', KaragirReportAPIView.as_view(), name='karagir-report'),
    path("craftsman/attachments/upload/", CraftsmanAttachmentUploadAPIView.as_view(), name="craftsman-attachment-upload"),
    path("craftsman/attachments/<int:jobwork_id>/", CraftsmanAttachmentListAPIView.as_view(), name="craftsman-attachment-list"),

    path("supplier-balance-report/", SupplierBalanceReportAPIView.as_view(), name="supplier-balance-report"),
    path("sales-report/", SalesReportAPIView.as_view(), name="sales-report"),
    path("gst-report/", GSTReportAPIView.as_view(), name="sales-report"),
    path("customer_ledger-report/", AllTransactionHistoryAPIView.as_view(), name="sales-report"),
    path('supplier/attachment/upload/', SupplierAttachmentUploadAPIView.as_view(), name='supplier-attachment-upload'),
    path('supplier/attachment/list/<int:purchase_invoice_id>/', SupplierAttachmentListAPIView.as_view(), name='supplier-attachment-list'),

    path('urd-adjustmentslist/', URDAdjustmentListView.as_view(), name='urdadjustment-list'),      # 🔹 All records
    #path('urd-adjustments/', URDAdjustmentListView.as_view(), name='urdadjustment-detail'),  # 🔹 One record
    path('get-notification/', NotificationListAPIView.as_view(), name='notification-list'),      # 🔹 All records


    path("send-whatsapp/", WhatsAppSendAPIView.as_view(), name="send-whatsapp"),

    path(
        "craftsman-attachments/<int:attachment_id>/delete/",
        CraftsmanAttachmentDeleteAPIView.as_view(),
        name="delete-craftsman-attachment"
    ),

    path(
        "supplier-attachments/<int:attachment_id>/delete/",
        SupplierAttachmentDeleteAPIView.as_view(),
        name="delete-supplier-attachment"
    ),


    path("bhishi/create/", BhishiCreateAPI.as_view(), name="bhishi-create"),
    path("bhishi/<int:pk>/", BhishiGetUpdateAPI.as_view(), name="bhishi-get-update"),
    path("bhishi/payment/", BhishiPaymentAPI.as_view(), name="bhishi-payment"),

    path('bhishi-list/', BhishiListAPI.as_view(), name='bhishi-list'),
    path('bhishi-paymentshistory/', BhishiPaymentHistoryAPI.as_view(), name='bhishi-payment-history'),
    path('bhishi-dashboard/', BhishiDashboardAPI.as_view(), name='bhishi-dashboard'),
    path('bhishi/<int:pk>/report/', BhishiReportPDFView.as_view(), name='bhishi-report-pdf'),
    path("bhishi/<int:bhishi_id>/delete/", DeleteBhishiAPIView.as_view(), name="delete-bhishi"),
    path("bhishi/payments/details/", BhishiPaymentDetailsAPIView.as_view(), name="bhishi-payment-details"),
    # urls.py

    path('bhishi/attachment/upload/', BhishiAttachmentUploadAPI.as_view(), name='bhishi-attachment-upload'),
    path('bhishi/attachment/list/', BhishiAttachmentListAPI.as_view(), name='bhishi-attachment-list'),

]