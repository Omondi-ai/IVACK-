from django import forms
from .models import Post
from departments.models import Department, Course
from accounts.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'target_type', 'department', 'course', 'professor', 'file', 'image']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PostForm, self).__init__(*args, **kwargs)
        
        if user and user.role == User.STUDENT:
            self.fields['professor'].queryset = User.objects.filter(role=User.PROFESSOR)
        
        if 'target_type' in self.data:
            try:
                target_type = self.data.get('target_type')
                if target_type == 'DE':
                    self.fields['department'].required = True
                    self.fields['course'].required = False
                    self.fields['professor'].required = False
                elif target_type == 'CO':
                    self.fields['course'].required = True
                    self.fields['department'].required = False
                    self.fields['professor'].required = False
                elif target_type == 'PR':
                    self.fields['professor'].required = True
                    self.fields['department'].required = False
                    self.fields['course'].required = False
                else:
                    self.fields['department'].required = False
                    self.fields['course'].required = False
                    self.fields['professor'].required = False
            except (ValueError, TypeError):
                pass