from django.urls import path
from .views import CustomerSaleItemsAPIView, RegisterView, LoginView, ResetPasswordAPIView, TodoTaskListCreate, TodoTaskRetrieveUpdateDestroy, UpdateProfilePictureView, UploadDocumentsView, UploadProfilePictureView, UserListView, UserUpdateView, UserDeleteView, \
    StockOpeningCreateView, StockOpeningListView, StockOpeningDetailView,UserDetailView,StockOpeningTotalWeightView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    path('users/', UserListView.as_view(), name='user-list'),
    path('users/username=<str:username>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:user_id>/update/', UserUpdateView.as_view(), name='user-update'),
    path('users/<int:user_id>/delete/', UserDeleteView.as_view(), name='user-delete'),

    # StockOpening APIs
    path('stockopening/', StockOpeningCreateView.as_view(), name='stockopening-create'), # POST
    path('stockopening/list/', StockOpeningListView.as_view(), name='stockopening-list'), # GET all
    path('stockopening/<int:pk>/', StockOpeningDetailView.as_view(), name='stockopening-detail'), # GET, PUT, DELETE by id
    path('stockopening/total-weight/', StockOpeningTotalWeightView.as_view(), name='stockopening-total-weight'),

    path('purchase-items/<int:customer_id>/', CustomerSaleItemsAPIView.as_view(), name='customer-sale-items'),

    path('upload/profile/', UploadProfilePictureView.as_view(), name='upload-profile'),
    path('update-profile-picture/', UpdateProfilePictureView.as_view()),

    path('upload/documents/', UploadDocumentsView.as_view(), name='upload-documents'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset password'),

    path('todo-tasks/', TodoTaskListCreate.as_view(), name='task-list-create'),
    path('todo-tasks/<int:pk>/', TodoTaskRetrieveUpdateDestroy.as_view(), name='task-detail-update-delete'),


]
