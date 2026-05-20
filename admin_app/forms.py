from django import forms
import re
class formValidations(forms.ModelForm):
   def is_valid_username(name):
        
        pattern = r'^[a-zA-Z0-9._%+-]+@+[a-zA-Z]+mail\.com$'
    
        if re.match(pattern, name):
            return True
        else:
            return False
 