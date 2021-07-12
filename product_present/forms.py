from django import forms

from .models import HandProductComment


class CommentForm(forms.ModelForm):
    # text = forms.CharField(widget=forms.Textarea,required=False, error_messages={"required":"bayad por mikardi"})
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'text-test'})
        self.fields['rate'].widget.attrs.update({'style':"color:red;"})

    class Meta:
        model = HandProductComment
        exclude = ("user", "hand_product",)
        labels ={
            "rate" : "ریت"
        }
        help_texts = {
            "rate": "ریت این کالا را وارد کن"
        }

        error_messages ={
            "rate":{
                "max_value": "عدد بیشتر از  5 ممنوعه",
                "min_value": "عدد کمتر از صفر ممنوعه",
            },
        }
