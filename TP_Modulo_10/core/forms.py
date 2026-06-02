"""ModelForm para Post, usado por CreateView y UpdateView."""

from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "published_date", "author", "tags"]
        widgets = {
            "published_date": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "content": forms.Textarea(attrs={"rows": 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Permite que el input datetime-local muestre el valor al editar
        self.fields["published_date"].input_formats = ["%Y-%m-%dT%H:%M"]
