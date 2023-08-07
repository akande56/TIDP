from django.http import JsonResponse, request
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.views.generic import View,CreateView
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

        messages.success(request, "A Verification link Has been sent to your email kindly verify")
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
class ContractorsUpdateView(View):
    def post(self, request, pk):
        contractor = Contractors.objects.get(pk=pk)
        print(contractor)
        status = request.POST.get('status')

        # Update the status
        contractor.status = status
        contractor.save()

        data = {
            'success': True,
            'message': 'Status updated successfully.',
        }
        return JsonResponse(data)


# contractor document list

def contractor_document_list(request, contractor_id):
    documents = ContractorDocument.objects.filter(contractor=contractor_id)
    return render(request, 'new/contractor_document_list.html', {'documents': documents})


def create_contractor_document(request):
    
    try:
        # Check if the user has a contractor persona associated with their account
        user = request.user
        account = Account.objects.get(user=user)
        contractor= Contractors.objects.get(account=account)
        print('ddddddddd')
        print(user)
        print(account)
        print(contractor)
    except AttributeError:
        # If the user does not have a contractor persona, return an error message
        messages.error(request, "You do not have permission to add contractor documents.")
        return redirect('dashboard')  # Redirect to home or any other page as per your app's design

    # if contractor_persona.persona_tier != 11:
    #     # Check if the user's persona tier is not 11 (contractors)
    #     messages.error(request, "You do not have permission to add contractor documents.")
    #     return redirect('dashboard')  # Redirect to home or any other page as per your app's design

    if request.method == 'POST':
        # Process the form data and create the contractor document
        form = ContractorDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.contractor = contractor
            print(form)
            document.save(commit=True)
            messages.success(request, "Contractor document added successfully.")
            form = ContractorDocumentForm()
            request.session['form'] = form
            print("Form is invalid. Errors:")
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"{field}: {error}")
            return redirect('dashboard')  # Redirect to home or any other page after successful form submission
        else:
            print("Form is invalid. Errors:")
            print(form)
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"{field}: {error}")
    else:
        form = ContractorDocumentForm()
        request.session['form'] = form

    return redirect('dashboard')


## add precurment
class PrecurementCreateView(CreateView):
    model = Precurement
    form_class = PrecurmentCreateForm
    template_name = 'new/precurement.html'
    success_url = reverse_lazy('precurement_list')
    context_object_name = 'form'
    
    def dispatch(self, request, *args, **kwargs):
        print("MyModelCreateView is being accessed!")  # Add this line for debugging
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Save the form and return the result
        precurement = form.save(commit=True)
        #Get the selected tender type from the form
        tender_type = form.cleaned_data.get('tender_type')

        #Send notification to users based on the tender type i.e in tender list
        if tender_type == 'open tender':
            recipients = User.objects.all()  # Modify this query to select the appropriate recipients
        elif tender_type == 'selective tender':
            contractors = form.cleaned_data.get('contractor')
            recipients = [contractor.account.user for contractor in contractors]
        elif tender_type == 'internal labour':
            recipients = User.objects.exclude(user_persona__name='contractor')
        for recipient in recipients:
            Precurement_contractors.objects.create(
                invite = recipient,
                precurement = precurement
            )
        return super().form_valid(form)

    def form_invalid(self, form):
        # Print form errors to the terminal for debugging

        # form._errors['contractor'] = None
        
        print("Form is invalid. Errors:")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"{field}: {error}")
        return super().form_invalid(form)
    
    

def fetch_contractors(request):
  contractors = Contractors.objects.all().values('pk', 'company_name')
  
  return JsonResponse({'contractors': list(contractors)})



