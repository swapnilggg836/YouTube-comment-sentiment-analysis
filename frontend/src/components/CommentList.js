import React from 'react';

const CommentList = ({ sentiment, comments }) => {
  return (
    <div>
      <h3>{sentiment.toUpperCase()} Comments</h3>
      <ul>
        {comments.map((c, i) => (
          <li key={i}>{c}</li>
        ))}
      </ul>
    </div>
  );
};

export default CommentList;
