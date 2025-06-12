# Social Media Posts API

A FastAPI-based REST API for managing social media posts with PostgreSQL database integration using SQLModel/SQLAlchemy.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete posts
- **PostgreSQL Integration**: Robust database connection with SQLModel/SQLAlchemy
- **Environment Configuration**: Secure database credentials management
- **Data Validation**: Pydantic models for request/response validation
- **Auto Documentation**: Interactive API docs with FastAPI
- **Pagination Support**: Efficient data retrieval with skip/limit parameters

## Project Structure

```
social_media/
├── app/
│   ├── __init__.py
│   ├── database.py          # Database connection and session management
│   ├── main.py             # FastAPI application and API routes
│   └── models.py           # SQLModel data models and schemas
├── .env                    # Environment variables (create this file)
└── README.md              # This file
```
## API Endpoints

### Posts Management

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| `GET` | `/` | Root endpoint | None |
| `POST` | `/posts/` | Create a new post | `PostCreate` |
| `GET` | `/posts/` | Get all posts (with pagination) | Query params: `skip`, `limit` |
| `GET` | `/posts/{post_id}` | Get specific post by ID | None |
| `PUT` | `/posts/{post_id}` | Update specific post | `PostUpdate` |
| `DELETE` | `/posts/{post_id}` | Delete specific post | None |

### Example Requests

#### Create a Post
```bash
curl -X POST "http://localhost:8000/posts/" \
-H "Content-Type: application/json" \
-d '{
  "title": "My First Post",
  "content": "This is the content of my first post!",
  "published": true
}'
```

#### Get All Posts
```bash
curl "http://localhost:8000/posts/?skip=0&limit=10"
```

#### Update a Post
```bash
curl -X PUT "http://localhost:8000/posts/1" \
-H "Content-Type: application/json" \
-d '{
  "title": "Updated Post Title",
  "content": "Updated content"
}'
```

## Data Models

### Post Schema
```python
{
  "id": int,                    # Auto-incrementing primary key
  "title": str,                 # Required, post title
  "content": str,               # Required, post content
  "published": bool,            # Optional, defaults to true
  "date_created": datetime      # Auto-generated timestamp
}
```

### Request/Response Models
- **PostCreate**: For creating new posts (`title`, `content`, `published?`)
- **PostRead**: For API responses (all fields including `id` and `date_created`)
- **PostUpdate**: For updating posts (all fields optional)

## Database Schema

The `posts` table is automatically created with the following structure:

```sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    content VARCHAR NOT NULL,
    published BOOLEAN DEFAULT true,
    date_created TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Development

### Database Connection
The application uses SQLModel (built on SQLAlchemy) for database operations:
- Connection pooling and session management
- Automatic table creation on startup
- Environment-based configuration

### Error Handling
- 404 errors for non-existent posts
- Validation errors for invalid input data
- Database connection error handling

### Logging
Database queries are logged when running in development mode (`echo=True` in engine configuration).

### Planned Work
- Create user registration system using JWT and OAuth2
- Implementing likes
- Containerize using Heroku and Docker
- Set up testing and production environments
- Set up CI/CD pipeline using Github Actions
- Deploy