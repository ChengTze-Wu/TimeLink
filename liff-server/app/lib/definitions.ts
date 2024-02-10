// This file contains type definitions for your data.
// It describes the shape of the data, and what data type each property should accept.
// For simplicity of teaching, we're manually defining these types.
// However, these types are generated automatically if you're using an ORM such as Prisma.
import { UUID } from "crypto";

export type Group = {
  id: UUID;
  name: string;
  line_group_id: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  services: Service[];
};

export type Service = {
  id: UUID;
  name: string;
  price: number;
  image: string;
  description: string;
  working_period: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  groups: Group[];
  working_hours: WorkingHour[];
};

export type WorkingHour = {
  id: UUID;
  day_of_week: string;
  start_time: string;
  end_time: string;
};
