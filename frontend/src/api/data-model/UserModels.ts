

export type LoginRequest = {
  username: string;
  password: string;
};

export type LoginResponse = {
  username: string;
  user_id: string;
};

export type UserResponse = {
  id: string;
  username: string;
  role: string;
  is_locked: boolean;
  logout_timestamp?: string;
}

export type CreateUserRequest = {
  username: string;
  password: string;
  password_confirmation: string;
  role: string;
}