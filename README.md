## pmpapi1000

#### 技术栈:

python3 -m venv flask

source flask/bin/activate

pip3 install flask

pip3 install flask-restful

pip3 install pymongo

#### -----------------------------------------------------------------------------

#### 当前版本：mongodb 3.6.3

#### 安装mongodb:
https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/#install-mongodb-community-edition



#### 配置3.6

http://blog.51cto.com/13598811/2083092

### 安装好以后，添加管理员账号：

use admin

db.createUser(
{
	user:"admin",
	pwd:"admin",
	roles: [ { role: "root", db: "admin" } ]
}
)


#### 添加测试数据库及数据库用户：

use testdb

db.createUser(
{
    user: "pmptikutest",
    pwd: "123456",
    roles: [ { role: "readWrite", db: "testdb" } ]
}
)


#### 编辑远程连接配置：

vim /etc/mongod.conf

#### 修改内容：

 network interfaces
net:
  port: 27017
  bindIp: 0.0.0.0
security:
  authorization: enabled