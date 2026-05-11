"""
**Input Prompt**: Handle a user-submitted message and insert it into the database.
**Intention**: Store user messages securely and redirect the user back to the main page.
**Functionality**:
    - Retrieves username and message from the request.
    - Calls `insert_user_message_in_db` function to save the message.
    - Redirects user back to the main page.
"""

from django.shortcuts import redirect, render
from .forms import MessageForm
from .models import UserMessage


def post(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            user_message = form.save(commit=False)
            user_message.username = request.user.username
            user_message.save()
            return redirect("main")
    else:
        form = MessageForm()

    messages = UserMessage.objects.all().order_by("-created_at")
    context = {"form": form, "messages": messages}
    return render(request, "main.html", context)
