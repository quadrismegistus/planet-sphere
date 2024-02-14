import { entity } from 'simpler-state';
import { PostObject } from '../types/types'; // Import your interfaces

export const postsQueueState = entity<PostObject[]>([]);
export const postsQueueIndexState = entity(0);
export const activePostState = entity<PostObject|null>(null);
export const readPostIdsState = entity(new Set());
export const postsLoadedState = entity(false);