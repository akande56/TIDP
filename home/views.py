from django.shortcuts import render, redirect

from home.models import Unit
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.views.generic import View
from django.contrib.auth.models import User
from accounts.models import Account, UserPersona, Contractors
from accounts.forms import (
    CreateUserForm,
    UserRegistrationForm,
    BusinessInfoForm,
    CreateUserrForm,
    UserLoginForm,
)
from .forms import (
    AddUsertoUnit,
    CreatePersonaForm,
    UnitForm
)
from procurement.models import Precurement, Precurement_contractors
from procurement.forms import ContractorDocumentForm
# Create your views here.
def home(request):
    return render(request, "landing.html")


class NewMail(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        context = {

        }   
        return render(request, "new/new_mail.html", context)


class Dashboard(LoginRequiredMixin, View):
    
    def get(self, request, **kwargs):
        context = {
            'value': 1,
            # 'form': BusinessInfoForm,
            'form': ContractorDocumentForm,
        }
        user = Account.objects.get(user=request.user)
        print(user.user_persona.persona_tier)
        if user.user_persona.persona_tier == 11:
            # get contractor status
            contractor = Contractors.objects.get(account=user)
            #list of concerned precurement... @abdul
            precurements_contractor = Precurement_contractors.objects.filter(invite = request.user)
            print(precurements_contractor)
            precurements = [contractor.precurement for contractor in precurements_contractor]
            context['precurements'] = precurements
            context['status'] = contractor.status


            return render(request, "new/contractor_dashboard.html", context)
        return render(request, "new/dashboard.html", context)


class DashboardOld(LoginRequiredMixin, View):
    
    def get(self, request, **kwargs):
        context = {
            'form': BusinessInfoForm
        }   
        return render(request, "dashboard.html", context)

    def post(self, request):
        form = BusinessInfoForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Business Information')
            return redirect("dashboard")
        messages.error(request, "Failed saving information")
        return redirect("dashboard")

class UserPersonaView(LoginRequiredMixin, View):
    model = UserPersona
    template_name = "new/user_persona.html"
    
    def get(self, request, **kwargs):
        context = {
        "personas": self.model.objects.all(),
        "form": CreatePersonaForm,
        'value': 6,
        'internal': 1,

        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = CreatePersonaForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'User Persona Created Sucessfully')
            return redirect("user_persona")
        messages.error(request, "Failed saving information")
        return redirect('user_persona')


class UserGroupDetail(LoginRequiredMixin, View):
    template_name = "group_detail.html"

    def get(self, request, slug, **kwargs):
        form = CreateUserrForm()
        group = UserGroup.objects.get(slug=slug)
        
        context = {
            'form': form,
            'group': group,
            'users': Account.objects.filter(user_group=group),
        }
        return render(request, self.template_name, context)

    def post(self, request, slug):
        form = CreateUserrForm(request.POST)
        group = UserGroup.objects.get(slug=slug)
        
        if form.is_valid():
            account = form.cleaned_data['users']
            account.user_group.add(group)
            messages.success(request, 'User added to group successfully')
            return redirect("group_detail", slug=slug)
        messages.error(request, "Failed Adding User to group")
        return redirect("group_detail", slug=slug)


class RemoveUserFromGroup(LoginRequiredMixin, View):
    def get(self, request, id, slug, **kwargs):
        group = UserGroup.objects.get(slug=slug)
        account = Account.objects.get(id=id)    
        account.user_group.remove(group)
        messages.success(request, 'User removed from group successfully')
        return redirect("group_detail", slug=slug)


class GroupState(LoginRequiredMixin, View):
    
    def get(self, request, slug, **kwargs):
        group = UserGroup.objects.get(slug=slug)
        group.active = not group.active
        group.save()
        return redirect('user_persona')


class UsersView(LoginRequiredMixin, View):
    
    def get(self, request, **kwargs):
        print ("a111")
        context = {
            'form': CreateUserForm(),
            'users': Account.objects.filter(),
            'inactive_users': Account.objects.filter(user__is_active=False),
            'active_users': Account.objects.filter(user__is_active=True),
            'value': 6,
            'internal': 2,
        }
        return render(request, "new/users.html", context)

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            staff_id = form.cleaned_data["username"]
            password = form.cleaned_data['password']
            fullname = form.cleaned_data['fullname']
            persona = form.cleaned_data['persona']
            try:
                user = User()
                user.username = staff_id
                user.first_name = fullname
                user.set_password(password)
                with transaction.atomic():
                    user.save()
                    Account.objects.create(
                        user=user,
                        user_persona=persona
                    )
                messages.success(
                            request, 'User created successfully')
            except Exception as e:
                messages.error(
                    request, 'Fail to save user details {}'.format(e))
        
        return redirect("users_view")


class UserStateView(LoginRequiredMixin, View):
    
    def get(self, request, id, **kwargs):
        the_user = User.objects.get(id=id)
        
        if the_user.is_superuser:
            messages.error(request, "Superadmin cannot be deactivated")
            return redirect('users_view')
        the_user.is_active = not the_user.is_active
        the_user.save()
        messages.success(request, "Action performed Successfully")
        return redirect('users_view')


class UnitView(LoginRequiredMixin, View):
    template_name = "new/unit.html"

    def get(self, request, **kwargs):
        form = UnitForm()
        
        context = {
            'form': form,
            'units': Unit.objects.all(),
            'value': 6,
            'internal': 3,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UnitForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Unit Created successfully')
            return redirect("units_view")
        messages.error(request, "Failed Creating Unit")
        return redirect("units_view")


class UnitDetailsView(LoginRequiredMixin, View):
    template_name = "new/unit_details.html"

    def get(self, request, slug, **kwargs):
        form = AddUsertoUnit()
        unit = Unit.objects.get(slug=slug)
        
        context = {
            'form': form,
            'unit': unit,
            'value': 6,
            'internal': 3,
        }
        return render(request, self.template_name, context)

    def post(self, request, slug):
        form = AddUsertoUnit(request.POST)
        unit = Unit.objects.get(slug=slug)

        if form.is_valid():
            staff = form.cleaned_data['staff']
            if unit.unit_type=='Minister/DG' and (staff.user_persona.persona_tier==1 or staff.user_persona.persona_tier==8 or staff.user_persona.persona_tier==6 or staff.user_persona.persona_tier==7):
                if (staff.user_persona.persona_tier==1):
                    for get_staff in unit.users.select_related():
                        if get_staff == staff:
                            messages.error(request, "Minister/DG was already added to this unit")
                        else:
                            messages.error(request, "Sorry the system can accept only one Ministers/DGs") 
                        return redirect("unit_detail", slug=slug)           
                    
                    unit.users.add(staff)
                    unit.save()
                    messages.success(request, 'Congratulations You Have Added the {} Successfully'.format(staff.user_persona.name))
                elif staff.user_persona.persona_tier==6:
                    unit.users.add(staff)
                    unit.save()
                    messages.success(request, 'Congratulations You Have Added a clearical officer to this office')
                elif staff.user_persona.persona_tier==8:
                    unit.users.add(staff)
                    unit.save()
                    messages.success(request, 'Congratulations other officers added successfully')
                else:
                    for get_staff in unit.users.select_related():
                        if get_staff == staff:
                            messages.error(request, "Protocol Officer already exist")
                            return redirect("unit_detail", slug=slug)
                        elif get_staff.user_persona.persona_tier == 7:
                            messages.error(request, "Sorry the system can only accept one protocol officer") 
                            return redirect("unit_detail", slug=slug)
                        
                    unit.users.add(staff)
                    unit.save()
                    messages.success(request, 'Congratulations You Have Added a Protocol officerto this office')
                return redirect("unit_detail", slug=slug)
            elif unit.unit_type=='Secretery' and (staff.user_persona.persona_tier==2 or staff.user_persona.persona_tier==8 or staff.user_persona.persona_tier==6 or staff.user_persona.persona_tier==7):
                if (staff.user_persona.persona_tier==2):
                    for get_staff in unit.users.select_related():
                        if get_staff == staff:
                            messages.error(request, "{} was already added to this unit".format(staff.user_persona.name))
                            return redirect("unit_detail", slug=slug)
                        elif get_staff.user_persona.persona_tier==2:
                            messages.error(request, "Sorry the system can accept only one {}".format(staff.user_persona.name)) 
                            return redirect("unit_detail", slug=slug)           
                    
                    unit.users.add(staff)
                    unit.save()
                    messages.success(request, 'Congratulations You Have Added the {} Successfully'.format(staff.user_persona.name))
                elif staff.user_persona.persona_tier==6:
                    unit.users.add(staff)
                    unit.save()
                    messages.success(request, 'Congratulations You Have Added a {} to this office'.format(staff.user_persona.name))
                elif staff.user_persona.persona_tier==8:
                    unit.users.add(staff)
                    unit.save()
                    messages.success(request, 'Congratulations other officers added successfully')
                else:
                    for get_staff in unit.users.select_related():
                        if get_staff == staff:
                            messages.error(request, "Protocol Officer already exist")
                            return redirect("unit_detail", slug=slug)
                        elif get_staff.user_persona.persona_tier == 7:
                            messages.error(request, "Sorry the system can only accept one protocol officer") 
                            return redirect("unit_detail", slug=slug)
                    unit.users.add(staff)
                    unit.save()
                    messages.success(request, 'Congratulations You Have Added a Protocol officer to this office')
                return redirect("unit_detail", slug=slug)
                
                unit.users.add(staff)
                unit.save()
                messages.success(request, 'Congratulations the Staff has been added to Unit successfully')
                return redirect("unit_detail", slug=slug)
            elif unit.unit_type=='Department' and (staff.user_persona.persona_tier==3 or staff.user_persona.persona_tier==8 or staff.user_persona.persona_tier==4 or staff.user_persona.persona_tier==5 or staff.user_persona.persona_tier==6):
                if (staff.user_persona.persona_tier==3):
                    for get_staff in unit.users.select_related():
                        if get_staff == staff:
                            messages.error(request, "Director was already added to this unit")
                        else:
                            messages.error(request, "Sorry the system can accept only one Director per Unit") 
                        return redirect("unit_detail", slug=slug)           
                    
                    unit.users.add(staff)
                    unit.save()
                    messages.success(request, 'Congratulations You Have Added a Director to this Unit')
                elif staff.user_persona.persona_tier==4:
                    for get_staff in unit.users.select_related():
                        if get_staff == staff:
                            messages.error(request, "Deputy Director already exist for this unit")
                        else:
                            messages.error(request, "Sorry the system can accept only one Ass. Director per Unit") 
                        return redirect("unit_detail", slug=slug)           
                    
                    unit.users.add(staff)
                    unit.save()
                    messages.success(request, 'Congratulations You Have Added a Duputy Director to this Unit')
                elif staff.user_persona.persona_tier==5:
                    for get_staff in unit.users.select_related():
                        if get_staff == staff:
                            messages.error(request, "Ass. Director already exist for this unit")
                        else:
                            messages.error(request, "Sorry the system can accept only one Ass. Director per Unit") 
                        return redirect("unit_detail", slug=slug)           
                    
                    unit.users.add(staff)
                    unit.save()
                    messages.success(request, 'Congratulations You Have Added a Ass. Director to this Unit')
                elif staff.user_persona.persona_tier==8:
                    unit.users.add(staff)
                    unit.save()
                    messages.success(request, 'Congratulations other officers added successfully')
                else:
                    unit.users.add(staff)
                    unit.save()
                    messages.success(request, 'Congratulations You Have Added a clearical officer to this office')
                
                return redirect("unit_detail", slug=slug)
        messages.error(request, "User category can't be added to this unit")
        return redirect("unit_detail", slug=slug)
