from django import forms
from .models import Message
from accounts.models import User
from django.db.models import Q

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text', 'attachment']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Type your message here...',
                'rows': 3
            }),
            'attachment': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,.pdf,.doc,.docx,.ppt,.pptx,.xls,.xlsx'
            })
        }
class NewThreadForm(forms.Form):
    recipient = forms.ModelChoiceField(queryset=User.objects.none())
    message = forms.CharField(widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(NewThreadForm, self).__init__(*args, **kwargs)
        
        if user:
            if user.role == User.STUDENT:
                self.fields['recipient'].queryset = User.objects.filter(
                    Q(role=User.PROFESSOR, department=user.department) | 
                    Q(role=User.STUDENT, department=user.department)
                ).exclude(id=user.id)
            elif user.role == User.PROFESSOR:
                self.fields['recipient'].queryset = User.objects.filter(
                    Q(role=User.STUDENT, department=user.department) | 
                    Q(role=User.PROFESSOR)
                ).exclude(id=user.id)