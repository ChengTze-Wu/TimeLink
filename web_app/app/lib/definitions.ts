// This file contains type definitions for your data.
// It describes the shape of the data, and what data type each property should accept.
// For simplicity of teaching, we're manually defining these types.
// However, these types are generated automatically if you're using an ORM such as Prisma.
import { UUID } from "crypto";

export type Auth = {
  id: UUID;
  name: string;
  username: string;
  email: string;
  role: string;
  token: {
    access_token: string;
    token_type: string;
    expires_in: number;
  };
  status: number;
};

export type User = {
  id: UUID;
  name: string;
  username: string;
  email: string;
  phone: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  role: string;
};

export type Group = {
  id: UUID;
  name: string;
  line_group_id: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  services: Service[];
  owner: Owner;
};

export type Owner = {
  id: UUID;
  username: string;
};

export type Service = {
  id: UUID;
  name: string;
  price: number;
  image: string;
  description: string;
  working_period: number;
  owner: Owner;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  groups: Group[];
  working_hours: WorkingHour[];
};

export type WorkingHour = {
  day_of_week: string;
  start_time: string;
  end_time: string;
};

export type Role = {
  id: UUID;
  name: string;
};
