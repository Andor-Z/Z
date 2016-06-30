from django import forms
from .models import Article, BlogComment


class BlogCommentFrom(forms.ModelForm):
    class Meta:
        # Meta 包含一系列选项
        # 这里指定一些 Meta 选项以改变 form 被渲染后的样式
        model = BlogComment

        fields = ['user_name', 'user_email', 'body']
        widgets = {
            # 为各个需要渲染的字段指定渲染成什么html组件，主要是为了添加css样式。
            # 例如 user_name 渲染后的html组件如下：
            # <input type="text" class="form-control" placeholder="Username" aria-describedby="sizing-addon1">
            'user_name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':"请输入昵称",
                'aria-describedby':'sizing-addon1',
            }),
            'user_email': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':"请输入邮箱",
                'aria-describedby':'sizing-addon1',
            }),
            'body': forms.Textarea(attrs={
                'class':'form-control',
                'rows': "3",
                'placeholder':"来说两句",
            }),
        }