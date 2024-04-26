# Determined AI训练平台搭建避坑

## Master节点搭建过程

### 准备镜像
使用如下命令分别拉取postgres和determined-master的镜像。

``` docker
docker pull postgres:10
docker pull determinedai/determined-master:VERSION 
```
> docker命令解析
> 
> `docker pull`:用于从远程仓库下载镜像。它是常用的 Docker 操作之一，用于获取远程仓库中的镜像，以便在本地 Docker 环境中运行容器。
> - postgres：这指定了要下载的镜像的名称。在这个例子中，postgres 表明下载的是 PostgreSQL 数据库的官方 Docker 镜像。
> - :10：这是镜像的标签（tag），用于指定想要下载的镜像版本。标签 10 指定了你希望下载的是 PostgreSQL 版本 10 的镜像。不同的标签可以对应同一镜像的不同版本，例如不同的发布版本或配置。如果不指定标签，Docker 默认使用 latest 标签，即最新版本的镜像。

### 启动PostgreSql容器
PostgreSQL 是一个非常流行的开源关系数据库系统，广泛用于生产环境中提供高可靠性、灵活性和强大的功能。Docker 容器化技术使得在各种环境中部署 PostgreSQL 变得更加简单和一致。

使用 Docker 容器运行 PostgreSQL 提供了以下优势：

1. 一致性和可重复性：容器确保了在任何地方运行的一致性，从而减少了“在我机器上可以运行”的问题。
2. 快速部署和隔离：容器可以在几秒钟内启动，每个容器运行在隔离的环境中，不会相互影响。
3. 易于配置：使用 Docker 镜像，可以预先定义和配置好数据库环境，使得部署更加方便快捷。
4. 开发与生产环境一致性：在开发、测试和生产环境中使用相同的容器，可以减少环境差异带来的问题。

使用如下命令启动PostgreSql镜像:
```
docker run \
    --name determined-db \
    -p 5432:5432 \
    -v determined_db:/var/lib/postgresql/data \
    -e POSTGRES_DB=determined \
    -e POSTGRES_PASSWORD=<DB password> \
    postgres:10
```
> docker命令解析
> - docker run: 这是 Docker 的命令，用于创建并启动一个新的容器。
>  - --name determined-db: 指定容器的名称为 determined-db。作为后续引用容器的唯一标识，例如在停止或查看日志时。
> - -p 5432:5432: 端口映射参数。这将容器内部的 5432 端口（PostgreSQL 的默认端口）映射到宿主机的 5432 端口。这允许外部系统（如另一台计算机或宿主机上的其他程序）通过宿主机的 5432 端口连接到容器中运行的 PostgreSQL 数据库。
> - -v determined_db:/var/lib/postgresql/data: 卷挂载参数。这将 Docker 卷 determined_db 挂载到容器内的 /var/lib/postgresql/data 目录。这是 PostgreSQL 存储其数据文件的地方，使用 Docker 卷可以确保即使容器被删除，数据也能持久保存。
> - -e POSTGRES_DB=determined: 环境变量，用于在容器启动时创建一个名为 determined 的数据库。
> - -e POSTGRES_PASSWORD=<DB password>: 环境变量，设置 PostgreSQL 数据库的密码。这里 <DB password> 应该被替换为你希望设定的实际数据库密码。
> - postgres:10: 指定要使用的 Docker 镜像及其版本。这里使用的是 PostgreSQL 的官方 Docker 镜像，版本号为 10。
