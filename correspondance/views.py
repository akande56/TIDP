from datetime import datetime
from pyexpat import model
from venv import create
from django import forms
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.views.generic import View
from django.http import response, JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.utils.decorators import method_decorator
from accounts.models import Account
from accounts.decorators import user_passes_test, is_persona_tier_12 
from home.models import Unit
from .models import (
    Folder,
    File,
    Folder_Content,
    Routing,
    Comment
)
from .forms import (
    InternalMemoForm,
    MinuteOnMemoForm,
    UploadFileForm,
    CommentForm,
    CombineInternalMemoForm_UploadForm,
)
import random
import string
from django.contrib import messages
from config.utility import set_cookie
from django.template.response import TemplateResponse
import os
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes
from django.db.models import Q
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

# Create your views here.
def downloadfile(request, id):
    file = File.objects.get(id=id)
    the_file = file.media.path
    filename = os.path.basename(the_file)
    chunck_size = 8092
    response = StreamingHttpResponse(FileWrapper(open(the_file, 'rb'), chunck_size),
                                     content_type=mimetypes.guess_type(the_file[0]))
    response["Content-Length"] = os.path.getsize(the_file)
    response["Content-Disposition"] = "Attachment;filename=%s" % filename
    return response


class Correspondance(LoginRequiredMixin, View):
    template_name = "new/correspondance.html"

    def get(self, request, **kwargs):
        account = Account.objects.get(user=request.user)
        account_id = account.id
        unit = Unit.objects.get(users=account)
        routes = Routing.objects.filter(initiated_unit=1)
        context = {
            'form': InternalMemoForm,
            'value': 2,
            "internal": 2,
        }
        if account.user_persona.persona_tier <= 5:
            context['unread'] = Routing.objects.filter(
                send_to=account, viewed=False, reciever_stage='Done').count()
            context['incoming_mails'] = Routing.objects.filter(send_to_id=account_id,
                intended_unit=unit, sender_stage='Done', reciever_stage='Done'
                )
            context['send_memos'] = Routing.objects.filter(
                forwarded_by=account)
            context['drafts'] = Folder.objects.filter(
                draft=True, created_by=account)
        elif account.user_persona.persona_tier == 6:
            context['clearing_mails'] = Routing.objects.filter(
                (Q(initiated_unit=unit) |
                 Q(intended_unit=unit, sender_stage="Done"))
            )
            context['incoming_mails'] = Routing.objects.filter(
                (Q(initiated_unit=unit) |
                 Q(intended_unit=unit, sender_stage="Done")),
                
            )
            context['outgoing_mails'] = Routing.objects.filter(
                initiated_unit=unit, forwarded_by=account)
        elif account.user_persona.persona_tier == 7:
            context['memos'] = Routing.objects.filter(
                Q(sender_stage="Done", reciever_stage="Protocol", intended_unit=unit) |
                Q(intended_unit=unit, sender_stage="Done")
            )
        print(context)
        return render(request, self.template_name, context)


class CorrespondanceDetails(LoginRequiredMixin, View):

    def get(self, request, id, **kwargs):
        account = Account.objects.get(user=request.user)
        route   = Routing.objects.get(id=id)
        folders = Folder_Content.objects.filter(folder=route.folder)
        files = File.objects.filter(folder_content__in=folders)
        

        form_initials = {
            "content_type": route.get_content_type,
            "object_id": route.id
        }
        form = CommentForm(initial=form_initials)

        context = {
            'memo': route,
            'folders': folders,
            'files': files,
            'comment_form': form
        }
        return render(request, 'new/message_details.html', context)

    def post(self, request, id, *args):
        route = Routing.objects.get(id=id)
        form = CommentForm(request.POST)
        print(form.errors)
        if form.is_valid():
            c_type = form.cleaned_data.get("content_type")
            content_type = ContentType.objects.get(pk=c_type)
            obj_id = form.cleaned_data.get('object_id')
            content_data = form.cleaned_data.get("content")
            account = Account.objects.get(user=request.user)
            Comment.objects.create(
                account=account,
                content_type=content_type,
                object_id=obj_id,
                content=content_data
            )
        return redirect("correspondance_details", id=id)




