from django.shortcuts import render
from django.views import View

class VerifyOTPView(View):
    def get(self, request, *args, **kwargs):
        check_email = kwargs.get('email')
        if not check_email:
            return render(request,'admin/notfound/notfound.html')
        return render(request,'verify-otp.html', context={'email': check_email})