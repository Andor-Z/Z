from django.db import models
from django.core.urlresolvers import reverse
from collections import defaultdict

# Create your models here.
class ArticleManager(models.Manager):
    def archive(self):
        date_list = Article.objects.datetimes('created_time', 'month', order='DESC')
        date_dict = defaultdict(list)
        for d in date_list:
            date_dict[d.year].append(d.month)
         # 模板不支持dict，因此把它转换成一个二级列表，由于字典转换后无序，因此重新降序排序
        return sorted(date_dict.items(), reverse=True)


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),  # draft（草稿）
        ('p', 'Published'),  # 已发布的
        ('s', 'secrecy')  # 保密
    )

    title = models.CharField('标题', max_length=70)
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    # auto_now_add 参数为True时， 则在创建时会自动添加当时时间
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)
    # auto_now=True表示每次修改时自动添加修改的时间
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES)
    # choices选项会使该field在被渲染成form时被渲染为一个select组件
    abstract = models.CharField('摘要', max_length=54, blank=True, null=True,
                                help_text="可选，若为空则将摘取正文的前54个字符")
    # help_text 在该 field 被渲染成 form 时显示帮助信息
    views = models.PositiveIntegerField('浏览量', default=0)
    # PositiveIntegerField存储非负整数
    likes = models.PositiveIntegerField('点赞数', default=0)
    topped = models.BooleanField('置顶', default=False)
    category = models.ForeignKey('Category', verbose_name='分类', null=True,
                                 on_delete=models.SET_NULL)
    # 外键的定义是：如果数据库中某个表的列的值是另外一个表的主键。
    # on_delete=models.SET_NULL表示删除某个分类（category）后该分类下所有的Article的外键设为null（空）
    tags = models.ManyToManyField('Tag', verbose_name='标签', blank=True)

    objects = ArticleManager()

    def __str__(self):
        return self.title

    class Meta:
        # Meta 包含一系列选项，这里的 ordering 表示排序，- 号表示逆序。即当从数据库中取出文章时，
        # 其是按文章最后一次修改时间逆序排列的。
        ordering = ['-last_modified_time']


    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'article_id': self.pk})


class Category(models.Model):
    name = models.CharField('类名', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField('标签名', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.name


class BlogComment(models.Model):
    user_name = models.CharField('评论者名字', max_length=100)
    user_email = models.EmailField('评论者邮箱', max_length=255)
    body = models.TextField('评论内容')
    created_time = models.DateTimeField('评论发表时间', auto_now_add=True)
    article = models.ForeignKey('Article', verbose_name='评论所属文章', on_delete=models.CASCADE)

    def __str__(self):
        return self.body[:20]