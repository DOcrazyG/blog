# 博客后端API文档

## 1. 文档说明

本文档详细描述了博客后端系统的所有API端点，旨在为前端开发团队提供清晰、规范的接口参考。文档内容基于当前后端实现，符合RESTful API设计规范，包含了所有必要的信息以支持前端开发和集成。

### 1.1 基础信息

- **API基础路径**: `/api`
- **认证方式**: Bearer Token (JWT)
- **响应格式**: JSON
- **数据传输**: UTF-8编码

### 1.2 状态码说明

| 状态码 | 描述 | 说明 |
|--------|------|------|
| 200 | OK | 请求成功 |
| 201 | Created | 资源创建成功 |
| 204 | No Content | 请求成功但无内容返回 |
| 400 | Bad Request | 请求参数错误 |
| 401 | Unauthorized | 未授权，需要登录 |
| 403 | Forbidden | 禁止访问，权限不足 |
| 404 | Not Found | 资源不存在 |
| 500 | Internal Server Error | 服务器内部错误 |

## 2. 认证相关API

### 2.1 用户注册

**路径**: `/api/auth/register`
**方法**: `POST`
**功能**: 注册新用户

#### 请求体参数

| 参数名 | 数据类型 | 是否必填 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| username | string | 是 | 无 | 用户名，长度3-50字符 |
| email | string | 是 | 无 | 邮箱地址，需符合邮箱格式 |
| password | string | 是 | 无 | 密码，长度至少6字符 |
| full_name | string | 否 | 无 | 用户全名，长度不超过100字符 |

#### 成功响应

**状态码**: `200 OK`

