from django import forms

chartChoice = (
    ("Line", "Line Chart"),
    ("Bar", "Bar Chart"),
)


class UploadFileForm(forms.Form):
    feature1 = forms.IntegerField()
    feature2 = forms.IntegerField()
    startRow = forms.IntegerField()
    endRow = forms.IntegerField()
    file = forms.FileField()
    chartType = forms.ChoiceField(choices=chartChoice)
