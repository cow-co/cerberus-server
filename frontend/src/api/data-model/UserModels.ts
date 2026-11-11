

export interface LoginRequest {
  username: string;
  password: string;
};

export interface LoginResponse {
  username: string;
  user_id: string;
};

export interface UserResponse {
  id: string;
  username: string;
  role: string;
  is_locked: boolean;
  logout_timestamp?: string;
}