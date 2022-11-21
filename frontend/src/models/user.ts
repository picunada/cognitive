import type { Organization } from './organization'

export interface User {
  id: number
  email: string
  first_name: string
  last_name: string
  organization: Organization
  role: string
  created_at: Date
}

export interface UserCreate extends User {
  password: string
  confirm_password: string
}

export enum Roles {
  admin = 'administrator',
  manager = 'manager',
  client = 'client',
}
