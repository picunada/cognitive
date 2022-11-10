import type { User } from '~/models/user'

export const admin: User = {
  id: 0,
  email: 'admin@example.com',
  first_name: 'admin',
  last_name: 'test',
  role: 'admin',
  created_at: new Date(),
}

export const manager: User = {
  id: 1,
  email: 'admin@example.com',
  first_name: 'admin',
  last_name: 'test',
  role: 'manager',
  created_at: new Date(),
}

export const users: Array<User> = [
  {
    id: 2,
    email: 'xlayst@example.com',
    first_name: 'Daniil',
    last_name: 'Test',
    role: 'user',
    created_at: new Date(),
  },
  {
    id: 3,
    email: 'test@example.com',
    first_name: 'John',
    last_name: 'Test',
    role: 'user',
    created_at: new Date(),
  },
  {
    id: 4,
    email: 'test1@example.com',
    first_name: 'Ava',
    last_name: 'Test',
    role: 'user',
    created_at: new Date(),
  },
  {
    id: 5,
    email: 'test2@example.com',
    first_name: 'Charlie',
    last_name: 'Test',
    role: 'user',
    created_at: new Date(),
  },
  {
    id: 6,
    email: 'test3@example.com',
    first_name: 'Joe',
    last_name: 'Knows',
    role: 'user',
    created_at: new Date(),
  },
]
