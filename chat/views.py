from django.shortcuts import render
from django.views import View
from django.contrib.auth import get_user_model
from django.shortcuts import Http404
from chat.models import Thread, Message
from lxfpro.mongo_models import MongoChatMessage, MongoActivityLog
from datetime import datetime


class ThreadView(View):
    template_name = 'chat/chat.html'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        self.other_user = get_user_model().objects.get(username=other_username)
        obj = Thread.objects.get_or_create_personal_thread(self.request.user, self.other_user)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = {}
        context['me'] = self.request.user
        context['thread'] = self.get_object()
        context['user'] = self.other_user
        context['messages'] = self.get_object().message_set.all()
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context=context)

    def post(self, request, **kwargs):
        self.object = self.get_object()
        thread = self.get_object()
        data = request.POST
        user = request.user
        text = data.get("message")
        
        # Save to SQLite (existing)
        Message.objects.create(sender=user, thread=thread, text=text)
        
        # Save to MongoDB Atlas with notification
        try:
            MongoChatMessage.create(
                sender_id=user.id,
                receiver_id=self.other_user.id,
                message=text,
                thread_id=str(thread.id)
            )
            
            # Log activity
            MongoActivityLog.log(
                user_id=user.id,
                action='sent_message',
                details={'to': self.other_user.username, 'text': text[:50]}
            )
        except Exception as e:
            print(f"MongoDB save error: {e}")
        
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context=context)