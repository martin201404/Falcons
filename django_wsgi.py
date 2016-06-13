<uwsgi>
    <socket>127.0.0.1:8080</socket> <!-- 和nginx中定义的要一致 -->
    <chdir>/home/rich/django-puppet-web-admin/puppet_web</chdir>      <!-- 你django的项目目录 -->
    <module>django_wsgi</module> <!-- 名称为刚才上面定义的py文件名 -->
    <processes>4</processes> <!-- 进程数 --> 
    <daemonize>/var/log/uwsgi.log</daemonize>
</uwsgi>
