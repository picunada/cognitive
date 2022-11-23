import type { Organization } from './organization'

export interface User {
  id: number
  email: string
  first_name: string
  last_name: string
  role: string
  created_at: Date
}

export interface UserRetrieve extends User {
  organization: Organization[]
}

export interface UserCreate extends User {
  organization: [number]
  password: string
  confirm_password: string
}

export enum Roles {
  admin = 'administrator',
  manager = 'manager',
  client = 'client',
}
