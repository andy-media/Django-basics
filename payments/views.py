import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from .utils import send_confirmation_email  # Add this import

from registration.models import School, Payment

@login_required
def payment_view(request):
    try:
        school = request.user.school
        if not school.registration_complete:
            messages.warning(request, 'Please complete your registration first.')
            return redirect('coach_info')
    except School.DoesNotExist:
        messages.warning(request, 'Please complete your registration first.')
        return redirect('school_info')

    if school.payment_verified:
        messages.info(request, 'Your payment has already been verified.')
        return redirect('dashboard')

    amount = 150000 # 150000 in the smallest currency unit (e.g., cedis Ghana)
    
    if request.method == 'POST':
        # Initialize Paystack payment
        paystack_url = 'https://api.paystack.co/transaction/initialize'
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        callback_url = request.build_absolute_uri(reverse('payment_verify'))
        
        data = {
            'email': request.user.email,
            'name': request.user.username,
            'amount': amount,
            'callback_url': callback_url,
            'metadata': {
                'school_id': school.id,
                'user_id': request.user.id,
            }
        }
        
        try:
            response = requests.post(paystack_url, headers=headers, json=data)
            response_data = response.json()
            
            if response_data.get('status'):
                # Create payment record
                payment = Payment.objects.create(
                    school=school,
                    amount=amount/100,  # Convert to main currency unit
                    paystack_ref=response_data['data']['reference'],
                )
                return redirect(response_data['data']['authorization_url'])
            else:
                messages.error(request, 'Error initializing payment: ' + response_data.get('message', 'Unknown error'))
        except Exception as e:
            messages.error(request, f'Error connecting to Paystack: {str(e)}')
    
    return render(request, 'payments/payment.html', {'amount': amount/100})

@login_required
def payment_verify_view(request):
    reference = request.GET.get('reference')
    if not reference:
        messages.error(request, 'No payment reference provided')
        return redirect('dashboard')

    try:
        payment = Payment.objects.get(paystack_ref=reference, school=request.user.school)
    except Payment.DoesNotExist:
        messages.error(request, 'Invalid payment reference')
        return redirect('dashboard')

    if payment.verified:
        messages.info(request, 'Payment already verified')
        return redirect('dashboard')

    # Verify payment with Paystack
    paystack_url = f'https://api.paystack.co/transaction/verify/{reference}'
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
    }
    
    try:
        response = requests.get(paystack_url, headers=headers)
        response_data = response.json()
        
        if response_data.get('status') and response_data['data']['status'] == 'success':
            payment.verified = True
            payment.save()
            
            # Update school payment status
            school = request.user.school
            school.payment_verified = True
            school.save()
            
            # Send confirmation email
            send_confirmation_email(school, payment)
            
            messages.success(request, 'Payment verified successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Payment verification failed: ' + response_data.get('message', 'Unknown error'))
    except Exception as e:
        messages.error(request, f'Error verifying payment: {str(e)}')
    
    return redirect('dashboard')