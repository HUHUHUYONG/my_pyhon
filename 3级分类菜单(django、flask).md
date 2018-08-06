# 3级分类菜单(django、flask)

## django

### models.py

```
class Category(models.Model):
    cate_id = models.AutoField('分类ID',
                               primary_key=True)
    name = models.CharField('名称', max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name = '分类菜单'
        verbose_name_plural = '菜单管理'
        
        
 class SubMenu(models.Model):
    sub_menu_id = models.AutoField('ID', primary_key=True)
    name = models.CharField('名称', max_length=255, blank=True, null=True)
    cate = models.ForeignKey(Category, models.DO_NOTHING, db_column='cate_id', db_index=True,
                             verbose_name='父菜单')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sub_menu'
        verbose_name = '一级菜单'
        verbose_name_plural = '一级菜单管理'


class SubMenu2(models.Model):
    sub_menu2_id = models.AutoField('ID', primary_key=True)
    name = models.CharField('名称', max_length=255)
    sub_menu = models.ForeignKey(SubMenu, models.DO_NOTHING, db_column='sub_menu_id', db_index=True,
                                 verbose_name='父菜单')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sub_menu2'
        verbose_name = '二级菜单'
        verbose_name_plural = '二级菜单管理'
```

### views.py

```
def index(request):
    # 获取分类菜单的数据
    categories = Category.objects.all()
    for category in categories:
        #通过遍历得到每个一级分类的子类
        category.subs = category.submenu_set.all()
        # 获取分类二级菜单的数据
        for sub in category.subs:
            # 获取分类二级菜单的子数据
            sub.subs2 = sub.submenu2_set.all()

    return render(request, 'index.html', {'categories': categories})
```

### urls.py

```
from apps.home import views
from django.conf.urls import url

urlpatterns = [
  url('^$', views.index, name='index'),
]
```

### html

```
<div class="category_menu">
    {% for category in  categories %}
        <!-- 一级菜单的数据-->
        <div class="category_menu_item">
            <span class="glyphicon glyphicon-gift"></span>
            <a href="">{{ category.name }}</a>
        </div>
        <!-- 一级菜单对应的二级菜单的数据-->
        <ul class="category_sub">
            {% for  sub in  category.subs %}
                <li class="clear">
                    <a style="float: left" href="#">{{ sub.name }}</a>
                    {% for sub2 in sub.subs2 %}
                        <div style="float: left">
                            <a class="category_sub_item">{{ sub2.name }}</a>
                        </div>
                    {% endfor %}
                </li>
            {% endfor %}
        </ul>
    {% endfor %}
</div>
```

### css

```
.glyphicon {
  position: relative;
  top: 1px;
  display: inline-block;
  font-family: 'Glyphicons Halflings';
  -webkit-font-smoothing: antialiased;
  font-style: normal;
  font-weight: normal;
  line-height: 1;
  -moz-osx-font-smoothing: grayscale;
}

.glyphicon:empty {
  width: 1em;
}

.category_sub {
    background: white;
    width: 800px;
    height: 510px;
    display: none;
    position: absolute;
    top: 0;
    left: 200px;
}

.category_sub > li, .category_sub_item {
    padding: 10px 15px;
    cursor: pointer;
}

.category_sub a {
    color: #A7A7A7;
    font-size: 15px;
}

/*清除浮动*/
.clear {
    zoom: 1;
}

.clear:after {
    clear: both;
    content: '';
    display: block;
    width: 0;
    height: 0;
    visibility: hidden;
}


```



### js

```
<script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.js"></script>
<script type="text/javascript" language="JavaScript">
    $(function () {

        $('.category_menu_item').mouseover(function () {
            // 隐藏所有二级子菜单
            $('.category_sub').hide();
            $(this).next().show();
        });
        $('.category_menu').mouseleave(function () {
            // 隐藏所有二级子菜单
            $('.category_sub').hide();
        });

        $('#banner').unslider({auto: true, dots: true});

        $('.selected').click(function () {
            $(this).toggle();
            $('.shop_review_wrap').toggle()
        });

        $('.detail_review_link').click(function () {
            $(this).toggle();
            $('.shop_param_part_warp').toggle()
        })
    });
</script>
```

