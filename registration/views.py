from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .models import Document
from django.core.paginator import Paginator

from .forms import SchoolForm, ContestantFormSet, CoachForm
from .models import School, Contestant, Coach, Payment



@login_required
def dashboard_view(request):
    try:
        school = request.user.school
        context = {
            'school': school,
            'contestants': school.contestants.all(),
            'coaches': school.coaches.all(),
            'payments': school.payments.filter(verified=True),
        }
        return render(request, 'registration/dashboard.html', context)
    except School.DoesNotExist:
        messages.warning(request, 'Please complete your registration.')
        return redirect('school_info')
@login_required
def school_info_view(request):
    try:
        school = request.user.school
    except School.DoesNotExist:
        school = None

    if request.method == 'POST':
        form = SchoolForm(request.POST, instance=school)
        if form.is_valid():
            school = form.save(commit=False)
            school.user = request.user
            school.save()
            messages.success(request, 'School information saved successfully!')
            return redirect('contestant_info')
    else:
        form = SchoolForm(instance=school)
    
    return render(request, 'registration/school_info.html', {'form': form})

@login_required
def contestant_info_view(request):
    try:
        school = request.user.school
    except School.DoesNotExist:
        messages.warning(request, 'Please complete school information first.')
        return redirect('school_info')

    if request.method == 'POST':
        formset = ContestantFormSet(request.POST, instance=school)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Contestant information saved successfully!')
            return redirect('coach_info')
    else:
        formset = ContestantFormSet(instance=school)
    
    return render(request, 'registration/contestant_info.html', {'formset': formset})

@login_required
def coach_info_view(request):
    try:
        school = request.user.school
    except School.DoesNotExist:
        messages.warning(request, 'Please complete school information first.')
        return redirect('school_info')

    coaches = school.coaches.all()
    coach_types = ['science', 'maths', 'computing']

    if request.method == 'POST':
        for coach_type in coach_types:
            form = CoachForm(request.POST, prefix=coach_type)
            if form.is_valid():
                coach = form.save(commit=False)
                existing = coaches.filter(coach_type=coach_type).first()
                if existing:
                        # Update the existing coach instead of creating a new one
                    existing.name = coach.name
                    existing.contact_number = coach.contact_number
                    existing.save()
                else:
                    coach.school = school
                    coach.coach_type = coach_type
                    coach.save()
        
        school.registration_complete = True
        school.save()
        messages.success(request, 'Registration complete! Proceed to payment.')
        return redirect('payment')
    
    forms = {}
    for coach_type in coach_types:
        try:
            coach = coaches.get(coach_type=coach_type)
            forms[coach_type] = CoachForm(prefix=coach_type, instance=coach)
        except Coach.DoesNotExist:
            forms[coach_type] = CoachForm(prefix=coach_type)
    
    return render(request, 'registration/coach_info.html', {'forms': forms})

@login_required
def dashboard_view(request):
    try:
        school = request.user.school
        context = {
            'school': school,
            'contestants': school.contestants.all(),
            'coaches': school.coaches.all(),
            'payments': school.payments.filter(verified=True),
        }
        return render(request, 'registration/dashboard.html', context)
    except School.DoesNotExist:
        messages.warning(request, 'Please complete your registration.')
        return redirect('school_info')

def generate_receipt_pdf(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id, school=request.user.school)
    except Payment.DoesNotExist:
        messages.error(request, 'Payment not found')
        return redirect('dashboard')

    template_path = 'registration/receipt_pdf.html'
    context = {'payment': payment, 'school': request.user.school}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{payment.id}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors generating the PDF')
    return response

def send_confirmation_email(school, payment):
    subject = 'Registration Confirmation'
    message = render_to_string('registration/confirmation_email.html', {
        'school': school,
        'payment': payment,
    })
    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [school.user.email],
    )
    email.content_subtype = "html"
    email.send(fail_silently=False)


@login_required
def download_questions(request):
    school = request.user.school
    payments = school.payments.filter(verified=True).exists()
    documents = Document.objects.all()

    paginator = Paginator(documents, 10)               # 10 documents per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        # 'documents': Document.objects.all(),
        'payments': payments,
        'page_obj': page_obj
    }
    return render(request, 'registration/past_questions.html', context)