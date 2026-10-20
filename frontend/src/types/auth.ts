export interface User {
  id: string;
  username: string;
  is_active: boolean;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface LoginPayload {
  username: string;
  password: string;
}