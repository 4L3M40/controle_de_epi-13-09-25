# IMPORTANTE
# Você adicionou o campo `status` em EmprestimoItem.
# Execute as migrações no seu ambiente:
#   python manage.py makemigrations emprestimos
#   python manage.py migrate

Alterações:
{
  "emprestimos/forms.py:clean_previsao_devolucao": "Added future-date validation.",
  "emprestimos/forms.py:item": "Expose status field; restrict choices on create; include devolvido_em/observacao.",
  "emprestimos/views.py:ReadonlyContextMixin": "Added readonly context mixin.",
  "templates/emprestimos/emprestimo_form.html": "Structured form, readonly banner, conditional fields logic.",
  "templates/base.html": "Added quick links to EPIs and Empréstimos."
}