from django import forms

class HeartDiseaseForm(forms.Form):
    age = forms.FloatField(label="Age", min_value=1, max_value=120)
    gender = forms.ChoiceField(
        choices=[(1, "Nữ"), (2, "Nam")]
    )
    height = forms.FloatField(min_value=100, max_value=220)
    weight = forms.FloatField(min_value=30, max_value=200)
    ap_hi = forms.FloatField(label="Systolic blood pressure", min_value=80, max_value=250)
    ap_lo = forms.FloatField(label="Diastolic blood pressure", min_value=40, max_value=150)
    cholesterol = forms.ChoiceField(
        choices=[(1, "Ổn Định"), (2, "Cao"), (3, "Rất Cao")]
    )
    gluc = forms.ChoiceField(
        choices=[(1, "Ổn Định"), (2, "Cao"), (3, "Rất Cao")]
    )
    smoke = forms.ChoiceField(choices=[(0, "Không"), (1, "Có")])
    alco = forms.ChoiceField(choices=[(0, "Không"), (1, "Có")])
    active = forms.ChoiceField(choices=[(0, "Không"), (1, "Có")])
