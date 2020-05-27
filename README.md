## 校园 “知乎” 网页应用（Django）—— SJTU-SE407软件工程课第06组小组项目

### 注：该仓库中只包含Django网页应用的部分必要代码文件，不含db.sqlite3等文件。

#### 2020.5.27更新

#### 网站访问链接：

[点击访问](http://175.24.50.200:8000/)

#### 功能演示视频链接：

[点击访问](https://www.bilibili.com/video/BV15Q4y1P7B8/)

## 包括源代码文件如下：

> manage.py（服务器管理）


### --project/

> settings.py（服务器设置）

> urls.py（根路由）

> _init_.py

> asgi.py

> wsgi.py


### --login/（登录app）
> admin.py（管理）

> apps.py

> forms.py（表单）

> models.py（模型）

> tests.py

> urls.py（路由）

> views.py（视图函数）

>_init_.py

#### 以下省略其它app的类似.py文件

#### 包含以下模板文件
> about.html（我的信息）

> index.html（主页）

> login.html（登录页）

> register.html（注册页）

> comments.html（我的评论）

> follows.html（我的好友）

> info.html（别人看到的我的信息）

> likes.html（我的点赞）

> mailbox.html（我的信箱）

> posts.html（我的帖子）

> posts_ta（TA的帖子）

### --course/（课程板块app）

#### 包含以下模板文件

> index.html（课程版块主页）

> upload_file.html（上传资料页）

> courses/detail.html（课程信息详情页）

> teachers/detail.html（老师信息详情页）

> search/search.html（搜索结果页）

### --bbs/（帖子app）

#### 包含以下模板文件

> index.html（帖子版块主页）

> detail.html（帖子详情页）

> edit_page.html（帖子编辑页）

> comment_page.html（帖子评论页）
