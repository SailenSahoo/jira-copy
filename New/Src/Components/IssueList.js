import React from 'react';

const IssueList = ({ issues }) => {
  return (
    <div>
      {issues.map((issue) => (
        <div key={issue.id} style={{ borderBottom: '1px solid #ccc', padding: '10px' }}>
          <strong>{issue.pkey}-{issue.issuenum}</strong>: {issue.summary}
        </div>
      ))}
    </div>
  );
};

export default IssueList;
