from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 7)]
SIZE_CHOICES = (
    ('-0.75', '-0.75'),
    ('-1.00', '-1.00'),
    ('-1.50', '-1.50'),
    ('-2.00', '-2.00'),
    ('-2.50', '-2.50'),
    ('-3.00', '-3.00'),
    ('-3.25', '-3.25'),
    ('-3.50', '-3.50'),
    ('-4.00', '-4.00'),
    ('-4.50', '-4.50'),
    ('-5.00', '-5.00'),
    ('-5.50', '-5.50'),
    ('-6.50', '-6.50'),
    ('-7.00', '-7.00'),
    ('+0.75', '+0.75'),
    ('+1.00', '+1.00'),
    ('+1.50', '+1.50'),
    ('+2.00', '+2.00'),
    ('+2.25', '+2.25'),
    ('+2.50', '+2.50'),
    ('+3.00', '+3.00'),
    ('+3.25', '+3.25'),
    ('+3.50', '+3.50'),
    ('+4.00', '+4.00'),
    ('+4.50', '+4.50'),
    ('+5.00', '+5.00'),
    ('+5.50', '+5.50'),
    ('+6.50', '+6.50'),
    ('+7.00', '+7.00'),
)


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(label='Количество',
                                      choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int,
                                      widget=forms.Select)

    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)

    size = forms.ChoiceField(label='size',
                             required=True,
                             choices=SIZE_CHOICES,
                             widget=forms.Select)


    class Meta:
        fields = ['quantity', 'update', 'size', ]
