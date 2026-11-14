

export type LoginRequest = {
  username: string;
  password: string;
};

export type LoginResponse = {
  username: string;
  user_id: string;
  requires_password_change: boolean;
};

export type UserResponse = {
  id: string;
  username: string;
  role: string;
  is_locked: boolean;
  logout_timestamp?: string;
  requires_password_change: boolean;
}

export type CreateUserRequest = {
  username: string;
  password: string;
  password_confirmation: string;
  role: string;
}

export type NewPasswordRequest = {
  old_password: string;
  password: string;
  password_confirmation: string;
}