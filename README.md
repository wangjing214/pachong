# pachong
菜鸟教程(https://www.runoob.com/)，该网站有多种语言的入门教程，我是从站点地图为入口查询网站提供的所有教程的入口，然后在第一个入口页面查询该教程对应的所有学习内容列表。该程序暂时不支持下载图片。全部教程采集成功后，如果需要在页面上展示，需要将内容页的相关css样式也复制下来否则呈现的效果和源网站样式不一样就会好丑。

华为云博客(https://bbs.huaweicloud.com/blogs)，这个网站比较好的地方是，有一个展示全部博客的页面，能展示就意味着可以被下载保存。huaweiyun.py是抓取该博客的程序，使用了log_huaweiyun和log_huaweiyun_data这2个数据表来保存数据，因为博客内容较长如果和标题、发布时间放在一起在做查询列表时会慢，所以分别做了存储。该程序支持下载内容中的图片，并用本地路径替换内容的图片连接。

安全客(https://www.anquanke.com/)，这个网站比较好的地方是，有一个可以查询全部博客的api接口（爽歪歪~），最主要的是该接口中可以自定义每页展示数量size（这点减少好多次循环），一开始size设置了100可以很快返回，size设置1000大概5秒，size设置1500时页面异常了，抓取时可以设置为size=100，这样一来不会成为慢查询被安全客运维人员发现二来抓取速度稳定。为了不被网站运维人员禁封iP，在调用api和拉详情页时睡眠2秒钟假装自己是正常访客，该程序不支持下载图片。anquanke.py是抓取该博客的程序，使用了log_anquanke这个数据表来保存数据，该表将标题和内容一并保存了。
