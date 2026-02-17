import { z } from 'zod';

export const TaskSchema = z.object({
  title: z.string().min(1, 'Title is required').max(200, 'Title too long'),
  description: z.string().max(1000, 'Description too long').optional(),
  completed: z.boolean().default(false),
});

// Export type inference
export type TaskFormData = z.infer<typeof TaskSchema>;