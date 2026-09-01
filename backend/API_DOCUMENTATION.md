# Campus Skill Network - Backend API Documentation

## Base URL

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

---

# 1. Authentication APIs

## Signup

### POST `/auth/signup`

Creates a new user account.

### Request Body

```json
{
  "email": "student@gmail.com",
  "password": "student123"
}