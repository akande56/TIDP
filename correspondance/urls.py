from django.urls import path
from .views import (
   Correspondance,
   RecieverClearicalFiles,
   SenderClearicalFiles,
   downloadfile,
   NewMail,
   ProtocolView,
   ProtocolViewMemo,
   SenderProtocolFiles,
   CorrespondanceDetails,
)

urlpatterns = [
    path('new/mail/', NewMail.as_view(), name='new_mail'),
    path('', Correspondance.as_view(), name='correspondance'),
    path('<int:id>/', CorrespondanceDetails.as_view(), name='correspondance_details'),
    path('clear/<int:id>/s/', RecieverClearicalFiles.as_view(), name='reciever_clear'),
    path('clear/<int:id>/r/', SenderClearicalFiles.as_view(), name='sender_clear'),
    path('protocol/<int:id>/r/', SenderProtocolFiles.as_view(), name='protocol_approved'),
    path('protocol/view', ProtocolView.as_view(), name='protocol_view'),
    path('protocol/<int:id>/view/', ProtocolViewMemo.as_view(), name='protocol_view_memo'),
    path('download/<int:id>/', downloadfile, name='download_file'),
]

