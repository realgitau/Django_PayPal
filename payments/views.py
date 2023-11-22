from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
# third party imports
from paypal.standard.forms import PayPalPaymentsForm
from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
# local imports
from .models import Product

def product_purchase(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponse("Product not found", status=404)

    paypal_form = PayPalPaymentsForm(initial={
        'business': "djangoshop254@gmail.com",
        'amount': product.price,
        'item_name': product.name,
        'invoice': product_id,
        'currency_code': "USD",
        'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
        'return_url': request.build_absolute_uri(reverse('successful')),
        'cancel_return': request.build_absolute_uri(reverse('cancelled')),
    })

    context = {
        'product': product,
        'paypal_form': paypal_form,
    }

    return render(request, 'payments/purchase.html', context)


def payment_successful(request):
    return render(request, 'payments/successful.html')

def payment_cancelled(request):
    return render(request, 'payments/cancelled.html')

@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    """Function to reduce quantity once purchase is successful"""
    ipn_obj = sender

    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # payment successful
        product_id = ipn_obj.invoice
        product = Product.objects.get(id=product_id)
        product.quantity -= 1
        product.save()