---



## flask

### models.py

```
from apps.ext import db


class Category(db.Model):
    cate_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    submenus = db.relationship('SubMenu', backref='category')


class SubMenu(db.Model):
    sub_menu_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    cate_id = db.Column(db.Integer, db.ForeignKey(Category.cate_id))
    submenu2s = db.relationship('SubMenu2', backref='submenu')


class SubMenu2(db.Model):
    sub_menu2_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    sub_menu_id = db.Column(db.Integer, db.ForeignKey(SubMenu.sub_menu_id))
```

### views.py

```
from flask import Blueprint, render_template

from apps.menu.models import Category

menu = Blueprint('menu', __name__, template_folder='./templates')


@menu.route('/index/')
def index():
    # 获取分类菜单的数据
    categories = Category.query.all()
    for category in categories:
        # 通过遍历得到每个一级分类的子类
        category.subs = category.submenus
        # 获取分类二级菜单的数据
        for sub in category.subs:
            # 获取分类二级菜单的子数据
            sub.subs2 = sub.submenu2s

    return render_template('menu_index.html', categories=categories)
```

### menu_index.html

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        .glyphicon {
            position: relative;
            top: 1px;
            display: inline-block;
            font-family: 'Glyphicons Halflings';
            -webkit-font-smoothing: antialiased;
            font-style: normal;
            font-weight: normal;
            line-height: 1;
            -moz-osx-font-smoothing: grayscale;
        }

        .glyphicon:empty {
            width: 1em;
        }

        .category_sub {
            background: white;
            width: 800px;
            height: 510px;
            display: none;
            position: absolute;
            top: 0;
            left: 200px;
        }

        .category_sub > li, .category_sub_item {
            padding: 10px 15px;
            cursor: pointer;
        }

        .category_sub a {
            color: #A7A7A7;
            font-size: 15px;
        }

        /*清除浮动*/
        .clear {
            zoom: 1;
        }

        .clear:after {
            clear: both;
            content: '';
            display: block;
            width: 0;
            height: 0;
            visibility: hidden;
        }
    </style>
    <script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.js"></script>
    <script type="text/javascript" language="JavaScript">
        $(function () {

            $('.category_menu_item').mouseover(function () {
                // 隐藏所有二级子菜单
                $('.category_sub').hide();
                $(this).next().show();
            });
            $('.category_menu').mouseleave(function () {
                // 隐藏所有二级子菜单
                $('.category_sub').hide();
            });

            $('#banner').unslider({auto: true, dots: true});

            $('.selected').click(function () {
                $(this).toggle();
                $('.shop_review_wrap').toggle()
            });

            $('.detail_review_link').click(function () {
                $(this).toggle();
                $('.shop_param_part_warp').toggle()
            })
        });
    </script>
</head>
<body>
<div class="category_menu">
    {% for category in  categories %}
        <!-- 一级菜单的数据-->
        <div class="category_menu_item">
            <span class="glyphicon glyphicon-gift"></span>
            <a href="">{{ category.name }}</a>
        </div>
        <!-- 一级菜单对应的二级菜单的数据-->
        <ul class="category_sub">
            {% for  sub in  category.subs %}
                <li class="clear">
                    <a style="float: left" href="#">{{ sub.name }}</a>
                    {% for sub2 in sub.subs2 %}
                        <div style="float: left">
                            <a class="category_sub_item">{{ sub2.name }}</a>
                        </div>
                    {% endfor %}
                </li>
            {% endfor %}
        </ul>
    {% endfor %}
</div>


</body>
</html>
```

