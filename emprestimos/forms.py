from django.utils import timezone
from django import forms
from django.forms import inlineformset_factory
from .models import Emprestimo, EmprestimoItem

class EmprestimoForm(forms.ModelForm):
    def clean_previsao_devolucao(self):
        data = self.cleaned_data.get('previsao_devolucao')
        if data is None:
            return data
        # deve ser posterior ao momento atual
        if data <= timezone.now():
            raise forms.ValidationError("A data prevista para devolução deve ser futura.")
        return data

    class Meta:
        model = Emprestimo
        fields = ['colaborador', 'previsao_devolucao']

class EmprestimoItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # No cadastro (sem instance), ocultar opções Devolvido/Danificado/Perdido
        if not getattr(self.instance, 'pk', None):
            allowed = {'EMPRESTADO', 'FORNECIDO'}
            self.fields['status'].choices = [c for c in self.fields['status'].choices if c[0] in allowed]

    class Meta:
        model = EmprestimoItem
        fields = ['epi', 'quantidade', 'status', 'devolvido_em', 'observacao']

EmprestimoItemFormSet = inlineformset_factory(Emprestimo, EmprestimoItem, form=EmprestimoItemForm, extra=1)