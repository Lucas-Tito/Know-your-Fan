import React from "react";
import './bluesky_profile.css';

const BlueskyProfile = ({ profile_data }) => {
  const {
    handle,
    display_name,
    followers_count,
    following_count,
    esports_posts,
    last_updated,
  } = profile_data?.profile_data ?? {};

  console.log("oiii ", profile_data?.profile_data);
  

  const formattedDate = new Date(last_updated).toLocaleString();

  return (
    <>
      <div className="profile-card" role="region" aria-label="Bluesky profile data">
        <div className="header">
          <div className="handle">@{handle}</div>
          <div className="display-name">{display_name || "—"}</div>
          <div className="stats" aria-label="Followers and following counts">
            <div className="stat-item">
              <div className="stat-number">{followers_count}</div>
              <div>Followers</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">{following_count}</div>
              <div>Following</div>
            </div>
          </div>
        </div>

        <div className="posts-section">
          <div className="posts-header">
            Esports Posts ({esports_posts?.count})
          </div>
          {esports_posts?.sample?.length === 0 && <p>No esports posts found.</p>}
          {esports_posts?.sample?.map((post) => (
            <div key={post.uri} className="post">
              <a
                href={`https://bsky.social/${post.uri.replace("at://", "")}`}
                target="_blank"
                rel="noopener noreferrer"
                className="post-link"
                aria-label="Link to Bluesky post"
              >
                {post.uri}
              </a>
              <div className="post-text">{post.text}</div>
              <div className="post-meta">
                <div>👍 {post.likes}</div>
                <div>🔁 {post.reposts}</div>
              </div>
            </div>
          ))}
        </div>

        <div className="last-updated">Last updated: {formattedDate}</div>
      </div>
    </>
  );
};

export default BlueskyProfile;