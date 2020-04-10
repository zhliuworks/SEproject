## 校园“知乎”网页应用（Django）—— 软件工程课小组项目

### 注：该仓库中只包含Django网页应用的部分必要代码文件，不含db.sqlite3等文件。

### 目前进度：基本框架搭建完毕，然后逐步开始实现以下内容：

#### （1）后端：帖子功能设计与编码等

#### （2）前端：部分页面渲染工作

#### 2020.4.10更新（第一轮迭代：第二周）

## 包括源代码文件如下：

> manage.py（服务器管理）


### --project/

> settings.py（服务器设置）

> urls.py（根路由）


### --login/（登录app）
> admin.py（管理）

> apps.py

> forms.py（表单）

> models.py（模型）

> tests.py

> urls.py（路由）

> views.py（视图函数）

#### 以下省略其它app的类似.py文件

#### 包含以下模板文件
> about.html（我的信息）

> index.html（主页）

> login.html（登录页）

> register.html（注册页）

### --course/（课程板块app）

#### 包含以下模板文件

> index.html（课程版块主页）

> courses/index.html（课程信息页）

> courses/detail.html（课程信息详情页）

> teachers/index.html（老师信息页）

> teachers/detail.html（老师信息详情页）

### --bbs/（帖子app）

#### 包含以下模板文件

> index.html（帖子版块主页）

> detail.html（帖子详情页）

> edit_page.html（帖子编辑页）
