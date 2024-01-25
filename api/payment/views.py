from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import braintree

# Create your views here.


gateway = braintree.BraintreeGateway(
  braintree.Configuration(
      braintree.Environment.Sandbox,
      merchant_id="kcftjzz9dxpxnddm",
      public_key="555zjhkx6yspy3fp",
      private_key="244611aacbc62a51262ecbd3f0158043"
  )
)


def validate_user_session(id,token):
    UserModel=get_user_model()

    try:
        user = UserModel.objects.get(pk=id)
        if user.session_token == token:
            return True
        return False
    except UserModel.DoesNotExist:
        return False
    


@csrf_exempt
def generate_token(request,id,token):
    if not validate_user_session(id,token):
        return JsonResponse({'error':'invalid session ! please Login again'})
    
    return JsonResponse({'ClientToken': gateway.client_token.generate(),'success':True})


@csrf_exempt
def process_payment(request, id,token):
    if not validate_user_session(id,token):
        return JsonResponse({'error':'invalid session ! please Login again'})
    nonce_from_client =  request.POST["paymentMethodNonce"]
    amount_from_client = request.POST["amount"]

    result = gateway.transaction.sale({
        "amount": amount_from_client,
        "payment_method_nonce": nonce_from_client,
        "options": {
        "submit_for_settlement": True
        }
    })

    if result.is_success:
        return JsonResponse({"success":result.is_success,
                             "transaction":{'id': result.transaction.id,
                            'amount': result.transaction.amoun}})
    else:
        return JsonResponse({'error':True,'succes':False})
    
