from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.http import JsonResponse, request, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models.query import QuerySet
from django.db.models import Q
from django.views.generic import View,CreateView, ListView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .forms import (
    ContractorFormSignUp, 
    PrecurmentCreateForm,
    ContractorDocumentForm,
    PrecurmentEditForm,
    TenderDocumentForm,
    AwardContractorForm,
)
from .models import (
    Precurement, 
    Precurement_contractors, 
    Procurement_tender_doc,
    ContractorAward,
)
from accounts.models import UserPersona, Account, Contractors,ContractorDocument
from accounts.decorators import user_passes_test, is_persona_tier_12
# Create your views here.


class RegisterContractor(View):
    
    def get(self, request, **kwargs):
        context = {
            'form': ContractorFormSignUp
        }
        return render(request, "contractor_registration.html", context)

    
    def post(self, request, **kwargs):
        form = ContractorFormSignUp(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['email']).exists():
                messages.error(request, "Your Account Has been Registered kindly login")
                return redirect('login')
            user = User()
            user.first_name = form.cleaned_data['full_name']
            user.last_name = form.cleaned_data['company_name']
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password'])
            try:
                with transaction.atomic():
                    user.save()
                    tier = UserPersona.objects.get(persona_tier=11)
                    print('sssssssssss')
                    print(tier)
                    account = Account.objects.create(
                        user=user,
                        user_persona=tier
                    )
                    account.save()
                    contractor = Contractors(
                    account=account,
                    company_name=form.cleaned_data['company_name'],
                    status='pending',
                    category=form.cleaned_data['category'],
                 
                    )
                    contractor.save()
                    # redirect('contactor_register')
            except UserPersona.DoesNotExist:
                messages.error(request, "Error Contact Support, Contractor persona not supported at the moment")
                return redirect('login')

        messages.success(request, "Registration succssfull, please login to access dashboard")
        return redirect('login')


## abdul....##########

