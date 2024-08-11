import React, { useRef, useEffect, useState, ReactNode, createContext, useContext, Dispatch, SetStateAction } from 'react';
import axios from 'axios';
import { PostObject } from '../types/types'
import { REACT_APP_API_URL } from '../vars'
import { postsQueueState, postsQueueIndexState, activePostState, postsLoadedState, readPostIdsState } from '../entities/timelineEnts';

export interface TimelineContextType {
    // postsQueue: PostObject[];
    // activePost: PostObject|null;
    activatePost: (post: PostObject) => PostObject | undefined | null;
    // currentIndex: number;
    // postsLoaded: boolean;
    // setPostsQueue: (posts: PostObject[]) => void; 
    getCurrentPost: () => PostObject | undefined | null;
    getNextPost: () => PostObject | undefined | null;
    getPrevPost: () => PostObject | undefined | null;
    markPostRead: (post: PostObject) => void;
    addPostToBack: (post: PostObject) => void;
    addPostToFront: (post: PostObject) => void;
    markPostIdRead: (postId: number) => void;
  }
  
  

const TimelineContext = createContext<TimelineContextType | null>(null);

export const TimelineProvider: React.FC<{children:ReactNode}> = ({ children }) => {
    const [delay, setDelay] = useState(1000); // Initial delay of 1 second
    const postsQueue = postsQueueState.use();
        
    // Hook to fetch on startup
    useEffect(() => {
        console.log('hello????');
        (async () => {
            if(!postsLoadedState.get()) {
                const posts = await fetchPosts(readPostIdsState.get());
                if(posts && posts.length) {
                    const currentPostsQueue = postsQueueState.get();
                    const uniqueNewPosts = posts.filter(post => 
                        !currentPostsQueue.some(existingPost => existingPost.id === post.id)
                    );
                    postsLoadedState.set(true);
                    postsQueueState.set(oldPosts => [...uniqueNewPosts, ...oldPosts]);
                    activePostState.set(posts[0]);
                }
            }
        })();
    }, []);

    useEffect(() => {
        if(postsQueueState.get().length) {
            console.log('postsQueue changed to',postsQueueState.get());
        }
    }, [postsQueue])


    const addPostToFront = (post: PostObject) => {
        postsQueueState.set(prevPosts => [post, ...prevPosts]);
        postsQueueIndexState.set(prevIndex => prevIndex + 1);
    };

    const addPostToBack = (post: PostObject) => {
        postsQueueState.set(prevPosts => [...prevPosts, post]);
    };

    const getNextPost = () => {
        const index = (postsQueueIndexState.get() + 1 < postsQueueState.get().length) ? postsQueueIndexState.get() + 1 : 0;
        postsQueueIndexState.set(index);
        activePostState.set(postsQueueState.get()[index]); // Update the active post directly
        return activePostState.get();
    };

    const getPrevPost = () => {
        const index = (postsQueueIndexState.get() - 1 < 0) ? postsQueueState.get().length - 1 : postsQueueIndexState.get() - 1;
        postsQueueIndexState.set(index);
        activePostState.set(postsQueueState.get()[index]); // Update the active post directly
        return activePostState.get();
    };

    const activatePost = (post: PostObject) => {
        const index = postsQueueState.get().findIndex(p => p.id === post.id);
        if (index !== -1) {
            postsQueueIndexState.set(index);
            activePostState.set(post); // Set the active post
        }
        return activePostState.get();
    };

    // Simplify to use SimpleR State
    const markPostIdRead = (postId: number) => {
        readPostIdsState.set(oldSet => new Set([...oldSet, postId]));
    };

    const markPostRead = (post: PostObject) => {
        markPostIdRead(post.id);
    };

    const getCurrentPost = (): PostObject|undefined => {
        return postsQueueState.get()[postsQueueIndexState.get()]
    };



    // const markPostIdRead = (postId: number) => {
    //     // setReadPostIds(oldSet => {
    //     //     const updatedSet = new Set(oldSet);
    //     //     updatedSet.add(postId);
    //     //     return updatedSet;
    //     // });
    
    //     // setPostsQueue(prevPosts => {
    //     //     const removedIndex = prevPosts.findIndex(post => post.id === postId);
    //     //     // If post not found, no need to update the queue
    //     //     if (removedIndex === -1) {
    //     //         return prevPosts;
    //     //     }
    
    //     //     // Remove post by filtering it out
    //     //     const updatedPosts = prevPosts.filter(post => post.id !== postId);
    
    //     //     // Adjust currentIndex
    //     //     setCurrentIndex(prevIndex => {
    //     //         if (removedIndex < prevIndex) {
    //     //             // If the removed post is before the current post, decrement currentIndex
    //     //             return prevIndex - 1;
    //     //         } else if (removedIndex === prevIndex) {
    //     //             // If the removed post is the current post, decide how to adjust
    //     //             return prevIndex >= updatedPosts.length ? prevIndex - 1 : prevIndex;
    //     //         }
    //     //         // If the removed post is after the current post, no need to adjust currentIndex
    //     //         return prevIndex;
    //     //     });
    
    //     //     return updatedPosts;
    //     // });
    // };




//   useEffect(() => {
//     const unreadCount = postsQueue.length;
//     let timerId: any;

//     if (unreadCount >= 0 && unreadCount <= 10) {
//       console.log('trying to get posts, delay is currently',delay/1000)
//       // Only set the timeout if the unread count is within the specified range
//       timerId = setTimeout(() => {
//         fetchPosts()
//           .then((newPosts) => {
//             if (newPosts && newPosts.length > 0) {
//               // Reset delay if new posts were received
//               setDelay(1000); // Reset to initial delay
//               setPostsQueue(value => [...value, ...newPosts]);
//               setPostsLoaded(true);
//             } else {
//               // Increase delay for next fetch (exponential backoff)
//               setDelay((currentDelay) => Math.min(currentDelay * 5, 5 * 60 * 1000)); // Cap at 5 min
//             }
//           })
//           .catch((error) => {
//             console.error("Failed to fetch posts:", error);
//             // Optionally adjust delay on error as well
//               setDelay((currentDelay) => Math.min(currentDelay * 5, 5 * 60 * 1000)); // Cap at 5 min
//           });
//       }, delay);
//     }

//     // Cleanup function
//     return () => clearTimeout(timerId);
//   }, [delay]);



    return (
        <TimelineContext.Provider value={{activatePost,getCurrentPost,getNextPost,getPrevPost,markPostRead,addPostToBack,addPostToFront,markPostIdRead}}>
            {children}
        </TimelineContext.Provider>
    );
  };

  
  export const useTimeline = (): TimelineContextType => {
    const context = useContext(TimelineContext);
    if (context === null)
        throw new Error('useTimeline must be used within a TimelineProvider');
    return context;
};







// Function to fetch posts
const fetchPosts = async (readPostIds:Set<any>) => {
    console.log('fetching posts')
    try {
        const queryData = {type: "latest", seen: Array.from(readPostIds)};
        const response = await axios.post<PostObject[]>(REACT_APP_API_URL+'/posts/query', queryData);
        return response.data;
    } catch (error) {
        console.log('error fetching',error);
        return undefined;
    }
};
