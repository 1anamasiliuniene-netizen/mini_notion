from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Project, Task
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserProfileForm(forms.ModelForm):
    clear_photo = forms.BooleanField(required=False, label='Remove current photo')

    class Meta:
        model = UserProfile
        fields = ['photo', 'date_of_birth', 'address', 'drivers_category', 'education_documents']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Changes'))

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.cleaned_data.get('clear_photo'):
            profile.photo.delete(save=False)
            profile.photo = None
        if commit:
            profile.save()
        return profile


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'project_type', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Project'))

class ProjectEditForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'project_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'project_type': forms.Select(attrs={'class': 'form-select'}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'assigned_to', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Task'))


class TaskStatusForm(forms.ModelForm):
    completed = forms.BooleanField(required=False, label="Done")

    class Meta:
        model = Task
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.status == Task.STATUS_DONE:
            self.fields['completed'].initial = True

    def save(self, commit=True):
        task = self.instance
        if self.cleaned_data['completed']:
            task.status = Task.STATUS_DONE
        else:
            task.status = Task.STATUS_TODO
        if commit:
            task.save()
        return task
