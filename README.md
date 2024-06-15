# 数据库课程设计——海洋温度预测

## 环境

* 前端：html+bootstrap+jquery

* 后端：Flask

* 数据库：MySQL

## 部署

* 1.安装依赖

  ```Linux
  pip install -r requirements.txt
  ```

* 2.安装MySQL数据库，并在MySQL数据库中建立数据库（假设为shmetro）

* 3.修改同目录下config.py的 `SQLALCHEMY_DATABASE_URI`

  `SQLALCHEMY_DATABASE_URI`的格式为：

  ```Python
    f'mysql+pymysql://root:{password_of_mysql}@localhost/{database_name}'
    # 例如mysql+pymysql://root:012704@localhost/shmetro
  ```

* 4.导入数据

  ```Linux
  python initdb.py
  ```

* 5.启动服务器

  ```Linux
  ./start.bat
  ```

* (可选)修改manage.py，使服务器的端口为自己设备的端口

  ```python
  # manage.py
  app.run(host="0.0.0.0",port=8000,debug=True)
  ```
