// This file contains type definitions for your data.
// It describes the shape of the data, and what data type each property should accept.
// For simplicity of teaching, we're manually defining these types.
// However, these types are generated automatically if you're using an ORM such as Prisma.
import { UUID } from "crypto";

export type User = {
  id: UUID;
  name: string;
  username: string;
  email: string;
  phone: string;
  is_active: boolean;
  updated_at: string;
};
