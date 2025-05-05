from django import forms
from .models import Assessment, Result
from accounts.models import User
from departments.models import Course

class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['course', 'assessment_type', 'title', 'max_score', 'date_given', 'due_date', 'instructions']
        widgets = {
            'date_given': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'instructions': forms.Textarea(attrs={'rows': 3}),
        }

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'score', 'remarks']
    
    def __init__(self, *args, **kwargs):
        assessment = kwargs.pop('assessment', None)
        super(ResultForm, self).__init__(*args, **kwargs)
        
        if assessment:
            self.fields['student'].queryset = User.objects.filter(
                role=User.STUDENT,
                department=assessment.course.department
            )

class BulkResultUploadForm(forms.Form):
    assessment = forms.ModelChoiceField(queryset=Assessment.objects.all())
    file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with student results',
        widget=forms.FileInput(attrs={'accept': '.csv,text/csv'})
    )