class NewMail(LoginRequiredMixin, View):
    template_name = "new/new_mail.html"

    def get(self, request, **kwargs):
        account = Account.objects.get(user=request.user)
        form = CombineInternalMemoForm_UploadForm()
        # User Persona is Minister/DG
        if account.user_persona.persona_tier == 1:
            exclude_my_department = Unit.objects.exclude(
                id=account.unit_set.first().id)
            other_departments = Unit.objects.filter(unit_type='Secretery')
            form.fields['send_to'].queryset = exclude_my_department
        elif account.user_persona.persona_tier == 2:
            exclude_my_department = Unit.objects.exclude(
                id=account.unit_set.first().id)
            other_departments = Unit.objects.filter(
                Q(unit_type='Minister/DG') | Q(unit_type='Department'))
            form.fields['send_to'].queryset = exclude_my_department
        elif account.user_persona.persona_tier == 3:
            exclude_my_department = Unit.objects.exclude(
                id=account.unit_set.first().id)
            other_departments = Unit.objects.filter(
                Q(unit_type='Secretery') | Q(unit_type='Department'))
            form.fields['send_to'].queryset = exclude_my_department
        elif account.user_persona.persona_tier == 4:
            exclude_my_department = Unit.objects.exclude(
                id=account.unit_set.first().id)
            other_departments = Unit.objects.filter(unit_type='Department')
            form.fields['send_to'].queryset = exclude_my_department
        elif account.user_persona.persona_tier == 5:
            exclude_my_department = Unit.objects.exclude(
                id=account.unit_set.first().id)
            other_departments = Unit.objects.filter(unit_type='Department')
            form.fields['send_to'].queryset = exclude_my_department
        elif account.user_persona.persona_tier == 6:
            my_department = Unit.objects.filter(id=account.unit_set.first().id)
            form.fields['send_to'].queryset = my_department
        else:
            form = None
        
        context = {
            'form': form,
            'value': 2,
            "internal": 1,
        }
        
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = CombineInternalMemoForm_UploadForm(request.POST, request.FILES)
        if form.is_valid():
            account = Account.objects.get(user=request.user)
            files_list = request.FILES.getlist('media')
            # print('files list...')
            # print(files_list)
            # print('2nd file ist')
            # print(request.FILES)
            with transaction.atomic():
                # Create a new Folder instance
                folder = Folder(
                    title=form.cleaned_data["title"],
                    urgent=form.cleaned_data["urgent"]
                )
                
                identifier = ''.join(random.choice(
                    string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
                folder.unique_identifier = identifier
                folder.created_by = account
                folder.draft = True
                folder.save()

                # Create Folder_Content instance
                f_content = Folder_Content.objects.create(
                    folder=folder,
                    created_by=account,
                    content=form.cleaned_data['content'],
                    title=folder.title
                )

                # Get the current unit
                current_unit = Unit.objects.get(users=account)
                print('current user unit')
                print(current_unit)
                current_user = current_unit.users.filter(
                    Q(user_persona__persona_tier=1) |
                    Q(user_persona__persona_tier=2) |
                    Q(user_persona__persona_tier=3) |
                    Q(user_persona__persona_tier=4) |
                    Q(user_persona__persona_tier=5)
                ).first()
                print('current unit users tier from 1-5')
                print(current_user)

                
                if current_user.user_persona.persona_tier <= 5:
                    print('if the one creating memo is between tier 1-5')
                    
                    print('getting unit clerical officer')
                    
                    # send_to_user = current_unit.users.filter(
                    #     Q(user_persona__persona_tier=6)
                    # ).first()

                    # changed receiving user to intended offive clerical officer
                    send_to_unit = form.cleaned_data['send_to']
                    send_to_user = send_to_unit.users.filter(
                        Q(user_persona__persona_tier=6)
                    ).first()
                    
                    # removing sending to current unit clerical officer
                    # if current_unit.users.filter(user_persona__persona_tier=6).count():
                    #     print('send to clerical office of current unii')
                    #     Routing.objects.create(
                    #         send_to=send_to_user,
                    #         folder=folder,
                    #         forwarded_by=account,
                    #         intended_unit=send_to_unit,
                    #         sender_stage='Clearing',
                    #         initiated_unit=current_unit
                    #     )
                    if send_to_unit.users.filter(user_persona__persona_tier=6).count():
                        rout =Routing.objects.create(
                            send_to=send_to_user,
                            folder=folder,
                            forwarded_by=account,
                            intended_unit=send_to_unit,
                            sender_stage="Done",
                            reciever_stage="Clearing",
                            initiated_unit=current_unit
                        )
                        rout.save()

                    elif send_to_unit.users.filter(user_persona__persona_tier=7).count():
                        rout = Routing.objects.create(
                            send_to=send_to_unit.users.filter(
                        Q(user_persona__persona_tier=7)
                            ).first(),
                            folder=folder,
                            forwarded_by=account,
                            intended_unit=send_to_unit,
                            sender_stage="Done",
                            reciever_stage="Protocol",
                            initiated_unit=current_unit
                        )
                        rout.save()
                    else:
                        rout = Routing.objects.create(
                            send_to=send_to_unit.users.filter(
                                Q(user_persona__persona_tier=1) |
                                Q(user_persona__persona_tier=2) |
                                Q(user_persona__persona_tier=3) |
                                Q(user_persona__persona_tier=4) |
                                Q(user_persona__persona_tier=5)
                            ).first(),
                            folder=folder,
                            forwarded_by=account,
                            intended_unit=send_to_unit,
                            sender_stage="Done",
                            reciever_stage="Done",
                            initiated_unit=current_unit
                        )
                        rout.save()
                        
                elif current_user.user_persona.persona_tier == 6:
                    print('the one creating memo is the clerical officer of the current unit')
                    send_to = current_unit.users.filter(
                        Q(user_persona__persona_tier=1) |
                        Q(user_persona__persona_tier=2) |
                        Q(user_persona__persona_tier=3) |
                        Q(user_persona__persona_tier=4) |
                        Q(user_persona__persona_tier=5)
                    ).first()

                    rout = Routing.objects.create(
                        send_to=send_to,
                        folder=folder,
                        forwarded_by=account,
                        intended_unit=form.cleaned_data['send_to'],
                        sender_stage='Done',
                        reciever_stage='Done',
                        initiated_unit=current_unit
                    )
                    rout.save()
                # Create File instances
                try:
                    for file in files_list:
                        f = File.objects.create(
                            media=file,
                            folder_content=f_content
                        )
                        f.save()
                        print(f)
                except:
                    pass

            messages.success(request, 'Memo Sent Successfully')
        else:
            print(form.errors)

        return redirect('correspondance')



def delete_attachment(request, file_id):
    file_instance = get_object_or_404(File, id=file_id)
    file_instance.delete()
    if 'attachment' in request.session:
        request.session['attachment'] = [item for item in request.session['attachment'] if item['id'] != file_id]
    return JsonResponse({'status': 'success'})



class ProtocolView(LoginRequiredMixin, View):
    template_name = "protocol.html"

    def get(self, request, **kwargs):
        account = Account.objects.get(user=request.user)

        unit = Unit.objects.filter(users=account)
        for instance in unit:
            for user in instance.users.all():
                if user.user_persona.persona_tier <= 5:
                    the_account = user
        context = {
            'memos': Routing.objects.filter(send_to=the_account, reciever_stage="Protocol"),
        }
        return render(request, self.template_name, context)


class ProtocolViewMemo(LoginRequiredMixin, View):

    def get(self, request, id, **kwargs):
        account = Account.objects.get(user=request.user)
        folders = Folder_Content.objects.filter(folder__id=id)
        route = Routing.objects.get(folder=id, send_to=account)

        context = {
            'folders': folders,
            'route': route,
        }
        return render(request, 'protocol_view_memo.html', context)


class SenderProtocolFiles(LoginRequiredMixin, View):

    def get(self, request, id, **kwargs):
        route = Routing.objects.get(id=id)
        route.reciever_stage = 'Done'
        route.save()

        return redirect("correspondancex")


class SenderClearicalFiles(LoginRequiredMixin, View):
    template_name = "clearance.html"

    def get(self, request, id, **kwargs):
        route = Routing.objects.get(id=id)
        route.sender_stage = "Done"
        if route.intended_unit.users.filter(user_persona__persona_tier=7).count() == 1:
            route.reciever_stage = "Protocol"
        else:
            route.reciever_stage = "Clearing"

        route.save()

        return redirect('correspondance')


class RecieverClearicalFiles(LoginRequiredMixin, View):
    template_name = "clearance.html"

    def get(self, request, id, **kwargs):
        account = Account.objects.get(user=request.user)
        current_unit = Unit.objects.get(users=account)

        route = Routing.objects.get(id=id)
        route.reciever_stage = "Done"
        route.send_to = current_unit.users.filter(
                        Q(user_persona__persona_tier=1) |
                        Q(user_persona__persona_tier=2) |
                        Q(user_persona__persona_tier=3) |
                        Q(user_persona__persona_tier=4) |
                        Q(user_persona__persona_tier=5)
                    ).first()
        route.save()

        return redirect('correspondance')


class SendClearStatus(LoginRequiredMixin, View):

    def get(self, request, id, **kwargs):
        route = Routing.objects.get(id=id)
        route.sender_stage = "Done"
        route.reciever_stage = "Clearing"
        route.send = True
        route.save()
        return redirect("clearical_files")


class RecieveClearStatus(LoginRequiredMixin, View):

    def get(self, request, id, **kwargs):
        route = Routing.objects.get(id=id)
        account = Account.objects.get(user="request.user")
        unit = account.unit_set.first()
        for user in unit.users.all():
            if user.user_persona.persona_tier == 7:
                route.reciever_stage = "Protocol"
                route.save()
                return redirect("clearical_files")
            print("NOt protocol")

        route.reciever_stage = "Done"
        route.save()
        return redirect("clearical_files")


'''
class ViewCorrespondance(LoginRequiredMixin, View):
    
    def get(self, request, id, **kwargs):
        account = Account.objects.get(user=request.user)
        folders = Folder_Content.objects.filter(folder__id=id)
        route = Routing.objects.get(folder=id, forwarded_by=account)
        route.viewed = True
        route.save()

        context = {
            'form': MinuteOnMemoForm(),
            'folders': folders,
            
        }
        return render(request, 'new/view_memo.html', context)

    
    def post(self, request, id, **kwargs):
        form = MinuteOnMemoForm(request.POST)
        account = Account.objects.get(user=request.user)
        existing_folder_content = Folder_Content.objects.filter(folder__id=id).first()
        route = Routing.objects.get(send_to=account, folder=existing_folder_content.folder)
        
        if form.is_valid():
            with transaction.atomic():
                Folder_Content.objects.create(
                    folder=existing_folder_content.folder,
                    created_by=account,
                    content=form.cleaned_data["content"],
                )
                route.approved = True
                route.save()
            messages.success(request, 'Memo Appoved Succefully')
        return redirect('correspondance')



class OldCorrespondance(LoginRequiredMixin, View):
    template_name = "correspondance_l.html"
    def get(self, request, **kwargs):
        account = Account.objects.get(user=request.user)

        context = {
            'form': InternalMemoForm,
            'memos': Routing.objects.filter(send_to=account, reciever_stage='Done'),
            'unread': Routing.objects.filter(send_to=account, viewed=False, reciever_stage='Done').count(),
            'send_memos': Routing.objects.filter(forwarded_by=account),
            'drafts': Folder.objects.filter(draft=True, created_by=account)
        }
        return render(request, self.template_name, context)

'''


class NewCorrespondance(LoginRequiredMixin, View):
    template_name = "new_correspondance.html"

    def get(self, request, **kwargs):
        account = Account.objects.get(user=request.user)
        form = InternalMemoForm()
        # User Persona is Minister/DG
        if account.user_persona.persona_tier == 1:
            form.fields['send_to'].queryset = Account.objects.filter(
                user_persona__persona_tier=2)
        elif account.user_persona.persona_tier == 2:
            form.fields['send_to'].queryset = Account.objects.filter(
                Q(user_persona__persona_tier=1) | Q(user_persona__persona_tier=3))
        elif account.user_persona.persona_tier == 3:
            form.fields['send_to'].queryset = Account.objects.filter(
                Q(user_persona__persona_tier=2) | Q(user_persona__persona_tier=4))
        elif account.user_persona.persona_tier == 4:
            form.fields['send_to'].queryset = Account.objects.filter(
                Q(user_persona__persona_tier=3) | Q(user_persona__persona_tier=5))
        elif account.user_persona.persona_tier == 5:
            form.fields['send_to'].queryset = Account.objects.filter(
                Q(user_persona__persona_tier=4))
        elif account.user_persona.persona_tier == 6:
            print(1)
            unit_in = Unit.objects.filter(users=account)
            form.fields['send_to'].queryset = Account.objects.filter()
        else:
            form = None
        context = {
            'form': form,
            'upload_form': UploadFileForm,
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = InternalMemoForm(request.POST or None)
        account = Account.objects.get(user=request.user)
        upload_form = UploadFileForm(request.POST, request.FILES)
        if upload_form.is_valid():
            context = {
                'form': form,
                'upload_form': UploadFileForm
            }
            response = TemplateResponse(
                request, context=context, template=self.template_name)
            instance = upload_form.save()
            instance.name = request.FILES['media'].name
            instance.save()
            try:
                request.session['attachment'] += [instance.media.path, instance.id]
            except KeyError:
                request.session['attachment'] = [
                    instance.media.path, instance.id]
            return response

        if form.is_valid():
            with transaction.atomic():
                folder = form.save(commit=False)
                identifier = ''.join(random.choice(
                    string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
                folder.unique_identifier = identifier
                folder.created_by = account
                folder.draft = False
                folder.save()

                f_content = Folder_Content.objects.create(
                    folder=folder,
                    created_by=account,
                    content=form.cleaned_data["content"],
                    title=folder.title
                )

                Routing.objects.create(
                    send_to=form.cleaned_data["send_to"],
                    folder=folder,
                    forwarded_by=account,
                    sender_stage='Clearing'
                )
                try:
                    for item in request.session['attachment']:
                        attachments = (request.session['attachment'])
                        for i in range(1, len(attachments), 2):
                            file = File.objects.get(
                                id=attachments[i]
                            )
                            file.folder_content = f_content
                            file.save()

                        del request.session['attachment']
                        request.session.modified = True
                except:
                    pass
            messages.success(request, 'Memo Send Successfully')
        return redirect('correspondance')


# class PDFGenerationView(View):
#     def get(self, request, routing_id):
#         # Get the routing object
#         routing = get_object_or_404(Routing, id=routing_id)

#         # Create a response object with PDF content
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="routing_details.pdf"'

#         # Create PDF content using ReportLab
#         p = canvas.Canvas(response, pagesize=letter)

#         # Set font size and style for headers
#         p.setFont("Times-Bold", 16)

#         p.drawString(0.5 * inch, 10 * inch, 'Routing Details')

#         # Set font size and style for sub-headers
#         p.setFont("Times-Bold", 12)

#         # Add routing details
#         p.drawString(0.5 * inch, 9.5 * inch, f'Sender: {routing.forwarded_by}')
#         p.drawString(0.5 * inch, 9 * inch, f'Receiver: {routing.send_to}')
#         p.drawString(0.5 * inch, 8.5 * inch, f'Intended Unit: {routing.intended_unit}')
#         p.drawString(0.5 * inch, 8 * inch, f'Sender Stage: {routing.sender_stage}')
#         p.drawString(0.5 * inch, 7.5 * inch, f'Receiver Stage: {routing.reciever_stage}')

#         # Add folder details
#         folder = routing.folder
#         p.drawString(0.5 * inch, 7 * inch, f'Folder Details:')
#         p.drawString(0.7 * inch, 6.8 * inch, f'Title: {folder.title}')
#         p.drawString(0.7 * inch, 6.6 * inch, f'Unique Identifier: {folder.unique_identifier}')
#         p.drawString(0.7 * inch, 6.4 * inch, f'Created By: {folder.created_by}')
#         p.drawString(0.7 * inch, 6.2 * inch, f'Draft: {folder.draft}')
#         p.drawString(0.7 * inch, 6 * inch, f'Archive: {folder.archive}')
#         p.drawString(0.7 * inch, 5.8 * inch, f'Urgent: {folder.urgent}')

#         # Content
#         content = Folder_Content.objects.filter(folder=folder)
#         p.drawString(0.5 * inch, 5.4 * inch, f'Folder Content:')
#         y_position = 5.2 * inch
#         for item in content:
#             p.drawString(0.7 * inch, y_position, f'Title: {item.title}')
#             p.drawString(0.7 * inch, y_position - 0.2 * inch, f'Content: {item.content}')
#             y_position -= 0.4 * inch

#         # Add links to files
#         files = File.objects.filter(folder_content__folder=folder)
#         p.drawString(0.7 * inch, y_position - 0.4 * inch, 'Attached Files:')
#         y_position -= 0.6 * inch
#         for file in files:
#             file_link = f'<a href="{file.media.url}">{file.name}</a>'
#             p.drawString(0.7 * inch, y_position, file_link, True)
#             y_position -= 0.2 * inch

#         # Set font size and style for comments header
#         p.setFont("Times-BoldItalic", 12)
#         p.setFillColor(colors.yellow)

#         # Add comments header
#         p.drawString(0.7 * inch, y_position - 0.4 * inch, f'Comments:')
#         y_position -= 0.6 * inch

#         # Set font size and style for comments
#         p.setFont("Times-Italic", 12)
#         p.setFillColor(colors.black)

#         # Add comments
#         comments = Comment.objects.filter(content_type=routing.get_content_type, object_id=routing.id)
#         for comment in comments:
#             p.drawString(0.7 * inch, y_position, f'{comment.account}: {comment.content}')
#             y_position -= 0.2 * inch

#         p.showPage()
#         p.save()

#         return response
class PDFGenerationView(View):
    def get(self, request, routing_id):
        # Get the routing object
        routing = get_object_or_404(Routing, id=routing_id)

        # Create a response object with PDF content
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="routing_details.pdf"'

        # Create PDF content using ReportLab
        p = canvas.Canvas(response, pagesize=letter)

        # Set font size and style for headers
        p.setFont("Times-Bold", 16)

        p.drawString(0.5 * inch, 10 * inch, 'Routing Details')

        # Set font size and style for sub-headers (reduced size)
        p.setFont("Times-Bold", 10)

        # Add routing details in the first column
        p.drawString(0.5 * inch, 9.5 * inch, f'Sender: {routing.forwarded_by}')
        p.drawString(0.5 * inch, 9 * inch, f'Receiver: {routing.send_to}')
        p.drawString(0.5 * inch, 8.5 * inch, f'Intended Unit: {routing.intended_unit}')
        p.drawString(0.5 * inch, 8 * inch, f'Sender Stage: {routing.sender_stage}')
        p.drawString(0.5 * inch, 7.5 * inch, f'Receiver Stage: {routing.reciever_stage}')

        # Add folder details in the second column
        folder = routing.folder
        p.setFont("Times-Bold", 16)
        p.drawString(4 * inch, 10 * inch, f'Folder Details:')
        p.setFont("Times-Bold", 10)
        p.drawString(4.2 * inch, 9.5 * inch, f'Title: {folder.title}')
        p.drawString(4.2 * inch, 9 * inch, f'Unique Identifier: {folder.unique_identifier}')
        p.drawString(4.2 * inch, 8.5 * inch, f'Created By: {folder.created_by}')
        p.drawString(4.2 * inch, 8 * inch, f'Draft: {folder.draft}')
        p.drawString(4.2 * inch, 7.5 * inch, f'Archive: {folder.archive}')
        p.drawString(4.2 * inch, 7 * inch, f'Urgent: {folder.urgent}')

        p.setFont("Times-Bold", 12)
        # Content
        content = Folder_Content.objects.filter(folder=folder)
        p.drawString(0.5 * inch, 5.4 * inch, f'Folder Content:')
        y_position = 5.2 * inch
        for item in content:
            p.drawString(0.7 * inch, y_position, f'Title: {item.title}')
            p.drawString(0.7 * inch, y_position - 0.2 * inch, f'Content: {item.content}')
            y_position -= 0.4 * inch

        # Add links to files
        files = File.objects.filter(folder_content__folder=folder)
        p.drawString(0.7 * inch, y_position - 0.4 * inch, 'Attached Files:')
        y_position -= 0.6 * inch
        for file in files:
            file_link = f'<a href="{file.media.url}">{file.name}</a>'
            p.drawString(0.7 * inch, y_position, file_link, True)
            y_position -= 0.2 * inch

        # Set font size and style for comments header
        p.setFont("Times-BoldItalic", 12)
        p.setFillColor(colors.yellow)

        # Add comments header
        p.drawString(0.7 * inch, y_position - 0.4 * inch, f'Comments:')
        y_position -= 0.6 * inch

        # Set font size and style for comments
        p.setFont("Times-Italic", 12)
        p.setFillColor(colors.black)

        # Add comments with signatures
        comments = Comment.objects.filter(content_type=routing.get_content_type, object_id=routing.id)
        for comment in comments:
            p.drawString(0.7 * inch, y_position, f'{comment.account}: {comment.content}')
            y_position -= 0.2 * inch

            # Add user signature
            signature = comment.account.signature
            if signature:
                signature_image = ImageReader(signature.path)
                p.drawImage(signature_image, 0.7 * inch, y_position - 0.2 * inch, width=50, height=25)

            y_position -= 0.4 * inch


        p.showPage()
        p.save()

        return response