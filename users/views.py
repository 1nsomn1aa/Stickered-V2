from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from shop.models import Order
from home.models import ContactMessage
from .forms import UserRegisterForm, ProfileForm
from allauth.account.views import LoginView


# Order detail view
@login_required
def order_detail(request, order_number):
    order = get_object_or_404(
        Order,
        order_number=order_number,
        user=request.user)
    return render(request, 'users/order_detail.html', {'order': order})


# User profile page: view and update profile, view past orders and messages
@login_required
def profile_view(request):
    user = request.user
    profile = user.profile
    orders = Order.objects.filter(user=user).order_by('-created_at')
    contact_messages = ContactMessage.objects.filter(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile, user=user)

    return render(request, 'users/profile.html', {
        'form': form,
        'profile': profile,
        'orders': orders,
        'contact_messages': contact_messages,
    })


# User registration view
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                messages.error(
                    request, f'Username {username} is already taken.')
                return render(request, 'users/register.html', {'form': form})

            user = form.save()
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


# Custom login view
class CustomLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        return response


# Delete a contact message
@login_required
def delete_contact_message(request, message_id):
    message = get_object_or_404(
        ContactMessage,
        id=message_id,
        user=request.user)
    message.delete()
    messages.success(request, "Your message has been deleted.")
    return redirect('profile')
