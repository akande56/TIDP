from django.http import JsonResponse, request, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models.query import QuerySet
from django.views.generic import View,CreateView, DetailView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import (
    ContractorFormSignUp, 
    PrecurmentCreateForm,
    ContractorDocumentForm
)
from .models import Precurement, Precurement_contractors
from accounts.models import UserPersona, Account, Contractors,ContractorDocument

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
                messages.error(request, "Error Contact Support")
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
        precurements_contractor = Precurement_contractors.objects.filter(invite = request.user)
        precurements = [contractor.precurement for contractor in precurements_contractor]
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

        # Get the selected tender type from the form
        tender_type = form.cleaned_data.get('tender_type')

        # Send notification to users based on the tender type i.e in tender list
        if tender_type == 'open tender':
            recipients = User.objects.all()
        elif tender_type == 'selective tender':
            contractors = form.cleaned_data.get('contractor', [])
            if not isinstance(contractors, QuerySet):
                contractors = list(contractors)
            contractor_ids = [contractor.id for contractor in contractors]
            precurement.contractor.set(contractor_ids)
            recipients = [contractor.account.user for contractor in contractors]
        elif tender_type == 'direct labour':
            exclude_list = []
            exclude = Contractors.objects.all()
            exclude_list = [con.account.user for con in exclude]
            recipients = User.objects.exclude(pk__in=[instance.pk for instance in exclude_list])

        # Project file
        project_file = self.request.FILES.get('project_file')
        if not project_file:
            return HttpResponseBadRequest('No file provided.')

        # Additional validation if needed, e.g., check if it's an image
        if not project_file.content_type.startswith('image'):
            return HttpResponseBadRequest('Invalid file type. Please upload an image.')

        precurement.project_file = project_file
        precurement.save()

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
  contractors = Contractors.objects.all().values('pk', 'company_name')
  
  return JsonResponse({'contractors': list(contractors)})



class PrecurementDetailView(DetailView):
    model = Precurement
    template_name = 'new/precurement_detail.html'
    context_object_name = 'precurement'


def procurement_edit(request, pk):
    precurement = get_object_or_404(Precurement, pk=pk)
    
    if request.method == 'POST':
        form = PrecurmentCreateForm(request.POST, request.FILES,instance=precurement)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, "Procurement updated successfully!")
            return redirect('precurement_detail', pk=precurement.pk)
    else:
        form = PrecurmentCreateForm(instance=precurement)

    return redirect ('precurement_list')


def procurement_delete(request, pk):
    precurement = get_object_or_404(Precurement, pk=pk)
    precurement.delete()
    messages.success(request, "Procurement deleted successfully!")
    return redirect('precurement_list')

