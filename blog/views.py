from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from .models import Article, Category, Tag
from .forms import BlogCommentFrom
import markdown2

# Create your views here.
class IndexView(ListView):
    template_name = "blog/index.html"
    context_object_name = "article_list"
    # 给上下文变量取名

    def get_queryset(self):
        article_list = Article.objects.filter(status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'],)
        return article_list

    def get_context_data(self, **kwargs):
        # 增加额的数据，这里返回一个文章分类，以字典的形式
        # kwargs['category_list'] = Category.objects.all().order_by('name')
        # return super(IndexView, self).get_context_data(**kwargs)
        context = super(IndexView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all().order_by('name')
        context['tag_list'] = Tag.objects.all().order_by('name')
        context['date_archive'] = Article.objects.archive()
        return context 


class CategoryView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        article_list = Article.objects.filter(category=self.kwargs['cate_id'], status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'],)
        return article_list

    def get_context_data(self, **kwargs):
        # 增加额的数据，这里返回一个文章分类，以字典的形式
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all().order_by('name')
        context['tag_list'] = Tag.objects.all().order_by('name')
        context['date_archive'] = Article.objects.archive()
        return context


class TagView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        article_list = Article.objects.filter(tags=self.kwargs['tag_id'], status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'],)
        return article_list

    def get_context_data(self, **kwargs):
        # 增加额的数据，这里返回一个文章分类，以字典的形式
        context = super(TagView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all().order_by('name')
        context['tag_list'] = Tag.objects.all().order_by('name')
        context['date_archive'] = Article.objects.archive()
        return context


class ArchiveView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        article_list = Article.objects.filter(created_time__year=year, created_time__month=month, status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'],)
        return article_list

    def get_context_data(self, **kwargs):
        # 增加额的数据，这里返回一个文章分类，以字典的形式
        context = super(ArchiveView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all().order_by('name')
        context['tag_list'] = Tag.objects.all().order_by('name')
        context['date_archive'] = Article.objects.archive()
        return context


class ArticleDetailView(DetailView):
    # 继承于基于类的视图DetailView,用于显示一个对象的详情页面
    model = Article
    # 指定视图获取哪个model
    template_name = 'blog/detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'article_id'
    # 用于接收一个来自url中的主键，然后根据这个主键进行查询

    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        obj.body = markdown2.markdown(obj.body, extras=['fenced-code-blocks'],)
        # get_object返回该视图要显示的对象。若设有queryset，则该queryset用于对象的源
        # 否则将使用get_queryset().get_object()从视图的所有参数中查找 pk_url_kwarg 参数；
        # 如果找到了这个参数，该方法使用这个参数的值执行一个基于主键的查询。
        return obj

    def get_context_data(self, **kwargs):
        # 增加额的数据，这里返回一个文章分类，以字典的形式
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all().order_by('name')
        context['tag_list'] = Tag.objects.all().order_by('name')
        context['date_archive'] = Article.objects.archive()
        context['comment_list'] = self.object.blogcomment_set.all()
        context['form'] = BlogCommentFrom()
        return context


class CommentPostView(FormView):
    """提交的数据验证合法后的逻辑"""
    form_class = BlogCommentFrom
    template_name = 'blog/detail.html'

    def form_valid(self, form):
        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        comment = form.save(commit=False)

        comment.article = target_article
        comment.save()

        self.success_url = target_article.get_absolute_url()
        return  HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
         """提交的数据验证不合法后的逻辑"""
         target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])
         return render(self.request, 'blog/detail.html', {
            'form': form,
            'article': target_article,
            'comment_list': target_article.blogcomment_set.all(),
         })