from django.urls import path
from .views import (
    Procurement,
    RegisterContractor,
    PrecurementListView,
    # ContractorsUpdateView,
    update_contractor_status,
    PrecurementCreateView,
    contractor_document_list,
    create_contractor_document,
    fetch_contractors,
    PrecurementDetailView,
    procurement_edit,
    procurement_delete,
    procurement_list,
    procurement_files,
)

urlpatterns = [
    path('register', RegisterContractor.as_view(), name='contractor_register'),
    path('contractors/', Procurement.as_view(), name='procurement'),
    path('create/', PrecurementCreateView.as_view(), name='precurement_create'),
    path('precurement_list/', PrecurementListView.as_view(),name='precurement_list'), #contains both get and post
    path('contractor/<int:contractor_id>/documents/', contractor_document_list, name='contractor_document_list'),
    path('create_contractor_document/', create_contractor_document, name='create_contractor_document'),
    # path('contractors/<int:contractor_pk>/update/', ContractorsUpdateView.as_view(), name='contractor_update'),
    path('contractor/update_status/<int:contractor_id>/', update_contractor_status, name='update_contractor_status'),
    path('fetch-contractors/', fetch_contractors, name='fetch_contractors'),
    path('procurement/<int:pk>/', PrecurementDetailView.as_view(), name='precurement_detail'),
    path('procurement/<int:pk>/edit/', procurement_edit, name='precurement_edit'),
    path('delete/<int:pk>/', procurement_delete, name='precurement_delete'),
    path('file/procurement_list', procurement_list, name='fprocurement_list'),
    path('file/procurement_list/file_list/<int:pk>/', procurement_files, name='procurement_Filelist'),
]