```json
{
  "id": 1,
  "username": "user1",
  "email": "user1@example.com",
  "full_name": "User One",
  "is_active": true,
  "is_admin": false,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

#### 错误响应

**状态码**: `400 Bad Request`

```json
{
  "detail": "Username already registered"
}
```

或

```json
{
  "detail": "Email already registered"
}
```

### 2.2 用户登录

**路径**: `/api/auth/login`
**方法**: `POST`
**功能**: 用户登录并获取访问令牌

#### 请求体参数

| 参数名 | 数据类型 | 是否必填 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| username | string | 是 | 无 | 用户名 |
| password | string | 是 | 无 | 密码 |

#### 成功响应

**状态码**: `200 OK`

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 错误响应

**状态码**: `401 Unauthorized`

```json
{
  "detail": "Incorrect username or password"
}
```

## 3. 用户相关API

### 3.1 获取当前用户信息

**路径**: `/api/users/me`
**方法**: `GET`
**功能**: 获取当前登录用户的详细信息

#### 权限要求

- 需要登录（Bearer Token）

#### 成功响应

**状态码**: `200 OK`

```json
{
  "id": 1,
  "username": "user1",
  "email": "user1@example.com",
  "full_name": "User One",
  "is_active": true,
  "is_admin": false,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

### 3.2 更新当前用户信息

**路径**: `/api/users/me`
**方法**: `PUT`
**功能**: 更新当前登录用户的信息

#### 权限要求

- 需要登录（Bearer Token）

#### 请求体参数

| 参数名 | 数据类型 | 是否必填 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| email | string | 否 | 无 | 邮箱地址，需符合邮箱格式 |
| full_name | string | 否 | 无 | 用户全名，长度不超过100字符 |
| password | string | 否 | 无 | 密码，长度至少6字符 |

#### 成功响应

**状态码**: `200 OK`

```json
{
  "id": 1,
  "username": "user1",
  "email": "newemail@example.com",
  "full_name": "New Name",
  "is_active": true,
  "is_admin": false,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-02T00:00:00Z"
}
```

#### 错误响应

**状态码**: `400 Bad Request`

```json
{
  "detail": "Email already registered"
}
```

### 3.3 获取指定用户信息

**路径**: `/api/users/{user_id}`
**方法**: `GET`
**功能**: 获取指定ID用户的详细信息

#### 权限要求

- 需要登录（Bearer Token）

#### URL路径参数

| 参数名 | 数据类型 | 是否必填 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| user_id | integer | 是 | 无 | 用户ID |

#### 成功响应

**状态码**: `200 OK`

```json
{
  "id": 2,
  "username": "user2",
  "email": "user2@example.com",
  "full_name": "User Two",
  "is_active": true,
  "is_admin": false,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

## 4. 文章相关API

### 4.1 创建新文章

**路径**: `/api/posts/`
**方法**: `POST`
**功能**: 创建新文章

#### 权限要求

- 需要登录（Bearer Token）

#### 请求体参数

| 参数名 | 数据类型 | 是否必填 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| title | string | 是 | 无 | 文章标题，长度1-255字符 |
| content | string | 是 | 无 | 文章内容 |
| summary | string | 否 | 无 | 文章摘要，长度不超过500字符 |
| is_published | boolean | 否 | false | 是否发布 |
| tag_ids | array[integer] | 否 | [] | 标签ID列表 |

#### 成功响应

**状态码**: `200 OK`

```json
{
  "id": 1,
  "title": "文章标题",
  "content": "文章内容",
  "summary": "文章摘要",
  "is_published": true,
  "tag_ids": [1, 2],
  "author_id": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null,
  "published_at": "2024-01-01T00:00:00Z",
  "author": {
    "id": 1,
    "username": "user1",
    "email": "user1@example.com",
    "full_name": "User One",
    "is_active": true,
    "is_admin": false,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": null
  },
  "tags": [
    {
      "id": 1,
      "name": "技术",
      "description": "技术相关",
      "created_at": "2024-01-01T00:00:00Z"
    },
    {
      "id": 2,
      "name": "Python",
      "description": "Python相关",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### 4.2 获取文章列表

**路径**: `/api/posts/`
**方法**: `GET`
**功能**: 获取已发布的文章列表，支持分页和筛选

#### URL查询参数

| 参数名 | 数据类型 | 是否必填 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| skip | integer | 否 | 0 | 跳过的记录数，最小值为0 |
| limit | integer | 否 | 10 | 返回的记录数，范围1-100 |
| tag_id | integer | 否 | 无 | 标签ID，用于筛选特定标签的文章 |
| search | string | 否 | 无 | 搜索关键词，用于搜索文章标题、内容和摘要 |

#### 成功响应

**状态码**: `200 OK`

```json
[
  {
    "id": 1,
    "title": "文章标题",
    "content": "文章内容",
    "summary": "文章摘要",
    "author_id": 1,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": null,
    "published_at": "2024-01-01T00:00:00Z",
    "is_published": true,
    "author": {
      "id": 1,
      "username": "user1",
      "email": "user1@example.com",
      "full_name": "User One",
      "is_active": true,
      "is_admin": false,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": null
    },
    "tags": [
      {
        "id": 1,
        "name": "技术",
        "description": "技术相关",
        "created_at": "2024-01-01T00:00:00Z"
      }
    ]
  }
]
```

### 4.3 获取当前用户的文章列表

**路径**: `/api/posts/me`
**方法**: `GET`
**功能**: 获取当前登录用户的所有文章列表，包括未发布的

#### 权限要求

- 需要登录（Bearer Token）

#### URL查询参数

| 参数名 | 数据类型 | 是否必填 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| skip | integer | 否 | 0 | 跳过的记录数，最小值为0 |
| limit | integer | 否 | 10 | 返回的记录数，范围1-100 |

#### 成功响应

**状态码**: `200 OK`

```json
[
  {
    "id": 1,
    "title": "文章标题",
    "content": "文章内容",
    "summary": "文章摘要",
    "author_id": 1,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": null,
    "published_at": "2024-01-01T00:00:00Z",
    "is_published": true,
    "author": {
      "id": 1,
      "username": "user1",
      "email": "user1@example.com",
      "full_name": "User One",
      "is_active": true,
      "is_admin": false,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": null
    },
    "tags": [
      {
        "id": 1,
        "name": "技术",
        "description": "技术相关",
        "created_at": "2024-01-01T00:00:00Z"
      }
    ]
  }
]
```

### 4.4 获取指定文章

**路径**: `/api/posts/{post_id}`
**方法**: `GET`
**功能**: 获取指定ID的文章详情

#### URL路径参数

| 参数名 | 数据类型 | 是否必填 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| post_id | integer | 是 | 无 | 文章ID |

#### 权限要求

- 对于已发布的文章：无需登录
- 对于未发布的文章：需要登录且为文章作者

#### 成功响应

**状态码**: `200 OK`

```json
{
  "id": 1,
  "title": "文章标题",
  "content": "文章内容",
  "summary": "文章摘要",
  "author_id": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null,
  "published_at": "2024-01-01T00:00:00Z",
  "is_published": true,
  "author": {
    "id": 1,
    "username": "user1",
    "email": "user1@example.com",
    "full_name": "User One",
    "is_active": true,
    "is_admin": false,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": null
  },
  "tags": [
    {
      "id": 1,
      "name": "技术",
      "description": "技术相关",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### 错误响应

**状态码**: `403 Forbidden`

```json
{
  "detail": "Not enough permissions"
}
```

**状态码**: `404 Not Found`

```json
{
  "detail": "Post not found"
}
```

### 4.5 更新文章

**路径**: `/api/posts/{post_id}`
**方法**: `PUT`
**功能**: 更新指定ID的文章

#### 权限要求

- 需要登录（Bearer Token）
- 必须是文章作者

#### URL路径参数

| 参数名 | 数据类型 | 是否必填 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| post_id | integer | 是 | 无 | 文章ID |

#### 请求体参数

| 参数名 | 数据类型 | 是否必填 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| title | string | 否 | 无 | 文章标题，长度1-255字符 |
| content | string | 否 | 无 | 文章内容 |
| summary | string | 否 | 无 | 文章摘要，长度不超过500字符 |
| is_published | boolean | 否 | 无 | 是否发布 |
| tag_ids | array[integer] | 否 | [] | 标签ID列表 |

#### 成功响应

**状态码**: `200 OK`

```json
{
  "id": 1,
  "title": "更新后的标题",
  "content": "更新后的内容",
  "summary": "更新后的摘要",
  "author_id": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-02T00:00:00Z",
  "published_at": "2024-01-01T00:00:00Z",
  "is_published": true,
  "author": {
    "id": 1,
    "username": "user1",
    "email": "user1@example.com",
    "full_name": "User One",
    "is_active": true,
    "is_admin": false,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": null
  },
  "tags": [
    {
      "id": 1,
      "name": "技术",
      "description": "技术相关",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### 错误响应

**状态码**: `403 Forbidden`

```json
{
  "detail": "Not enough permissions"
}
```

**状态码**: `404 Not Found`

```json
{
  "detail": "Post not found"
}
```

### 4.6 删除文章

**路径**: `/api/posts/{post_id}`
**方法**: `DELETE`
**功能**: 删除指定ID的文章

#### 权限要求

- 需要登录（Bearer Token）
- 必须是文章作者

#### URL路径参数

| 参数名 | 数据类型 | 是否必填 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| post_id | integer | 是 | 无 | 文章ID |

#### 成功响应

**状态码**: `204 No Content`

#### 错误响应

**状态码**: `403 Forbidden`

```json
{
  "detail": "Not enough permissions"
}
```

**状态码**: `404 Not Found`

```json
{
  "detail": "Post not found"
}
```

## 5. 评论相关API

### 5.1 创建新评论

**路径**: `/api/comments/`
**方法**: `POST`
**功能**: 为指定文章创建新评论

#### 权限要求

- 需要登录（Bearer Token）

#### 请求体参数

| 参数名 | 数据类型 | 是否必填 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| content | string | 是 | 无 | 评论内容，长度至少1字符 |
| post_id | integer | 是 | 无 | 文章ID |

#### 成功响应

**状态码**: `200 OK`

```json
{
  "id": 1,
  "content": "评论内容",
  "author_id": 1,
  "post_id": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null,
  "is_active": true,
  "author": {
    "id": 1,
    "username": "user1",
    "email": "user1@example.com",
    "full_name": "User One",
    "is_active": true,
    "is_admin": false,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": null
  }
}
```

#### 错误响应

**状态码**: `404 Not Found`

```json
{
  "detail": "Post not found"
}
```

### 5.2 获取指定文章的评论

**路径**: `/api/comments/post/{post_id}`
**方法**: `GET`
**功能**: 获取指定文章的所有活跃评论

#### URL路径参数

| 参数名 | 数据类型 | 是否必填 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| post_id | integer | 是 | 无 | 文章ID |

#### URL查询参数

| 参数名 | 数据类型 | 是否必填 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| skip | integer | 否 | 0 | 跳过的记录数，最小值为0 |
| limit | integer | 否 | 50 | 返回的记录数，范围1-100 |

#### 成功响应

**状态码**: `200 OK`

```json
[
  {
    "id": 1,
    "content": "评论内容",
    "author_id": 1,
    "post_id": 1,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": null,
    "is_active": true,
    "author": {
      "id": 1,
      "username": "user1",
      "email": "user1@example.com",
      "full_name": "User One",
      "is_active": true,
      "is_admin": false,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": null
    }
  }
]
```

#### 错误响应

**状态码**: `404 Not Found`

```json
{
  "detail": "Post not found"
}
```

### 5.3 更新评论

**路径**: `/api/comments/{comment_id}`
**方法**: `PUT`
**功能**: 更新指定ID的评论

#### 权限要求

- 需要登录（Bearer Token）
- 必须是评论作者

#### URL路径参数

| 参数名 | 数据类型 | 是否必填 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| comment_id | integer | 是 | 无 | 评论ID |

#### 请求体参数

| 参数名 | 数据类型 | 是否必填 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| content | string | 是 | 无 | 评论内容，长度至少1字符 |

#### 成功响应

**状态码**: `200 OK`

```json
{
  "id": 1,
  "content": "更新后的评论内容",
  "author_id": 1,
  "post_id": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-02T00:00:00Z",
  "is_active": true,
  "author": {
    "id": 1,
    "username": "user1",
    "email": "user1@example.com",
    "full_name": "User One",
    "is_active": true,
    "is_admin": false,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": null
  }
}
```

#### 错误响应

**状态码**: `403 Forbidden`

```json
{
  "detail": "Not enough permissions"
}
```

**状态码**: `404 Not Found`

```json
{
  "detail": "Comment not found"
}
```

### 5.4 删除评论

**路径**: `/api/comments/{comment_id}`
**方法**: `DELETE`
**功能**: 软删除指定ID的评论（将is_active设为false）

#### 权限要求

- 需要登录（Bearer Token）
- 必须是评论作者

#### URL路径参数

| 参数名 | 数据类型 | 是否必填 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| comment_id | integer | 是 | 无 | 评论ID |

#### 成功响应

**状态码**: `204 No Content`

#### 错误响应

**状态码**: `403 Forbidden`

```json
{
  "detail": "Not enough permissions"
}
```

**状态码**: `404 Not Found`

```json
{
  "detail": "Comment not found"
}
```

## 6. 标签相关API

### 6.1 创建新标签

**路径**: `/api/tags/`
**方法**: `POST`
**功能**: 创建新标签

#### 权限要求

- 需要登录（Bearer Token）
- 必须是管理员

#### 请求体参数

| 参数名 | 数据类型 | 是否必填 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| name | string | 是 | 无 | 标签名称，长度1-50字符 |
| description | string | 否 | 无 | 标签描述，长度不超过255字符 |

#### 成功响应

**状态码**: `200 OK`

```json
{
  "id": 1,
  "name": "技术",
  "description": "技术相关",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### 错误响应

**状态码**: `400 Bad Request`

```json
{
  "detail": "Tag name already exists"
}
```

### 6.2 获取标签列表

**路径**: `/api/tags/`
**方法**: `GET`
**功能**: 获取所有标签列表

#### URL查询参数

| 参数名 | 数据类型 | 是否必填 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| skip | integer | 否 | 0 | 跳过的记录数，最小值为0 |
| limit | integer | 否 | 100 | 返回的记录数，范围1-100 |

#### 成功响应

**状态码**: `200 OK`

```json
[
  {
    "id": 1,
    "name": "技术",
    "description": "技术相关",
    "created_at": "2024-01-01T00:00:00Z"
  },
  {
    "id": 2,
    "name": "Python",
    "description": "Python相关",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### 6.3 获取指定标签

**路径**: `/api/tags/{tag_id}`
**方法**: `GET`
**功能**: 获取指定ID的标签详情

#### URL路径参数

| 参数名 | 数据类型 | 是否必填 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| tag_id | integer | 是 | 无 | 标签ID |

#### 成功响应

**状态码**: `200 OK`

```json
{
  "id": 1,
  "name": "技术",
  "description": "技术相关",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### 错误响应

**状态码**: `404 Not Found`

```json
{
  "detail": "Tag not found"
}
```

### 6.4 更新标签

**路径**: `/api/tags/{tag_id}`
**方法**: `PUT`
**功能**: 更新指定ID的标签

#### 权限要求

- 需要登录（Bearer Token）
- 必须是管理员

#### URL路径参数

| 参数名 | 数据类型 | 是否必填 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| tag_id | integer | 是 | 无 | 标签ID |

#### 请求体参数

| 参数名 | 数据类型 | 是否必填 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| name | string | 否 | 无 | 标签名称，长度1-50字符 |
| description | string | 否 | 无 | 标签描述，长度不超过255字符 |

#### 成功响应

**状态码**: `200 OK`

```json
{
  "id": 1,
  "name": "更新后的标签名",
  "description": "更新后的描述",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### 错误响应

**状态码**: `400 Bad Request`

```json
{
  "detail": "Tag name already exists"
}
```

**状态码**: `404 Not Found`

```json
{
  "detail": "Tag not found"
}
```

### 6.5 删除标签

**路径**: `/api/tags/{tag_id}`
**方法**: `DELETE`
**功能**: 删除指定ID的标签

#### 权限要求

- 需要登录（Bearer Token）
- 必须是管理员

#### URL路径参数

| 参数名 | 数据类型 | 是否必填 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| tag_id | integer | 是 | 无 | 标签ID |

#### 成功响应

**状态码**: `204 No Content`

#### 错误响应

**状态码**: `404 Not Found`

```json
{
  "detail": "Tag not found"
}
```

## 7. 认证与授权

### 7.1 认证流程

1. 前端通过 `/api/auth/register` 注册新用户
2. 前端通过 `/api/auth/login` 登录，获取 access_token
3. 后续请求在请求头中携带 `Authorization: Bearer {access_token}` 进行认证

### 7.2 权限说明

- **公开接口**: 无需登录即可访问，如获取已发布文章列表、获取文章详情（已发布）、获取标签列表等
- **用户接口**: 需要登录才能访问，如创建文章、评论、更新个人信息等
- **管理员接口**: 需要管理员权限才能访问，如创建、更新、删除标签等

## 8. 缓存策略

系统使用Redis进行缓存，主要缓存以下数据：

- 文章列表
- 文章详情
- 评论列表
- 标签列表

当相关数据发生变化时，系统会自动清除对应的缓存，确保数据一致性。

## 9. 特殊说明

### 9.1 速率限制

系统暂未实现速率限制，生产环境建议添加。

### 9.2 跨域处理

系统已配置CORS中间件，允许所有来源的请求。生产环境建议设置具体的域名。

### 9.3 错误处理

系统实现了全局异常处理器，统一处理各类错误，返回标准化的错误响应。

### 9.4 数据验证

系统使用Pydantic V2进行数据验证，确保所有输入数据符合预期格式。

## 10. 接口测试

可使用以下工具测试API接口：

1. **Swagger UI**: 访问 `http://localhost:8000/docs`
2. **ReDoc**: 访问 `http://localhost:8000/redoc`
3. **Postman**: 导入API文档进行测试

## 11. 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0 | 2024-01-01 | 初始版本 |

---

本文档由后端开发团队维护，如有任何疑问或建议，请联系相关负责人。