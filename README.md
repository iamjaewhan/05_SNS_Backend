# 과제 05- SNS_Backend

### 목차

------



#### 개발 기간

개발기간 : 2022.07.20 ~



#### 프로젝트 설명 분석

```
본 서비스는 SNS 서비스 입니다. 사용자는 본 서비스에 접속하여 게시물을 업로드하거나 다른 유저의 게시물을 확인하고, 좋아요를 할 수 있습니다.
```

##### 요구사항

##### A. 유저 관리

- 유저 회원가입

- 유저 로그인 및 인증

**B. 게시글**

- 게시글 생성
- 게시글 수정
- 게시글 삭제
- 게시글 복구
- 게시글 상세 보기
- 게시글 목록 보기





#### DB ERD







#### API 설계

| 기능명           | METHOD | URI                         | Path Variable                | Query Parameter                                              |
| ---------------- | ------ | --------------------------- | ---------------------------- | ------------------------------------------------------------ |
| 회원가입         | POST   | /users/signup               |                              | filter: 검색 해시태그<br/>search : 검색 게시글 내용, 제목<br/>order : 정렬 순서 |
| 로그인           | POST   | /users/login                |                              |                                                              |
| 게시글 목록 조회 | GET    | /posts                      |                              |                                                              |
| 게시글 등록      | POST   | /posts                      |                              |                                                              |
| 게시글 상세 조회 | GET    | /posts/\<int:post_id\>      | post_id(integer) : 게시글 ID |                                                              |
| 게시글 수정      | PATCH  | /posts/\<int:post_id\>      | post_id(integer) : 게시글 ID | title : 수정될 게시글 제목<br/>content : 수정될 게시글 내용<br/>hashtags : 수정될 해시태그 |
| 게시글 삭제      | DELETE | /posts/\<int:post_id\>      | post_id(integer) : 게시글 ID |                                                              |
| 삭제 게시글 복구 | PUT    | /posts/\<int:post_id\>      | post_id(integer) : 게시글 ID |                                                              |
| 게시글 좋아요    | PUT    | /posts/\<int:post_id\>/like | post_id(integer) : 게시글 ID |                                                              |
<details>
  <summary>회원가입</summary>
  
  - Request
  ```
  [POST] /users/signup
  {
    "email": "email",
    "password": ""
  }
  ```
  - Response
  ```
  201 Created
  {
    "user":{
      "id":1,
      "email":"email
    }
  }
  ```
</details>
<details>
  <summary>로그인</summary>
  
  - Request
  ```
  [POST] /users/login
  {
    "email": "email",
    "password": ""
  }
  ```
  - Response
  ```
  200 OK
    {
        "user": {
            "id": 1,
            "email": "사용자 이메일"
        },
        "access_token": "access token",
        "refresh_token": "refresh token"
    }
  ```
</details>
<details>
  <summary>게시글 목록 조회</summary>
  
  - Request
  ```
  [GET] /posts
  ```
  - Response
  ```
  200 OK
  {
    "current_page": 1,
    "previous_page": 1,
    "next_page": 9,
    "posts": [
        {
            "id": 1,
            "user": {
                "id": 2,
                "email": "user1@user.com"
            },
            "hashtag": [
                {
                    "id": 3,
                    "tag": "tag1"
                },
                {
                    "id": 5,
                    "tag": "taag3"
                },
                {
                    "id": 6,
                    "tag": "tag4"
                }
            ],
            "title": "test",
            "content": "test edited",
            "view_count": 18,
            "created_at": "2022-07-22T07:06:58.390862Z",
            "modified_at": "2022-07-27T12:50:28.066119Z"
        },
        ...
     ]
  }
  ```
</details>
<details>
  <summary>게시글 등록</summary>
  
  - Request
  ```
  [POST] /posts
  {
    "title":"post title",
    "content":"post content",
    "hashtags":"#new,#newpost,#new post with hashtags,#test"
  }
  ```
  - Response
  ```
  201 Created
  {
    "id": 12,
    "user": {
        "id": 2,
        "email": "user1@user.com"
    },
    "hashtag": [
        {
            "id": 8,
            "tag": "newpost"
        },
        {
            "id": 16,
            "tag": "test"
        },
        {
            "id": 17,
            "tag": "new"
        },
        {
            "id": 18,
            "tag": "new post with hashtags"
        }
    ],
    "title": "post title",
    "content": "post content",
    "view_count": 0,
    "created_at": "2022-08-03T06:40:57.261860Z",
    "modified_at": "2022-08-03T06:40:57.275859Z"
}
  ```
</details>
<details>
  <summary>게시글 상세 조회</summary>
  
  - Request
  ```
  [GET] /posts/<int:post_id>
  ```
  - Response
  ```
  200 OK
  {
    "id": 1,
    "user": {
        "id": 2,
        "email": "user1@user.com"
    },
    "hashtag": [
        {
            "id": 3,
            "tag": "tag1"
        },
        {
            "id": 5,
            "tag": "taag3"
        },
        {
            "id": 6,
            "tag": "tag4"
        }
    ],
    "title": "test",
    "content": "test edited",
    "view_count": 19,
    "created_at": "2022-07-22T07:06:58.390862Z",
    "modified_at": "2022-08-03T06:28:57.851554Z"
  }
  ```
</details>
<details>
  <summary>게시글 수정</summary>
  
  - Request
  ```
  [PATCH] /posts/<int:post_id>
  {
    "title":"modified title",
    "content":"modified content",
    "hashtags":"#new,#newpost,#modified"
  }
  ```
  - Response
  ```
  200 OK
  {
    "id": 1,
    "user": {
        "id": 2,
        "email": "user1@user.com"
    },
    "hashtag": [
        {
            "id": 17,
            "tag": "new"
        },
        {
            "id": 8,
            "tag": "newpost"
        },
        {
            "id": 19,
            "tag": "modified"
        }
    ],
    "title": "modified title",
    "content": "modified content",
    "view_count": 19,
    "created_at": "2022-07-22T07:06:58.390862Z",
    "modified_at": "2022-08-03T06:28:57.851554Z"
  }  
  ```
</details>
<details>
  <summary>게시글 삭제</summary>
  
  - Request
  ```
  [DELETE] /posts/<int:post_id>

  ```
  - Response
  ```
  200 OK

  ```
</details>
<details>
  <summary>삭제 게시글 복구</summary>
  
  - Request
  ```
  [PUT] /posts/<int:post_id>
  ```
  - Response
  ```
  200 OK

  ```
</details>
<details>
  <summary>게시글 좋아요</summary>
  
  - Request
  ```
  [POST] /post/<int:post_id>/like

  ```
  - Response
  ```
  201 Created

  ```
</details>



#### 테스트


