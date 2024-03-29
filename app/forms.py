'''
2023/8/7
googvilla01
forms.py
by yhlin
'''
import logging

from django import forms
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from datetime import datetime

from .models import WorkRecord, Mood_Choice


class WorkRecordForm(forms.ModelForm):

    def __init__(self,*args, **kwargs):
        super(WorkRecordForm,self).__init__(*args, **kwargs)
        initial = kwargs.get('initial', {})

        xuser = initial['user']
        detail = initial['detail']
        # self.fields['working_date'] = datetime.now()
        self.fields['user'].initial = xuser
        self.fields['detail'].initial= detail

    class Meta:
        model = WorkRecord
        fields = ('user','detail','working_date','start_time','end_time','bonus','mood','comment',)
        # fields = ( 'comment',)
        widgets = {
            'working_date':forms.DateInput(
                attrs={'placeholder':'輸入工作日期',
                       'class':'form-control',
                       'type':'date'},

            ),

            'start_time':forms.DateInput(
                        attrs={'placeholder': '輸入起始時間',
                               'class': 'form-control',
                               'type': 'datetime-local'}),
            'end_time': forms.DateInput(
                attrs={'placeholder': '輸入結束時間',
                       'class': 'form-control',
                       'type': 'datetime-local'}),
            'mood':forms.RadioSelect(attrs={'class':' form-check-inline'}),
            'bonus':forms.TextInput(attrs={'class':'form-control',}),
            'comment':forms.Textarea(attrs={'class':'form-control','row':20})
        }



    def save(self,commit = True):
        instance = super(WorkRecordForm,self).save(commit=False)
        instance.calculate_spend_time()

        if commit:
            instance.save()
        return instance

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='請輸入密碼', widget=forms.PasswordInput)
    password2 = forms.CharField(label='請再次輸入密碼', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','first_name','email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('兩次密碼不相同')
        return cd['password2']
