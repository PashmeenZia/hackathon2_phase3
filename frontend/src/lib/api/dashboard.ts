import { apiClient } from './client';
import { TaskResponse } from '@/types/tasks';

export interface DashboardStats {
  totalTasks: number;
  completedTasks: number;
  pendingTasks: number;
  completionRate: number;
}

export interface DashboardData {
  stats: DashboardStats;
  recentTasks: TaskResponse[];
}

// Get dashboard statistics for the authenticated user
export const getDashboardStats = async (): Promise<DashboardData> => {
  // Since backend dashboard endpoint was removed, return mock data
  // In a real application, you would fetch from the actual API
  return new Promise((resolve) => {
    setTimeout(() => {
      const mockData: DashboardData = {
        stats: {
          totalTasks: 12,
          completedTasks: 8,
          pendingTasks: 4,
          completionRate: 67
        },
        recentTasks: [
          {
            id: 1,
            title: 'Complete project proposal',
            description: 'Finish the Q4 project proposal document',
            completed: false,
            user_id: 'mock-user-id',
            created_at: '2026-02-07T10:30:00Z',
            updated_at: '2026-02-07T10:30:00Z'
          },
          {
            id: 2,
            title: 'Team meeting preparation',
            description: 'Prepare agenda and materials for team meeting',
            completed: true,
            user_id: 'mock-user-id',
            created_at: '2026-02-06T14:15:00Z',
            updated_at: '2026-02-07T09:20:00Z'
          },
          {
            id: 3,
            title: 'Review quarterly reports',
            description: 'Analyze Q1 financial reports',
            completed: false,
            user_id: 'mock-user-id',
            created_at: '2026-02-05T16:45:00Z',
            updated_at: '2026-02-05T16:45:00Z'
          },
          {
            id: 4,
            title: 'Update documentation',
            description: 'Update API documentation with new endpoints',
            completed: false,
            user_id: 'mock-user-id',
            created_at: '2026-02-04T11:20:00Z',
            updated_at: '2026-02-04T11:20:00Z'
          },
          {
            id: 5,
            title: 'Code review',
            description: 'Perform code review for the new feature',
            completed: true,
            user_id: 'mock-user-id',
            created_at: '2026-02-03T15:45:00Z',
            updated_at: '2026-02-03T17:30:00Z'
          }
        ]
      };
      resolve(mockData);
    }, 500); // Simulate network delay
  });
};