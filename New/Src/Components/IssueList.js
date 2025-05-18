import React, { useEffect, useState } from 'react';
import api from '../api';

function IssueList({ searchKey }) {
  const [issues, setIssues] = useState([]);

  useEffect(() => {
    api.get('/fetch-issues')
      .then(res => setIssues(res.data))
      .catch(err => console.error('Error fetching issues:', err));
  }, []);

  const filteredIssues = issues.filter(issue =>
    issue.pkey.toLowerCase().includes(searchKey.toLowerCase())
  );

  return (
    <div>
      <h2>Archived Issues</h2>
      <ul>
        {filteredIssues.map(issue => (
          <li key={issue.id}>
            <strong>{issue.pkey}</strong>: {issue.summary} (Status: {issue.status}, Priority: {issue.priority})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default IssueList;
