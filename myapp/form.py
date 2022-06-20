from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        fields = ('postid','creatorid','creator','panchayath','description','pimage')

# class UserForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(UserForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control'
#     class Meta:
#         model = UserReg
#         fields = ('uid','fname','lname','house_name','house_number','gender','dob','photo','username', 'password', 'email', 'phone_number', 'panchayath', 'district', 'state', 'country')
#         # widgets = {
        #     'uid': forms.NumberInput(attrs={'class': 'form-control'}),
        #     'fname': forms.TextInput(attrs={'class': 'form-control'}),
        #     'lname': forms.TextInput(attrs={'class': 'form-control'}),
        #     'username': forms.TextInput(attrs={'class': 'form-control'}),
        #     'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'house_name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'house_number': forms.NumberInput(attrs={'class': 'form-control'}),
        #     'gender': forms.TextInput(attrs={'class': 'form-control' }),
        #     # 'dob': forms.DateField(),
        #     # 'photo': forms.ImageField(),
        #
        #     'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        #     'panchayath': forms.TextInput(attrs={'class': 'form-control'}),
        #     'district': forms.TextInput(attrs={'class': 'form-control'}),
        #     'state': forms.TextInput(attrs={'class': 'form-control'}),
        #     'country': forms.TextInput(attrs={'class': 'form-control'}),
        #
        # }


# class MessageForm(forms.ModelForm):
#     class Meta:
#         model = Message
#         fields = ['message']

# class ComplaintForm(forms.ModelForm):
#     class Meta:
#         model = Complaints
#         fields = '__all__'

# class AnnouncementForm(forms.ModelForm):
#     class Meta:
#         model = Announcement
#         fields = '__all__'
