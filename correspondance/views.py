import imp
from pyexpat import model
from venv import create
from django import forms
from django.shortcuts import redirect, render
from django.contrib.contenttypes.models import ContentType
from django.views.generic import View
from django.http import response
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from accounts.models import Account
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
    CommentForm
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
        print('ssssss')
        print(account_id)
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
        route = Routing.objects.get(id=id)
        folders = Folder_Content.objects.filter(folder=route.folder)

        form_initials = {
            "content_type": route.get_content_type,
            "object_id": route.id
        }
        form = CommentForm(initial=form_initials)

        context = {
            'memo': route,
            'folders': folders,
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
        form = InternalMemoForm()
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
            'upload_form': UploadFileForm,
            'value': 2,
            "internal": 1,
        }

        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        print('under post......')
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
            print('post request initiated....')
            with transaction.atomic():
                folder = form.save(commit=False)
                identifier = ''.join(random.choice(
                    string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
                folder.unique_identifier = identifier
                folder.created_by = account
                folder.draft = True
                folder.save()
                f_content = Folder_Content.objects.create(
                    folder=folder,
                    created_by=account,
                    content=form.cleaned_data["content"],
                    title=folder.title
                )
                # Get the current unit
                current_unit = Unit.objects.get(users=account)
                # Get Curremt Unit and Check if there is clearical officer then forward to be ecleared int he registry else send direct
                # current_user = current_unit.users.get(user_persona__persona_tier=6)
                # print('{}, {}'.format(send_to, account))
                current_user = current_unit.users.filter(
                    Q(user_persona__persona_tier=1) |
                    Q(user_persona__persona_tier=2) |
                    Q(user_persona__persona_tier=3) |
                    Q(user_persona__persona_tier=4) |
                    Q(user_persona__persona_tier=5)
                ).first()
                print('Current Users units:')
                print(current_user)
                if current_user.user_persona.persona_tier <= 5:
                    print('tire less than 5....')
                    send_to_user = current_unit.users.filter(
                        Q(user_persona__persona_tier=6)
                    ).first()
                    
                    print('chosen selected recipient:')
                    print(form.cleaned_data['send_to'])

                    send_to_unit = form.cleaned_data['send_to']
                    print(send_to_unit.users.filter(
                        user_persona__persona_tier=1).count())
                    # Unit has a clearical office
                    if current_unit.users.filter(user_persona__persona_tier=6).count():
                        print('count before creating routing...')
                        print(current_unit.users.filter(user_persona__persona_tier=6).count())
                        Routing.objects.create(
                            send_to=send_to_user,
                            folder=folder,
                            forwarded_by=account,
                            intended_unit=send_to_unit,
                            sender_stage='Clearing',
                            initiated_unit=current_unit
                        )
                    # Current unit don't have clearical officer we send to intended unit clearifcal officer
                    elif send_to_unit.users.filter(user_persona__persona_tier=6).count():
                        Routing.objects.create(
                            send_to=send_to_user,
                            folder=folder,
                            forwarded_by=account,
                            intended_unit=send_to_unit,
                            sender_stage='Done',
                            reciever_stage="Clearing",
                            initiated_unit=current_unit
                        )
                    elif send_to_unit.users.filter(user_persona__persona_tier=7).count():
                        print(send_to_unit.users.filter(
                            user_persona__persona_tier=7))
                        Routing.objects.create(
                            send_to=send_to_user,
                            folder=folder,
                            forwarded_by=account,
                            intended_unit=send_to_unit,
                            sender_stage='Done',
                            reciever_stage="Protocol",
                            initiated_unit=current_unit
                        )
                    else:
                        Routing.objects.create(
                            send_to=send_to_user,
                            folder=folder,
                            forwarded_by=account,
                            intended_unit=send_to_unit,
                            sender_stage='Done',
                            reciever_stage="Done",
                            initiated_unit=current_unit
                        )
                elif current_user.user_persona.persona_tier == 6:
                    send_to = current_unit.users.filter(
                        Q(user_persona__persona_tier=1) |
                        Q(user_persona__persona_tier=2) |
                        Q(user_persona__persona_tier=3) |
                        Q(user_persona__persona_tier=4) |
                        Q(user_persona__persona_tier=5)
                    ).first()

                    Routing.objects.create(
                        send_to=send_to,
                        folder=folder,
                        forwarded_by=account,
                        intended_unit=form.cleaned_data['send_to'],
                        sender_stage='Done',
                        reciever_stage='Done',
                        initiated_unit=current_unit
                    )
                else:
                    pass
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
        route = Routing.objects.get(id=id)
        route.reciever_stage = "Done"
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
