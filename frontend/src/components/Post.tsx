import Map, { Marker, NavigationControl, MapRef, MapEvent, MapLayerMouseEvent, Popup, MapMouseEvent, MarkerEvent, Projection } from 'react-map-gl';
import React, { useState, useEffect } from 'react';
import { PostObject } from '../types/types';
import { formatDistanceToNow } from 'date-fns';
import './Post.css'
import { flyToOnMap, getMarkerSVG } from '../utils/maputils';

const howLongAgo = (timestamp:number): string => {
  return formatDistanceToNow(new Date(timestamp * 1000), { addSuffix: true });
}

interface PostProps {
    post:PostObject|null
}

export const PostView: React.FC<PostProps> = ({post = null}) => {
    if(!post) return;

    return (
        <div className="post">
            <div className="post_meta">
                <div className="post_user">{post.user.name}</div>
                <div className="post_place">{post.place.name}</div>
                <div className="post_time">{howLongAgo(post.timestamp)}</div>
            </div>
            <div className="post_txt">{post.text.txt}</div>
        </div>
    )

};

export const PostPopup: React.FC<PostProps> = ({post = null}) => {
    if(!post) return
    return (
        <Popup
          className='post-popup'
          latitude={post.place.lat}
          longitude={post.place.lon}
          closeButton={false}
          closeOnClick={true}
          offset={1 * 40} // Adjust this value as needed to position the popup above the marker
          anchor="bottom" // This makes the popup's bottom edge aligned with the marker position      
        //   onClose={() => setPopupInfo(null)} // Reset clicked marker id on close
      >
          <PostView post={post} />
        </Popup>
    )
}

interface PostMarkerProps {
    post:PostObject|null;
    activePost:PostObject|null;
    clickPost: any|null;
}

export const PostMarker: React.FC<PostMarkerProps> = ({post = null, activePost = null, clickPost = null}) => {
    if(!post) return;

    return <Marker
        key={'marker-'.concat(post.id.toString())}
        longitude={post.place.lon}
        latitude={post.place.lat}
        onClick={(event: any) => clickPost(post,event)}
      >
        {getMarkerSVG(1, (post && activePost && activePost.id==post.id) ? "red" : "blue")}
      </Marker>
};