#get list of contractors...abduls(due to existing naming, this may be confusing)
class Procurement(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        context = {
            'contractors': Contractors.objects.all()    
        }
        return render(request, "new/contractors.html", context)

     
    # def post(self, request, **kwargs):
    #     messages.error(request, "Feature not enabled by admin")
    #     return redirect('procurement')        




#add new project/precurement...

# class addPrecurmentView(LoginRequiredMixin, CreateView):
#     model = Precurement
#     form_class = PrecurmentCreateForm 
#     template_name = "new/precurement.html"
#     context_object_name = 'form'


class PrecurementListView(View):
    template_name = 'new/precurement.html'
    form_class = PrecurmentCreateForm

    def get(self, request):
        # precurements_contractor = Precurement_contractors.objects.filter(invite = request.user)
        # precurements = [contractor.precurement for contractor in precurements_contractor]
        precurements = Precurement.objects.all()
        form = self.form_class()
        return render(request, self.template_name, {'precurements': precurements, 'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('precurement_list')
        precurements = Precurement.objects.all()
        return render(request, self.template_name, {'precurements': precurements, 'form': form})    
    

### update contractor status
# class ContractorsUpdateView(request, contractor_id):
#         contractor = Contractors.objects.get(pk=pk)
#         print(contractor)
#         status = request.POST.get('status')

#         # Update the status
#         contractor.status = status
#         contractor.save()

#     return render(data)
# contractor document list

def update_contractor_status(request, contractor_id):
    if request.method == 'POST' and request.is_ajax():
        new_status = request.POST.get('status')

        try:
            contractor = Contractors.objects.get(id=contractor_id)
            valid_statuses = [choice[0] for choice in Contractors._meta.get_field('status').choices]
            
            if new_status in valid_statuses:
                contractor.status = new_status
                contractor.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid status choice'})
        except Contractors.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Contractor not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


def contractor_document_list(request, contractor_id):
    documents = ContractorDocument.objects.filter(contractor=contractor_id)
    return render(request, 'new/contractor_document_list.html', {'documents': documents})

# contractor portofolio
def create_contractor_document(request):
    
    try:
        # Check if the user has a contractor persona associated with their account
        user = request.user
        account = Account.objects.get(user=user)
        contractor= Contractors.objects.get(account=account)
    except AttributeError:
        # If the user does not have a contractor persona, return an error message
        messages.error(request, "You do not have permission to add contractor documents.")
        return redirect('dashboard')  # Redirect to home or any other page as per your app's design

    if request.method == 'POST':
        form = ContractorDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            contractor_document = form.save(commit=False)
            contractor_document.contractor = contractor  # Replace 'contractor' with your actual contractor instance
            contractor_document.save()
            messages.success(request, "Contractor document added successfully.")
            return redirect('dashboard')  # Redirect to home or any other page after successful form submission
        else:
            print("Form is invalid. Errors:")
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"{field}: {error}")
    else:
        form = ContractorDocumentForm()

    return redirect('dashboard')


## add precurment
@method_decorator(user_passes_test(is_persona_tier_12), name='dispatch')
class PrecurementCreateView(CreateView):
    model = Precurement
    form_class = PrecurmentCreateForm
    template_name = 'new/precurement.html'
    success_url = reverse_lazy('precurement_list')
    context_object_name = 'form'

    def dispatch(self, request, *args, **kwargs):
        print("PrecurementCreateView is being accessed!")  # Add this line for debugging
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Save the form and return the result
        precurement = form.save(commit=False)
        
        # Project file
        project_file = self.request.FILES.get('project_file')
        if not project_file:
            return HttpResponseBadRequest('No file provided.')

        # Additional validation if needed, e.g., check if it's an image
        if not project_file.content_type.startswith('image'):
            return HttpResponseBadRequest('Invalid file type. Please upload an image.')

        precurement.project_file = project_file
        precurement.save()

        # Get the selected tender type from the form
        tender_type = form.cleaned_data.get('tender_type')

        # Send notification to users based on the tender type i.e in tender list
        if tender_type == 'open tender':
            contractors = Contractors.objects.filter(status = 'verified')
            recipients = [contractor.account.user for contractor in contractors]
        elif tender_type == 'selective tender':
            contractors = form.cleaned_data.get('contractor', [])
            if not isinstance(contractors, QuerySet):
                contractors = list(contractors)
            contractor_ids = [contractor.id for contractor in contractors]
            precurement.contractor.set(contractor_ids)
            recipients = [contractor.account.user for contractor in contractors]
        elif tender_type == 'direct labour':
            # exclude_list = []
            # exclude = Contractors.objects.all()
            # exclude_list = [con.account.user for con in exclude]
            # recipients = User.objects.exclude(pk__in=[instance.pk for instance in exclude_list])
            tiers = Account.objects.filter(Q(user_persona__persona_tier=2) | Q(user_persona__persona_tier=1))
            recipients = tiers
            
        # Recipient
        for recipient in recipients:
            Precurement_contractors.objects.create(
                invite=recipient,
                precurement=precurement
            )

        messages.success(self.request, "New procurement added successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        errors = {field: form.errors[field] for field in form.errors}
        return JsonResponse({'errors': errors}, status=400)
    
    

def fetch_contractors(request):
  contractors = Contractors.objects.filter(status = 'verified').values('pk', 'company_name')
  
  return JsonResponse({'contractors': list(contractors)})


class PrecurementDetailView(View):
    template_name = 'new/precurement_detail.html'

    def get(self, request, pk):
        precurement = get_object_or_404(Precurement, pk=pk)    
        try:
            contractor = Contractors.objects.get(account__user=request.user)
        except Contractors.DoesNotExist:
            contractor = None
        if contractor:
            try:
                # contractor = get_object_or_404(Contractors, account__user=request.user)
                existing_document = Procurement_tender_doc.objects.get(precurement=precurement, contractor=contractor)
            except Procurement_tender_doc.DoesNotExist or Contractors.DoesNotExist:
                existing_document = None
        else:
            existing_document = None
        form = TenderDocumentForm()
        return render(request, self.template_name, {'precurement': precurement, 'form': form, 'existing_document': existing_document})
    
    #handle contractor tender document
    def post(self, request, pk):
        precurement = get_object_or_404(Precurement, pk=pk)
        form = TenderDocumentForm(request.POST, request.FILES)
        
        # Try to get the contractor or raise a 404 error
        contractor = get_object_or_404(Contractors, account__user=request.user)

        if form.is_valid():
            existing_document = Procurement_tender_doc.objects.filter(precurement=precurement).first()

            if existing_document:
                # Update the existing document
                existing_document.file = form.cleaned_data['file']
                existing_document.save()
                messages.success(request, "Tender document updated successfully!")
            else:
                # Create a new document
                Procurement_tender_doc.objects.create(contractor=contractor, precurement=precurement, file=form.cleaned_data['file'])
                messages.success(request, "Tender document added successfully!")
            return redirect('precurement_detail', pk=pk)

        return render(request, self.template_name, {'precurement': precurement, 'form': form})


@user_passes_test(is_persona_tier_12)
def procurement_edit(request, pk):
    precurement = get_object_or_404(Precurement, pk=pk)
    if request.method == 'POST':
        form = PrecurmentEditForm(request.POST, request.FILES, instance=precurement)
        if form.is_valid():
            precurement = form.save(commit=True)
        
            tender_type = precurement.tender_type
            
            # Send notification to users based on the tender type, i.e., update/create Precurment_contractors
            if tender_type == 'open tender':
                contractors = Contractors.objects.filter(status = 'verified')
                recipients = [contractor.account.user for contractor in contractors]  
            elif tender_type == 'selective tender':
                
                contractors = form.cleaned_data.get('contractor', [])
                
                if not isinstance(contractors, QuerySet):
                    contractors = list(contractors)
                contractor_ids = [contractor.id for contractor in contractors]
                precurement.contractor.set(contractor_ids)
                recipients = [contractor.account.user for contractor in contractors]
            elif tender_type == 'direct labour':
                tiers = Account.objects.filter(Q(user_persona__persona_tier=2) | Q(user_persona__persona_tier=1))
                recipients = tiers
            precurement.save()
            

            # Update or create Precurment_contractors objects for the recipients
            for recipient in recipients:
                Precurement_contractors.objects.update_or_create(
                    invite=recipient,
                    precurement=precurement
                )

            messages.success(request, "Procurement updated successfully!")
            return redirect('precurement_detail', pk=precurement.pk)
    else:
        form = PrecurmentEditForm(instance=precurement)

    return redirect('precurement_list')


def procurement_delete(request, pk):
    precurement = get_object_or_404(Precurement, pk=pk)
    precurement.delete()
    messages.success(request, "Procurement deleted successfully!")
    return redirect('precurement_list')


# Award contracors....

class AwardContractorView(View):
    template_name = 'new/award_contractor.html'

    def get(self, request, procurement_id):
        procurement = get_object_or_404(Precurement, id=procurement_id)
        contractors = Contractors.objects.filter(status='verified')

        # Paginate the list of contractors
        paginator = Paginator(contractors, 10)  # Show 10 contractors per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        form = AwardContractorForm()
        context = {
            'procurement': procurement,
            'contractors': page_obj,  # Pass the paginated queryset to the template
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, procurement_id):
        procurement = get_object_or_404(Precurement, id=procurement_id)
        contractors = Contractors.objects.filter(status='verified')

        form = AwardContractorForm(request.POST, request.FILES)
        if form.is_valid():
            selected_contractors = form.cleaned_data.get('contractors')
            award_date = form.cleaned_data.get('award_date')
            amount = form.cleaned_data.get('amount')
            document = form.cleaned_data.get('document')
            remarks = form.cleaned_data.get('remarks')

            try:
                # Check if the uploaded document is an image
                if document:
                    if not document.content_type.startswith('image'):
                        raise ValidationError('Invalid file type. Please upload an image.')

                contractor_award = ContractorAward.objects.create(
                    procurement=procurement,
                    award_date=award_date,
                    amount=amount,
                    document=document,
                    remarks=remarks
                )
                contractor_award.contractors.set(selected_contractors)
                contractor_award.save()
                messages.success(request, 'Contractors Awarded')
                return redirect('dashboard')
            except ValidationError as e:
                messages.error(request, e)


        context = {
            'procurement': procurement,
            'contractors': contractors,
            'form': form,
        }
        return render(request, self.template_name, context)


class ContractorAwardListView(ListView):
    template_name = 'new/contractor_award_list.html'
    model = ContractorAward
    context_object_name = 'awards'

    def get_queryset(self):
        user = self.request.user
        account = Account.objects.get(user=user)
        contractor= Contractors.objects.get(account=account)
        print(ContractorAward.objects.filter(contractors=contractor))
        return ContractorAward.objects.filter(contractors=contractor)



#FILES
def procurement_list(request):
    procurements = Precurement.objects.all()
    return render(request, 'new/procurement_list.html', {'procurements': procurements})

def procurement_files(request, pk):
    procurement = Precurement.objects.get(pk=pk)
    files = Procurement_tender_doc.objects.filter(precurement = procurement)
    return render (request, 'new/procurement_tender_documents.html', {'files': files, 'procurement': procurement})